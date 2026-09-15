import json,pathlib,re,gzip
from bs4 import BeautifulSoup
P=pathlib.Path(__file__).resolve().parent
S=P/'sources'
def read(p):
    b=p.read_bytes()
    return (gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b).decode('utf8',errors='replace')
def filings():
    jobs=[]; index=[]
    sponsors={'461008520','205205488','237825575','232888152','510198509','812644663','992255770','810737472','872995455','471052538'}
    for p in sorted(S.glob('org-*.html')):
        ein=p.stem.split('-')[1]
        soup=BeautifulSoup(read(p),'lxml')
        for section in soup.select('section.single-filing-period'):
            year=int(section['id'].replace('filing',''))
            if year<2019 or year>(2025 if ein in sponsors else 2024):continue
            for a in section.select('a[href$="/full"]'):
                obj=a['href'].split('/')[-2]
                form='IRS990PF' if ein=='461008520' else 'IRS990'
                index.append(dict(ein=ein,fiscal_end_year=year,object_id=obj,form=form,source_index=str(p.relative_to(P))))
                jobs.append((f'https://projects.propublica.org/nonprofits/full_text/{obj}/{form}',f'return-{obj}.html'))
                if ein in sponsors and ein!='461008520':
                    jobs.append((f'https://projects.propublica.org/nonprofits/full_text/{obj}/IRS990ScheduleI',f'schedule-{obj}.html'))
    (P/'filing-index.json').write_text(json.dumps(index,indent=2))
    jobs=list(dict.fromkeys(jobs))
    (P/'jobs-filings.json').write_text(json.dumps(jobs,indent=2))
    print('Filing retrieval queue',len(jobs))
if __name__=='__main__':filings()
