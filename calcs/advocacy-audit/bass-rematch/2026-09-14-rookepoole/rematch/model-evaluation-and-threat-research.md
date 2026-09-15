# METR

Audit date: 2026-09-14. Status: first bounded SFF edges finished; graphic claim OPEN.

## Frozen graphic claim

- **PG-METR-1** — The user-supplied transcription of the Poole graphic dated 14 September 2026 attributes approximately $2,120,000 to METR; grantor, grant date, filing year and money type are unspecified.

## Verdicts

| Row | Verdict | Reason | Source |
| --- | --- | --- | --- |
| PG-METR-1 | OPEN | Grantor, period and money type missing; original image unavailable. | [Thread](https://x.com/rookepoole/status/2099660837388501127); `sources/poole-thread.html.error.json` |
| SFF-2024-G0-R53-REC | KEEP | $204,000 recommendation, 2024; receiving entity **Model Evaluation and Threat Research, Inc.**. | [Primary page](https://survivalandflourishing.fund/2024/recommendations); `sources/sff-2024.html`; grid 0; data row 53; Total Funding Rec. |
| SFF-2025-G0-R56-REC | KEEP | $120,000 recommendation, 2025; receiving entity **Model Evaluation and Threat Research, Inc.**. | [Primary page](https://survivalandflourishing.fund/2025/recommendations); `sources/sff-2025.html`; grid 0; data row 56; Total Funding Rec. |
| SFF-2025-G0-R56-MATCH | KEEP | $428,000 commitment, 2025; receiving entity **Model Evaluation and Threat Research, Inc.**. | [Primary page](https://survivalandflourishing.fund/2025/recommendations); `sources/sff-2025.html`; grid 0; data row 56; Total Funding Rec. |

## Frozen primary claims

- **SFF-2024-G0-R53-REC** — SFF’s 2024 round lists Jaan Tallinn as source of a $204,000 published funding recommendation for Model Evaluation and Threat Research, with receiving charity Model Evaluation and Threat Research, Inc.; this does not establish a cash payment or filing year.
- **SFF-2025-G0-R56-REC** — SFF’s 2025 round lists Jaan Tallinn as source of a $120,000 non-matching portion of the published recommendation, derived as total minus included matching pledge for Model Evaluation & Threat Research (METR), with receiving charity Model Evaluation and Threat Research, Inc.; this does not establish a cash payment or filing year.
- **SFF-2025-G0-R56-MATCH** — SFF’s 2025 round lists Jaan Tallinn as source of a $428,000 conditional matching pledge included in the total recommendation for Model Evaluation & Threat Research (METR), with receiving charity Model Evaluation and Threat Research, Inc.; this does not establish a cash payment or filing year.

## Scope and gaps

Searched the SFF 2024 and 2025 main recommendation tables captured 2026-09-14, using the exact project aliases recorded in build.py. Amounts in parentheses are speculation annotations, not additional awards. Matching pledges are included in the published total: the non-matching component and pledge are separated in evidence_rows.csv. The separate pledge table repeats the same pledge and is not another edge. No all-time total or payment total is calculated.

The graphic amount remains OPEN: a differently scoped primary amount is not enough for KILL. Obtain the original arrow, legend, date range and fiscal-sponsor labels; then check FLI grant schedules and the relevant SFF rounds. Full funding history and legal identity audit are unfinished.

## Bass / Tarbell overlap

Bass **M38** is the same SFF 2024 $204,000 recommendation rematched above. **M39** splits 2025 into $120,000 and a $428,000 matching pledge, also rematched above. Reuse these row IDs when joining to Bass; do not add the Bass rows again. M35–M37 concern ARC/ARC Evals and are not automatically METR receipts. M52/M53/M55 are Tallinn-ledger claims: primary retrieval was robots-disallowed, so they remain unrematched here.

[METR About](https://metr.org/about), cached as `sources/metr-about.html`, confirms the SFF recommendation relationship but provides no matching dollar total. No payroll or donor-to-lab attribution follows. Prior F2 remains bounded to its original Coefficient/GVF corpus and cutoff; F3 remains OPEN.
