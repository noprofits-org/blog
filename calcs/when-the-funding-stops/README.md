# When the funding stops

Original analysis for the 2026-09-08 article. Sources retrieved 2026-09-08.
This is a cross-sectional study of government-grant recipients, not a causal
study, representative sector estimate, or longitudinal study of actual cuts.

## Reproduce

Use Python 3.13 and install `requirements.txt` in a virtual environment. Run
`python compute.py --download`, then `python figures.py`, from this directory
or supply their paths from another working directory. The four raw files total
about 1 GB and are cached under ignored `calcs/data/`. A download is written to
a temporary file before being renamed; existing inputs are not replaced.
`results.json` records exact file URLs, SHA-256 hashes, byte sizes and row counts.
Compare these hashes when rerunning: a provider can revise a versioned URL.
The tested package versions are pinned in `requirements.txt`.

The local audit CSV is also ignored. Published outputs are aggregate results,
scripts and the two PNGs, never a named list of charities labeled at risk.
Hakyll copies the Python scripts; this directory's JSON and documentation are
available on GitHub. `figures.py` needs only `results.json`, not raw data.

## Sources and field mapping

NCCS efile v2_1, tax year 2023:
<https://nccs.urban.org/nccs/datasets/efile/>

The download pattern is taken from Urban Institute's public workflow:
<https://github.com/UrbanInstitute/nonprofit_govt_grants/blob/main/R/config.R>.
We independently select our sample and add Part X; we do not reproduce Urban's
geographic filters, deduplication procedure or risk metric.

The current-vintage definitions were checked against the original form:
<https://www.irs.gov/pub/irs-prior/f990--2023.pdf> and its instructions:
<https://www.irs.gov/pub/irs-prior/i990--2023.pdf>.
NCCS retains historical names such as `UNRESTRICT` and `FOLLOW_SFAS117` for
modern net assets without donor restrictions and the ASC 958 checkbox.

| Alias | NCCS field (F9_ prefix) | 2023 Form 990 |
| --- | --- | --- |
| grants | 08_REV_CONTR_GOVT_GRANT | VIII 1e |
| revenue | 08_REV_TOT_TOT | VIII 12, column A |
| expenses | 09_EXP_TOT_TOT | IX 25, column A |
| depreciation | 09_EXP_DEPREC_TOT | IX 22, column A |
| unrestricted | 10_NAFB_UNRESTRICT_EOY | X 27, column B |
| restricted | 10_NAFB_RESTRICT_EOY | X 28, column B |
| net_assets | 10_NAFB_TOT_EOY | X 32, column B |
| fixed_assets | 10_ASSET_LAND_BLDG_NET_EOY | X 10c, column B |
| secured_debt | 10_LIAB_MTG_NOTE_EOY | X 23, column B |
| bonds | 10_LIAB_TAX_EXEMPT_BOND_EOY | X 20, column B |
| cash | 10_ASSET_CASH_EOY | X 1, column B |
| savings | 10_ASSET_SAVING_EOY | X 2, column B |

All financial values are dollars. Income/expense values describe the filing's
year; balance-sheet values are end of year. Tax year 2023 includes fiscal years
beginning in 2023, not just years ending on December 31, 2023.

## Population and checks

1. Require unique, nonmissing `(EIN2, OBJECTID)` in each part. Start with full
   Form 990 for tax year 2023. Keep latest timestamp per EIN, breaking timestamp
   ties deterministically by OBJECTID. This precedes all substantive filters;
   a failed latest return cannot be silently replaced with an older return.
2. Require the filing's 501(c)(3) checkbox and a 50-state/DC mailing address;
   exclude group/partial flags. Require a 360–371-day reporting period,
   inclusive, to admit full-year 52/53-week accounting. Here this duration
   check removes no additional rows after partial-return exclusions.
3. Join all financial parts to that exact filing, with one-to-one validation.
   All 244,821 selected headers match all three financial parts in this vintage.
4. Require positive grants, revenue, and expenses; exclude grants above revenue.
   Grants can exceed net total revenue legitimately (e.g. offsetting losses);
   this exclusion defines interpretable 0–100% bands, not erroneous filers.
5. Require ASC 958 checkbox, observed unrestricted and total net assets, and
   unrestricted + restricted net assets reconciling within $1,000. This absolute
   tolerance follows the earlier reserve series; it is not an audit standard.
6. Require nonnegative fixed assets, debt, bonds, cash, savings, depreciation;
   require expenses less depreciation to be positive. Negative unrestricted
   net assets and negative reserve estimates are retained.

The sequential counts are in `results.json`. The resulting 68,957 EINs are
85.7% of the 80,444 positive-grant recipients before financial filters.
The source, population, accounting checks and period differ from our previous
SOI-extract reserve articles; counts are not directly comparable.

## Missing components

Missing grant amounts are excluded, never categorized as zero dependence.
Missing revenue, expenses, unrestricted net assets or total net assets are
excluded. For omitted restricted assets, fixed assets, secured debt, bonds,
cash, savings and depreciation, the main analysis assumes zero. Missingness
counts before reconciliation are recorded separately. The assumption can
overstate or understate the proxy depending on which field is omitted.

The complete-component sensitivity requires all seven fields explicitly
reported, including zeros. Only 3,030 filings remain; selection is severe
(especially because most filers omit the bond field). It cannot establish
that omitted fields are zero, or serve as a corrected population estimate.
The high-versus-middle comparison survives, but the low-versus-high reserve
medians converge. We report that limitation in the article.

## Metrics

Let R be revenue, G government grants, E expenses, D depreciation, U net assets
without donor restrictions, P net property, S secured debt, B tax-exempt bonds.

- Grant dependence = G / R. Bins are (0,.1], (.1,.25], (.25,.5], (.5,1].
- Reserve proxy Q = U - P + S. Negative values are preserved.
- Adjusted expense denominator C = E - D, required positive. It is **not** a
  cash-flow statement and can include other noncash expenses.
- Reserve months = 12Q/C. Bond sensitivity = 12(Q+B)/C.
- No-debt-addback sensitivity = 12(U-P)/C.
- Cash/savings months = 12(cash+savings)/C, including any restricted cash.
- Expense bins are [0,500K), [500K,5M), [5M,50M), [50M,infinity).

Means of indicators and medians give each included EIN equal weight. Neither
figure is a dollar-weighted statistic. Figures are descriptive, without causal
adjustment or population-inference confidence intervals. Connecting lines in
Figure 2 do not represent a panel or fitted regression.

For a hypothetical grant loss fraction f, the annual gap is C - (R - fG).
Only positive gaps enter the coverage condition. For those filings, modeled
coverage is 12Q/gap. The threshold count includes Q <= 0 and positive Q with
coverage <= 3 months; we separately report those components. Denominator is
always the full 68,957, including filers without a modeled gap. The f=0
baseline includes preexisting deficits. No outcome is attributed causally
to a cut, and an annual grant reduction is not a model of a payment delay.

## Interpretation limits

Line 1e combines government levels and excludes payments classified elsewhere;
no federal-only or total-government-dependence estimate is possible here.
Property and secured liabilities are not necessarily matched; debt add-backs
and bonds are sensitivities, not a demonstration that funds are spendable.
ASC 958 net assets can contain receivables, investments and board designations.
The static scenario holds all other revenue/expenses fixed, treats recognized
revenue as available, includes restricted/noncash revenue, and ignores spending
responses, new gifts, working capital, debt principal, capital spending and
credit. These limitations prevent interpreting coverage as time to closure.

## Verification

`verify.py` checks all analyzed-row arithmetic with independent scalar formulas,
recounts the displayed groups and scenarios, checks the known source hashes,
and compares 12 fields in three deterministic sample filings to their original
XML. Run after compute.py. This is a spot check of extraction, not a complete
audit of every filer. The originals are downloaded only into ignored data.
Both figures are 1200×630, and the hero is used unchanged for the social card.
