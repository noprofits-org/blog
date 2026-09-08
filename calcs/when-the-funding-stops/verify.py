#!/usr/bin/env python3
"""Check arithmetic independently and spot-check NCCS fields against original XML.

Run after compute.py. Reads local audit data, fetches three public XML filings
if absent, and writes no published data. No named risk assessments are emitted.
"""
import csv
import gzip
import hashlib
import json
import math
import statistics
from pathlib import Path
from urllib.request import urlopen
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
D = json.loads((HERE / "results.json").read_text())


def main():
    for source in D["sources"]:
        with (DATA / source["file"]).open("rb") as f:
            assert hashlib.file_digest(f, "sha256").hexdigest() == source["sha256"]
    with gzip.open(DATA / "when-the-funding-stops-audit.csv.gz", "rt") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len({r["EIN2"] for r in rows}) == D["counts"]["analyzed"] == 68957
    groups = [[] for _ in range(4)]
    scenario_counts = [0] * 4
    for row in rows:
        n = {k: float(row[k]) for k in ["grants", "revenue", "expenses", "depreciation",
             "unrestricted", "fixed_assets", "secured_debt", "reserve_months", "dependence"]}
        reserve = n["unrestricted"] - n["fixed_assets"] + n["secured_debt"]
        cost = n["expenses"] - n["depreciation"]
        months = reserve / (cost / 12)
        share = n["grants"] / n["revenue"]
        assert math.isclose(months, n["reserve_months"], rel_tol=1e-12, abs_tol=1e-9)
        assert math.isclose(share, n["dependence"], rel_tol=1e-12, abs_tol=1e-15)
        index = next(i for i, upper in enumerate([.1, .25, .5, 1]) if share <= upper)
        groups[index].append(months)
        for i, fraction in enumerate([0, .25, .5, 1]):
            monthly_gap = (cost - n["revenue"] + fraction * n["grants"]) / 12
            # Multiplication checks the threshold without dividing by the gap.
            if monthly_gap > 0 and reserve <= 3 * monthly_gap:
                scenario_counts[i] += 1
    for i, values in enumerate(groups):
        assert len(values) == D["bands"][i]["n"]
        assert math.isclose(statistics.median(values), D["bands"][i]["reserve_median"])
        assert sum(v <= 3 for v in values) == D["bands"][i]["reserve_le3_n"]
    assert scenario_counts == [s["gap_and_le3_months_n"] for s in D["scenarios"]]

    ns = {"r": "http://www.irs.gov/efile"}
    paths = {
        "grants": "GovernmentGrantsAmt",
        "revenue": "TotalRevenueGrp/TotalRevenueColumnAmt",
        "expenses": "TotalFunctionalExpensesGrp/TotalAmt",
        "depreciation": "DepreciationDepletionGrp/TotalAmt",
        "unrestricted": "NoDonorRestrictionNetAssetsGrp/EOYAmt",
        "restricted": "DonorRestrictionNetAssetsGrp/EOYAmt",
        "net_assets": "TotalNetAssetsFundBalanceGrp/EOYAmt",
        "fixed_assets": "LandBldgEquipBasisNetGrp/EOYAmt",
        "secured_debt": "MortgNotesPyblScrdInvstPropGrp/EOYAmt",
        "bonds": "TaxExemptBondLiabilitiesGrp/EOYAmt",
        "cash": "CashNonInterestBearingGrp/EOYAmt",
        "savings": "SavingsAndTempCashInvstGrp/EOYAmt",
    }
    ordered = sorted(rows, key=lambda r: r["OBJECTID"])
    for index in [100, 20000, 50000]:
        row = ordered[index]
        file = DATA / (row["OBJECTID"] + ".xml")
        if not file.exists():
            with urlopen(row["xml_url"], timeout=60) as response:
                file.write_bytes(response.read())
        root = ET.parse(file).getroot()
        ein = root.findtext(".//r:ReturnHeader/r:Filer/r:EIN", namespaces=ns)
        assert ein == row["EIN2"].removeprefix("EIN-").replace("-", "")
        form = root.find(".//r:IRS990", ns)
        assert form is not None
        for alias, path in paths.items():
            node = form.find("/".join("r:" + part for part in path.split("/")), ns)
            raw = 0 if node is None else int(node.text)
            assert raw == float(row[alias]), (index, alias, raw, row[alias])
    print(f"PASS: {len(rows):,} scalar reserve calculations; all band counts/medians; four scenario counts;")
    print("four source hashes; EIN identity and 12 financial fields in three original XML filings.")


if __name__ == "__main__":
    main()
