from prepare_jobs import *
import re,json
for p in sorted(S.glob('sff-20*.html')):
    s=BeautifulSoup(read(p),'lxml')
    print(p.name,'grids',[(g.get('columns'),g.get('class')) for g in s.select('[columns]')], 'tables',len(s.find_all('table')))
    for x in s.find_all(string=re.compile('Safety|Policy Institute|Horizon|Safe AI Forum|ControlAI|Encode|Public Citizen|Policy and Strategy|Responsible Innovation',re.I)):
        if x.parent.name in ['script','style']:continue
        print(' ',str(x)[:120], 'parent', x.parent.parent.get('class'), 'grandparent',x.parent.parent.parent.get('class'))
s=BeautifulSoup(read(S/'ea-funds-grants.html'),'lxml');data=json.loads(s.find('script',id='__NEXT_DATA__').string)['props']['pageProps']['grantsList']
print('EA candidates',[(x['grantee'],x['amount'],x['round']) for x in data if re.search('safety|horizon|policy|encode|future of life',x['grantee'],re.I)])
