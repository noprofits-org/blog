"""Additional checked primary fields and explicit scope/missing-data records."""
import csv,json,re
from assemble_evidence import *

def run():
    # Prior-year values on the next return are primary comparative disclosures.
    fn='return-202133169349311818.html';fs=fields(S/fn);rr=[]
    for metric,tag in [('REV','PYTotalRevenueAmt[1]'),('EXPENSE','PYTotalExpensesAmt[1]'),('ASSETS','TotalAssetsBOYAmt[1]')]:
        q=val(fs,tag)
        rr.append(base('R-NETCHOICE-2019-'+metric+'-COMP',fn,q,
            'Prior-year revenue/expenses or opening assets explicitly reported on the subsequent calendar-year return. The standalone scanned prior-year return route is robots-disallowed; no scan was fetched. This is a comparative disclosure, not extraction from that blocked scan.',num(q),
            org_id='NETCHOICE',org_name='NetChoice',family='NETCHOICE',side='industry',ein='271716101',period_start='2019-01-01',period_end='2019-12-31',metric=metric,money_type='organization_'+metric.lower(),currency='USD',object_id='202133169349311818',field_path=next(k for k,v in fs if k.endswith('/'+tag)),selected='yes',verdict='KEEP'))
    fn='return-202502259349300600.html';fs=fields(S/fn);tag='TotalFunctionalExpensesGrp[1]/ProgramServicesAmt[1]';q=val(fs,tag)
    assert q=='0'
    rr.append(base('R-SAIF-2024-PROGRAM-IX',fn,q,'Current-year program-service expense explicitly reported in Part IX, even though the Part III total is blank. The filed zero is retained.',0,org_id='SAIF',org_name='Safe AI Forum',family='SAIF',side='safety',ein='934950919',period_start='2024-01-01',period_end='2024-12-31',metric='PROGRAM',money_type='organization_program',currency='USD',object_id='202502259349300600',field_path=next(k for k,v in fs if k.endswith('/'+tag)),selected='yes',verdict='KEEP'))
    write('financial_comparatives.csv',rr)
    rows=[]
    def add(rid,fn,q,note,**kw):
        assert ' '.join(q.split()) in ' '.join(text(fn).split()),rid
        rows.append(base(rid,fn,q,note,**kw))
    add('D-CRI','cri-home.html','Founders Pledge, the Laidir Foundation, Coefficient Giving, the David and Lucile Packard Foundation, Omidyar Network, and Sentinel Bio',
        'Own supporter list; amounts undisclosed. Added as the related research organization linked from the requested ARI website; standalone entity remains separate.',org_id='CRI',declared_funders='Founders Pledge;Laidir Foundation;Coefficient Giving;David and Lucile Packard Foundation;Omidyar Network;Sentinel Bio;individual donors',verdict='KEEP')
    add('D-ARI-CRI','ari-about.html','Center for Responsible Innovation',
        'ARI links to CRI in its own navigation. This supports including a related organization for coverage; it is not proof of a particular legal control or consolidation relationship.',org_id='ARI',verdict='KEEP')
    add('D-CONTROL-NO-PL-2025','controlai-accounts-2025.xhtml','the directors have not delivered to the registrar a copy of the Income and Expenditure Account.',
        'The later filed accounts also omit this statement. No annual revenue inferred from balance-sheet or surplus figures.',org_id='CONTROL',verdict='KEEP')
    add('D-XCORP-SCOPE','lda-x-corp-context.html','X Corp. (formerly Twitter, Inc.)',
        'This public lobbying report names X Corp. as client and registrant. It is not an xAI-named report; no xAI expense allocation is supplied. It is excluded from the xAI series.',org_id='xAI',verdict='OPEN')
    add('D-PC-POLICY','citizen-annual.html','We do not accept corporate or government money',
        'Attributed funding policy on the official annual-report page. This is not an independent verification of every receipt or a donor-by-period funding share.',org_id='PC',declared_funders='Individual donors and foundation grants (categories only)',verdict='KEEP')
    add('D-FAS','fas-annual-2023.html','National Philanthropic Trust',
        'Official annual report names philanthropic and agency supporters, including the sources in declared_funders. No per-supporter dollar allocations are supplied in this list.',org_id='FAS',declared_funders='Good Ventures Foundation;Open Philanthropy;Future of Life Institute;Horizon Institute for Public Service;National Philanthropic Trust;Silicon Valley Community Foundation;William and Flora Hewlett Foundation;Gates Foundation;Schmidt Futures;federal agencies;other listed supporters',verdict='KEEP')
    write('supplement_disclosures.csv',rows)
    q='$51 million in new commitments';assert q in text('fas-annual-2023.html')
    write('commitments.csv',[base('C-FAS-2023','fas-annual-2023.html',q,'Organization-reported new commitments in its annual report. Not cash receipts, filed grant disbursements or Form 990 revenue. No donor-by-donor allocation provided.',51000000,org_id='FAS',period='2023',currency='USD',money_type='commitment',verdict='KEEP')])
    # Metadata and methodological quantities also have row IDs.
    specs=[
      ('M-START',2019,'2019','Start of requested financial-history and lobbying window; user-defined scope, not a source finding.'),
      ('M-REV-END',2024,'2024','Final fiscal-year-ending year for the requested org revenue chart.'),
      ('M-GRANT-END',2025,'2025','Final fiscal-year-ending year allowed in the filed-grant pool; source-specific coverage is in grant_searches.csv.'),
      ('M-LDA-END',2026,'2026','Latest requested lobbying year. Only completed calendar quarters are aggregated.'),
      ('M-LDA-QUARTER',2,'2026-06-30','Last completed quarter used in the partial-year comparison; no annualization.'),
      ('M-WIDTH',1200,'1200','Requested raster image width in pixels.'),('M-HEIGHT',630,'630','Requested raster image height in pixels.'),
      ('M-MILLION',1000000,'1000000','Display conversion: dollars per million dollars; all evidence retains original dollars.'),
      ('M-PERCENT',100,'100','Percentage display conversion; ratio is restricted to identified filed cash grants.'),
    ]
    scope=[dict(row_id=rid,amount=a,source_url='user-provided://advocacy-audit-brief',snapshot_date=DATE,verbatim_quote_from_source=q,note=n,money_type='scope_or_unit',unit='metadata') for rid,a,q,n in specs]
    scope.append(dict(row_id='M-SNAPSHOT',amount='',source_url='local://retrieval-metadata',snapshot_date=DATE,verbatim_quote_from_source=DATE,note='Snapshot date attached to every retained source response. It is not a filing date.',money_type='snapshot_date'))
    write('scope.csv',scope)
    # Explicit registry and filing availability for every legal entity / year.
    fin=list(csv.DictReader((R/'financials.csv').open()))+rr
    entities=list(csv.DictReader((R/'entities.csv').open()));hist=[]
    for e in entities:
        for year in range(2019,2025):
            got=[r for r in fin if r['org_id']==e['org_id'] and r['period_end'][:4]==str(year) and r['metric']=='REV' and r['selected']=='yes']
            hist.append(dict(row_id=f"H-{e['org_id']}-{year}",amount='',source_url=e['source_url'],snapshot_date=DATE,verbatim_quote_from_source=e['verbatim_quote_from_source'],note='Revenue is available in the linked evidence row.' if got else 'No standalone annual revenue evidence for this fiscal-year-ending year in the captured organization registry/filing listing (or UK filed accounts for ControlAI). This is an availability flag, not zero revenue or proof of nonexistence.',org_id=e['org_id'],period=str(year),verdict='KEEP' if got else 'OPEN',input_row_ids=';'.join(r['row_id'] for r in got) or e['row_id'],closing_document='' if got else 'Standalone primary annual return or accounts disclosing revenue for this legal entity and fiscal period; sponsor-wide returns do not close the project-level question.'))
    write('history_coverage.csv',hist)
    print('Supplemental fields and coverage written.')
if __name__=='__main__':run()
