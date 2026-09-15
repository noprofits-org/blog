# Funding around AI regulation: editor’s evidence notes

**Publication boundary:** this audit establishes institutional funding routes, filed financial amounts and attributed self-disclosures. It does not establish a total budget for AI-regulation messaging, donor intent, or the identity of advisers behind particular DAF-sponsor grants. The source population is deliberately bounded and uneven. [V-REMATCH-SCOPE; V-REMATCH-DONOR; V-CAIS-SHARES]

Snapshot: **2026-09-14**. Organization financial histories cover fiscal years ending **2019–2024**; the identified grant pool uses available fiscal years ending **2019–2025**; lobbying covers **2019–2026**, with the latest year limited to completed quarters through **June 30**. [M-SNAPSHOT; M-START; M-REV-END; M-GRANT-END; M-LDA-END; M-LDA-QUARTER]

Every bracketed code is a row ID in [research/](research/). Those rows carry the exact amount, public source URL, snapshot, source excerpt and caveat. Calculated rows in [aggregates.csv](research/aggregates.csv) list every input row. KEEP means the stated, bounded claim is confirmed by its primary source; an attributed self-disclosure confirms what the organization says. KILL means contradicted. OPEN means the necessary evidence is unavailable or insufficient.

## Findings a writer can use

- **The rematch arithmetic survives with a narrower description.** Vanguard’s cash grants to the original figure’s selected recipient set were $8,157,254 [RM-FIGURE-2024] and $65,627,700 [RM-FIGURE-2025] in the fiscal years ending June 2024 and June 2025, respectively. This does not establish messaging expenditure or a source in employee liquidity proceeds. [V-REMATCH-ARITH; V-REMATCH-SCOPE; V-REMATCH-TENDER; V-REMATCH-DONOR]
- **Named institutional grants and company support are both observable.** Good Ventures appears as a filed grant payer to CAIS; Chamber of Progress publicly names corporate partners; ITIF discloses supporters above a threshold. These are different disclosure types and should be described separately. [MX-CAIS-GV; D-PROGRESS; D-ITIF]
- **The organizations also fund one another.** NetChoice’s filed cash grants to TechFreedom total $1,065,000 [MX-TECHFREEDOM-NETCHOICE]; Horizon’s filed cash grants to FAS total $543,982 [MX-FAS-HORIZON]. These flows must not be added across recipients to estimate unique original funding.
- **DAF-sponsor routes occur across the requested groups.** CAIS and TechFreedom both appear in sponsor schedules. The named payer is visible; the adviser and the specific fund type remain unresolved in these rows. [MX-CAIS-SV; MX-CAIS-NP; MX-CAIS-VG; MX-TECHFREEDOM-NP; V-CAIS-SHARES; V-TECHFREEDOM-SHARES]
- **Project and legal-entity accounts require care.** The recommendation pages name receiving charities for AIPI, Encode and IAPS. A receiving charity’s total revenue is not a project budget, and a recommendation is not a paid grant. [S-SFF-2025-C6-6; S-SFF-2024-C9-29; S-SFF-2025-C6-81; V-SFF-CASH]
- **Revenue is not a usable messaging-spend estimate.** FLI’s filed revenue series includes a large positive year followed by negative revenue, with investment results reported separately. ControlAI’s UK filings omit the income-and-expenditure account. [RV-FLI-2021; RV-FLI-2022; V-CONTROL-REVENUE]
- **Lobbying is an all-issues series.** Company expense reports and outside firms’ fees overlap. Blank amounts, missing reports and explicitly named intermediary clients are handled separately; none becomes an invented exact payment. [EX-OpenAI-2024; FE-OpenAI-2024; SF-Anthropic-2024; D-LDA-TOS]

## Three sentences ready to quote

> Vanguard Charitable reported $8,157,254 [RM-FIGURE-2024] and $65,627,700 [RM-FIGURE-2025] in cash grants to the original figure’s selected recipient set in its fiscal years ending June 2024 and June 2025, respectively; the grant rows do not identify the donor advisers. [V-REMATCH-DONOR]

> Chamber of Progress names corporate partners, while ITIF names supporters above a disclosure threshold; neither captured list supplies a complete donor-by-donor funding ledger. [D-PROGRESS; D-ITIF; V-PROGRESS-SHARES; V-ITIF-SHARES]

> NetChoice’s filed cash grants to TechFreedom total $1,065,000 [MX-TECHFREEDOM-NETCHOICE] across its fiscal years ending 2022–2024, while National Philanthropic Trust’s fiscal year ending June 2025 schedule reports $280,000 [MX-TECHFREEDOM-NP]; the schedules do not identify how much supported AI-regulation messaging. [V-TECHFREEDOM-CASH]

## Rematch verdicts and population sensitivity

The original package names **Vanguard Charitable**. Substituting SVCF, NPT or Tides for that payer changes the claim. The incorrect sponsor identifiers in the brief were corrected to SVCF **20-5205488** and NPT **23-7825575**, using primary documents. The examined sponsors file **Form 990, Schedule I**; Good Ventures uses **Form 990-PF**. [D-REMATCH-CLAIM; V-REMATCH-SPONSOR; D-SVCF-EIN; D-NPT-EIN; V-SPONSOR-FORM]

| Author-selected population | Fiscal year ending June 2024 [RM-FIGURE-2024] | Fiscal year ending June 2025 [RM-FIGURE-2025] |
|---|---:|---:|
| Original figure, excluding the author’s borderline tier | $8,157,254 [RM-FIGURE-2024] | $65,627,700 [RM-FIGURE-2025] |
| Same broad category including borderline recipients | $8,384,254 [RM-BORDER-2024] | $65,698,900 [RM-BORDER-2025] |
| Only recipients labeled AI safety by the author | $6,555,488 [RM-AI-2024] | $52,557,061 [RM-AI-2025] |

These are membership sensitivity calculations, not competing estimates of messaging expenditure. The author’s broad category also contains general EA infrastructure; even its AI-safety label does not establish how each grant was used. Recipient names, purpose text, author labels and exact EIN rematches are retained in [rematch.csv](research/rematch.csv). [V-REMATCH-SCOPE]

| Funding claim | Verdict | What the evidence establishes |
|---|---|---|
| The original figure’s rounded growth is supported for its selected recipient set | **KEEP** [V-REMATCH-ARITH] | Exact Vanguard amounts rematch the primary schedules. The figure excludes the author’s borderline tier. This is a recipient-population arithmetic finding, not a spending-purpose finding. |
| The cited growth calculation comes from SVCF, NPT or Tides schedules | **KILL** [V-REMATCH-SPONSOR] | The original claim and exact rematched amounts concern Vanguard Charitable. The named alternative sponsors are separate datasets. |
| Every dollar in the selected cluster is established as AI-regulation messaging spending | **OPEN** [V-REMATCH-SCOPE] | The author’s recipient labels include AI safety and broader EA infrastructure; grant rows do not allocate all recipient spending to policy messaging. |
| The increase occurred in the year of Anthropic’s first tender offer | **OPEN** [V-REMATCH-TENDER] | Primary Vanguard fiscal-period dates are established. No primary tender-offer document confirming both the first-offer status and transaction dates was verified; the temporal and causal link is not established. |
| The rematched filings identify the donor advisers or a tender-proceeds source | **OPEN** [V-REMATCH-DONOR] | The searched Schedule I rows identify the institutional payer and recipient, not the donor adviser. This does not establish that no other public document identifies an adviser. |
| The supplied SVCF EIN identifies the requested sponsor | **KILL** [V-SVCF-ID] | The primary institutional disclosure supplies a different EIN; corrected before grant matching. |
| The supplied NPT EIN identifies the requested sponsor | **KILL** [V-NPT-ID] | The primary return supplies a different EIN; corrected before grant matching. |
| The examined DAF sponsors use private-foundation grant schedules | **KILL** [V-SPONSOR-FORM] | The examined sponsor documents are public-charity Form 990 returns and Schedule I. Good Ventures uses Form 990-PF. |
| SFF recommendation amounts establish completed cash grants | **KILL** [V-SFF-CASH] | The source explicitly warns that some recommended grants might not happen. Recommendations and matching pledges remain separate. |
| The Coefficient grants archive is a single legal payer’s cash ledger | **OPEN** [V-CG-CASH] | The governance page identifies multiple awarding entities and routes. Archive dates and award amounts do not establish cash payment dates or payer identity. |
| The full mixed-purpose Rethink Priorities grant can be allocated to IAPS | **OPEN** [V-IAPS-ALLOCATION] | The filed purpose includes general support and IAPS; no split is supplied. Only explicitly earmarked rows are separately totaled as project grants. |
| ControlAI’s published UK balance sheet establishes annual revenue | **KILL** [V-CONTROL-REVENUE] | The filed accounts expressly omit the income-and-expenditure account. Balance-sheet amounts cannot be substituted for revenue. |
| Historical FTX-related funding amounts to the requested entities are established here | **OPEN** [V-HISTORICAL-FTX] | The captured Building a Stronger Future return’s domestic schedule has no matched universe grantee. The historical FTX Future Fund site was inaccessible during retrieval. No historical payment, promise, recovery or present funding is imputed. |

## How to read the funding shares

**Declared share of total funding: OPEN. Confirmed DAF share of total funding: OPEN. Unidentified share of total funding: OPEN.** This applies across the universe: there is no reconciled public donor-by-period receipts ledger in the examined records. “Unidentified” is therefore an unquantified gap, not a percentage residual. [V-CAIS-SHARES; V-AIPI-SHARES; V-ENCODE-SHARES; V-FLI-SHARES; V-CONTROL-SHARES; V-SAIF-SHARES; V-IAPS-SHARES; V-HORIZON-SHARES; V-ARI-SHARES; V-PC-SHARES; V-FAS-SHARES; V-PROGRESS-SHARES; V-ITIF-SHARES; V-TECHFREEDOM-SHARES; V-NETCHOICE-SHARES]

The observable ratio is **DAF-sponsor-routed cash / (DAF-sponsor-routed cash + direct-institution cash)** within the identified filed-grant pool. Both cash subtotals remain separately labeled. This denominator excludes awards, recommendations, matching pledges, commitments, lobbying and organization revenue. It also excludes unallocated project grants, foreign schedules, unnamed subgrants and funding outside the searched returns. The sponsors report maintaining donor-advised funds or similar accounts in their own returns. The legal sponsor alone does not establish that each individual grant was donor-advised. [DP-CAIS; DP-TECHFREEDOM; V-IAPS-ALLOCATION; SP-SVCF; SP-NPT; SP-Vanguard; SP-Tides]

A high ratio can reflect narrow source coverage. For example, the FLI ratio describes the small identified payer-side pool, while its own donor page names other donors without dollar amounts. It cannot be used as a share of FLI’s whole budget. A zero route subtotal describes an empty subset of an observed pool; an absent pool is OPEN. [DP-FLI; D-FLI; DP-ARI; DP-AIPI]

## Organization profiles

Group assignments follow the brief. Related legal entities are shown separately. CAIS Action Fund and AI Policy Network address the requested advocacy arms; Encode Research is identified by Encode’s own legal notice; Public Citizen Foundation is its related charitable entity; CRI is included because ARI links to it as the related research organization. No consolidated budget or particular legal-control relationship is inferred from a website link. No requested family was established to be defunct in the bounded identity review. [ID-CAISAF; D-AIPI-AIPN; D-ENCODE-ARMS; ID-PCF; D-ARI-CRI; ID-CONTROL]

### Center for AI Safety

The charitable entity and Action Fund have distinct returns. Their amounts are not consolidated here. [ID-CAIS; ID-CAISAF]

- **Center for AI Safety**: 501(c)(3); EIN 881751310. [ID-CAIS]
- **Center for AI Safety Action Fund**: 501(c)(4); EIN 932442608. [ID-CAISAF]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Center for AI Safety | 2024-12-31 [R-CAIS-2024-REV-3615] | $10,235,085 [R-CAIS-2024-REV-3615] | $12,638,754 [R-CAIS-2024-ASSETS-3615] | $6,288,786 [R-CAIS-2024-PROGRAM-3615] |
| Center for AI Safety Action Fund | 2024-12-31 [R-CAISAF-2024-REV-3287] | $3,577,153 [R-CAISAF-2024-REV-3287] | $1,890,527 [R-CAISAF-2024-ASSETS-3287] | $2,265,597 [R-CAISAF-2024-PROGRAM-3287] |

**Declared sources (amount shares OPEN).**
No adequate amount-bearing supporter ledger in the specifically captured pages; the per-entity page search is listed in STATE.md. [V-CAIS-DECLARED; V-CAISAF-DECLARED]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.

| Recipient | Filed payer | Cash |
|---|---|---:|
| Center for AI Safety | Good Ventures | $11,052,288 [MX-CAIS-GV] |
| Center for AI Safety | NPT | $222,000 [MX-CAIS-NP] |
| Center for AI Safety | SVCF | $2,505,740 [MX-CAIS-SV] |
| Center for AI Safety | Vanguard | $1,298,500 [MX-CAIS-VG] |

**Separate money types — do not add to the cash table.**

| Entity/project | Source period | Type | Amount |
|---|---|---|---:|
| Center for AI Safety | 2022 [AW-CAIS-2022-published_award] | published award | $5,160,000 [AW-CAIS-2022-published_award] |
| Center for AI Safety | 2023 [AW-CAIS-2023-published_award] | published award | $7,325,288 [AW-CAIS-2023-published_award] |
| Center for AI Safety | 2023 [RC-CAIS-2023-recommendation] | recommendation | $931,154 [RC-CAIS-2023-recommendation] |
| Center for AI Safety | 2024 [RC-CAIS-2024-recommendation] | recommendation | $1,146,000 [RC-CAIS-2024-recommendation] |
| Center for AI Safety | 2025 [RC-CAIS-2025-recommendation] | recommendation | $289,000 [RC-CAIS-2025-recommendation] |
| CAIS Action Fund | 2023 [RC-CAISAF-2023-recommendation] | recommendation | $420,000 [RC-CAISAF-2023-recommendation] |
| CAIS Action Fund | 2024 [RC-CAISAF-2024-recommendation] | recommendation | $1,621,000 [RC-CAISAF-2024-recommendation] |
| CAIS Action Fund | 2025 [RC-CAISAF-2025-recommendation] | recommendation | $772,000 [RC-CAISAF-2025-recommendation] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Center for AI Safety | $4,026,240 [DN-CAIS] | $11,052,288 [DD-CAIS] | 26.7% [DP-CAIS] |
| Center for AI Safety Action Fund | OPEN [DN-CAISAF] | OPEN [DD-CAISAF] | OPEN [DP-CAISAF] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-CAIS-SHARES; V-CAISAF-SHARES]

### AI Policy Institute

Standalone AIPI tax identity remains OPEN; its own site claims charitable status. The IRS registry identifies AI Policy Network separately. SFF’s later recommendation names The Hack Foundation as receiving charity; this does not establish an AIPI cash receipt or make Hack’s total revenue an AIPI budget. [ID-AIPI; ID-AIPN; D-AIPI-AIPN; S-SFF-2025-C6-6]

- **AI Policy Network**: 501(c)(4); EIN 994513850. [ID-AIPN]
- **AI Policy Institute**: Self-described charity; fiscal-sponsored recommendation identified; standalone identifier unresolved. [ID-AIPI]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| AI Policy Network | OPEN | OPEN [H-AIPN-2024] | OPEN [ID-AIPN] | OPEN [ID-AIPN] |
| AI Policy Institute | OPEN | OPEN [H-AIPI-2024] | OPEN [ID-AIPI] | OPEN [ID-AIPI] |

**Declared sources (amount shares OPEN).**
No adequate amount-bearing supporter ledger in the specifically captured pages; the per-entity page search is listed in STATE.md. [V-AIPN-DECLARED; V-AIPI-DECLARED]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.
No matched legal-grantee cash amount in the searched schedules. [CV-AIPN; CV-AIPI]

**Separate money types — do not add to the cash table.**

| Entity/project | Source period | Type | Amount |
|---|---|---|---:|
| AI Policy Institute | 2024 [RC-AIPI-2024-recommendation] | recommendation | $142,000 [RC-AIPI-2024-recommendation] |
| AI Policy Institute | 2025 [RC-AIPI-2025-recommendation] | recommendation | $1,635,000 [RC-AIPI-2025-recommendation] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| AI Policy Network | OPEN [DN-AIPN] | OPEN [DD-AIPN] | OPEN [DP-AIPN] |
| AI Policy Institute | OPEN [DN-AIPI] | OPEN [DD-AIPI] | OPEN [DP-AIPI] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-AIPN-SHARES; V-AIPI-SHARES]

### Encode Justice / Encode

Encode’s legal notice names a corporation and research foundation. The foundation has a registry identity; the corporation’s EIN/determination remains OPEN. SFF names March On Foundation in the earlier recommendation and Encode AI Corporation in the later one. Encode also reports individual donations from rank-and-file frontier-lab employees; those are not corporate grants. [D-ENCODE-ARMS; ID-ENCODE; ID-ENCODER; S-SFF-2024-C9-29; S-SFF-2025-C6-32; D-ENCODE-EMPLOYEES]

- **Encode Research Foundation**: 501(c)(3); EIN 333199430. [ID-ENCODER]
- **Encode AI Corporation / Encode Justice**: Self-described 501(c)(4); standalone identifier unresolved. [ID-ENCODE]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Encode Research Foundation | OPEN | OPEN [H-ENCODER-2024] | OPEN [ID-ENCODER] | OPEN [ID-ENCODER] |
| Encode AI Corporation / Encode Justice | OPEN | OPEN [H-ENCODE-2024] | OPEN [ID-ENCODE] | OPEN [ID-ENCODE] |

**Declared sources (amount shares OPEN).**
Rank-and-file frontier-lab employees, Heising-Simons Foundation, Survival and Flourishing Fund, Responsible Technology Youth Power Fund, Archewell Foundation, We Are Family Foundation, Future of Life Institute, America’s Promise Alliance. [D-ENCODE-EMPLOYEES]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.
No matched legal-grantee cash amount in the searched schedules. [CV-ENCODER; CV-ENCODE]

**Separate money types — do not add to the cash table.**

| Entity/project | Source period | Type | Amount |
|---|---|---|---:|
| Encode AI | 2024 [RC-ENCODE-2024-recommendation] | recommendation | $50,000 [RC-ENCODE-2024-recommendation] |
| Encode AI | 2025 [RC-ENCODE-2025-recommendation] | recommendation | $516,000 [RC-ENCODE-2025-recommendation] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Encode Research Foundation | OPEN [DN-ENCODER] | OPEN [DD-ENCODER] | OPEN [DP-ENCODER] |
| Encode AI Corporation / Encode Justice | OPEN [DN-ENCODE] | OPEN [DD-ENCODE] | OPEN [DP-ENCODE] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-ENCODER-SHARES; V-ENCODE-SHARES]

### Future of Life Institute

Its donor page identifies Vitalik Buterin as its largest donor and names other supporters, without donor-by-period amounts. The annual revenue series must retain investment gains and losses. [D-FLI; RV-FLI-2021; RV-FLI-2022]

- **Future of Life Institute**: 501(c)(3); EIN 471052538. [ID-FLI]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Future of Life Institute | 2024-12-31 [R-FLI-2024-REV-3667] | $21,273,381 [R-FLI-2024-REV-3667] | $6,348,222 [R-FLI-2024-ASSETS-3667] | $15,846,086 [R-FLI-2024-PROGRAM-3667] |

**Declared sources (amount shares OPEN).**
Vitalik Buterin, Jaan Tallinn, Elon Musk (historical seed funding), Erik Otto. [D-FLI]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.

| Recipient | Filed payer | Cash |
|---|---|---:|
| Future of Life Institute | SVCF | $556,200 [MX-FLI-SV] |

**Separate money types — do not add to the cash table.**

| Entity/project | Source period | Type | Amount |
|---|---|---|---:|
| Future of Life Institute | 2015 [AW-FLI-2015-published_award] | published award | $1,186,000 [AW-FLI-2015-published_award] |
| Future of Life Institute | 2016 [AW-FLI-2016-published_award] | published award | $100,000 [AW-FLI-2016-published_award] |
| Future of Life Institute | 2017 [AW-FLI-2017-published_award] | published award | $100,000 [AW-FLI-2017-published_award] |
| Future of Life Institute | 2018 [AW-FLI-2018-published_award] | published award | $250,000 [AW-FLI-2018-published_award] |
| Future of Life Institute | 2019 [AW-FLI-2019-published_award] | published award | $100,000 [AW-FLI-2019-published_award] |
| Future of Life Institute | 2020 [AW-FLI-2020-published_award] | published award | $176,000 [AW-FLI-2020-published_award] |
| Future of Life Institute | 2020 [RC-FLI-2020-recommendation] | recommendation | $510,000 [RC-FLI-2020-recommendation] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Future of Life Institute | $556,200 [DN-FLI] | $0 [DD-FLI] | 100.0% [DP-FLI] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-FLI-SHARES]

### ControlAI

Companies House establishes a company limited by guarantee, currently named CONTROLAI and previously Secure Future Research Ltd. That does not establish charity tax exemption. Filed balance sheets are in uk_accounts.csv; the filings omit annual income-and-expenditure accounts. The site’s separate US social-welfare entity claim remains unverified. [ID-CONTROL; D-CONTROL-NAME; D-CONTROL-NO-PL; D-CONTROL-NO-PL-2025; D-CONTROL-US]

- **ControlAI (UK)**: UK company limited by guarantee; charitable tax status OPEN; company 15088415. [ID-CONTROL]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| ControlAI (UK) | 2024-12-31 [UKA-CONTROL-2024] | OPEN [H-CONTROL-2024] | £5,506,577 [UKA-CONTROL-2024] | OPEN [D-CONTROL-NO-PL] |

**Declared sources (amount shares OPEN).**
No adequate amount-bearing supporter ledger in the specifically captured pages; the per-entity page search is listed in STATE.md. [V-CONTROL-DECLARED]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.
No matched legal-grantee cash amount in the searched schedules. [CV-CONTROL]

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| ControlAI (UK) | OPEN [DN-CONTROL] | OPEN [DD-CONTROL] | OPEN [DP-CONTROL] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-CONTROL-SHARES]

### Safe AI Forum

The standalone legal entity has a primary financial return. SFF’s earlier recommendation separately names FAR AI as receiving charity; FAR AI’s whole budget is not assigned to this entity. The program-expense field is an explicit filed zero in Part IX. [ID-SAIF; S-SFF-2024-C9-62; R-SAIF-2024-PROGRAM-IX]

- **Safe AI Forum**: 501(c)(3); EIN 934950919. [ID-SAIF]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Safe AI Forum | 2024-12-31 [R-SAIF-2024-REV-0600] | $2,182,205 [R-SAIF-2024-REV-0600] | $2,133,588 [R-SAIF-2024-ASSETS-0600] | $0 [R-SAIF-2024-PROGRAM-IX] |

**Declared sources (amount shares OPEN).**
No adequate amount-bearing supporter ledger in the specifically captured pages; the per-entity page search is listed in STATE.md. [V-SAIF-DECLARED]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.

| Recipient | Filed payer | Cash |
|---|---|---:|
| Safe AI Forum | Good Ventures | $1,100,000 [MX-SAIF-GV] |
| Safe AI Forum | NPT | $345,000 [MX-SAIF-NP] |

**Separate money types — do not add to the cash table.**

| Entity/project | Source period | Type | Amount |
|---|---|---|---:|
| Safe AI Forum | 2023 [AW-SAIF-2023-published_award] | published award | $1,167,513 [AW-SAIF-2023-published_award] |
| Safe AI Forum | 2024 [RC-SAIF-2024-recommendation] | recommendation | $580,000 [RC-SAIF-2024-recommendation] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Safe AI Forum | $345,000 [DN-SAIF] | $1,100,000 [DD-SAIF] | 23.9% [DP-SAIF] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-SAIF-SHARES]

### Institute for AI Policy and Strategy

The IRS registry identifies the present standalone charity, while the captured historical SFF recommendations name Rethink Priorities as receiving charity. Good Ventures’ expressly earmarked project payments to Rethink are a separate dataset. The mixed-purpose grant’s full amount cannot be assigned to IAPS. [ID-IAPS; S-SFF-2025-C6-81; V-IAPS-ALLOCATION]

- **Institute for AI Policy and Strategy**: 501(c)(3); EIN 320839313. [ID-IAPS]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Institute for AI Policy and Strategy | OPEN | OPEN [H-IAPS-2024] | OPEN [ID-IAPS] | OPEN [ID-IAPS] |

**Declared sources (amount shares OPEN).**
Coefficient Giving, Hewlett Foundation, Longview, Macroscopic Ventures, Survival and Flourishing Fund, allied government, individual donors. [D-IAPS]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.
No matched legal-grantee cash amount in the searched schedules. [CV-IAPS]

**Separate money types — do not add to the cash table.**

| Entity/project | Source period | Type | Amount |
|---|---|---|---:|
| IAPS | 2024 [AW-IAPS-2024-published_award] | published award | $3,839,944 [AW-IAPS-2024-published_award] |
| IAPS | 2025 [AW-IAPS-2025-published_award] | published award | $11,510,081 [AW-IAPS-2025-published_award] |
| IAPS | 2024 [PJ-IAPS-2024-filed_mixed_purpose_grant] | filed mixed purpose grant | $2,100,000 [PJ-IAPS-2024-filed_mixed_purpose_grant] |
| IAPS | 2024 [PJ-IAPS-2024-filed_project_earmarked_grant] | filed project earmarked grant | $2,448,234 [PJ-IAPS-2024-filed_project_earmarked_grant] |
| IAPS | 2025 [PJ-IAPS-2025-filed_project_earmarked_grant] | filed project earmarked grant | $1,391,710 [PJ-IAPS-2025-filed_project_earmarked_grant] |
| IAPS | 2024 [RC-IAPS-2024-recommendation] | recommendation | $183,000 [RC-IAPS-2024-recommendation] |
| IAPS | 2025 [RC-IAPS-2025-matching_commitment] | matching commitment | $300,000 [RC-IAPS-2025-matching_commitment] |
| IAPS | 2025 [RC-IAPS-2025-recommendation] | recommendation | $572,000 [RC-IAPS-2025-recommendation] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Institute for AI Policy and Strategy | OPEN [DN-IAPS] | OPEN [DD-IAPS] | OPEN [DP-IAPS] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-IAPS-SHARES]

### Horizon Institute for Public Service

Horizon’s current page names funders and says no donor supplies a majority. The page does not define a covered fiscal period; that statement is not applied to earlier returns. Horizon also appears as a payer to FAS. [D-HORIZON; MX-FAS-HORIZON]

- **Horizon Institute for Public Service**: 501(c)(3); EIN 874657441. [ID-HORIZON]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Horizon Institute for Public Service | 2024-12-31 [R-HORIZON-2024-REV-4082] | $13,091,933 [R-HORIZON-2024-REV-4082] | $20,024,961 [R-HORIZON-2024-ASSETS-4082] | $4,827,290 [R-HORIZON-2024-PROGRAM-4082] |

**Declared sources (amount shares OPEN).**
Helena, Renaissance Philanthropy, Maurice Amado Foundation, Policy Entrepreneurs Network, Lonsdale Family Philanthropic Fund, Coefficient Giving, Navigation Fund, Packard Foundation, Fulcrum Science, Food Systems Innovation, John Quincy Adams Society, Sentinel Bio. [D-HORIZON]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.

| Recipient | Filed payer | Cash |
|---|---|---:|
| Horizon Institute | Coefficient Action Fund | $100,000 [MX-HORIZON-CA] |
| Horizon Institute | Good Ventures | $11,837,990 [MX-HORIZON-GV] |
| Horizon Institute | NPT | $7,527,232 [MX-HORIZON-NP] |
| Horizon Institute | SVCF | $6,451,344 [MX-HORIZON-SV] |
| Horizon Institute | Vanguard | $7,617,664 [MX-HORIZON-VG] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Horizon Institute for Public Service | $21,596,240 [DN-HORIZON] | $11,937,990 [DD-HORIZON] | 64.4% [DP-HORIZON] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-HORIZON-SHARES]

### Americans for Responsible Innovation

ARI and CRI have separate legal identities and returns. A Coefficient archive award and the Action Fund’s paid-grant amount are distinct measures; their difference is not silently “corrected” or added together. The ARI website link supports including CRI, without establishing consolidated control. [ID-ARI; ID-CRI; D-ARI-CRI; MX-ARI-CA; V-CG-CASH]

- **Americans for Responsible Innovation**: 501(c)(4); EIN 933248564. [ID-ARI]
- **Center for Responsible Innovation**: 501(c)(3); EIN 990921925. [ID-CRI]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Americans for Responsible Innovation | 2024-12-31 [R-ARI-2024-REV-2380] | $5,244,469 [R-ARI-2024-REV-2380] | $3,514,963 [R-ARI-2024-ASSETS-2380] | $2,083,880 [R-ARI-2024-PROGRAM-2380] |
| Center for Responsible Innovation | 2024-12-31 [R-CRI-2024-REV-2505] | $4,631,047 [R-CRI-2024-REV-2505] | $4,176,715 [R-CRI-2024-ASSETS-2505] | $950,000 [R-CRI-2024-PROGRAM-2505] |

**Declared sources (amount shares OPEN).**
Inclusive Abundance Action, Omidyar Network, Coefficient Giving, Brad Carson and Julie Carson, Eric Gastfriend and Caroline Mehl, Steve Newman. [D-ARI]
Founders Pledge, Laidir Foundation, Coefficient Giving, David and Lucile Packard Foundation, Omidyar Network, Sentinel Bio, individual donors. [D-CRI]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.

| Recipient | Filed payer | Cash |
|---|---|---:|
| Americans for Responsible Innovation | Coefficient Action Fund | $2,948,728 [MX-ARI-CA] |
| Center for Responsible Innovation | Good Ventures | $3,000,000 [MX-CRI-GV] |
| Center for Responsible Innovation | Vanguard | $700,000 [MX-CRI-VG] |

**Separate money types — do not add to the cash table.**

| Entity/project | Source period | Type | Amount |
|---|---|---|---:|
| Americans for Responsible Innovation | 2024 [AW-ARI-2024-published_award] | published award | $3,000,000 [AW-ARI-2024-published_award] |
| Center for Responsible Innovation | 2024 [AW-CRI-2024-published_award] | published award | $3,000,000 [AW-CRI-2024-published_award] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Americans for Responsible Innovation | $0 [DN-ARI] | $2,948,728 [DD-ARI] | 0.0% [DP-ARI] |
| Center for Responsible Innovation | $700,000 [DN-CRI] | $3,000,000 [DD-CRI] | 18.9% [DP-CRI] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-ARI-SHARES; V-CRI-SHARES]

### Public Citizen

Public Citizen and its foundation are kept separate, including the foundation’s grants to Public Citizen. The official annual-report page states that it does not accept corporate or government money; that is an attributed policy, not an audited donor ledger. [ID-PC; ID-PCF; MX-PC-PCF; D-PC-POLICY]

- **Public Citizen**: 501(c)(4); EIN 237104508. [ID-PC]
- **Public Citizen Foundation**: 501(c)(3); EIN 521263996. [ID-PCF]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Public Citizen | 2024-09-30 [R-PC-2024-REV-0917] | $8,390,404 [R-PC-2024-REV-0917] | $3,281,426 [R-PC-2024-ASSETS-0917] | $5,931,037 [R-PC-2024-PROGRAM-0917] |
| Public Citizen Foundation | 2024-09-30 [R-PCF-2024-REV-1107] | $14,844,863 [R-PCF-2024-REV-1107] | $35,761,953 [R-PCF-2024-ASSETS-1107] | $15,488,946 [R-PCF-2024-PROGRAM-1107] |

**Declared sources (amount shares OPEN).**
Individual donors and foundation grants (categories only). [D-PC-POLICY]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.

| Recipient | Filed payer | Cash |
|---|---|---:|
| Public Citizen | Public Citizen Foundation | $625,000 [MX-PC-PCF] |
| Public Citizen | Tides | $1,210,360 [MX-PC-TI] |
| Public Citizen Foundation | NPT | $182,750 [MX-PCF-NP] |
| Public Citizen Foundation | SVCF | $21,250 [MX-PCF-SV] |
| Public Citizen Foundation | Tides | $3,474,640 [MX-PCF-TI] |
| Public Citizen Foundation | Vanguard | $519,050 [MX-PCF-VG] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Public Citizen | $1,210,360 [DN-PC] | $625,000 [DD-PC] | 65.9% [DP-PC] |
| Public Citizen Foundation | $4,197,690 [DN-PCF] | $0 [DD-PCF] | 100.0% [DP-PCF] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-PC-SHARES; V-PCF-SHARES]

### Federation of American Scientists

FAS is a comparator with a broad program portfolio. Its annual report names philanthropic and agency supporters. The separately reported new commitments are $51,000,000 [C-FAS-2023]; this is not revenue or paid-grant cash. [D-FAS]

- **Federation of American Scientists**: 501(c)(3); EIN 237185827. [ID-FAS]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Federation of American Scientists | 2024-06-30 [R-FAS-2024-REV-3450] | $29,395,631 [R-FAS-2024-REV-3450] | $32,515,997 [R-FAS-2024-ASSETS-3450] | $23,692,039 [R-FAS-2024-PROGRAM-3450] |

**Declared sources (amount shares OPEN).**
Good Ventures Foundation, Open Philanthropy, Future of Life Institute, Horizon Institute for Public Service, National Philanthropic Trust, Silicon Valley Community Foundation, William and Flora Hewlett Foundation, Gates Foundation, Schmidt Futures, federal agencies, other listed supporters. [D-FAS]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.

| Recipient | Filed payer | Cash |
|---|---|---:|
| Federation of American Scientists | Coefficient Action Fund | $1,011,000 [MX-FAS-CA] |
| Federation of American Scientists | Future of Life Institute | $750,000 [MX-FAS-FL] |
| Federation of American Scientists | Good Ventures | $1,807,003 [MX-FAS-GV] |
| Federation of American Scientists | Horizon Institute for Public Service | $543,982 [MX-FAS-HORIZON] |
| Federation of American Scientists | NPT | $643,800 [MX-FAS-NP] |
| Federation of American Scientists | SVCF | $1,615,500 [MX-FAS-SV] |
| Federation of American Scientists | Vanguard | $70,000 [MX-FAS-VG] |

**Separate money types — do not add to the cash table.**

| Entity/project | Source period | Type | Amount |
|---|---|---|---:|
| Federation of American Scientists | 2020 [AW-FAS-2020-published_award] | published award | $175,000 [AW-FAS-2020-published_award] |
| Federation of American Scientists | 2021 [AW-FAS-2021-published_award] | published award | $1,080,000 [AW-FAS-2021-published_award] |
| Federation of American Scientists | 2023 [AW-FAS-2023-published_award] | published award | $352,150 [AW-FAS-2023-published_award] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Federation of American Scientists | $2,329,300 [DN-FAS] | $4,111,985 [DD-FAS] | 36.2% [DP-FAS] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-FAS-SHARES]

### Chamber of Progress

The corporate-partner page names Amazon, Google, OpenAI and other companies. No per-company payment is supplied there. The filed organization total is not an AI-only budget. [D-PROGRESS; V-PROGRESS-SHARES]

- **Chamber of Progress**: 501(c)(6); EIN 853963084. [ID-PROGRESS]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Chamber of Progress | 2024-12-31 [R-PROGRESS-2024-REV-0333] | $9,683,024 [R-PROGRESS-2024-REV-0333] | $14,346,791 [R-PROGRESS-2024-ASSETS-0333] | OPEN [O-METRIC-PROGRESS-2024-PROGRAM] |

**Declared sources (amount shares OPEN).**
Amazon, Google, OpenAI, Apple, a16z, other listed corporate partners. [D-PROGRESS]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.
No matched legal-grantee cash amount in the searched schedules. [CV-PROGRESS]

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Chamber of Progress | OPEN [DN-PROGRESS] | OPEN [DD-PROGRESS] | OPEN [DP-PROGRESS] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-PROGRESS-SHARES]

### ITIF

The supporter page’s disclosure threshold is greater than $10,000 [D-ITIF]. The page includes Alphabet, Amazon, Anthropic, Meta and Microsoft, but it does not define a precise ending date for its “past fiscal year” or give each payment amount. [D-ITIF]

- **Information Technology and Innovation Foundation**: 501(c)(3); EIN 204403497. [ID-ITIF]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| Information Technology and Innovation Foundation | 2024-02-29 [R-ITIF-2024-REV-1018] | $6,645,853 [R-ITIF-2024-REV-1018] | $11,213,072 [R-ITIF-2024-ASSETS-1018] | $4,474,367 [R-ITIF-2024-PROGRAM-1018] |

**Declared sources (amount shares OPEN).**
Alphabet, Amazon, Anthropic, Meta, Microsoft, other listed supporters. [D-ITIF]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.

| Recipient | Filed payer | Cash |
|---|---|---:|
| ITIF | NPT | $233,300 [MX-ITIF-NP] |
| ITIF | Vanguard | $43,200 [MX-ITIF-VG] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| Information Technology and Innovation Foundation | $276,500 [DN-ITIF] | $0 [DD-ITIF] | 100.0% [DP-ITIF] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-ITIF-SHARES]

### TechFreedom

The captured About page does not provide an adequate funder list. Payer-side schedules nevertheless identify NetChoice cash grants and a separate NPT-routed grant. The NPT grant’s generic filed purpose is retained verbatim, without using it to classify TechFreedom’s activities. [D-TECHFREEDOM; MX-TECHFREEDOM-NETCHOICE; MX-TECHFREEDOM-NP]

- **TechFreedom**: 501(c)(3); EIN 273567814. [ID-TECHFREEDOM]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| TechFreedom | 2024-12-31 [R-TECHFREEDOM-2024-REV-9381] | $1,459,546 [R-TECHFREEDOM-2024-REV-9381] | $130,714 [R-TECHFREEDOM-2024-ASSETS-9381] | $1,057,077 [R-TECHFREEDOM-2024-PROGRAM-9381] |

**Declared sources (amount shares OPEN).**
No adequate amount-bearing supporter ledger in the specifically captured pages; the per-entity page search is listed in STATE.md. [V-TECHFREEDOM-DECLARED]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.

| Recipient | Filed payer | Cash |
|---|---|---:|
| TechFreedom | NetChoice | $1,065,000 [MX-TECHFREEDOM-NETCHOICE] |
| TechFreedom | NPT | $280,000 [MX-TECHFREEDOM-NP] |

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| TechFreedom | $280,000 [DN-TECHFREEDOM] | $1,065,000 [DD-TECHFREEDOM] | 20.8% [DP-TECHFREEDOM] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-TECHFREEDOM-SHARES]

### NetChoice

The captured current About page has an Association Members heading but no member names in that section. This is a bounded snapshot observation, not a claim about every public membership disclosure. Its own grant schedule establishes payments to TechFreedom. Earlier revenue, expenses and assets use explicitly filed comparatives where the scanned-return route was disallowed. [D-NETCHOICE; MX-TECHFREEDOM-NETCHOICE; R-NETCHOICE-2019-REV-COMP; ACCESS-NETCHOICE-SCAN]

- **NetChoice**: 501(c)(6); EIN 271716101. [ID-NETCHOICE]

**Latest financials in the requested window**

| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |
|---|---|---:|---:|---:|
| NetChoice | 2024-12-31 [R-NETCHOICE-2024-REV-0534] | $22,621,094 [R-NETCHOICE-2024-REV-0534] | $13,679,206 [R-NETCHOICE-2024-ASSETS-0534] | OPEN [O-METRIC-NETCHOICE-2024-PROGRAM] |

**Declared sources (amount shares OPEN).**
No adequate amount-bearing supporter ledger in the specifically captured pages; the per-entity page search is listed in STATE.md. [V-NETCHOICE-DECLARED]

**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.
No matched legal-grantee cash amount in the searched schedules. [CV-NETCHOICE]

**Observed sponsor route and unknown shares.**

| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |
|---|---:|---:|---:|
| NetChoice | OPEN [DN-NETCHOICE] | OPEN [DD-NETCHOICE] | OPEN [DP-NETCHOICE] |
Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. [V-NETCHOICE-SHARES]

## Complete organization × claim verdict table

Cash = a matched legal-grantee cash payment in the searched filings. Declared = an attributed funding-source disclosure, sometimes categories rather than names. Route = a matched DAF-sponsor payment. Shares = complete shares of total funding. Related entities are listed within their requested family.

| Organization / legal entity | Identity and tax status | Filed cash | Declared sources | DAF-sponsor route | Complete funding shares |
|---|---|---|---|---|---|
| Center for AI Safety | KEEP [V-CAIS-STATUS] | KEEP [V-CAIS-CASH] | OPEN [V-CAIS-DECLARED] | KEEP [V-CAIS-ROUTE] | OPEN [V-CAIS-SHARES] |
| Center for AI Safety Action Fund | KEEP [V-CAISAF-STATUS] | OPEN [V-CAISAF-CASH] | OPEN [V-CAISAF-DECLARED] | OPEN [V-CAISAF-ROUTE] | OPEN [V-CAISAF-SHARES] |
| AI Policy Network | KEEP [V-AIPN-STATUS] | OPEN [V-AIPN-CASH] | OPEN [V-AIPN-DECLARED] | OPEN [V-AIPN-ROUTE] | OPEN [V-AIPN-SHARES] |
| AI Policy Institute | OPEN [V-AIPI-STATUS] | OPEN [V-AIPI-CASH] | OPEN [V-AIPI-DECLARED] | OPEN [V-AIPI-ROUTE] | OPEN [V-AIPI-SHARES] |
| Encode Research Foundation | KEEP [V-ENCODER-STATUS] | OPEN [V-ENCODER-CASH] | OPEN [V-ENCODER-DECLARED] | OPEN [V-ENCODER-ROUTE] | OPEN [V-ENCODER-SHARES] |
| Encode AI Corporation / Encode Justice | OPEN [V-ENCODE-STATUS] | OPEN [V-ENCODE-CASH] | KEEP [V-ENCODE-DECLARED] | OPEN [V-ENCODE-ROUTE] | OPEN [V-ENCODE-SHARES] |
| Future of Life Institute | KEEP [V-FLI-STATUS] | KEEP [V-FLI-CASH] | KEEP [V-FLI-DECLARED] | KEEP [V-FLI-ROUTE] | OPEN [V-FLI-SHARES] |
| ControlAI (UK) | OPEN [V-CONTROL-STATUS] | OPEN [V-CONTROL-CASH] | OPEN [V-CONTROL-DECLARED] | OPEN [V-CONTROL-ROUTE] | OPEN [V-CONTROL-SHARES] |
| Safe AI Forum | KEEP [V-SAIF-STATUS] | KEEP [V-SAIF-CASH] | OPEN [V-SAIF-DECLARED] | KEEP [V-SAIF-ROUTE] | OPEN [V-SAIF-SHARES] |
| Institute for AI Policy and Strategy | KEEP [V-IAPS-STATUS] | OPEN [V-IAPS-CASH] | KEEP [V-IAPS-DECLARED] | OPEN [V-IAPS-ROUTE] | OPEN [V-IAPS-SHARES] |
| Horizon Institute for Public Service | KEEP [V-HORIZON-STATUS] | KEEP [V-HORIZON-CASH] | KEEP [V-HORIZON-DECLARED] | KEEP [V-HORIZON-ROUTE] | OPEN [V-HORIZON-SHARES] |
| Americans for Responsible Innovation | KEEP [V-ARI-STATUS] | KEEP [V-ARI-CASH] | KEEP [V-ARI-DECLARED] | OPEN [V-ARI-ROUTE] | OPEN [V-ARI-SHARES] |
| Center for Responsible Innovation | KEEP [V-CRI-STATUS] | KEEP [V-CRI-CASH] | KEEP [V-CRI-DECLARED] | KEEP [V-CRI-ROUTE] | OPEN [V-CRI-SHARES] |
| Public Citizen | KEEP [V-PC-STATUS] | KEEP [V-PC-CASH] | KEEP [V-PC-DECLARED] | KEEP [V-PC-ROUTE] | OPEN [V-PC-SHARES] |
| Public Citizen Foundation | KEEP [V-PCF-STATUS] | KEEP [V-PCF-CASH] | OPEN [V-PCF-DECLARED] | KEEP [V-PCF-ROUTE] | OPEN [V-PCF-SHARES] |
| Federation of American Scientists | KEEP [V-FAS-STATUS] | KEEP [V-FAS-CASH] | KEEP [V-FAS-DECLARED] | KEEP [V-FAS-ROUTE] | OPEN [V-FAS-SHARES] |
| Chamber of Progress | KEEP [V-PROGRESS-STATUS] | OPEN [V-PROGRESS-CASH] | KEEP [V-PROGRESS-DECLARED] | OPEN [V-PROGRESS-ROUTE] | OPEN [V-PROGRESS-SHARES] |
| Information Technology and Innovation Foundation | KEEP [V-ITIF-STATUS] | KEEP [V-ITIF-CASH] | KEEP [V-ITIF-DECLARED] | KEEP [V-ITIF-ROUTE] | OPEN [V-ITIF-SHARES] |
| TechFreedom | KEEP [V-TECHFREEDOM-STATUS] | KEEP [V-TECHFREEDOM-CASH] | OPEN [V-TECHFREEDOM-DECLARED] | KEEP [V-TECHFREEDOM-ROUTE] | OPEN [V-TECHFREEDOM-SHARES] |
| NetChoice | KEEP [V-NETCHOICE-STATUS] | OPEN [V-NETCHOICE-CASH] | OPEN [V-NETCHOICE-DECLARED] | OPEN [V-NETCHOICE-ROUTE] | OPEN [V-NETCHOICE-SHARES] |

## Lab lobbying figures a writer can quote

**These are numeric reported amounts, not exact economic costs or AI-specific allocations.** Amendments replace earlier reports for the same registrant/client/year/quarter. Company expenses and outside fees overlap and must not be added. Explicitly named intermediary clients are a separate fee series in the CSVs. An inconsistent expense-field report from a different registrant is excluded and recorded as OPEN. The named company scope includes the documented corporate names and subsidiaries, with separately branded or unrelated matches excluded. [EX-Microsoft-2024; FE-Microsoft-2024; SF-Microsoft-2019; D-XCORP-SCOPE]

The latest year is a completed-quarter subtotal, not an annualized estimate. OpenAI’s earliest numeric reports in this series cover only the final quarter of that year. An OPEN cell means no eligible numeric report in the bounded client-name queries; it never means no spending. The xAI queries did not yield a numeric report; X Corp.’s report is not allocated to xAI. [M-LDA-QUARTER; EX-OpenAI-2023; FE-OpenAI-2023; EX-xAI-2026; D-XCORP-SCOPE]

| Company | Filing year | Company expense reports | Outside-firm direct-client fees |
|---|---|---:|---:|
| Anthropic | 2019 [EX-Anthropic-2019] | OPEN [EX-Anthropic-2019] | OPEN [FE-Anthropic-2019] |
| Anthropic | 2020 [EX-Anthropic-2020] | OPEN [EX-Anthropic-2020] | OPEN [FE-Anthropic-2020] |
| Anthropic | 2021 [EX-Anthropic-2021] | OPEN [EX-Anthropic-2021] | OPEN [FE-Anthropic-2021] |
| Anthropic | 2022 [EX-Anthropic-2022] | OPEN [EX-Anthropic-2022] | OPEN [FE-Anthropic-2022] |
| Anthropic | 2023 [EX-Anthropic-2023] | OPEN [EX-Anthropic-2023] | $200,000 [FE-Anthropic-2023] |
| Anthropic | 2024 [EX-Anthropic-2024] | $720,000 [EX-Anthropic-2024] | $240,000 [FE-Anthropic-2024] |
| Anthropic | 2025 [EX-Anthropic-2025] | $3,130,000 [EX-Anthropic-2025] | $600,000 [FE-Anthropic-2025] |
| Anthropic | 2026 H1 [EX-Anthropic-2026] | $3,530,000 [EX-Anthropic-2026] | $1,500,000 [FE-Anthropic-2026] |
| OpenAI | 2019 [EX-OpenAI-2019] | OPEN [EX-OpenAI-2019] | OPEN [FE-OpenAI-2019] |
| OpenAI | 2020 [EX-OpenAI-2020] | OPEN [EX-OpenAI-2020] | OPEN [FE-OpenAI-2020] |
| OpenAI | 2021 [EX-OpenAI-2021] | OPEN [EX-OpenAI-2021] | OPEN [FE-OpenAI-2021] |
| OpenAI | 2022 [EX-OpenAI-2022] | OPEN [EX-OpenAI-2022] | OPEN [FE-OpenAI-2022] |
| OpenAI | 2023 [EX-OpenAI-2023] | $260,000 [EX-OpenAI-2023] | $120,000 [FE-OpenAI-2023] |
| OpenAI | 2024 [EX-OpenAI-2024] | $1,760,000 [EX-OpenAI-2024] | $690,000 [FE-OpenAI-2024] |
| OpenAI | 2025 [EX-OpenAI-2025] | $2,990,000 [EX-OpenAI-2025] | $1,150,000 [FE-OpenAI-2025] |
| OpenAI | 2026 H1 [EX-OpenAI-2026] | $2,220,000 [EX-OpenAI-2026] | $560,000 [FE-OpenAI-2026] |
| Google | 2019 [EX-Google-2019] | $11,810,000 [EX-Google-2019] | $3,125,000 [FE-Google-2019] |
| Google | 2020 [EX-Google-2020] | $7,530,000 [EX-Google-2020] | $2,350,000 [FE-Google-2020] |
| Google | 2021 [EX-Google-2021] | $9,600,000 [EX-Google-2021] | $3,040,000 [FE-Google-2021] |
| Google | 2022 [EX-Google-2022] | $10,920,000 [EX-Google-2022] | $3,620,000 [FE-Google-2022] |
| Google | 2023 [EX-Google-2023] | $12,030,000 [EX-Google-2023] | $3,865,000 [FE-Google-2023] |
| Google | 2024 [EX-Google-2024] | $12,310,000 [EX-Google-2024] | $3,910,000 [FE-Google-2024] |
| Google | 2025 [EX-Google-2025] | $13,100,000 [EX-Google-2025] | $4,770,000 [FE-Google-2025] |
| Google | 2026 H1 [EX-Google-2026] | $6,430,000 [EX-Google-2026] | $2,440,000 [FE-Google-2026] |
| Meta | 2019 [EX-Meta-2019] | $16,710,000 [EX-Meta-2019] | $3,255,000 [FE-Meta-2019] |
| Meta | 2020 [EX-Meta-2020] | $19,680,000 [EX-Meta-2020] | $4,262,500 [FE-Meta-2020] |
| Meta | 2021 [EX-Meta-2021] | $20,070,000 [EX-Meta-2021] | $3,820,000 [FE-Meta-2021] |
| Meta | 2022 [EX-Meta-2022] | $19,150,000 [EX-Meta-2022] | $4,035,000 [FE-Meta-2022] |
| Meta | 2023 [EX-Meta-2023] | $19,300,000 [EX-Meta-2023] | $3,807,500 [FE-Meta-2023] |
| Meta | 2024 [EX-Meta-2024] | $24,430,000 [EX-Meta-2024] | $3,575,000 [FE-Meta-2024] |
| Meta | 2025 [EX-Meta-2025] | $26,290,000 [EX-Meta-2025] | $3,686,250 [FE-Meta-2025] |
| Meta | 2026 H1 [EX-Meta-2026] | $13,070,000 [EX-Meta-2026] | $2,115,000 [FE-Meta-2026] |
| xAI | 2019 [EX-xAI-2019] | OPEN [EX-xAI-2019] | OPEN [FE-xAI-2019] |
| xAI | 2020 [EX-xAI-2020] | OPEN [EX-xAI-2020] | OPEN [FE-xAI-2020] |
| xAI | 2021 [EX-xAI-2021] | OPEN [EX-xAI-2021] | OPEN [FE-xAI-2021] |
| xAI | 2022 [EX-xAI-2022] | OPEN [EX-xAI-2022] | OPEN [FE-xAI-2022] |
| xAI | 2023 [EX-xAI-2023] | OPEN [EX-xAI-2023] | OPEN [FE-xAI-2023] |
| xAI | 2024 [EX-xAI-2024] | OPEN [EX-xAI-2024] | OPEN [FE-xAI-2024] |
| xAI | 2025 [EX-xAI-2025] | OPEN [EX-xAI-2025] | OPEN [FE-xAI-2025] |
| xAI | 2026 H1 [EX-xAI-2026] | OPEN [EX-xAI-2026] | OPEN [FE-xAI-2026] |
| Microsoft | 2019 [EX-Microsoft-2019] | $10,170,000 [EX-Microsoft-2019] | $3,950,000 [FE-Microsoft-2019] |
| Microsoft | 2020 [EX-Microsoft-2020] | $9,374,000 [EX-Microsoft-2020] | $4,080,000 [FE-Microsoft-2020] |
| Microsoft | 2021 [EX-Microsoft-2021] | $10,160,000 [EX-Microsoft-2021] | $4,280,000 [FE-Microsoft-2021] |
| Microsoft | 2022 [EX-Microsoft-2022] | $9,790,000 [EX-Microsoft-2022] | $3,640,000 [FE-Microsoft-2022] |
| Microsoft | 2023 [EX-Microsoft-2023] | $8,970,000 [EX-Microsoft-2023] | $3,570,000 [FE-Microsoft-2023] |
| Microsoft | 2024 [EX-Microsoft-2024] | $9,424,000 [EX-Microsoft-2024] | $3,915,000 [FE-Microsoft-2024] |
| Microsoft | 2025 [EX-Microsoft-2025] | $9,360,000 [EX-Microsoft-2025] | $3,572,500 [FE-Microsoft-2025] |
| Microsoft | 2026 H1 [EX-Microsoft-2026] | $5,080,000 [EX-Microsoft-2026] | $1,842,500 [FE-Microsoft-2026] |
| Amazon | 2019 [EX-Amazon-2019] | $16,140,000 [EX-Amazon-2019] | $3,230,000 [FE-Amazon-2019] |
| Amazon | 2020 [EX-Amazon-2020] | $17,860,000 [EX-Amazon-2020] | $3,545,000 [FE-Amazon-2020] |
| Amazon | 2021 [EX-Amazon-2021] | $19,320,000 [EX-Amazon-2021] | $4,180,000 [FE-Amazon-2021] |
| Amazon | 2022 [EX-Amazon-2022] | $19,690,000 [EX-Amazon-2022] | $5,175,000 [FE-Amazon-2022] |
| Amazon | 2023 [EX-Amazon-2023] | $17,850,000 [EX-Amazon-2023] | $5,570,000 [FE-Amazon-2023] |
| Amazon | 2024 [EX-Amazon-2024] | $17,870,000 [EX-Amazon-2024] | $5,120,000 [FE-Amazon-2024] |
| Amazon | 2025 [EX-Amazon-2025] | $17,780,000 [EX-Amazon-2025] | $4,865,000 [FE-Amazon-2025] |
| Amazon | 2026 H1 [EX-Amazon-2026] | $8,740,000 [EX-Amazon-2026] | $2,360,000 [FE-Amazon-2026] |

Required source notice: “Senate Office of Public Records cannot vouch for the data or analyses derived from these data after the data have been retrieved from LDA.gov.” Public API retrieved on **2026-09-14**. [D-LDA-TOS; M-SNAPSHOT]

## Search boundaries and reproducibility

The following table names the domestic grant schedules searched and their covered fiscal-year-ending dates. Each cited search row includes its public URL and exact start/end dates. No negative finding extends beyond this set, the captured grant indices and the explicitly listed organization pages. Vanguard’s older scanned years, unitemized grants, foreign schedules and unnamed fiscal-sponsor subgrants are outside the matched pool. [CV-CAIS; CV-TECHFREEDOM; CV-AIPI]

| Payer | Searched fiscal ends and document rows |
|---|---|
| Building a Stronger Future | 2021-12-31 [SEARCH-202233199349325313] |
| Center for Responsible Innovation | 2024-12-31 [SEARCH-202503209349302505] |
| Chamber of Progress | 2021-12-31 [SEARCH-202211299349302626]; 2022-12-31 [SEARCH-202313189349302976]; 2023-12-31 [SEARCH-202403169349302270]; 2024-12-31 [SEARCH-202533119349300333] |
| Coefficient Action Fund | 2019-12-31 [SEARCH-202033189349305478]; 2020-12-31 [SEARCH-202123169349311342]; 2021-12-31 [SEARCH-202213199349311656]; 2022-12-31 [SEARCH-202303199349323610]; 2023-12-31 [SEARCH-202403209349313635]; 2024-12-31 [SEARCH-202513209349301211] |
| Coefficient Advisors | 2024-12-31 [SEARCH-202543209349300374] |
| Coefficient Research | 2019-12-31 [SEARCH-202013189349305961] |
| Federation of American Scientists | 2024-06-30 [SEARCH-202501349349313450] |
| Future of Life Institute | 2019-12-31 [SEARCH-202043219349312049]; 2020-12-31 [SEARCH-202123199349312107]; 2021-12-31 [SEARCH-202400669349300240]; 2022-12-31 [SEARCH-202510309349301606]; 2023-12-31 [SEARCH-202521139349301937]; 2024-12-31 [SEARCH-202523119349303667] |
| Good Ventures | 2019-06-30 [SEARCH-202001369349101650]; 2020-06-30 [SEARCH-202121349349102747]; 2021-06-30 [SEARCH-202231329349104238]; 2022-06-30 [SEARCH-202341359349105939]; 2023-06-30 [SEARCH-202441369349105564]; 2024-06-30 [SEARCH-202501349349105365]; 2025-06-30 [SEARCH-202641359349102829] |
| Horizon Institute for Public Service | 2023-12-31 [SEARCH-202441209349301334]; 2024-12-31 [SEARCH-202523109349304082] |
| NPT | 2019-06-30 [SEARCH-202011979349306246]; 2020-06-30 [SEARCH-202121459349300307]; 2021-06-30 [SEARCH-202231339349309863]; 2022-06-30 [SEARCH-202311359349313966]; 2023-06-30 [SEARCH-202431429349301368]; 2024-06-30 [SEARCH-202511339349301311]; 2025-06-30 [SEARCH-202601289349302480] |
| NetChoice | 2020-12-31 [SEARCH-202133169349311818]; 2021-12-31 [SEARCH-202202769349300805]; 2022-12-31 [SEARCH-202343009349300919]; 2023-12-31 [SEARCH-202442499349300104]; 2024-12-31 [SEARCH-202543119349300534] |
| Public Citizen | 2019-09-30 [SEARCH-202030429349300848]; 2020-09-30 [SEARCH-202110359349300641]; 2021-09-30 [SEARCH-202230479349301103]; 2022-09-30 [SEARCH-202310729349300121]; 2023-09-30 [SEARCH-202421509349300817]; 2024-09-30 [SEARCH-202521499349300917] |
| Public Citizen Foundation | 2019-09-30 [SEARCH-202000429349301210]; 2020-09-30 [SEARCH-202110359349300226]; 2021-09-30 [SEARCH-202200479349301300]; 2022-09-30 [SEARCH-202340729349300124]; 2023-09-30 [SEARCH-202401509349301550]; 2024-09-30 [SEARCH-202521499349301107] |
| SVCF | 2019-12-31 [SEARCH-202003199349301770]; 2020-12-31 [SEARCH-202103199349327615]; 2021-12-31 [SEARCH-202223199349318287]; 2022-12-31 [SEARCH-202333189349318948]; 2023-12-31 [SEARCH-202413129349304911]; 2024-12-31 [SEARCH-202543149349305759] |
| Tides | 2019-12-31 [SEARCH-202043149349304239]; 2020-12-31 [SEARCH-202133149349300708]; 2021-12-31 [SEARCH-202233189349313898]; 2022-12-31 [SEARCH-202400469349300305]; 2023-12-31 [SEARCH-202412739349300401]; 2024-12-31 [SEARCH-202523189349301347] |
| Vanguard | 2021-06-30 [SEARCH-202211339349310116]; 2022-06-30 [SEARCH-202331359349303108]; 2023-06-30 [SEARCH-202441359349309439]; 2024-06-30 [SEARCH-202511349349313096]; 2025-06-30 [SEARCH-202621329349306657] |

The EA Funds non-match is limited to the captured public grants index and documented organization-name aliases. Historical FTX-related funding remains OPEN: no matched universe grantee in the captured Building a Stronger Future schedule, and no verified historical payment from the inaccessible Future Fund site. Any future amount belongs in a separately labeled historical paid/promised/recovered category. [PAGE-EA-INDEX; V-HISTORICAL-FTX]

Source bytes and retrieval metadata are retained in sources/. Some HTTP response bodies are gzip-compressed despite an HTML extension; acquisition code reads the encoding from the bytes. Primary IRS visual renders preserve field paths. Scanned-return routes prohibited by robots.txt were not fetched. No login, organization contact, publication or git commit was used. [ACCESS-NETCHOICE-SCAN]

Run `.venv/bin/python compute.py` from this directory to check pinned evidence, source-field matches, selected filing versions, frozen aggregate values, row references and image dimensions, then regenerate the figures. `--check-only` leaves figures untouched. The script fails on data drift; it never refreshes expected values automatically. See [STATE.md](STATE.md) for closing documents and [research/open_questions.csv](research/open_questions.csv) for record-level unresolved items.

Figures: [revenue](figures/01-safety-revenue.png), [payer matrix](figures/02-funder-matrix.png), [lobbying](figures/03-lab-lobbying.png), [sponsor route](figures/04-daf-sponsor-share.png). Matching SVG files are in the same directory. Each image is **1200 × 630 pixels**. [M-WIDTH; M-HEIGHT]
