"""Public-source retrieval with cached responses and robots checks. No authentication."""
import csv, hashlib, json, pathlib, re, sys, time
import urllib.request, urllib.error, urllib.parse, urllib.robotparser
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / 'sources'
RAW.mkdir(exist_ok=True)
UA = 'NonprofitFundingAudit/1.0 (public filing research; no authentication)'
DATE = '2026-09-14'
def get(url, name=None):
    key = name or hashlib.sha256(url.encode()).hexdigest()[:24]
    path = RAW / key
    if path.exists(): return path.read_bytes()
    origin = urllib.parse.urlsplit(url)
    roburl = f'{origin.scheme}://{origin.netloc}/robots.txt'
    rpfile = RAW / ('robots-' + origin.netloc.replace(':','_') + '.txt')
    if not rpfile.exists():
        try:
            with urllib.request.urlopen(urllib.request.Request(roburl, headers={'User-Agent':UA}),timeout=40) as r: robots=r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404,410): robots=b'# No robots.txt published (HTTP not found)'
            else: raise RuntimeError(f'Cannot establish robots policy: {roburl}: {e}')
        rpfile.write_bytes(robots)
    rp=urllib.robotparser.RobotFileParser();rp.parse(rpfile.read_text(errors='replace').splitlines())
    if not rp.can_fetch(UA,url): raise RuntimeError('robots disallows '+url)
    time.sleep(0.3)
    if origin.netloc=='lda.gov': time.sleep(5)
    try:
        for attempt in range(6):
            try:
                response=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=40)
                break
            except urllib.error.HTTPError as e:
                if e.code!=429:raise
                delay=max(60,int(e.headers.get('Retry-After','60')))
                print('Rate limit; waiting',delay,'seconds',flush=True)
                for _ in range((delay+9)//10):time.sleep(10)
        else: raise RuntimeError('Rate limit persists: '+url)
        with response as r:
            data=r.read(); meta={'url':url,'resolved_url':r.url,'snapshot_date':DATE,'sha256':hashlib.sha256(data).hexdigest(),'status':r.status}
        path.write_bytes(data); path.with_name(path.name+'.meta.json').write_text(json.dumps(meta,indent=2))
        return data
    except Exception as e:
        path.with_name(path.name+'.error.json').write_text(json.dumps({'url':url,'snapshot_date':DATE,'error':str(e)},indent=2))
        raise

QUERIES = ['Center for AI Safety','AI Policy Institute','Encode Justice','Future of Life Institute','Safe Artificial Intelligence Forum','Institute for AI Policy and Strategy','Horizon Institute for Public Service','Americans for Responsible Innovation','Public Citizen','Federation of American Scientists','Chamber of Progress','Information Technology and Innovation Foundation','TechFreedom','NetChoice']
EINS = ['881751310','932442608','471052538','934950919','320839313','874657441','933248564','990921925','237104508','521263996','237185827','853963084','204403497','273567814','271716101','461008520','205205458','237327907']
def orgs():
    for ein in EINS:
        for ext,url in [('json',f'https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json'),('html',f'https://projects.propublica.org/nonprofits/organizations/{ein}')]:
            try: print(ein,ext,len(get(url,f'org-{ein}.{ext}')),flush=True)
            except Exception as e: print(ein,ext,str(e),flush=True)
    for q in ['Artificial Intelligence Policy','Encode','AI Policy Network']:
        try:
            j=json.loads(get('https://projects.propublica.org/nonprofits/api/v2/search.json?q='+urllib.parse.quote(q),'search-'+re.sub('[^a-z]+','-',q.lower())+'.json'))
            print(q,[(o['ein'],o['name']) for o in j.get('organizations',[])],flush=True)
        except Exception as e: print(q,str(e),flush=True)
def lda():
    terms=['Anthropic','OpenAI','Google','Meta Platforms','Facebook','Microsoft','Amazon','xAI','X.AI']
    for term in terms:
        for year in range(2019,2027):
            url='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'client_name':term,'filing_year':year,'page_size':100})
            page=1
            while url:
                name=f'lda-{re.sub("[^a-z]+","-",term.lower())}-{year}-p{page}.json'
                try:
                    j=json.loads(get(url,name)); print(name,j.get('count'),len(j.get('results',[])),flush=True)
                    url=j.get('next'); page+=1
                except Exception as e: print(name,str(e),flush=True);break
def discover():
    for q in QUERIES:
        try:
            j=json.loads(get('https://projects.propublica.org/nonprofits/api/v2/search.json?q='+urllib.parse.quote(q),'search-'+re.sub('[^a-z]+','-',q.lower())+'.json'))
            print(q,[(o['ein'],o['name'],o.get('subseccd')) for o in j.get('organizations',[])],flush=True)
        except Exception as e: print(q,str(e),flush=True)
    for url,name in [
        ('https://api.github.com/repos/kevinnbass/metr-money-figure/git/trees/master?recursive=1','rematch-tree.json'),
        ('https://lda.senate.gov/api/v1/','lda-api.json'),
        ('https://lda.senate.gov/','lda-home.html'),
        ('https://coefficientgiving.org/grants/','coefficient-index.html'),
        ('https://survivalandflourishing.fund/sff-2024','sff-2024.html')]:
        try: print(name,len(get(url,name)),flush=True)
        except Exception as e: print(name,str(e),flush=True)

if __name__=='__main__':
    if sys.argv[1]=='discover': discover()
    elif sys.argv[1]=='orgs': orgs()
    elif sys.argv[1]=='lda': lda()
    elif sys.argv[1]=='batch':
        jobs=json.loads((ROOT/sys.argv[2]).read_text())
        def work(pair):
            url,name=pair
            try: return name,len(get(url,name))
            except Exception as e: return name,str(e)
        with ThreadPoolExecutor(max_workers=3) as pool:
            for result in pool.map(work,jobs): print(*result,flush=True)
    elif sys.argv[1]=='get':
        for url,name in zip(sys.argv[2::2],sys.argv[3::2]):
            try: print(name,len(get(url,name)),flush=True)
            except Exception as e: print(name,str(e),flush=True)
