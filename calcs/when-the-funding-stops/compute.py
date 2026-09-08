#!/usr/bin/env python3
"""Government-grant dependence and reserve proxies, NCCS efile v2_1, TY2023.

Run from any directory: python compute.py [--download]
Dependencies: see requirements.txt. Raw downloads stay in ignored calcs/data/.
No cross-year or EIN-only financial joins: each part joins on EIN2 + OBJECTID.
See README.md for population, missing-value policy and interpretation.
"""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
BASE = "https://nccs-efile.s3.us-east-1.amazonaws.com/public/efile_v2_1/"
KEY = ["EIN2", "OBJECTID"]
PARTS = {
    "P00-T00-HEADER": {
        "RETURN_TYPE": "form", "TAX_YEAR": "year", "RETURN_TIME_STAMP": "timestamp",
        "TAX_PERIOD_BEGIN_DATE": "begin", "TAX_PERIOD_END_DATE": "end",
        "RETURN_GROUP_X": "group", "RETURN_PARTIAL_X": "partial",
        "F9_00_EXEMPT_STAT_501C3_X": "c3", "F9_00_ORG_ADDR_STATE": "state",
        "URL": "xml_url",
    },
    "P08-T00-REVENUE": {"F9_08_REV_CONTR_GOVT_GRANT": "grants",
                            "F9_08_REV_TOT_TOT": "revenue"},
    "P09-T00-EXPENSES": {"F9_09_EXP_TOT_TOT": "expenses",
                            "F9_09_EXP_DEPREC_TOT": "depreciation"},
    "P10-T00-BALANCE-SHEET": {
        "F9_10_NAFB_FOLLOW_SFAS117_X": "fasb",
        "F9_10_NAFB_UNRESTRICT_EOY": "unrestricted",
        "F9_10_NAFB_RESTRICT_EOY": "restricted",
        "F9_10_NAFB_TOT_EOY": "net_assets",
        "F9_10_ASSET_LAND_BLDG_NET_EOY": "fixed_assets",
        "F9_10_LIAB_MTG_NOTE_EOY": "secured_debt",
        "F9_10_LIAB_TAX_EXEMPT_BOND_EOY": "bonds",
        "F9_10_ASSET_CASH_EOY": "cash",
        "F9_10_ASSET_SAVING_EOY": "savings",
    },
}
STATES = set("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split())
BANDS = [(0, .1, "0–10%"), (.1, .25, "10–25%"), (.25, .5, "25–50%"), (.5, 1, "50–100%")]
SIZE = [(0, 5e5, "Under $500K"), (5e5, 5e6, "$500K–$5M"),
        (5e6, 5e7, "$5M–$50M"), (5e7, np.inf, "$50M or more")]
OPTIONAL = ["restricted", "fixed_assets", "secured_debt", "bonds", "cash", "savings", "depreciation"]


def flagged(series):
    return series.fillna("").str.upper().isin(["X", "TRUE", "1"])


def summary(df):
    assert len(df) > 0
    return {"n": len(df), "reserve_median": float(df.reserve_months.median()),
            "reserve_le3_n": int((df.reserve_months <= 3).sum()),
            "reserve_le3_pct": float((df.reserve_months <= 3).mean() * 100),
            "reserve_le0_pct": float((df.reserve_months <= 0).mean() * 100),
            "cash_median": float(df.cash_months.median()),
            "bond_reserve_median": float(df.bond_months.median()),
            "no_debt_addback_median": float(df.no_debt_months.median())}


def by_band(df):
    return [{"band": label, **summary(df[(df.dependence > lo) & (df.dependence <= hi)])}
            for lo, hi, label in BANDS]


def main(download=False):
    DATA.mkdir(parents=True, exist_ok=True)
    previous = HERE / "results.json"
    expected_hashes = ({s["file"]: s["sha256"] for s in json.loads(previous.read_text())["sources"]}
                       if previous.exists() else {})
    manifest, tables = [], []
    for part, cols in PARTS.items():
        name = f"F9-{part}-2023.CSV"
        path = DATA / name
        if not path.exists():
            if not download:
                raise FileNotFoundError(f"{path}; rerun with --download")
            tmp = path.with_suffix(".part")
            with urlopen(BASE + name, timeout=120) as response, tmp.open("wb") as out:
                while chunk := response.read(1024 * 1024):
                    out.write(chunk)
            tmp.replace(path)
        with path.open("rb") as f:
            digest = hashlib.file_digest(f, "sha256").hexdigest()
        if name in expected_hashes and digest != expected_hashes[name]:
            raise ValueError(f"Source changed: {name}; preserve the published results and investigate")
        df = pd.read_csv(path, usecols=KEY + list(cols), dtype="string").rename(columns=cols)
        assert df[KEY].notna().all().all(), f"Missing join key: {part}"
        assert not df.duplicated(KEY).any(), f"Non-unique filing keys: {part}"
        manifest.append({"file": name, "url": BASE + name, "sha256": digest,
                         "bytes": path.stat().st_size, "rows": len(df)})
        tables.append(df)

    counts = {}
    df = tables[0]
    counts["header_rows"] = len(df)
    # Select latest submission before substantive filters; never fall back to an
    # older filing merely because the latest one fails an analytical criterion.
    df = df[(df.form == "990") & (df.year == "2023")].copy()
    counts["full_990_ty2023"] = len(df)
    df["timestamp"] = pd.to_datetime(df.timestamp, utc=True, errors="raise", format="mixed")
    assert df.timestamp.notna().all()
    df = df.sort_values(["timestamp", "OBJECTID"]).drop_duplicates("EIN2", keep="last")
    counts["unique_eins"] = len(df)
    df = df[flagged(df.c3) & df.state.isin(STATES)]
    counts["domestic_c3"] = len(df)
    df = df[~flagged(df.group) & ~flagged(df.partial)]
    counts["nongroup_nonpartial"] = len(df)
    days = (pd.to_datetime(df.end, errors="raise") - pd.to_datetime(df.begin, errors="raise")).dt.days + 1
    df = df[days.between(360, 371)]
    counts["full_year"] = len(df)
    for source in tables[1:]:
        df = df.merge(source, on=KEY, how="inner", validate="one_to_one")
    counts["all_four_parts"] = len(df)
    numeric = ["grants", "revenue", "expenses", "unrestricted", "net_assets"] + OPTIONAL
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="raise").astype(float)
    counts["grant_missing"] = int(df.grants.isna().sum())
    counts["grant_explicit_zero"] = int((df.grants == 0).sum())
    counts["grant_negative"] = int((df.grants < 0).sum())
    df = df[df.grants > 0].copy()
    counts["positive_grant_recipients"] = len(df)
    df = df[(df.revenue > 0) & (df.expenses > 0)]
    counts["positive_revenue_expenses"] = len(df)
    counts["grants_exceed_revenue"] = int((df.grants > df.revenue).sum())
    df = df[df.grants <= df.revenue].copy()
    counts["grant_share_at_most_one"] = len(df)
    df = df[flagged(df.fasb) & df.unrestricted.notna() & df.net_assets.notna()].copy()
    counts["fasb_and_core_balances_present"] = len(df)
    missing = df[OPTIONAL].isna()
    df["complete_optional"] = ~missing.any(axis=1)
    blank_counts = missing.sum().astype(int).to_dict()
    # An explicit assumption for omitted component fields, not missing totals.
    # Report a complete-component sensitivity alongside the main results.
    df[OPTIONAL] = df[OPTIONAL].fillna(0)
    df = df[(df.unrestricted + df.restricted - df.net_assets).abs() <= 1000].copy()
    counts["net_assets_reconcile"] = len(df)
    df = df[(df[["fixed_assets", "secured_debt", "bonds", "cash", "savings", "depreciation"]] >= 0).all(axis=1)].copy()
    counts["nonnegative_components"] = len(df)
    df["cash_expenses"] = df.expenses - df.depreciation
    df = df[df.cash_expenses > 0].copy()
    counts["analyzed"] = len(df)
    df["reserve"] = df.unrestricted - df.fixed_assets + df.secured_debt
    df["reserve_months"] = 12 * df.reserve / df.cash_expenses
    df["bond_months"] = 12 * (df.reserve + df.bonds) / df.cash_expenses
    df["no_debt_months"] = 12 * (df.unrestricted - df.fixed_assets) / df.cash_expenses
    df["cash_months"] = 12 * (df.cash + df.savings) / df.cash_expenses
    df["dependence"] = df.grants / df.revenue
    assert df.EIN2.is_unique and np.isfinite(df[numeric]).all().all()
    assert ((df.dependence > 0) & (df.dependence <= 1)).all()
    bands = by_band(df)
    assert sum(b["n"] for b in bands) == len(df)
    size = [{"size": label, "bands": by_band(df[(df.expenses >= lo) & (df.expenses < hi)])}
            for lo, hi, label in SIZE]
    # Stylized financing gap: all other annual revenue and expenses unchanged;
    # subtract depreciation only, no claim to model actual cash flows.
    scenarios = []
    for fraction in [0, .25, .5, 1]:
        gap = df.cash_expenses - (df.revenue - fraction * df.grants)
        positive_gap = gap > 0
        cover = 12 * df.reserve / gap.where(positive_gap)
        short = positive_gap & (cover <= 3)
        scenarios.append({"grant_loss_fraction": fraction,
                          "positive_gap_n": int(positive_gap.sum()),
                          "positive_gap_pct": float(positive_gap.mean() * 100),
                          "gap_and_le3_months_n": int(short.sum()),
                          "gap_and_le3_months_pct": float(short.mean() * 100),
                          "positive_reserve_gap_le3_n": int((short & (df.reserve > 0)).sum()),
                          "nonpositive_reserve_gap_n": int((positive_gap & (df.reserve <= 0)).sum())})
    assert all(a["gap_and_le3_months_n"] <= b["gap_and_le3_months_n"]
               for a, b in zip(scenarios, scenarios[1:]))
    complete = df[df.complete_optional]
    results = {"tax_year": 2023, "source_version": "NCCS efile_v2_1",
               "sources": manifest, "counts": counts,
               "omitted_component_counts_before_reconciliation": blank_counts,
               "overall": summary(df), "bands": bands, "expense_bands": size,
               "complete_components": {"overall": summary(complete), "bands": by_band(complete)},
               "scenarios": scenarios}
    (HERE / "results.json").write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    # Local audit data, not a list of organizations published as being at risk.
    df.to_csv(DATA / "when-the-funding-stops-audit.csv.gz", index=False, compression="gzip")
    print(json.dumps({k: v for k, v in results.items() if k != "sources"}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    main(parser.parse_args().download)
