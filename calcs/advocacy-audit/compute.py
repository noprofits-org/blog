#!/usr/bin/env python3
"""Reproduce and assert the audit. Never rewrites source CSVs or expected values.

    .venv/bin/python compute.py             # validate, calculate, render figures
    .venv/bin/python compute.py --check-only

Expected values are frozen in research/aggregates.csv. LOCK.json pins evidence,
source snapshots and field caches. Any drift is a hard error requiring review.
"""
import argparse,csv,hashlib,json,re,sys
from collections import defaultdict
from decimal import Decimal
from functools import lru_cache
from audit_core import P,R,read,calculate
REQUIRED={'row_id','amount','source_url','snapshot_date','verbatim_quote_from_source','note'}

def check_lock():
    lock=json.loads((P/'LOCK.json').read_text())
    assert set(lock['research_files'])=={str(p.relative_to(P)) for p in R.glob('*.csv')},'CSV inventory drift'
    for name,digest in lock['files'].items():
        path=P/name
        assert path.is_file(),'Missing locked evidence: '+name
        assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Evidence drift: '+name
    for p in (P/'sources').glob('*.meta.json'):
        meta=json.loads(p.read_text());body=p.with_name(p.name.removesuffix('.meta.json'))
        assert hashlib.sha256(body.read_bytes()).hexdigest()==meta['sha256'],'Retrieval hash mismatch: '+str(body)

@lru_cache(maxsize=4)
def source_fields(name):
    p=P/'extracted'/(name.split('/')[-1]+'.json')
    assert p.exists(),'Missing pinned field extraction: '+str(p)
    return json.loads(p.read_text())
@lru_cache(maxsize=4)
def field_map(name):
    data=defaultdict(set)
    for k,v in source_fields(name):data[k].add(v)
    return data
@lru_cache(maxsize=4)
def lda_source(name):return {r['filing_uuid']:r for r in json.loads((P/name).read_text())['results']}

def validate_primary():
    for r in read('sponsor_status.csv'):
        assert r['verbatim_quote_from_source'] in field_map(r['source_file'])[r['field_path']],r['row_id']
    original_claim=list(csv.DictReader((P/'sources/rematch-cluster.csv').open()))
    rematch=read('rematch.csv')
    assert {r['row_id'] for r in original_claim}=={r['author_row_id'] for r in rematch},'Incomplete rematch population'
    assert len(original_claim)==len(rematch),'Ambiguous rematch multiplicity'
    for s in read('grant_searches.csv'):
        pf=s['funder']=='Good Ventures';name=('return-' if pf else 'schedule-')+s['object_id']+'.html'
        group='GrantOrContributionPdDurYrGrp' if pf else 'RecipientTable'
        numbers={re.search('/'+group+r'\[(\d+)\]/',k)[1] for k,v in source_fields('sources/'+name) if re.search('/'+group+r'\[(\d+)\]/',k)}
        assert len(numbers)==int(s['amount']),('Schedule row-count drift',s['row_id'])
    for q in read('lobbying_queries.csv'):
        seen=set()
        for name in json.loads(q['pages']):
            page=json.loads((P/'sources'/name).read_text());assert page['count']==int(q['amount']),q['row_id']
            seen.update(r['filing_uuid'] for r in page['results'])
        assert len(seen)==int(q['amount']),('Incomplete query pages',q['row_id'])
    for r in read('financials.csv')+read('financial_comparatives.csv'):
        fm=field_map(r['source_file'])
        assert r['verbatim_quote_from_source'] in fm[r['field_path']],r['row_id']
        assert Decimal(r['verbatim_quote_from_source'].replace(',',''))==Decimal(r['amount']),r['row_id']
        fs=source_fields(r['source_file'])
        ein=next(v for k,v in fs if k.endswith('/Filer[1]/EIN[1]'))
        assert re.sub(r'\D','',ein)==r['ein'],('Wrong filer',r['row_id'])
        if not r['row_id'].endswith('-COMP'):
            for column,tag in [('period_start','TaxPeriodBeginDt[1]'),('period_end','TaxPeriodEndDt[1]')]:
                vals=[v for k,v in fs if k.endswith('/'+tag) and v]
                if vals:
                    mm,dd,yyyy=vals[0].split('-');assert r[column]==f'{yyyy}-{mm}-{dd}',('Wrong fiscal period',r['row_id'],column)
    for filename in ['grants.csv','project_grants.csv','rematch.csv']:
        for r in read(filename):
            fm=field_map(r['source_file']);sf=json.loads(r['source_fields'])
            group='GrantOrContributionPdDurYrGrp' if r['funder']=='Good Ventures' else 'RecipientTable'
            marker='/'+group+'['
            k=next(k for k in fm if marker in k)
            prefix=k.split(marker)[0]+f"/{group}[{r['schedule_row']}]/"
            for tag,value in sf.items():assert value in fm[prefix+tag],('Grant field mismatch',r['row_id'],tag)
            cash=sf['Amt[1]'] if group.startswith('Grant') else sf['CashGrantAmt[1]']
            assert cash==r['verbatim_quote_from_source'] and Decimal(cash.replace(',',''))==Decimal(r['amount']),r['row_id']
            assert sf['RecipientBusinessName[1]/BusinessNameLine1Txt[1]']==r['recipient_name'],r['row_id']
            if r.get('recipient_ein'):
                assert re.sub(r'\D','',sf['RecipientEIN[1]'])==r['recipient_ein'],r['row_id']
    # Compare each reported amount and its identity/quarter to the saved public API response.
    for r in read('lobbying.csv'):
        original=lda_source(r['source_file'])[r['filing_uuid']]
        for key,value in json.loads(r['verbatim_quote_from_source']).items():assert original[key]==value,('LDA source mismatch',r['row_id'],key)
        assert original['client']['name']==r['client_name'] and original['registrant']['name']==r['registrant_name'],r['row_id']
        if r['amount']!='':assert Decimal(original[r['amount_field']])==Decimal(r['amount']),r['row_id']
    # Latest-version selection is checked independently of amount aggregation.
    eligible=defaultdict(list)
    for r in read('lobbying.csv'):
        if r['filing_type'] not in ['RR','RA'] and not (r['period']=='2026' and int(r['quarter'])>2):
            eligible[(r['registrant_id'],r['client_id'],r['period'],r['quarter'])].append(r)
    for rr in eligible.values():
        last=max(rr,key=lambda r:(r['dt_posted'],r['filing_uuid']))
        for r in rr:
            if r['selected']=='yes':assert r['row_id']==last['row_id'],('Superseded LDA report selected',r['row_id'])
    # Numeric source excerpts are literal; they are not reconstructed donor values.
    for filename in ['awards.csv','recommendations.csv']:
        for r in read(filename):
            q=r['verbatim_quote_from_source'];assert Decimal(q.replace('$','').replace(',',''))==Decimal(r['amount']),r['row_id']
    from bs4 import BeautifulSoup
    for name in {r['source_file'] for r in read('uk_accounts.csv')}:
        soup=BeautifulSoup((P/name).read_bytes(),'xml')
        contexts={c.get('id'):c.find('instant').get_text() for c in soup.find_all('context') if c.find('instant')}
        for r in [r for r in read('uk_accounts.csv') if r['source_file']==name]:
            node=next(x for x in soup.find_all() if x.name.lower()=='nonfraction' and x.get('name')==r['field_name'] and x.get('contextRef')==r['context'])
            quote=node.get_text(' ',strip=True);assert quote==r['verbatim_quote_from_source'],r['row_id']
            signed=Decimal(quote.replace(',',''))*(-1 if node.get('sign')=='-' else 1)
            assert signed==Decimal(r['amount']) and contexts[r['context']]==r['period_end'],r['row_id']

def validate_rows():
    rows={}
    for p in sorted(R.glob('*.csv')):
        with p.open(newline='') as f:
            reader=csv.DictReader(f);assert REQUIRED<=set(reader.fieldnames),(p.name,'Required columns')
            for r in reader:
                assert r['row_id'] and r['row_id'] not in rows,('Duplicate row ID',r['row_id'])
                assert r['source_url'] and r['snapshot_date']=='2026-09-14',('Missing provenance',r['row_id'])
                if r['amount']:assert Decimal(r['amount']).is_finite(),r['row_id']
                rows[r['row_id']]=r
    for r in rows.values():
        for ident in r.get('input_row_ids','').split(';'):
            if ident:assert ident in rows,('Broken row reference',r['row_id'],ident)
    for p in [P/'NOTES.md',P/'STATE.md']:
        if p.exists():
            for group in re.findall(r'\[([^\]\n]+)\]',p.read_text()):
                if re.match(r'^(?:R-|RV-|RM-|MX-|DP-|DN-|DD-|V-|ID-|M-|D-|CV-|H-|FE-|EX-|SF-|C-|O-|G-|RC-|AW-|PJ-|S-|SEARCH-|PAGE-|ACCESS-|METHOD-)',group):
                    for rid in group.split('; '):assert rid in rows,('Broken prose row citation',p.name,rid)
    return rows

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check-only',action='store_true');args=parser.parse_args()
    check_lock();rows=validate_rows();validate_primary()
    actual,_=calculate();expected=read('aggregates.csv')
    norm=lambda r:{k:str(v) for k,v in r.items() if v!=''}
    assert {r['row_id']:norm(r) for r in actual}=={r['row_id']:norm(r) for r in expected},'Aggregate drift: calculated rows differ from frozen research/aggregates.csv'
    # Independent benchmark values from the manually reviewed primary rematch.
    a={r['row_id']:r for r in actual}
    assert Decimal(a['RM-FIGURE-2024']['amount'])==Decimal('8157254'),'Rematch baseline changed'
    assert Decimal(a['RM-FIGURE-2025']['amount'])==Decimal('65627700'),'Rematch comparison changed'
    for r in actual:
        if r['row_id'].startswith('DP-') and r['amount']:assert 0<=Decimal(r['amount'])<=100,r['row_id']
    for r in read('figure_index.csv'):
        if r.get('value_row_id'):
            assert r['amount']==rows[r['value_row_id']]['amount'],('Figure value drift',r['row_id'])
    if not args.check_only:
        from plot_figures import build
        from PIL import Image
        build()
        for p in (P/'figures').glob('*.png'):
            assert Image.open(p).size==(int(rows['M-WIDTH']['amount']),int(rows['M-HEIGHT']['amount'])),('Image size drift',p.name)
    print('PASS: pinned evidence, primary field matches, version selection, row references, frozen aggregates and figure data agree.')
if __name__=='__main__':
    try:main()
    except Exception as e:
        print('AUDIT FAILED: '+str(e),file=sys.stderr);raise
