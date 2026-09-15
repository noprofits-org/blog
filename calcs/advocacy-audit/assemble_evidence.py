"""Build the evidence register. This is acquisition code; compute.py never runs it."""
import csv,datetime,hashlib,json,re
from collections import defaultdict
from bs4 import BeautifulSoup
from parse_filings import P,S,R,DATE,ORGS,SPONSORS,read,write,fields,val,num

def source(fn):return json.loads((S/(fn+'.meta.json')).read_text())['url']
def text(fn):
    soup=BeautifulSoup(read(S/fn),'lxml')
    for x in soup(['script','style','svg']):x.decompose()
    return soup.get_text(' ',strip=True)
def base(rid,fn,quote,note,amount='',**kw):
    return dict(row_id=rid,amount=amount,source_url=source(fn),snapshot_date=DATE,verbatim_quote_from_source=quote,note=note,source_file='sources/'+fn,**kw)
def clean(s):return re.sub('[^a-z0-9]','',s.lower())
NAMES={clean(v[1]):v[0] for v in ORGS.values()}
NAMES.update({clean(k):v for k,v in {
 'Center for AI Safety Inc':'CAIS','The Center for AI Safety Inc':'CAIS','Center for Artificial Intelligence Safety Inc':'CAIS',
 'Center for AI Safety Action Fund Inc':'CAISAF','Safe Artificial Intelligence Forum Institute':'SAIF','Center for Responsible Innovation Ltd':'CRI',
 'Americans for Responsible Innovation Ltd':'ARI','Public Citizen Inc':'PC','Public Citizen Foundation Inc':'PCF','Public Citizen Foundation':'PCF',
 'AI Policy Institute':'AIPI','AI Policy Institute (AIPI)':'AIPI','Artificial Intelligence Policy Institute':'AIPI','Encode Justice':'ENCODE',
 'The AI Policy Institute':'AIPI','Center for AI Safety (CAIS)':'CAIS','Center for AI Safety Action Fund (CAIS AF)':'CAISAF','The Institute for AI Policy and Strategy (IAPS)':'IAPS',
 'Encode AI Corporation':'ENCODE','Encode':'ENCODE','ControlAI':'CONTROL','Secure Future Research Ltd':'CONTROL',
 'Federation of American Scientists Inc':'FAS','Institute for AI Policy and Strategy (IAPS)':'IAPS',
 }.items()})
def match(name,ein=''):
    if ein in ORGS:return ORGS[ein][0]
    return NAMES.get(clean(name))

def identities():
    rows=[]
    for ein,(code,name,side,family) in ORGS.items():
        fn=f'org-{ein}.json'
        if not (S/fn).exists():continue
        org=json.loads((S/fn).read_text())['organization']
        rows.append(base('ID-'+code,fn,json.dumps({k:org.get(k) for k in ['name','ein','subsection_code','ruling_date']},separators=(',',':')),
            'Identity from the IRS Business Master File as distributed by the public Nonprofit Explorer API. This is a registry listing, not proof of current activity or a donor disclosure.',
            org_id=code,org_name=name,family=family,side=side,ein=ein,tax_status=f"501(c)({org['subsection_code']})",verdict='KEEP',legal_name=org['name']))
    rows.append(base('ID-AIPI','aipi-donate.html','We’re a donor-supported 501(c)(3) non-profit.','Self-description only. Separate standalone EIN and determination letter unresolved. SFF lists The Hack Foundation as receiving charity; project-level money is not the sponsor’s total revenue.',org_id='AIPI',org_name='AI Policy Institute',family='AIPI',side='safety',ein='',tax_status='Self-described charity; fiscal-sponsored recommendation identified',verdict='OPEN',legal_name='Unresolved standalone legal entity'))
    rows.append(base('ID-ENCODE','encode-privacy.html','Encode AI Corporation, a 501(c)(4) social welfare organization','Own legal notice establishes the name and claimed status. IRS determination/EIN not located in the bounded search; registry status remains OPEN.',org_id='ENCODE',org_name='Encode AI Corporation / Encode Justice',family='ENCODE',side='safety',ein='',tax_status='Self-described 501(c)(4)',verdict='OPEN',legal_name='Encode AI Corporation'))
    rows.append(base('ID-CONTROL','controlai-registry.html','Private Limited Company by guarantee without share capital use of \'Limited\' exemption','Companies House confirms legal existence and company form. Company registration is not charitable tax status. Former name Secure Future Research Ltd; no charity registration inferred.',org_id='CONTROL',org_name='ControlAI (UK)',family='CONTROL',side='safety',ein='',company_number='15088415',tax_status='UK company limited by guarantee; charitable tax status OPEN',verdict='KEEP',legal_name='CONTROLAI'))
    write('entities.csv',rows)

def funding():
    raw=json.loads((P/'extracted/all-grants.json').read_text()); rows=[];project=[]
    for g in raw:
        code=match(g['recipient'],g['recipient_ein'])
        if not code and 'INSTITUTE FOR AI POLICY AND STRATEGY' in g['purpose'].upper():
            # Never allocate a mixed-purpose grant wholly to the named project.
            code='IAPS';allocated='mixed-purpose' if 'GENERAL SUPPORT AND' in g['purpose'] else 'earmarked-project'
        else:allocated='legal-grantee'
        if not code:continue
        fn=g['source_file'].split('/')[-1]
        rid=f"G-{g['funder_ein']}-{g['object_id']}-{g['schedule_row']}"
        route='DAF_sponsor_unspecified_fund' if g['funder'] in ['SVCF','NPT','Vanguard','Tides'] else 'direct_named_institution'
        r=base(rid,fn,g['verbatim_quote_from_source'],
            'Filed cash disbursement. Grantee matched by EIN when supplied, otherwise normalized legal name. Sponsor name does not establish the original donor. Separate duplicate filing versions are retained and flagged.',g['amount'],
            org_id=code,funder=g['funder'],funder_ein=g['funder_ein'],recipient_name=g['recipient'],recipient_ein=g['recipient_ein'],period_start=g['period_start'],period_end=g['period_end'],currency='USD',money_type='filed_cash_grant',route=route,allocation=allocated,selected=g['selected'],object_id=g['object_id'],schedule_row=g['schedule_row'],purpose=g['purpose'],noncash_amount=g['noncash'],source_fields=json.dumps(g['source_fields'],sort_keys=True),verdict='KEEP' if allocated!='mixed-purpose' else 'OPEN')
        if allocated!='legal-grantee':
            r['money_type']='filed_project_earmarked_grant' if allocated=='earmarked-project' else 'filed_mixed_purpose_grant';project.append(r)
        else:rows.append(r)
    write('grants.csv',rows);write('project_grants.csv',project)
    # Reproduce the rematch author's population, without endorsing its category labels.
    claimed=list(csv.DictReader((S/'rematch-cluster.csv').open()))
    rematch=[]
    for c in claimed:
        found=[g for g in raw if g['funder']=='Vanguard' and g['period_end'][:4]==c['fiscal_year'][-4:] and g['recipient_ein']==re.sub(r'\D','',c['ein']).zfill(9) and g['selected']=='yes']
        for g in found:
            fn=g['source_file'].split('/')[-1]
            rematch.append(base('RM-'+c['row_id'],fn,g['verbatim_quote_from_source'],'Primary filing rematch by recipient EIN and exact fiscal period. Author-selected tier retained as a classification claim, not a finding about each recipient’s activities.',g['amount'],
                currency='USD',money_type='filed_cash_grant',funder='Vanguard',period_start=g['period_start'],period_end=g['period_end'],recipient_name=g['recipient'],recipient_ein=g['recipient_ein'],object_id=g['object_id'],schedule_row=g['schedule_row'],purpose=g['purpose'],author_row_id=c['row_id'],author_amount=c['amount'],author_tier=c['tier'],author_name=c['canonical_name'],source_fields=json.dumps(g['source_fields'],sort_keys=True),verdict='KEEP' if g['amount']==int(c['amount']) else 'KILL'))
        if not found:print('UNMATCHED REMATCH',c['row_id'],c['recipient'],c['ein'])
    write('rematch.csv',rematch)
    # Search log ties all bounded negatives to complete documents, not keyword-only search results.
    docs=list(csv.DictReader((R/'filing_documents.csv').open()))
    search=[]
    for d in docs:
        if d['ein'] not in SPONSORS or d['selected']!='yes':continue
        if d['ein']!='461008520' and not (S/f"schedule-{d['object_id']}.html").exists():continue
        gg=[g for g in raw if g['object_id']==d['object_id']]
        search.append(dict(row_id='SEARCH-'+d['object_id'],amount=len(gg),source_url=d['source_url'] if d['ein']=='461008520' else f"https://projects.propublica.org/nonprofits/full_text/{d['object_id']}/IRS990ScheduleI",snapshot_date=DATE,verbatim_quote_from_source=d['verbatim_quote_from_source'],note='All domestic organization grant entries parsed and searched by the entity EIN and documented name aliases; foreign schedules and unnamed subgrants not inferred. Count is the number of parsed source rows.',funder=SPONSORS[d['ein']],period_start=d['period_start'],period_end=d['period_end'],object_id=d['object_id'],money_type='source_row_count',unit='rows'))
    write('grant_searches.csv',search)

def published():
    awards=[]
    fn='coefficient-archive.csv'
    for n,r in enumerate(csv.DictReader((S/fn).open()),2):
        code=match(r['Organization Name'])
        if not code:continue
        amt=r['Amount'].replace('$','').replace(',','');dt=datetime.datetime.strptime(r['Date'],'%B %Y').strftime('%Y-%m')
        awards.append(base(f'A-CG-{n}',fn,r['Amount'],'Funder-published award/recommendation record; neither cash payment timing nor paying legal entity established by this archive. Do not add to filed grants.',amt,org_id=code,funder='Coefficient Giving / Open Philanthropy',money_type='published_award',currency='USD',period=dt,source_row=n,grant_title=r['Grant'],purpose=r['Details'],verdict='KEEP'))
    write('awards.csv',awards)
    recs=[]
    for p in sorted(S.glob('sff-20*.html')):
        soup=BeautifulSoup(read(p),'lxml');candidates=[]
        for ti,table in enumerate(soup.find_all('table')):
            rr=table.find_all('tr');headers=[c.get_text(' ',strip=True) for c in rr[0].find_all(['th','td'])]
            oi=next((i for i,h in enumerate(headers) if 'Organization' in h),None)
            ais=[i for i,h in enumerate(headers) if any(t in h for t in ['Amount','Funding','Recommendation'])]
            if oi is None or not ais:
                print('REVIEW SFF HEADERS',p.name,headers);continue
            for j,row in enumerate(rr[1:],1):
                vs=[c.get_text(' ',strip=True) for c in row.find_all(['th','td'])]
                if len(vs)!=len(headers):continue
                code=match(vs[oi])
                if not code:continue
                ri=next((i for i,h in enumerate(headers) if 'Receiving' in h),None)
                si=next((i for i,h in enumerate(headers) if h=='Source'),None)
                for ai in ais:
                    m=re.search(r'\$([\d,]+(?:\.\d+)?)',vs[ai])
                    if not m or float(m[1].replace(',',''))==0:continue
                    recs.append(base(f'S-{p.stem.upper()}-T{ti}-{j}-C{ai}',p.name,m[0],'Published recommendation, not a confirmed cash disbursement. Parenthesized amounts are excluded; source column retained.',m[1].replace(',',''),org_id=code,funder=vs[si] if si is not None else headers[ai],money_type='recommendation',currency='USD',period=p.stem.replace('sff-',''),source_row=j,source_column=headers[ai],recipient_project=vs[oi],receiving_charity=vs[ri] if ri is not None else '',raw_cells=json.dumps(vs),verdict='KEEP'))
        for grid in soup.select('[columns]'):
            n=int(grid['columns']);cells=grid.find_all('div',class_='in-grid',recursive=False)
            if not cells:continue
            headers=[c.get_text(' ',strip=True) for c in cells[:n]]
            orgindex=next((i for i,h in enumerate(headers) if h=='Organization'),None)
            amountindex=next((i for i,h in enumerate(headers) if 'Total Funding' in h),None)
            if amountindex is None:amountindex=next((i for i,h in enumerate(headers) if 'Amount' in h or 'Funding' in h or h=='Recommendation'),None)
            if orgindex is None or amountindex is None:continue
            for j in range(n,len(cells),n):
                cc=cells[j:j+n]
                if len(cc)!=n:continue
                values=[c.get_text(' ',strip=True) for c in cc];code=match(values[orgindex])
                if not code:continue
                m=re.search(r'\$([\d,]+(?:\.\d+)?)',values[amountindex])
                if not m:continue
                sourceidx=next((i for i,h in enumerate(headers) if h=='Source'),None)
                recv=next((i for i,h in enumerate(headers) if 'Receiving' in h),None)
                rid=f'S-{p.stem.upper()}-C{n}-{j//n}'
                matching='Matching Pledge Amount' in headers
                recs.append(base(rid,p.name,m[0],'Published matching pledge, not a paid grant.' if matching else 'Published recommendation only. Main recommendation amount excludes separately parenthesized speculation amounts and matching amounts; those are not additional cash disbursements here.',m[1].replace(',',''),org_id=code,funder=values[sourceidx] if sourceidx is not None else 'See recommendation page',money_type='matching_commitment' if matching else 'recommendation',currency='USD',period=p.stem.replace('sff-',''),source_row=j//n,recipient_project=values[orgindex],receiving_charity=values[recv] if recv is not None else '',raw_cells=json.dumps(values),verdict='KEEP'))
    write('recommendations.csv',recs)
    soup=BeautifulSoup(read(S/'ea-funds-grants.html'),'lxml');data=json.loads(soup.find('script',id='__NEXT_DATA__').string)['props']['pageProps']['grantsList'];ea=[]
    for g in data:
        code=match(g['grantee'])
        if code:
            ea.append(base('EA-'+g['id'],'ea-funds-grants.html',str(g['amount']),'Fund-published grant entry; payment date and legal payer not established in this index. Keep separate from filed cash grants.',g['amount'],org_id=code,funder=g['fund'],money_type='published_grant',currency='USD',period=g['round'],purpose=g['description'],source_record=json.dumps(g),verdict='KEEP'))
    write('ea_funds.csv',ea)

def uk():
    rows=[]
    for year in ['2024','2025']:
        fn='controlai-accounts-'+year+'.xhtml';s=BeautifulSoup(read(S/fn),'xml')
        contexts={c.get('id'):c.find('instant').get_text() for c in s.find_all('context') if c.find('instant')}
        for i,x in enumerate(s.find_all()):
            if x.name.lower()=='nonfraction':
                name=x.get('name','');amount=x.get_text(' ',strip=True)
                if not amount:continue
                if any(k in name for k in ['FixedAssets','CurrentAssets','Prepayments','Creditors','TotalAssetsLess','AccruedLiabilities']):
                    ctx=x.get('contextRef','');signed=num(amount)*(-1 if x.get('sign')=='-' else 1)
                    rows.append(base('UK-'+year+'-'+str(i),fn,amount,'As filed in iXBRL; sign attribute preserved. Comparative amounts retain their own context date. Balance-sheet amount only, not annual revenue or donor funding. No currency conversion.',signed,org_id='CONTROL',money_type='UK_balance_sheet',currency='GBP',period_end=contexts[ctx],filing_year=year,field_name=name,context=ctx,sign=x.get('sign',''),verdict='KEEP'))
    write('uk_accounts.csv',rows)

if __name__=='__main__':
    identities();funding();published();uk()
    print('Evidence register written; audit missing histories, aliases and amounts next.')
