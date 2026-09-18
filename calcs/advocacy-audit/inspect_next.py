from prepare_jobs import *
from parse_filings import fields,val
import json,re
for fn in ['coefficient-advisors-2024.html','coefficient-action-2024.html','coefficient-research-2024.html']:
    f=fields(S/fn); print(fn,val(f,'Filer[1]/EIN[1]'),val(f,'Filer[1]/BusinessName[1]/BusinessNameLine1Txt[1]'))
for fn in ['lda-tos.html','coefficient-action-schedule-2024.html','coefficient-advisors-schedule-2024.html']:
    print(fn,BeautifulSoup(read(S/fn),'lxml').get_text(' ',strip=True)[-7000:])
for fn in ['progress-partners.html','netchoice-about.html','techfreedom-about.html']:
    s=BeautifulSoup(read(S/fn),'lxml');t=s.get_text(' ',strip=True)
    print(fn, '\n'.join(t[max(0,m.start()-150):m.end()+350] for m in re.finditer('Amazon|Google|Meta|Microsoft|fund|donor|support|members',t,re.I))[:4000])
print('IAPS',BeautifulSoup(read(S/'iaps-about.html'),'lxml').get_text(' ',strip=True)[-5000:])
