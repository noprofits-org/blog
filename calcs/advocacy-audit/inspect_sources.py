import sys,re,json,csv
from prepare_jobs import *
for fn in ['itif-about.html','horizon-home.html','techfreedom-about.html','ari-about.html','coefficient-governance.html','controlai-filings.html','encode-home.html']:
    s=BeautifulSoup(read(S/fn),'lxml')
    print(fn,[(a.get_text(' ',strip=True)[:65],a.get('href')) for a in s.select('a[href]') if any(t in a.get('href','').lower() for t in ['fund','support','990','financial','document'])])
print('REGISTRY',BeautifulSoup(read(S/'controlai-registry.html'),'lxml').get_text(' ',strip=True)[2500:5000])
for fn in ['fli-funding.html','ari-about.html','horizon-home.html','itif-about.html']:
    s=BeautifulSoup(read(S/fn),'lxml');t=s.get_text(' ',strip=True)
    print(fn, '\n'.join(t[max(0,m.start()-90):m.end()+400] for m in re.finditer('funded|funders|donors|funding|supporters|501',t,re.I))[:3500])
