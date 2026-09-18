"""Deterministic calculations. No network, no editorial inference, Decimal dollars."""
import csv,json,pathlib
from collections import defaultdict
from decimal import Decimal
P=pathlib.Path(__file__).resolve().parent;R=P/'research'
def read(name):
    with (R/name).open(newline='') as f:return list(csv.DictReader(f))
def fmt(value):
    return format(value,'f') if isinstance(value,Decimal) else str(value)
def calculate():
    allrows={}
    for p in sorted(R.glob('*.csv')):
        if p.name in ['aggregates.csv','verdicts.csv','open_questions.csv','figure_index.csv']:continue
        for r in read(p.name):
            assert r['row_id'] not in allrows,('Duplicate row ID',r['row_id'])
            allrows[r['row_id']]=r
    out=[]
    def add(rid,inputs,amount,operation,note,**kw):
        ins=[allrows[i] for i in inputs]
        out.append(dict(row_id=rid,amount=fmt(amount) if amount!='' else '',
            source_url=ins[0]['source_url'] if ins else 'user-provided://advocacy-audit-brief',
            snapshot_date='2026-09-14',
            verbatim_quote_from_source=json.dumps({r['row_id']:r['verbatim_quote_from_source'] for r in ins},ensure_ascii=False),
            note=note,input_row_ids=';'.join(inputs),operation=operation,verdict='OPEN' if amount=='' else 'KEEP',**kw))
        allrows[rid]=out[-1]
    def total(rows):return sum((Decimal(r['amount']) for r in rows),Decimal(0))
    def ids(rows):return sorted(r['row_id'] for r in rows)
    financial=read('financials.csv')+read('financial_comparatives.csv')
    for r in financial:
        if r['selected']=='yes' and r['metric']=='REV':
            add(f"RV-{r['org_id']}-{r['period_end'][:4]}",[r['row_id']],Decimal(r['amount']),'identity','Organization-wide filed total revenue; fiscal year ends in the plotted year. Not spending or a measure of AI-policy activity.',org_id=r['org_id'],period=r['period_end'][:4],period_end=r['period_end'],currency='USD',money_type='organization_revenue')
    for year in ['2024','2025']:
        rr=[r for r in read('uk_accounts.csv') if r['filing_year']==year and r['period_end']==year+'-12-31' and r['field_name'] in ['core:FixedAssets','core:CurrentAssets','core:PrepaymentsAccruedIncomeNotExpressedWithinCurrentAssetSubtotal']]
        assert len(rr)==3,('Incomplete UK asset components',year)
        add('UKA-CONTROL-'+year,ids(rr),total(rr),'sum','Total assets calculated from fixed assets, current assets and the explicitly excluded prepayments subtotal. GBP retained; no revenue or funding amount inferred.',org_id='CONTROL',period=year,period_end=year+'-12-31',currency='GBP',money_type='UK_balance_sheet_assets')
    grants=[r for r in read('grants.csv') if r['selected']=='yes' and '2019'<=r['period_end'][:4]<='2025']
    matrix=defaultdict(list)
    for r in grants:
        assert r['money_type']=='filed_cash_grant' and r['currency']=='USD' and r['amount']!='',r['row_id']
        matrix[(r['org_id'],r['funder'])].append(r)
    fcodes={'SVCF':'SV','NPT':'NP','Vanguard':'VG','Tides':'TI','Good Ventures':'GV','Coefficient Action Fund':'CA','Future of Life Institute':'FL'}
    fcodes.update({e['org_name']:e['org_id'] for e in read('entities.csv') if e['org_name'] not in fcodes})
    for (org,funder),rr in sorted(matrix.items()):
        add(f'MX-{org}-{fcodes[funder]}',ids(rr),total(rr),'sum','Same legal payer’s selected filed cash grants across available fiscal periods. Source-specific coverage is uneven; no recommendation, award, organization revenue, foreign schedule or unnamed subgrant is added.',org_id=org,funder=funder,funder_code=fcodes[funder],currency='USD',money_type='filed_cash_grant',route=rr[0]['route'],period_start=min(r['period_start'] for r in rr),period_end=max(r['period_end'] for r in rr))
    for entity in read('entities.csv'):
        org=entity['org_id'];pool=[r for r in grants if r['org_id']==org]
        sponsor=[r for r in pool if r['route']=='DAF_sponsor_unspecified_fund'];direct=[r for r in pool if r['route']=='direct_named_institution']
        for suffix,rr,typ in [('N',sponsor,'DAF_sponsor_routed_cash_grants'),('D',direct,'direct_institution_cash_grants')]:
            add(f'D{suffix}-{org}',ids(rr) or ids(pool) or [entity['row_id']],total(rr) if pool else '', 'sum' if rr else ('empty_subset' if pool else 'unavailable'),
                'Separate route subtotal within the identified filed cash-grant pool only. A zero is an empty route subset of an otherwise nonempty observed pool, not proof of no funding. DAF-sponsor status does not identify an adviser or establish each grant’s fund type.',org_id=org,money_type=typ,currency='USD')
        pct=total(sponsor)/total(pool)*100 if pool and total(pool)>0 else ''
        add(f'DP-{org}',[f'DN-{org}',f'DD-{org}'],pct,'route_percentage' if pct!='' else 'unavailable',
            'DAF-sponsor-routed cash divided by the sum of separately retained sponsor-routed and direct-institution cash subtotals. Coverage-limited ratio, not a share of organization revenue, all donations, declared donors, or confirmed donor-advised grants. Unknown when no identified pool exists.',org_id=org,money_type='DAF_sponsor_route_percentage',unit='percent')
    for filename,prefix in [('awards.csv','AW'),('recommendations.csv','RC'),('ea_funds.csv','EA'),('project_grants.csv','PJ')]:
        groups=defaultdict(list)
        for r in read(filename):
            if r.get('selected','yes')!='yes':continue
            year=r.get('period',r.get('period_end',''))[:4]
            groups[(r['org_id'],year,r['money_type'])].append(r)
        for (org,year,kind),rr in sorted(groups.items()):
            add(f'{prefix}-{org}-{year}-{kind}',ids(rr),total(rr),'sum','Same labeled money type only. Source rows retain receiving charities, payer uncertainty and allocation limits; amounts must not be added across types.',org_id=org,period=year,money_type=kind,currency='USD')
    rematch=read('rematch.csv')
    assert all(r['amount']==r['author_amount'] and r['verdict']=='KEEP' for r in rematch),'Primary rematch mismatch'
    for year in sorted({r['period_end'][:4] for r in rematch}):
        for code,select in [('FIGURE',lambda t:t.startswith('A-') and t!='A-borderline'),('BORDER',lambda t:t.startswith('A-')),('AI',lambda t:t=='A-AI safety')]:
            rr=[r for r in rematch if r['period_end'][:4]==year and select(r['author_tier'])]
            add(f'RM-{code}-{year}',ids(rr),total(rr),'sum','Vanguard fiscal-year cash grants to the claim author’s selected recipient population. Category is the author’s label, not an audit attribution of all spending to AI policy. FIGURE excludes the author’s borderline tier; BORDER includes it; AI uses only the author’s AI-safety tier.',funder='Vanguard',period=year,money_type='filed_cash_grant',currency='USD')
    lobbying=read('lobbying.csv')
    for code,kind in [('FE','lobbying_external_fees'),('EX','lobbying_self_expenses'),('SF','lobbying_subcontractor_fees')]:
        for lab in ['Anthropic','OpenAI','Google','Meta','xAI','Microsoft','Amazon']:
            for year in range(2019,2027):
                rr=[r for r in lobbying if r['selected']=='yes' and r['org_id']==lab and r['period']==str(year) and r['money_type']==kind and r['amount']!='']
                term={'Meta':'meta-platforms','xAI':'xai'}.get(lab,lab.lower())
                add(f'{code}-{lab}-{year}',ids(rr) or [f'LQ-{term}-{year}'],total(rr) if rr else '', 'sum' if rr else 'unavailable',
                    'Sum of numeric amounts on latest eligible quarterly reports, all issues combined. Blank reports are not zero and are not added. Separately named intermediaries excluded from direct fees. Outside fees and company expenses overlap and must never be added. Latest year uses completed quarters only; no annualization. No numeric reports means OPEN, not zero spending.',org_id=lab,period=str(year),money_type=kind,currency='USD',quarters=';'.join(sorted({r['quarter'] for r in rr})))
    return sorted(out,key=lambda r:r['row_id']),allrows
