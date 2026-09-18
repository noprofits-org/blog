"""Public LDA reports; preserve amendments and distinguish expenses from fees."""
import json,re
from collections import defaultdict
from assemble_evidence import P,S,DATE,write,base

QUARTERS={'first_quarter':1,'second_quarter':2,'third_quarter':3,'fourth_quarter':4}
def classify(name):
    n=name.upper()
    if n in ['O.N.E. AMAZON','EVERSHEDS SUTHERLAND ON BEHALF OF AMAZONAS HOLDINGS LLC','GOOGLE, INC. ON BEHALF OF X','WING (FORMERLY X (GOOGLE INC ))']:
        return '', 'Unrelated or separately branded client; excluded from lab scope.'
    for term,lab in [('ANTHROPIC','Anthropic'),('OPENAI','OpenAI'),('GOOGLE','Google'),('META PLATFORMS','Meta'),('FACEBOOK','Meta'),('MICROSOFT','Microsoft'),('AMAZON','Amazon')]:
        if term in n:return lab,''
    if n.startswith(('XAI','X.AI')):return 'xAI',''
    raise ValueError('Unreviewed client name: '+name)

def run():
    raw={};queries=[];aliases={}
    for p in sorted(S.glob('lda-*-p1.json')):
        m=re.fullmatch(r'lda-(.+)-(20\d\d)-p1.json',p.name)
        if not m:continue
        term,year=m.groups();part=json.loads(p.read_text());n=1;seen=set();pages=[]
        count=part['count']
        while True:
            fn=f'lda-{term}-{year}-p{n}.json';part=json.loads((S/fn).read_text());pages.append(fn)
            assert part['count']==count,('Query changed while paging',fn)
            for r in part['results']:
                assert r['filing_uuid'] not in seen,('Duplicate within query',fn,r['filing_uuid'])
                seen.add(r['filing_uuid']);raw.setdefault(r['filing_uuid'],(r,fn))
            if not part['next']:break
            n+=1
        assert len(seen)==count,(term,year,len(seen),count)
        queries.append(base(f'LQ-{term}-{year}',p.name,f'"count": {count}',
            'Complete public client-name query for this filing year, including all pages. A zero count is a bounded search result, not zero spending.',count,
            term=term,period=year,money_type='query_result_count',unit='filings',pages=json.dumps(pages),verdict='KEEP'))
    latest={}
    for r,fn in raw.values():
        if r['filing_type'] in ['RR','RA']:continue
        q=QUARTERS[r['filing_period']]
        if r['filing_year']==2026 and q>2:continue
        key=(r['registrant']['id'],r['client']['id'],r['filing_year'],q)
        if key not in latest or (r['dt_posted'],r['filing_uuid'])>(latest[key]['dt_posted'],latest[key]['filing_uuid']):latest[key]=r
    chosen={r['filing_uuid'] for r in latest.values()};rows=[]
    for uuid,(r,fn) in sorted(raw.items()):
        client=r['client']['name'];reg=r['registrant']['name'];lab,reason=classify(client)
        aliasid='LA-'+str(r['client']['id'])
        aliases.setdefault(aliasid,base(aliasid,fn,client,reason or 'Named corporate client, assigned to this lab family. Historical corporate names are retained exactly as returned by the API; no subsidiary-specific AI allocation.',org_id=lab,client_id=r['client']['id'],client_name=client,verdict='KEEP' if lab else 'OPEN'))
        q=QUARTERS[r['filing_period']];selected='yes' if uuid in chosen else 'superseded_or_registration_or_incomplete_quarter'
        if not lab:selected='excluded_client'
        subcontract=bool(re.search(r'\bOBO\b|ON BEHALF OF',client.upper()))
        same=reg.upper()==client.upper()
        if r['expenses'] is not None:
            money='lobbying_self_expenses' if same else 'lobbying_ambiguous_expenses'
            amount=r['expenses'];field='expenses'
            if not same:selected='excluded_inconsistent_expense_filer'
        elif r['income'] is not None:
            money='lobbying_subcontractor_fees' if subcontract else 'lobbying_external_fees'
            amount=r['income'];field='income'
        else:money='lobbying_unquantified_report';amount='';field='income/expenses'
        if r['income'] is not None and r['expenses'] is not None:raise ValueError('Both money fields: '+uuid)
        note='Latest report per registrant/client/year/quarter is eligible; registrations and superseded reports are excluded. All issues combined; no dollar allocation to AI. Income is the outside registrant’s reported fee, not lab self-reported expense. API blank amounts remain unknown.'
        if subcontract:note+=' Client expressly names an intermediary; excluded from direct external-fee totals to avoid counting subcontracts twice.'
        if money=='lobbying_ambiguous_expenses':note+=' Expense reported by a different registrant than the client; excluded from standard totals and flagged for review.'
        quote=json.dumps({k:r[k] for k in ['filing_uuid','filing_type','filing_year','filing_period', 'income','expenses']},separators=(',',':'))
        out=base('L-'+uuid,fn,quote,note,amount,
            org_id=lab,client_id=r['client']['id'],client_name=client,registrant_id=r['registrant']['id'],registrant_name=reg,
            currency='USD',money_type=money,period=str(r['filing_year']),quarter=q,filing_type=r['filing_type'],filing_type_display=r['filing_type_display'],
            dt_posted=r['dt_posted'],filing_uuid=uuid,selected=selected,amount_field=field,client_self_select=r['client']['client_self_select'],
            issue_codes=';'.join(sorted({a['general_issue_code'] for a in r['lobbying_activities']})),
            issue_descriptions=json.dumps([a['description'] for a in r['lobbying_activities']]),
            api_url=r['url'],verdict='OPEN' if money in ['lobbying_ambiguous_expenses','lobbying_unquantified_report'] else 'KEEP')
        out['source_url']=r['filing_document_url'];rows.append(out)
    write('lobbying.csv',rows);write('lobbying_queries.csv',queries);write('lobbying_aliases.csv',list(aliases.values()))
    print('LDA files parsed; complete query counts and latest-report selection checked.')
if __name__=='__main__':run()
