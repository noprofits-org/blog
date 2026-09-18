"""Extract fields from public IRS e-file visual renders, without interpreting donors."""
import csv,datetime,gzip,hashlib,json,pathlib,re
from html.parser import HTMLParser
from collections import defaultdict
P=pathlib.Path(__file__).resolve().parent; S=P/'sources'; R=P/'research';R.mkdir(exist_ok=True)
DATE='2026-09-14'
class Spans(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.active=[];self.out=[]
    def handle_starttag(self,tag,attrs):
        if tag=='span':
            a=dict(attrs);self.active.append([a.get('id',''),[]])
    def handle_data(self,data):
        for _,a in self.active:a.append(data)
    def handle_endtag(self,tag):
        if tag=='span' and self.active:
            key,t=self.active.pop()
            if key.startswith('/AppData/'):self.out.append((key,' '.join(''.join(t).split())))
def read(p):
    b=p.read_bytes();return (gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b).decode('utf8',errors='replace')
def fields(p):
    cache=P/'extracted'/ (p.name+'.json');cache.parent.mkdir(exist_ok=True)
    if cache.exists():return json.loads(cache.read_text())
    parser=Spans();parser.feed(read(p));cache.write_text(json.dumps(parser.out));return parser.out
def val(f,ending):
    found=[v for k,v in f if k.endswith('/'+ending) and v]
    assert len(set(found))<=1,(ending,found)
    return found[0] if found else ''
def num(t):return int(t.replace(',','').replace('$','')) if t else None
def date(t):
    if not t:return ''
    return datetime.datetime.strptime(t,'%m-%d-%Y').strftime('%Y-%m-%d')
def write(name,rows):
    cols=['row_id','amount','source_url','snapshot_date','verbatim_quote_from_source','note']
    cols+=sorted(set().union(*(x.keys() for x in rows))-set(cols)) if rows else []
    with (R/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)

ORGS={
 '881751310':('CAIS','Center for AI Safety','safety','CAIS'),
 '932442608':('CAISAF','Center for AI Safety Action Fund','safety','CAIS'),
 '471052538':('FLI','Future of Life Institute','safety','FLI'),
 '934950919':('SAIF','Safe AI Forum','safety','SAIF'),
 '320839313':('IAPS','Institute for AI Policy and Strategy','safety','IAPS'),
 '874657441':('HORIZON','Horizon Institute for Public Service','safety','HORIZON'),
 '933248564':('ARI','Americans for Responsible Innovation','safety','ARI'),
 '990921925':('CRI','Center for Responsible Innovation','safety','ARI'),
 '237104508':('PC','Public Citizen','comparator','PC'),
 '521263996':('PCF','Public Citizen Foundation','comparator','PC'),
 '237185827':('FAS','Federation of American Scientists','comparator','FAS'),
 '853963084':('PROGRESS','Chamber of Progress','industry','PROGRESS'),
 '204403497':('ITIF','Information Technology and Innovation Foundation','industry','ITIF'),
 '273567814':('TECHFREEDOM','TechFreedom','industry','TECHFREEDOM'),
 '271716101':('NETCHOICE','NetChoice','industry','NETCHOICE'),
 '994513850':('AIPN','AI Policy Network','safety','AIPI'),
 '333199430':('ENCODER','Encode Research Foundation','safety','ENCODE'),
}
SPONSORS={'461008520':'Good Ventures','205205488':'SVCF','237825575':'NPT','232888152':'Vanguard','510198509':'Tides','812644663':'Coefficient Action Fund','992255770':'Coefficient Advisors','810737472':'Coefficient Research','872995455':'Building a Stronger Future','471052538':'Future of Life Institute'}
SPONSORS.update({ein:org[1] for ein,org in ORGS.items() if ein not in SPONSORS})

def run():
    financial=[];identities=[];grantrows=[];docs=[];rawgrants=[]
    index={x['object_id']:x for x in json.loads((P/'filing-index.json').read_text())}
    for obj,x in index.items():
        p=S/f'return-{obj}.html'
        if not p.exists():continue
        fs=fields(p)
        ein=re.sub(r'\D','',val(fs,'Filer[1]/EIN[1]'))
        assert ein==x['ein'],(ein,x)
        begin=date(val(fs,'TaxPeriodBeginDt[1]'));end=date(val(fs,'TaxPeriodEndDt[1]'))
        # Calendar-year filers can leave dates blank in older visual renders.
        if not end:
            text=read(p);match=re.search(r'>(20\d\d)</span>',text)
            if match:begin=f'{match[1]}-01-01';end=f'{match[1]}-12-31'
        name=val(fs,'Filer[1]/BusinessName[1]/BusinessNameLine1Txt[1]')
        source=json.loads(p.with_name(p.name+'.meta.json').read_text())['url']
        submitted=re.search(r'Submission:\s*(\d{4}-\d{2}-\d{2})',read(p))
        submitted=submitted[1] if submitted else ''
        docs.append(dict(row_id='DOC-'+obj,amount='',source_url=source,snapshot_date=DATE,verbatim_quote_from_source=' | '.join([name,val(fs,'TaxPeriodBeginDt[1]'),val(fs,'TaxPeriodEndDt[1]')]),note='Primary IRS e-file visual render hosted by Nonprofit Explorer; full source bytes retained.',ein=ein,period_start=begin,period_end=end,object_id=obj,form=x['form'],source_file=str(p.relative_to(P)),submission_date=submitted))
        if ein in ORGS:
            code,display,side,family=ORGS[ein]
            for metric,tag in [('REV','CYTotalRevenueAmt[1]'),('ASSETS','TotalAssetsEOYAmt[1]'),('PROGRAM','TotalProgramServiceExpensesAmt[1]'),('EXPENSE','CYTotalExpensesAmt[1]'),('CONTRIB','CYContributionsGrantsAmt[1]'),('INVEST','CYInvestmentIncomeAmt[1]'),('NETSALES','NetGainOrLossInvestmentsGrp[1]/TotalRevenueColumnAmt[1]')]:
                t=val(fs,tag)
                if t:
                    financial.append(dict(row_id=f'R-{code}-{end[:4]}-{metric}-{obj[-4:]}',amount=num(t),source_url=source,snapshot_date=DATE,verbatim_quote_from_source=t,note='Exact filed field; fiscal period dates taken from return header. Organization-wide amount; no AI allocation.',org_id=code,org_name=display,family=family,side=side,ein=ein,period_start=begin,period_end=end,metric=metric,money_type='organization_'+metric.lower(),currency='USD',object_id=obj,field_path=next(k for k,v in fs if k.endswith('/'+tag) and v==t),source_file=str(p.relative_to(P))))
        if ein in SPONSORS:
            funder=SPONSORS[ein]
            if funder=='Good Ventures':group='GrantOrContributionPdDurYrGrp';gfs=fs;gp=p
            else:
                gp=S/f'schedule-{obj}.html'
                if not gp.exists():continue
                gfs=fields(gp);group='RecipientTable'
            groups=defaultdict(dict)
            for k,v in gfs:
                m=re.search('/'+group+r'\[(\d+)\]/(.*)',k)
                if m:groups[int(m[1])][m[2]]=v
            for n,g in groups.items():
                recipient=g.get('RecipientBusinessName[1]/BusinessNameLine1Txt[1]','')
                recipient2=g.get('RecipientBusinessName[1]/BusinessNameLine2Txt[1]','')
                re_ein=re.sub(r'\D','',g.get('RecipientEIN[1]',''))
                cash=g.get('Amt[1]','') if funder=='Good Ventures' else g.get('CashGrantAmt[1]','')
                purpose=g.get('GrantOrContributionPurposeTxt[1]',g.get('PurposeOfGrantTxt[1]',''))
                row=dict(funder=funder,funder_ein=ein,recipient=recipient,recipient2=recipient2,recipient_ein=re_ein,amount=num(cash),noncash=g.get('NonCashAssistanceAmt[1]',''),purpose=purpose,period_start=begin,period_end=end,object_id=obj,schedule_row=n,source_file=str(gp.relative_to(P)),source_url=json.loads(gp.with_name(gp.name+'.meta.json').read_text())['url'],verbatim_quote_from_source=cash,source_fields=g)
                rawgrants.append(row)
    selected={}
    for d in docs:
        key=(d['ein'],d['period_start'],d['period_end'])
        if key not in selected or (d['submission_date'],d['object_id'])>(selected[key]['submission_date'],selected[key]['object_id']):selected[key]=d
    selected_ids={d['object_id'] for d in selected.values()}
    for d in docs:d['selected']='yes' if d['object_id'] in selected_ids else 'superseded'
    for r in financial:r['selected']='yes' if r['object_id'] in selected_ids else 'superseded'
    for r in rawgrants:r['selected']='yes' if r['object_id'] in selected_ids else 'superseded'
    (P/'extracted'/'all-grants.json').write_text(json.dumps(rawgrants))
    write('financials.csv',financial);write('filing_documents.csv',docs)
    print('Financial extraction complete. Inspect periods and grant identity matches before aggregation.')
    for g in rawgrants:
        if re.search(r'AI POLICY|ENCODE|ARTIFICIAL INTELLIGENCE POLICY|HORIZON INSTITUTE|SAFETY ACTION|SAFE ARTIFICIAL',g['recipient'],re.I):
            print(g['funder'],g['period_end'],g['recipient'],g['recipient_ein'],g['amount'])
if __name__=='__main__':run()
