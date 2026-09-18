"""Write the editor handoff from the frozen row register, with explicit citations."""
from collections import defaultdict
from decimal import Decimal
from audit_core import read,P,R
from finalize_register import PAGES
from plot_figures import LABELS

def run():
    files={p.name:read(p.name) for p in R.glob('*.csv')};rows={r['row_id']:r for rr in files.values() for r in rr}
    entities=files['entities.csv'];a=files['aggregates.csv'];f=files['financials.csv']+files['financial_comparatives.csv']
    families=['CAIS','AIPI','ENCODE','FLI','CONTROL','SAIF','IAPS','HORIZON','ARI','PC','FAS','PROGRESS','ITIF','TECHFREEDOM','NETCHOICE']
    names={'CAIS':'Center for AI Safety','AIPI':'AI Policy Institute','ENCODE':'Encode Justice / Encode','FLI':'Future of Life Institute','CONTROL':'ControlAI','SAIF':'Safe AI Forum','IAPS':'Institute for AI Policy and Strategy','HORIZON':'Horizon Institute for Public Service','ARI':'Americans for Responsible Innovation','PC':'Public Citizen','FAS':'Federation of American Scientists','PROGRESS':'Chamber of Progress','ITIF':'ITIF','TECHFREEDOM':'TechFreedom','NETCHOICE':'NetChoice'}
    def cite(*ids):return '['+'; '.join(ids)+']'
    def money(rid):
        r=rows[rid];return ('OPEN' if r['amount']=='' else f"${Decimal(r['amount']):,.0f}")+' '+cite(rid)
    def pct(rid):return ('OPEN' if rows[rid]['amount']=='' else f"{Decimal(rows[rid]['amount']):.1f}%")+' '+cite(rid)
    lines=['# Funding around AI regulation: editor’s evidence notes','',
      '**Publication boundary:** this audit establishes institutional funding routes, filed financial amounts and attributed self-disclosures. It does not establish a total budget for AI-regulation messaging, donor intent, or the identity of advisers behind particular DAF-sponsor grants. The source population is deliberately bounded and uneven. [V-REMATCH-SCOPE; V-REMATCH-DONOR; V-CAIS-SHARES]','',
      'Snapshot: **2026-09-14**. Organization financial histories cover fiscal years ending **2019–2024**; the identified grant pool uses available fiscal years ending **2019–2025**; lobbying covers **2019–2026**, with the latest year limited to completed quarters through **June 30**. [M-SNAPSHOT; M-START; M-REV-END; M-GRANT-END; M-LDA-END; M-LDA-QUARTER]','',
      'Every bracketed code is a row ID in [research/](research/). Those rows carry the exact amount, public source URL, snapshot, source excerpt and caveat. Calculated rows in [aggregates.csv](research/aggregates.csv) list every input row. KEEP means the stated, bounded claim is confirmed by its primary source; an attributed self-disclosure confirms what the organization says. KILL means contradicted. OPEN means the necessary evidence is unavailable or insufficient.','',
      '## Findings a writer can use','',
      f'- **The rematch arithmetic survives with a narrower description.** Vanguard’s cash grants to the original figure’s selected recipient set were {money("RM-FIGURE-2024")} and {money("RM-FIGURE-2025")} in the fiscal years ending June 2024 and June 2025, respectively. This does not establish messaging expenditure or a source in employee liquidity proceeds. [V-REMATCH-ARITH; V-REMATCH-SCOPE; V-REMATCH-TENDER; V-REMATCH-DONOR]',
      '- **Named institutional grants and company support are both observable.** Good Ventures appears as a filed grant payer to CAIS; Chamber of Progress publicly names corporate partners; ITIF discloses supporters above a threshold. These are different disclosure types and should be described separately. [MX-CAIS-GV; D-PROGRESS; D-ITIF]',
      f'- **The organizations also fund one another.** NetChoice’s filed cash grants to TechFreedom total {money("MX-TECHFREEDOM-NETCHOICE")}; Horizon’s filed cash grants to FAS total {money("MX-FAS-HORIZON")}. These flows must not be added across recipients to estimate unique original funding.',
      '- **DAF-sponsor routes occur across the requested groups.** CAIS and TechFreedom both appear in sponsor schedules. The named payer is visible; the adviser and the specific fund type remain unresolved in these rows. [MX-CAIS-SV; MX-CAIS-NP; MX-CAIS-VG; MX-TECHFREEDOM-NP; V-CAIS-SHARES; V-TECHFREEDOM-SHARES]',
      '- **Project and legal-entity accounts require care.** The recommendation pages name receiving charities for AIPI, Encode and IAPS. A receiving charity’s total revenue is not a project budget, and a recommendation is not a paid grant. [S-SFF-2025-C6-6; S-SFF-2024-C9-29; S-SFF-2025-C6-81; V-SFF-CASH]',
      '- **Revenue is not a usable messaging-spend estimate.** FLI’s filed revenue series includes a large positive year followed by negative revenue, with investment results reported separately. ControlAI’s UK filings omit the income-and-expenditure account. [RV-FLI-2021; RV-FLI-2022; V-CONTROL-REVENUE]',
      '- **Lobbying is an all-issues series.** Company expense reports and outside firms’ fees overlap. Blank amounts, missing reports and explicitly named intermediary clients are handled separately; none becomes an invented exact payment. [EX-OpenAI-2024; FE-OpenAI-2024; SF-Anthropic-2024; D-LDA-TOS]','',
      '## Three sentences ready to quote','',
      f'> Vanguard Charitable reported {money("RM-FIGURE-2024")} and {money("RM-FIGURE-2025")} in cash grants to the original figure’s selected recipient set in its fiscal years ending June 2024 and June 2025, respectively; the grant rows do not identify the donor advisers. [V-REMATCH-DONOR]','',
      '> Chamber of Progress names corporate partners, while ITIF names supporters above a disclosure threshold; neither captured list supplies a complete donor-by-donor funding ledger. [D-PROGRESS; D-ITIF; V-PROGRESS-SHARES; V-ITIF-SHARES]','',
      f'> NetChoice’s filed cash grants to TechFreedom total {money("MX-TECHFREEDOM-NETCHOICE")} across its fiscal years ending 2022–2024, while National Philanthropic Trust’s fiscal year ending June 2025 schedule reports {money("MX-TECHFREEDOM-NP")}; the schedules do not identify how much supported AI-regulation messaging. [V-TECHFREEDOM-CASH]','',
      '## Rematch verdicts and population sensitivity','',
      'The original package names **Vanguard Charitable**. Substituting SVCF, NPT or Tides for that payer changes the claim. The incorrect sponsor identifiers in the brief were corrected to SVCF **20-5205488** and NPT **23-7825575**, using primary documents. The examined sponsors file **Form 990, Schedule I**; Good Ventures uses **Form 990-PF**. [D-REMATCH-CLAIM; V-REMATCH-SPONSOR; D-SVCF-EIN; D-NPT-EIN; V-SPONSOR-FORM]','',
      '| Author-selected population | Fiscal year ending June 2024 [RM-FIGURE-2024] | Fiscal year ending June 2025 [RM-FIGURE-2025] |',
      '|---|---:|---:|',
      f'| Original figure, excluding the author’s borderline tier | {money("RM-FIGURE-2024")} | {money("RM-FIGURE-2025")} |',
      f'| Same broad category including borderline recipients | {money("RM-BORDER-2024")} | {money("RM-BORDER-2025")} |',
      f'| Only recipients labeled AI safety by the author | {money("RM-AI-2024")} | {money("RM-AI-2025")} |','',
      'These are membership sensitivity calculations, not competing estimates of messaging expenditure. The author’s broad category also contains general EA infrastructure; even its AI-safety label does not establish how each grant was used. Recipient names, purpose text, author labels and exact EIN rematches are retained in [rematch.csv](research/rematch.csv). [V-REMATCH-SCOPE]','',
      '| Funding claim | Verdict | What the evidence establishes |','|---|---|---|']
    for v in files['verdicts.csv']:
        if not v['org_id']:
            lines.append(f"| {v['claim']} | **{v['verdict']}** {cite(v['row_id'])} | {v['note']} |")
    lines+=['','## How to read the funding shares','',
      '**Declared share of total funding: OPEN. Confirmed DAF share of total funding: OPEN. Unidentified share of total funding: OPEN.** This applies across the universe: there is no reconciled public donor-by-period receipts ledger in the examined records. “Unidentified” is therefore an unquantified gap, not a percentage residual. [V-CAIS-SHARES; V-AIPI-SHARES; V-ENCODE-SHARES; V-FLI-SHARES; V-CONTROL-SHARES; V-SAIF-SHARES; V-IAPS-SHARES; V-HORIZON-SHARES; V-ARI-SHARES; V-PC-SHARES; V-FAS-SHARES; V-PROGRESS-SHARES; V-ITIF-SHARES; V-TECHFREEDOM-SHARES; V-NETCHOICE-SHARES]','',
      'The observable ratio is **DAF-sponsor-routed cash / (DAF-sponsor-routed cash + direct-institution cash)** within the identified filed-grant pool. Both cash subtotals remain separately labeled. This denominator excludes awards, recommendations, matching pledges, commitments, lobbying and organization revenue. It also excludes unallocated project grants, foreign schedules, unnamed subgrants and funding outside the searched returns. The sponsors report maintaining donor-advised funds or similar accounts in their own returns. The legal sponsor alone does not establish that each individual grant was donor-advised. [DP-CAIS; DP-TECHFREEDOM; V-IAPS-ALLOCATION; SP-SVCF; SP-NPT; SP-Vanguard; SP-Tides]','',
      'A high ratio can reflect narrow source coverage. For example, the FLI ratio describes the small identified payer-side pool, while its own donor page names other donors without dollar amounts. It cannot be used as a share of FLI’s whole budget. A zero route subtotal describes an empty subset of an observed pool; an absent pool is OPEN. [DP-FLI; D-FLI; DP-ARI; DP-AIPI]','',
      '## Organization profiles','',
      'Group assignments follow the brief. Related legal entities are shown separately. CAIS Action Fund and AI Policy Network address the requested advocacy arms; Encode Research is identified by Encode’s own legal notice; Public Citizen Foundation is its related charitable entity; CRI is included because ARI links to it as the related research organization. No consolidated budget or particular legal-control relationship is inferred from a website link. No requested family was established to be defunct in the bounded identity review. [ID-CAISAF; D-AIPI-AIPN; D-ENCODE-ARMS; ID-PCF; D-ARI-CRI; ID-CONTROL]','']
    extra={
      'CAIS':'The charitable entity and Action Fund have distinct returns. Their amounts are not consolidated here. [ID-CAIS; ID-CAISAF]',
      'AIPI':'Standalone AIPI tax identity remains OPEN; its own site claims charitable status. The IRS registry identifies AI Policy Network separately. SFF’s later recommendation names The Hack Foundation as receiving charity; this does not establish an AIPI cash receipt or make Hack’s total revenue an AIPI budget. [ID-AIPI; ID-AIPN; D-AIPI-AIPN; S-SFF-2025-C6-6]',
      'ENCODE':'Encode’s legal notice names a corporation and research foundation. The foundation has a registry identity; the corporation’s EIN/determination remains OPEN. SFF names March On Foundation in the earlier recommendation and Encode AI Corporation in the later one. Encode also reports individual donations from rank-and-file frontier-lab employees; those are not corporate grants. [D-ENCODE-ARMS; ID-ENCODE; ID-ENCODER; S-SFF-2024-C9-29; S-SFF-2025-C6-32; D-ENCODE-EMPLOYEES]',
      'FLI':'Its donor page identifies Vitalik Buterin as its largest donor and names other supporters, without donor-by-period amounts. The annual revenue series must retain investment gains and losses. [D-FLI; RV-FLI-2021; RV-FLI-2022]',
      'CONTROL':'Companies House establishes a company limited by guarantee, currently named CONTROLAI and previously Secure Future Research Ltd. That does not establish charity tax exemption. Filed balance sheets are in uk_accounts.csv; the filings omit annual income-and-expenditure accounts. The site’s separate US social-welfare entity claim remains unverified. [ID-CONTROL; D-CONTROL-NAME; D-CONTROL-NO-PL; D-CONTROL-NO-PL-2025; D-CONTROL-US]',
      'SAIF':'The standalone legal entity has a primary financial return. SFF’s earlier recommendation separately names FAR AI as receiving charity; FAR AI’s whole budget is not assigned to this entity. The program-expense field is an explicit filed zero in Part IX. [ID-SAIF; S-SFF-2024-C9-62; R-SAIF-2024-PROGRAM-IX]',
      'IAPS':'The IRS registry identifies the present standalone charity, while the captured historical SFF recommendations name Rethink Priorities as receiving charity. Good Ventures’ expressly earmarked project payments to Rethink are a separate dataset. The mixed-purpose grant’s full amount cannot be assigned to IAPS. [ID-IAPS; S-SFF-2025-C6-81; V-IAPS-ALLOCATION]',
      'HORIZON':'Horizon’s current page names funders and says no donor supplies a majority. The page does not define a covered fiscal period; that statement is not applied to earlier returns. Horizon also appears as a payer to FAS. [D-HORIZON; MX-FAS-HORIZON]',
      'ARI':'ARI and CRI have separate legal identities and returns. A Coefficient archive award and the Action Fund’s paid-grant amount are distinct measures; their difference is not silently “corrected” or added together. The ARI website link supports including CRI, without establishing consolidated control. [ID-ARI; ID-CRI; D-ARI-CRI; MX-ARI-CA; V-CG-CASH]',
      'PC':'Public Citizen and its foundation are kept separate, including the foundation’s grants to Public Citizen. The official annual-report page states that it does not accept corporate or government money; that is an attributed policy, not an audited donor ledger. [ID-PC; ID-PCF; MX-PC-PCF; D-PC-POLICY]',
      'FAS':'FAS is a comparator with a broad program portfolio. Its annual report names philanthropic and agency supporters. The separately reported new commitments are '+money('C-FAS-2023')+'; this is not revenue or paid-grant cash. [D-FAS]',
      'PROGRESS':'The corporate-partner page names Amazon, Google, OpenAI and other companies. No per-company payment is supplied there. The filed organization total is not an AI-only budget. [D-PROGRESS; V-PROGRESS-SHARES]',
      'ITIF':'The supporter page’s disclosure threshold is greater than '+money('D-ITIF')+'. The page includes Alphabet, Amazon, Anthropic, Meta and Microsoft, but it does not define a precise ending date for its “past fiscal year” or give each payment amount. [D-ITIF]',
      'TECHFREEDOM':'The captured About page does not provide an adequate funder list. Payer-side schedules nevertheless identify NetChoice cash grants and a separate NPT-routed grant. The NPT grant’s generic filed purpose is retained verbatim, without using it to classify TechFreedom’s activities. [D-TECHFREEDOM; MX-TECHFREEDOM-NETCHOICE; MX-TECHFREEDOM-NP]',
      'NETCHOICE':'The captured current About page has an Association Members heading but no member names in that section. This is a bounded snapshot observation, not a claim about every public membership disclosure. Its own grant schedule establishes payments to TechFreedom. Earlier revenue, expenses and assets use explicitly filed comparatives where the scanned-return route was disallowed. [D-NETCHOICE; MX-TECHFREEDOM-NETCHOICE; R-NETCHOICE-2019-REV-COMP; ACCESS-NETCHOICE-SCAN]',
    }
    for family in families:
        es=[e for e in entities if e['family']==family];codes={e['org_id'] for e in es}
        lines+=['### '+names[family],'',extra[family],'']
        for e in es:
            ident=('EIN '+e['ein']) if e['ein'] else ('company '+e.get('company_number','') if e.get('company_number') else 'standalone identifier unresolved')
            lines.append(f"- **{e['org_name']}**: {e['tax_status']}; {ident}. {cite(e['row_id'])}")
        lines+=['','**Latest financials in the requested window**','', '| Legal entity | Fiscal end | Revenue | Assets at year end | Program-service expenses |','|---|---|---:|---:|---:|']
        for e in es:
            org=e['org_id'];rr=[r for r in f if r['org_id']==org and r['selected']=='yes'];revs=[r for r in rr if r['metric']=='REV']
            if not revs:
                if org=='CONTROL':
                    rid='UKA-CONTROL-2024';asset=f"£{Decimal(rows[rid]['amount']):,.0f} "+cite(rid)
                    lines.append(f"| {e['org_name']} | {rows[rid]['period_end']} {cite(rid)} | OPEN {cite('H-CONTROL-2024')} | {asset} | OPEN {cite('D-CONTROL-NO-PL')} |");continue
                lines.append(f"| {e['org_name']} | OPEN | OPEN {cite('H-'+org+'-2024')} | OPEN {cite('ID-'+org)} | OPEN {cite('ID-'+org)} |");continue
            last=max(revs,key=lambda r:r['period_end']);vals=[]
            for metric in ['REV','ASSETS','PROGRAM']:
                item=next((r for r in rr if r['period_end']==last['period_end'] and r['metric']==metric),None)
                vals.append(money(item['row_id']) if item else 'OPEN '+cite(f"O-METRIC-{org}-{last['period_end'][:4]}-{metric}"))
            lines.append('| '+e['org_name']+' | '+last['period_end']+' '+cite(last['row_id'])+' | '+' | '.join(vals)+' |')
        disclosures=[d for fn in ['disclosures.csv','supplement_disclosures.csv'] for d in files[fn] if d.get('org_id') in codes and d.get('declared_funders')]
        lines+=['','**Declared sources (amount shares OPEN).**']
        if disclosures:
            for d in disclosures:lines.append(d['declared_funders'].replace(';',', ')+'. '+cite(d['row_id']))
        else:lines.append('No adequate amount-bearing supporter ledger in the specifically captured pages; the per-entity page search is listed in STATE.md. '+cite(*['V-'+e['org_id']+'-DECLARED' for e in es]))
        mx=[r for r in a if r['row_id'].startswith('MX-') and r['org_id'] in codes]
        lines+=['','**Filed cash grants, by named payer.** Available source periods only; these totals are not annual revenue.']
        if mx:
            lines+=['','| Recipient | Filed payer | Cash |','|---|---|---:|']
            for r in mx:lines.append('| '+LABELS[r['org_id']]+' | '+r['funder']+' | '+money(r['row_id'])+' |')
        else:lines.append('No matched legal-grantee cash amount in the searched schedules. '+cite(*['CV-'+e['org_id'] for e in es]))
        other=[r for r in a if r.get('org_id') in codes and r['row_id'].startswith(('AW-','RC-','PJ-'))]
        if other:
            lines+=['','**Separate money types — do not add to the cash table.**','', '| Entity/project | Source period | Type | Amount |','|---|---|---|---:|']
            for r in other:lines.append('| '+LABELS[r['org_id']]+' | '+r['period']+' '+cite(r['row_id'])+' | '+r['money_type'].replace('_',' ')+' | '+money(r['row_id'])+' |')
        lines+=['','**Observed sponsor route and unknown shares.**','', '| Entity | Sponsor-routed cash | Direct-institution cash | Sponsor-route share of identified cash |','|---|---:|---:|---:|']
        for e in es:
            org=e['org_id'];lines.append('| '+e['org_name']+' | '+money('DN-'+org)+' | '+money('DD-'+org)+' | '+pct('DP-'+org)+' |')
        lines.append('Declared-donor, confirmed-DAF and unidentified shares of total funding all remain OPEN. '+cite(*['V-'+e['org_id']+'-SHARES' for e in es]));lines.append('')
    lines+=['## Complete organization × claim verdict table','',
      'Cash = a matched legal-grantee cash payment in the searched filings. Declared = an attributed funding-source disclosure, sometimes categories rather than names. Route = a matched DAF-sponsor payment. Shares = complete shares of total funding. Related entities are listed within their requested family.','',
      '| Organization / legal entity | Identity and tax status | Filed cash | Declared sources | DAF-sponsor route | Complete funding shares |',
      '|---|---|---|---|---|---|']
    for family in families:
        for e in [e for e in entities if e['family']==family]:
            cells=[]
            for suffix in ['STATUS','CASH','DECLARED','ROUTE','SHARES']:
                rid='V-'+e['org_id']+'-'+suffix;cells.append(rows[rid]['verdict']+' '+cite(rid))
            lines.append('| '+e['org_name']+' | '+' | '.join(cells)+' |')
    lines+=['','## Lab lobbying figures a writer can quote','',
      '**These are numeric reported amounts, not exact economic costs or AI-specific allocations.** Amendments replace earlier reports for the same registrant/client/year/quarter. Company expenses and outside fees overlap and must not be added. Explicitly named intermediary clients are a separate fee series in the CSVs. An inconsistent expense-field report from a different registrant is excluded and recorded as OPEN. The named company scope includes the documented corporate names and subsidiaries, with separately branded or unrelated matches excluded. [EX-Microsoft-2024; FE-Microsoft-2024; SF-Microsoft-2019; D-XCORP-SCOPE]','',
      'The latest year is a completed-quarter subtotal, not an annualized estimate. OpenAI’s earliest numeric reports in this series cover only the final quarter of that year. An OPEN cell means no eligible numeric report in the bounded client-name queries; it never means no spending. The xAI queries did not yield a numeric report; X Corp.’s report is not allocated to xAI. [M-LDA-QUARTER; EX-OpenAI-2023; FE-OpenAI-2023; EX-xAI-2026; D-XCORP-SCOPE]','',
      '| Company | Filing year | Company expense reports | Outside-firm direct-client fees |','|---|---|---:|---:|']
    for lab in ['Anthropic','OpenAI','Google','Meta','xAI','Microsoft','Amazon']:
        for year in range(2019,2027):lines.append(f'| {lab} | '+str(year)+(' H1' if year==2026 else '')+' '+cite(f'EX-{lab}-{year}')+' | '+money(f'EX-{lab}-{year}')+' | '+money(f'FE-{lab}-{year}')+' |')
    lines+=['','Required source notice: “Senate Office of Public Records cannot vouch for the data or analyses derived from these data after the data have been retrieved from LDA.gov.” Public API retrieved on **2026-09-14**. [D-LDA-TOS; M-SNAPSHOT]','',
      '## Search boundaries and reproducibility','',
      'The following table names the domestic grant schedules searched and their covered fiscal-year-ending dates. Each cited search row includes its public URL and exact start/end dates. No negative finding extends beyond this set, the captured grant indices and the explicitly listed organization pages. Vanguard’s older scanned years, unitemized grants, foreign schedules and unnamed fiscal-sponsor subgrants are outside the matched pool. [CV-CAIS; CV-TECHFREEDOM; CV-AIPI]','',
      '| Payer | Searched fiscal ends and document rows |','|---|---|']
    bypayer=defaultdict(list)
    for s in files['grant_searches.csv']:bypayer[s['funder']].append(s)
    for payer,ss in sorted(bypayer.items()):lines.append('| '+payer+' | '+'; '.join(s['period_end']+' '+cite(s['row_id']) for s in sorted(ss,key=lambda s:s['period_end']))+' |')
    lines+=['',
      'The EA Funds non-match is limited to the captured public grants index and documented organization-name aliases. Historical FTX-related funding remains OPEN: no matched universe grantee in the captured Building a Stronger Future schedule, and no verified historical payment from the inaccessible Future Fund site. Any future amount belongs in a separately labeled historical paid/promised/recovered category. [PAGE-EA-INDEX; V-HISTORICAL-FTX]','',
      'Source bytes and retrieval metadata are retained in sources/. Some HTTP response bodies are gzip-compressed despite an HTML extension; acquisition code reads the encoding from the bytes. Primary IRS visual renders preserve field paths. Scanned-return routes prohibited by robots.txt were not fetched. No login, organization contact, publication or git commit was used. [ACCESS-NETCHOICE-SCAN]','',
      'Run `.venv/bin/python compute.py` from this directory to check pinned evidence, source-field matches, selected filing versions, frozen aggregate values, row references and image dimensions, then regenerate the figures. `--check-only` leaves figures untouched. The script fails on data drift; it never refreshes expected values automatically. See [STATE.md](STATE.md) for closing documents and [research/open_questions.csv](research/open_questions.csv) for record-level unresolved items.','',
      'Figures: [revenue](figures/01-safety-revenue.png), [payer matrix](figures/02-funder-matrix.png), [lobbying](figures/03-lab-lobbying.png), [sponsor route](figures/04-daf-sponsor-share.png). Matching SVG files are in the same directory. Each image is **1200 × 630 pixels**. [M-WIDTH; M-HEIGHT]','']
    (P/'NOTES.md').write_text('\n'.join(lines))
    # STATE groups repeated questions for humans; the CSV preserves each record.
    state=['# Open questions and the documents needed to close them','',
      'Snapshot: **2026-09-14**. OPEN is an evidence verdict, not a zero or a donor allegation. Every record-level OPEN and its closing-document prescription is in [open_questions.csv](research/open_questions.csv). [M-SNAPSHOT]','',
      '## Cross-cutting questions','',
      '| Question | Current bound | Public document that would close it |','|---|---|---|']
    for v in files['verdicts.csv']:
        if v['verdict']=='OPEN' and not v['org_id']:state.append('| '+v['claim']+' '+cite(v['row_id'])+' | '+v['note']+' | '+v['closing_document']+' |')
    state+=['',
      '**All organizations: complete funding shares remain OPEN.** A public donor-by-period receipts ledger, grant-level fund-type labels and a reconciliation to recipient accounting would be needed. Payer-side cash disbursements and recipient accrual revenue cannot substitute for that reconciliation. These are closing-document descriptions, not requests to contact anyone. [V-CAIS-SHARES; V-NETCHOICE-SHARES]','',
      '**Legal-arm questions.** AIPI’s standalone EIN/determination, Encode AI Corporation’s EIN/determination, ControlAI’s US entity identifier, and ControlAI’s UK charitable tax status require public registry or determination documents. ARI’s link to CRI alone does not establish a legal-control or consolidation relationship; a related-organization schedule or public governing document would close that narrower question. [ID-AIPI; ID-ENCODE; D-CONTROL-US; ID-CONTROL; D-ARI-CRI]','',
      '## Missing standalone financial histories','',
      'These missing fiscal-year-ending periods are bounded to the captured registry/filing listings and UK accounts. The closing document for each is a standalone primary annual return or annual accounts naming the entity and disclosing revenue, assets and program expenses. A fiscal sponsor’s whole return does not close a project-level gap.','',
      '| Entity | Missing revenue periods |','|---|---|']
    for e in entities:
        hs=[h for h in files['history_coverage.csv'] if h['org_id']==e['org_id'] and h['verdict']=='OPEN']
        if hs:state.append('| '+e['org_name']+' | '+'; '.join(h['period']+' '+cite(h['row_id']) for h in hs)+' |')
    state+=['','## Missing fields within available histories','', '| Entity | Period / field | Closing document |','|---|---|---|']
    for o in files['open_questions.csv']:
        if o['row_id'].startswith('O-METRIC-'):state.append('| '+LABELS[o['org_id']]+' | '+o['period']+' / '+o['metric']+' '+cite(o['row_id'])+' | '+o['closing_document']+' |')
    state+=['',
      'The latest public filing version for a fiscal period is selected by submission date, with object ID as a deterministic tie-breaker. Earlier versions remain marked superseded in financials.csv and filing_documents.csv. ITIF has differing same-period values in the captured versions; the selected return is used without adding the versions. The full amended filing, accompanying explanation or audited reconciliation would establish why they differ. [RV-ITIF-2022]','',
      '## Bounded organization-page searches','',
      'Each page below was captured at the snapshot date. An attributed source list confirms the organization’s statement, not each transfer. Where an adequate list was unavailable, a dated official supporter list or annual report naming sources would close that question; amounts would still need a public donor-by-period ledger. [M-SNAPSHOT]','',
      '| Entity | Exact captured documents |','|---|---|']
    for e in entities:
        ps=[p for p in files['page_searches.csv'] if p.get('org_id')==e['org_id']]
        state.append('| '+e['org_name']+' | '+'; '.join('['+p['document_name']+']('+p['source_url']+') '+cite(p['row_id']) for p in ps)+' |')
    state+=['','## Source coverage still outside the matched pool','',
      '- **Historical and future funder periods:** the exact searched fiscal ends are listed in NOTES.md and grant_searches.csv. Missing periods need their public payer-side return and grant schedules. The pool does not claim to cover every year for every payer. [CV-CAIS]',
      '- **Foreign grants and project subgrants:** the domestic schedules can miss payments to UK recipients or to legal fiscal sponsors with unnamed projects. A foreign-grant schedule naming the recipient, or an explicit public project designation, would close the relevant match. A broad sponsor name alone is insufficient. [CV-CONTROL; CV-IAPS; CV-AIPI]',
      '- **DAF fund type and adviser identity:** a sponsor’s exact grant-level designation or public adviser disclosure is required. The route percentages do not answer either question. [DP-CAIS; DP-TECHFREEDOM; V-REMATCH-DONOR]',
      '- **Past FTX-related money:** a historical primary grant ledger, payer-side return or bankruptcy document must establish recipient, amount and paid/promised/recovered status. No current-funding amount is assigned from an old promise. [V-HISTORICAL-FTX]',
      '- **EA Funds:** exact-name matching of the captured public index did not identify a target organization entry. A primary entry naming the legal grantee or an expressly designated project would close the gap. [PAGE-EA-INDEX]',
      '- **NetChoice’s scanned earlier return:** robots.txt disallowed that route. Explicit comparatives supply some financial fields; the earlier program-expense field remains unresolved. A public annual report or other permitted primary copy would close it. [ACCESS-NETCHOICE-SCAN; R-NETCHOICE-2019-REV-COMP; O-METRIC-NETCHOICE-2019-PROGRAM]','',
      '## Lobbying questions','',
      'The exact public client-name queries and pagination counts are in lobbying_queries.csv, covering the requested filing years at the snapshot. All pages were checked against each query’s reported count. Client and registrant identities, issue codes, report types, dates and amendment choices are preserved in lobbying.csv. [FE-Google-2024; EX-Google-2024; M-START; M-LDA-END; M-SNAPSHOT]','',
      'Each blank-dollar or inconsistent expense-field report has a record-specific OPEN entry with its original filing URL. That original report or a public amendment is needed to resolve the number. A disclosure of a threshold range would leave exact dollars OPEN. Numeric subtotals are publishable only with the stated limitation; they are not asserted to be complete actual costs. [FE-Microsoft-2024; EX-Microsoft-2024]','',
      'Missing lab/year/type cells remain OPEN. In particular, xAI-name queries do not justify allocating X Corp.’s separate filing to xAI. A public quarterly filing naming xAI, or a corporate disclosure establishing attributable costs for the lab, would close that question. Future completed quarters and any subsequent amendments require a new snapshot and a reviewed recalculation. [EX-xAI-2026; FE-xAI-2026; D-XCORP-SCOPE; M-LDA-QUARTER]','',
      'The issue descriptions do not assign a dollar amount to AI. Public itemized costs or activity-level fee allocations would be required for an AI-only lobbying series. Corporate-family alias scope, direct-fee classification and intermediary exclusions are documented in lobbying_aliases.csv and lobbying.csv. [EX-OpenAI-2024; FE-OpenAI-2024; SF-Anthropic-2024]','']
    (P/'STATE.md').write_text('\n'.join(state));print('Editor notes and open-document handoff written.')
if __name__=='__main__':run()
