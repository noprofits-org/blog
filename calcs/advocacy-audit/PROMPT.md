# Prompt used to generate this audit

Delivered to OpenAI Codex on 2026-09-14, verbatim. The audit artifacts in
this directory (research/*.csv, figures/, NOTES.md, STATE.md) were produced
under these rules; the blog post quotes this prompt in full.

```
Audit who funds the messaging — both sides — in the fight over AI regulation. This is the data backbone for a data-journalism post on blog.noprofits.org; humans write the post, you build the dataset, run the calculations, make the plots, and hand back a quotable summary. That blog's brand is every number traceable to a primary public filing, so the rules below are non-negotiable.

RULES
1. Every number traces to a row in research/*.csv. Each row: row_id, amount, source_url, snapshot_date, verbatim_quote_from_source, note. No number anywhere without a row id.
2. Verdicts per claim: KEEP (primary document confirms), KILL (contradicts), OPEN (unverifiable). OPEN is a valid, expected outcome — never fill gaps with inference.
3. Never sum different money types: grants, recommendations, commitments, lobbying fees, DAF-routed grants, and org revenue totals stay separate and labeled as what they are.
4. "None found" must be bounded: name the documents searched and their dates.
5. No motive language anywhere, including plot labels. Describe funding structures. The words "front group", "astroturf", and "proxy" are banned.
6. Public data only; respect robots.txt and terms of service; no logins; do not contact any organization.

ORG UNIVERSE (~15 max; verify existence and tax status first, add orgs you discover with a one-line justification, drop dead ones)
- Safety/regulation side: Center for AI Safety (incl. any c4 arm), AI Policy Institute (incl. c4), Encode Justice, Future of Life Institute, ControlAI (UK), Safe AI Forum, Institute for AI Policy and Strategy, Horizon Institute for Public Service, Americans for Responsible Innovation.
- Established-org comparators: Public Citizen, Federation of American Scientists.
- Industry/innovation side: Chamber of Progress, ITIF, TechFreedom, NetChoice.
- Labs' own lobbying spend (LDA): Anthropic, OpenAI, Google, Meta, xAI, Microsoft, Amazon.

DATA SOURCES, in reliability order
1. Funder-side 990-PF grant schedules — the WORKING direction for who-funded-whom (grantee names are public): Coefficient Giving grants index + its 990; Good Ventures Foundation EIN 46-1008520 (through FYE June 2025); Open Philanthropy historical grants database; Survival and Flourishing Fund recommendation pages (recommendations ≠ grants — label them); EA Funds; FTX Future Fund and Building a Stronger Future (historical; label dead money).
2. Org-side Forms 990 via IRS e-file XML (apps.irs.gov/pub/epostcard/990/xml/ index files) or ProPublica Nonprofit Explorer API: total revenue, assets, program expenses, 2019–2024. Schedule B donor detail is redacted for most post-2020 filers — do not attempt donor identification from c3 filings; use direction 1.
3. DAF-sponsor 990-PFs — Silicon Valley Community Foundation EIN 20-5205458, National Philanthropic Trust EIN 23-7327907, Tides if relevant: their grant schedules name grantees even when donors are anonymous. For each org compute the DAF-routed share of identified funding.
4. Lobbying: Senate LDA bulk data (lda.senate.gov) — registrants, clients, issue codes, fee totals, 2019–2026 YTD.
5. Org self-disclosures ("our funders" pages, annual reports) — capture verbatim with URLs and dates.
6. UK entities via Companies House where filings exist.

REMATCH TASK
The claim package kevinnbass/metr-money-figure asserts donor-advised money to the AI-safety cluster grew from $8M to $66M in the year of Anthropic's first tender offer, with no filing saying whose it is. Verify, bound, or kill that claim from SVCF/NPT/Tides 990-PF data, same KEEP/KILL/OPEN discipline.

DELIVERABLES, in calcs/advocacy-audit/
- research/*.csv — row-id-keyed, per the rules
- compute.py — reads the CSVs, reproduces every aggregate, and asserts each figure; fails loudly on drift
- figures/*.png at 1200x630 plus .svg: (1) safety-side org revenue 2019–2024; (2) funder×org matrix heatmap (sourced amounts only); (3) LDA lobbying fees by lab per year; (4) DAF-routed share per org. Honest axes, label any truncation, captions a non-specialist can read
- STATE.md — every open question, each with the document that would close it
- NOTES.md — the quotable summary: per-org funding profile (declared / DAF-routed / unidentified shares), the verdict table (org × funding-claim × KEEP/KILL/OPEN), top-line findings, and the three strongest sentences a careful writer could publish — each carrying its row ids

SUCCESS CRITERIA
A human can write the post from NOTES.md alone; every number in it survives a hostile fact-check; the verdict table is complete for the org universe; the plots need no rework to publish.

Do NOT commit to git, do not publish anything.
```
