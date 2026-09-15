"""Document bounded page searches, figure keys and remaining field-level gaps."""
import json,csv,re
from collections import defaultdict
from assemble_evidence import base,text,S,DATE,write
from audit_core import P,R,read

PAGES={
 'CAIS':['cais-faq.html'],'CAISAF':['cais-faq.html'],
 'AIPI':['aipi-about.html','aipi-donate.html'],'AIPN':['aipn-home.html'],
 'ENCODE':['encode-privacy.html','encode-donation.html'],'ENCODER':['encode-privacy.html','encode-donation.html'],
 'FLI':['fli-funding.html'],'CONTROL':['controlai-about.html','controlai-registry.html','controlai-accounts-2024.xhtml','controlai-accounts-2025.xhtml'],
 'SAIF':['saif-home.html'],'IAPS':['iaps-funding.html'],'HORIZON':['horizon-about.html'],
 'ARI':['ari-about.html'],'CRI':['cri-home.html'],'PC':['citizen-annual.html'],'PCF':['citizen-annual.html'],
 'FAS':['fas-about.html','fas-annual-2023.html'],'PROGRESS':['progress-partners.html'],'ITIF':['itif-supporters.html'],
 'TECHFREEDOM':['techfreedom-about.html'],'NETCHOICE':['netchoice-about.html'],
}
def run():
    rows=[]
    for org,names in PAGES.items():
        for name in names:
            if not (S/name).exists():continue
            quote=' '.join(text(name).split())[:140]
            rows.append(base(f'PAGE-{org}-{name.split(".")[0]}',name,quote,'This specific captured page was searched for identity and funding disclosures. This is not an exhaustive crawl or a claim about other pages or dates.',org_id=org,search_scope='public page snapshot',document_name=name))
    rows.append(base('PAGE-EA-INDEX','ea-funds-grants.html','Grants','Full embedded public grant index searched against the EIN/name alias register where names are supplied. No exact organization-name match found; no person-level or sponsor-wide grant allocated to an organization. This non-match is bounded to this index snapshot.',search_scope='embedded grantsList array',document_name='EA Funds public grant index'))
    rows.append(base('PAGE-PC-REVIEW','citizen-review-2024.pdf','2024','The annual-review PDF linked as the requested fiscal-year review was text-extracted and searched for funding/donor disclosures. No donor-by-period ledger found. This is a bounded search of this document, not all Public Citizen publications.',org_id='PC',document_name='Public Citizen year-in-review PDF'))
    write('page_searches.csv',rows)
    # Record blocked routes without manufacturing source quotes from failed retrievals.
    rows=[dict(row_id='ACCESS-NETCHOICE-SCAN',amount='',source_url='https://projects.propublica.org/nonprofits/display_990/271716101/08_2021_prefixes_27-34%2F271716101_201912_990O_2021081718734733',snapshot_date=DATE,verbatim_quote_from_source='Disallow: /nonprofits/display_990*',note='robots.txt disallows the scanned-return route; not fetched. Prior-year financial comparatives on the subsequent permitted primary render were used where explicitly reported.',source_file='sources/robots-projects.propublica.org.txt',verdict='OPEN')]
    write('access_limits.csv',rows)
    a=read('aggregates.csv');entities={r['org_id']:r for r in read('entities.csv')};figs=[]
    for r in a:
        name=None
        if r['row_id'].startswith('RV-') and entities[r['org_id']]['side']=='safety':name='01-safety-revenue'
        if r['row_id'].startswith('MX-'):name='02-funder-matrix'
        if r['row_id'].startswith(('FE-','EX-')):name='03-lab-lobbying'
        if r['row_id'].startswith(('DP-','DN-','DD-')):name='04-daf-sponsor-share'
        if name:
            figs.append(dict(r,row_id='FIG-'+r['row_id'],input_row_ids=r['row_id'],value_row_id=r['row_id'],figure=name,org_name=entities[r['org_id']]['org_name'] if r['org_id'] in entities else r['org_id'],note='Plotted value maps directly to value_row_id. Dollar labels are rounded for display; exact amounts and fiscal periods are in the value row and its inputs. Organization and payer codes are those printed in the chart keys. '+r['note']))
    write('figure_index.csv',figs)
    # Expense-column gaps cannot be replaced by a total-expense number.
    fin=read('financials.csv')+read('financial_comparatives.csv');group=defaultdict(list);gaps=[]
    for r in fin:
        if r['selected']=='yes':group[(r['org_id'],r['period_end'])].append(r)
    for (org,end),rr in group.items():
        for metric in ['REV','ASSETS','PROGRAM']:
            if metric not in {r['metric'] for r in rr}:
                src=rr[0]
                gaps.append(dict(row_id=f'O-METRIC-{org}-{end[:4]}-{metric}',amount='',source_url=src['source_url'],snapshot_date=DATE,verbatim_quote_from_source=src['verbatim_quote_from_source'],note='The captured primary return does not provide the requested metric as a filled numeric field. Total expense is not substituted for program-service expense.',org_id=org,period=end[:4],metric=metric,verdict='OPEN',claim='Requested financial metric unavailable',input_row_ids=src['row_id'],closing_document='Public annual return or audited functional-expense statement giving this exact metric for the legal entity and period.'))
    existing=read('open_questions.csv');existing=[r for r in existing if not r['row_id'].startswith('O-METRIC-')];write('open_questions.csv',existing+gaps)
    print('Bounded page searches and figure value keys written.')
if __name__=='__main__':run()
