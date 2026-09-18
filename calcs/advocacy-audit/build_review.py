"""Curated claim/coverage register; generated review prose is separate from calculations."""
import csv,json
from collections import defaultdict
from audit_core import read,P,R
from parse_filings import write,DATE

def run():
    entities=read('entities.csv');grants=[r for r in read('grants.csv') if r['selected']=='yes'];searches=read('grant_searches.csv')
    disclosures=read('disclosures.csv')+read('supplement_disclosures.csv')
    evidence={r['row_id']:r for p in R.glob('*.csv') if p.name not in ['coverage.csv','verdicts.csv','open_questions.csv'] for r in read(p.name)}
    coverage=[];verdicts=[];opens=[]
    def row(rid,claim,verdict,inputs,note,org='',closing=''):
        rr=[evidence[i] for i in inputs]
        return dict(row_id=rid,amount='',source_url=rr[0]['source_url'],snapshot_date=DATE,
            verbatim_quote_from_source=rr[0]['verbatim_quote_from_source'],note=note,claim=claim,verdict=verdict,org_id=org,input_row_ids=';'.join(inputs),closing_document=closing)
    for e in entities:
        org=e['org_id'];found=[g for g in grants if g['org_id']==org]
        cv=row('CV-'+org,'Matched legal-grantee cash funding in the searched domestic grant schedules','KEEP' if found else 'OPEN',
            [s['row_id'] for s in searches],
            'Scope is exactly the funder returns and fiscal periods enumerated in searched_documents. Matching uses EIN and documented normalized names. No foreign-grantee schedule, smaller unitemized grant, unnamed subgrant, sponsor-wide project revenue or donor identity is inferred. A non-match is bounded to this document set.',org,
            '' if found else 'A primary payer-side schedule or public grant ledger naming this legal grantee or an expressly earmarked project, with an amount and period.')
        cv['searched_documents']=json.dumps([dict(row_id=s['row_id'],source_url=s['source_url'],funder=s['funder'],period_start=s['period_start'],period_end=s['period_end']) for s in searches]);cv['matched_row_ids']=';'.join(g['row_id'] for g in found)
        coverage.append(cv);evidence[cv['row_id']]=cv
        ds=[d for d in disclosures if d.get('org_id')==org and d.get('declared_funders')]
        routed=[g for g in found if g['route']=='DAF_sponsor_unspecified_fund']
        specs=[
          ('STATUS','The legal identity and stated tax status are verified','OPEN' if org=='CONTROL' else e['verdict'],[e['row_id']],e['note'],'IRS determination/registry entry identifying the unresolved standalone legal entity; UK charity registry or tax document where charitable status is claimed.'),
          ('CASH','A named institution filed a cash grant to this legal entity','KEEP' if found else 'OPEN',[g['row_id'] for g in found] or ['CV-'+org], 'KEEP confirms only the filed payer/grantee/amount/period; it does not allocate the grant to AI messaging. OPEN is a bounded non-match in the enumerated schedules.','Primary payer-side cash-grant schedule naming this legal grantee, amount and period.'),
          ('DECLARED','The organization publicly names funding sources','KEEP' if ds else 'OPEN',[d['row_id'] for d in ds] or [e['row_id']], 'KEEP confirms an attributed self-disclosure. It does not independently verify each payment or quantify donor shares. OPEN means no adequate funder list in the captured pages listed in STATE.md.','Dated official supporter list or annual report naming funding sources.'),
          ('ROUTE','A DAF sponsor filed a cash grant to this legal entity','KEEP' if routed else 'OPEN',[g['row_id'] for g in routed] or ['CV-'+org], 'KEEP establishes the institutional route only. The underlying fund type and adviser remain unresolved. OPEN is not a zero.','Primary DAF-sponsor grant schedule naming the grantee, amount and period.'),
          ('SHARES','Declared-donor, confirmed-DAF and unidentified shares of total funding can be computed','OPEN',[e['row_id'],'DP-'+org], 'Donor-by-period receipts and a reconciled denominator are not public in the examined records. No residual is calculated from grants divided by organization revenue. Sponsor-route ratio is a different, coverage-limited measure.','A reconciled public donor-by-period receipts ledger, grant-level fund-type designations and recipient accounting reconciliation; public releases only.'),
        ]
        for suffix,claim,v,ins,note,close in specs:
            verdicts.append(row(f'V-{org}-{suffix}',claim,v,ins,note,org,close if v=='OPEN' else ''))
    cases=[
      ('REMATCH-ARITH','The original figure’s rounded growth is supported for its selected recipient set','KEEP',['RM-FIGURE-2024','RM-FIGURE-2025'],'Exact Vanguard amounts rematch the primary schedules. The figure excludes the author’s borderline tier. This is a recipient-population arithmetic finding, not a spending-purpose finding.',''),
      ('REMATCH-SPONSOR','The cited growth calculation comes from SVCF, NPT or Tides schedules','KILL',['RM-FIGURE-2024','RM-FIGURE-2025','D-REMATCH-CLAIM'],'The original claim and exact rematched amounts concern Vanguard Charitable. The named alternative sponsors are separate datasets.',''),
      ('REMATCH-SCOPE','Every dollar in the selected cluster is established as AI-regulation messaging spending','OPEN',['RM-FIGURE-2025','RM-AI-2025'],'The author’s recipient labels include AI safety and broader EA infrastructure; grant rows do not allocate all recipient spending to policy messaging.','Grant restrictions and recipient project-expense disclosures that identify the share used for regulation messaging.'),
      ('REMATCH-TENDER','The increase occurred in the year of Anthropic’s first tender offer','OPEN',['D-REMATCH-CLAIM','RM-FIGURE-2024','RM-FIGURE-2025'],'Primary Vanguard fiscal-period dates are established. No primary tender-offer document confirming both the first-offer status and transaction dates was verified; the temporal and causal link is not established.','Public tender-offer announcement, transaction document or company filing establishing first-offer status, opening/settlement dates and relevant proceeds timing.'),
      ('REMATCH-DONOR','The rematched filings identify the donor advisers or a tender-proceeds source','OPEN',['RM-FIGURE-2025'],'The searched Schedule I rows identify the institutional payer and recipient, not the donor adviser. This does not establish that no other public document identifies an adviser.','Public sponsor or donor disclosure tying these exact grants to an adviser and, separately, to transaction proceeds.'),
      ('SVCF-ID','The supplied SVCF EIN identifies the requested sponsor','KILL',['D-SVCF-EIN'],'The primary institutional disclosure supplies a different EIN; corrected before grant matching.',''),
      ('NPT-ID','The supplied NPT EIN identifies the requested sponsor','KILL',['D-NPT-EIN'],'The primary return supplies a different EIN; corrected before grant matching.',''),
      ('SPONSOR-FORM','The examined DAF sponsors use private-foundation grant schedules','KILL',[s['row_id'] for s in searches if s['funder'] in ['SVCF','NPT','Vanguard','Tides']],'The examined sponsor documents are public-charity Form 990 returns and Schedule I. Good Ventures uses Form 990-PF.',''),
      ('SFF-CASH','SFF recommendation amounts establish completed cash grants','KILL',['D-SFF-CAVEAT'],'The source explicitly warns that some recommended grants might not happen. Recommendations and matching pledges remain separate.',''),
      ('CG-CASH','The Coefficient grants archive is a single legal payer’s cash ledger','OPEN',['D-CG-ROUTES'],'The governance page identifies multiple awarding entities and routes. Archive dates and award amounts do not establish cash payment dates or payer identity.','Award-specific paying-entity disclosure and cash disbursement schedule reconciled to that award.'),
      ('IAPS-ALLOCATION','The full mixed-purpose Rethink Priorities grant can be allocated to IAPS','OPEN',[r['row_id'] for r in read('project_grants.csv') if r['allocation']=='mixed-purpose'],'The filed purpose includes general support and IAPS; no split is supplied. Only explicitly earmarked rows are separately totaled as project grants.','Public grant agreement or payer schedule splitting the mixed grant between general support and IAPS.'),
      ('CONTROL-REVENUE','ControlAI’s published UK balance sheet establishes annual revenue','KILL',['D-CONTROL-NO-PL','D-CONTROL-NO-PL-2025'],'The filed accounts expressly omit the income-and-expenditure account. Balance-sheet amounts cannot be substituted for revenue.',''),
      ('HISTORICAL-FTX','Historical FTX-related funding amounts to the requested entities are established here','OPEN',[s['row_id'] for s in searches if s['funder']=='Building a Stronger Future'],'The captured Building a Stronger Future return’s domestic schedule has no matched universe grantee. The historical FTX Future Fund site was inaccessible during retrieval. No historical payment, promise, recovery or present funding is imputed.','Public historical funder grant ledger, payer-side return or bankruptcy filing naming the recipient, amount, paid/promised status, and any recovery.'),
    ]
    for suffix,claim,v,ins,note,close in cases:verdicts.append(row('V-'+suffix,claim,v,ins,note,closing=close))
    # Every machine-readable OPEN receives a closing-document prescription.
    for v in verdicts:
        if v['verdict']=='OPEN':opens.append(dict(v,row_id='O-'+v['row_id']))
    for h in read('history_coverage.csv'):
        if h['verdict']=='OPEN':opens.append(dict(h,row_id='O-'+h['row_id'],claim='Standalone revenue unavailable for this legal entity and fiscal-year-ending year'))
    for r in read('lobbying.csv'):
        if r['selected'] in ['yes','excluded_inconsistent_expense_filer'] and r['verdict']=='OPEN':
            opens.append(row('O-'+r['row_id'],'Exact lobbying dollars are unresolved for this report','OPEN',[r['row_id']],r['note'],r['org_id'],'The linked original quarterly report or public amendment establishing an exact dollar amount and correct income/expense classification. A threshold disclosure alone cannot close exact dollars.'))
    for r in read('aggregates.csv'):
        if r['verdict']=='OPEN' and r['row_id'].startswith(('FE-','EX-','SF-')):
            opens.append(row('O-'+r['row_id'],'No numeric eligible lobbying amount in this series/year','OPEN',[r['row_id']],r['note'],r['org_id'],'An eligible public quarterly filing under the covered client identity, or a public corporate filing that establishes an additional attributable legal name; no parent/sibling attribution inferred.'))
    write('coverage.csv',coverage);write('verdicts.csv',verdicts);write('open_questions.csv',opens)
    print('Complete entity claim table and closing-document register written.')
if __name__=='__main__':run()
