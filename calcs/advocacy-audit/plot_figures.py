"""Publication raster and vector figures, using validated CSV calculations only."""
import json,textwrap
from decimal import Decimal,ROUND_HALF_UP
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm,Normalize
from matplotlib.ticker import FuncFormatter,MaxNLocator
from audit_core import P,read

ORDER=['CAIS','CAISAF','AIPI','AIPN','ENCODE','ENCODER','FLI','CONTROL','SAIF','IAPS','HORIZON','ARI','CRI','PC','PCF','FAS','PROGRESS','ITIF','TECHFREEDOM','NETCHOICE']
LABELS={'CAIS':'Center for AI Safety','CAISAF':'CAIS Action Fund','AIPI':'AI Policy Institute','AIPN':'AI Policy Network','ENCODE':'Encode AI','ENCODER':'Encode Research','FLI':'Future of Life Institute','CONTROL':'ControlAI (UK)','SAIF':'Safe AI Forum','IAPS':'IAPS','HORIZON':'Horizon Institute','ARI':'Americans for Responsible Innovation','CRI':'Center for Responsible Innovation','PC':'Public Citizen','PCF':'Public Citizen Foundation','FAS':'Federation of American Scientists','PROGRESS':'Chamber of Progress','ITIF':'ITIF','TECHFREEDOM':'TechFreedom','NETCHOICE':'NetChoice'}
SHORT=dict(LABELS,ARI='Americans for Responsible Innovation',CRI='Center for Responsible Innovation',FAS='Federation of American Scientists')
BG='#fbfaf7';INK='#172d39';TEAL='#087e8b';BLUE='#315bb4';MUTED='#52636b';GRID='#e0e5e5'
def dollars(v):
    if abs(v)>=1e6:return f'${(Decimal(str(v))/1000000).quantize(Decimal(".01"),rounding=ROUND_HALF_UP):,}m'
    if abs(v)>=1e3:return f'${(Decimal(str(v))/1000).quantize(Decimal(".1"),rounding=ROUND_HALF_UP):,}k'
    return f'${v:,.0f}'
def setup():
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'figure.facecolor':BG,'axes.facecolor':BG,'text.color':INK,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'svg.fonttype':'none','savefig.facecolor':BG})
def title(fig,heading,sub):
    fig.text(.04,.945,heading,size=23,weight='bold',va='top')
    fig.text(.04,.888,sub,size=11,color=MUTED,va='top')
def footer(fig,lines):
    fig.text(.04,.115,'\n'.join(lines),fontsize=8.1,color=MUTED,va='top',linespacing=1.4)
    fig.text(.96,.025,'noprofits.org  •  Public filing audit',fontsize=8.2,color=MUTED,ha='right')
def save(fig,name):
    folder=P/'figures';folder.mkdir(exist_ok=True)
    fig.savefig(folder/(name+'.png'),dpi=100)
    fig.savefig(folder/(name+'.svg'))
    plt.close(fig)
def build():
    setup();a={r['row_id']:r for r in read('aggregates.csv')};entities={r['org_id']:r for r in read('entities.csv')}
    years=list(range(2019,2025));fig=plt.figure(figsize=(12,6.3))
    title(fig,'Revenue across the safety/regulation group','Organization-wide revenue, fiscal years ending 2019–2024 [M-START; M-REV-END]. USD millions; each panel has its own scale.')
    panels=[('Center for AI Safety',['CAIS','CAISAF']),('AI Policy Institute / Network',['AIPI','AIPN']),('Encode',['ENCODE','ENCODER']),('Future of Life Institute',['FLI']),('ControlAI (UK)',['CONTROL']),('Safe AI Forum',['SAIF']),('IAPS',['IAPS']),('Horizon Institute',['HORIZON']),('Responsible Innovation',['ARI','CRI'])]
    for i,(label,codes) in enumerate(panels):
        col=i%3;row=i//3;ax=fig.add_axes([.075+col*.32,.665-row*.237,.263,.142])
        ax.set_title(label,fontsize=11,loc='left',weight='bold',pad=6)
        anydata=False
        for j,code in enumerate(codes):
            vals=[float(a[f'RV-{code}-{y}']['amount'])/1e6 if f'RV-{code}-{y}' in a else np.nan for y in years]
            if not np.all(np.isnan(vals)):
                anydata=True;ax.plot(years,vals,marker='o',ms=3,lw=1.8,color=[TEAL,BLUE][j],label=code)
        ax.set_xlim(2018.7,2024.3);ax.set_xticks([2019,2022,2024]);ax.tick_params(axis='both',labelsize=8,length=0,pad=3)
        if anydata:
            lo,hi=ax.get_ylim();ax.set_ylim(min(0,lo),hi);ax.yaxis.set_major_locator(MaxNLocator(3));ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x:g}'))
            ax.axhline(0,lw=.6,color='#7e8c90');ax.grid(axis='y',color=GRID,lw=.6);ax.set_axisbelow(True)
            if codes==['FLI']:ax.set_ylim(-120,600);ax.set_yticks([-100,0,250,500])
            if len(codes)>1:ax.legend(loc='upper left',fontsize=7.5,frameon=False,ncol=2,bbox_to_anchor=(0,1.01),handlelength=1.1,borderaxespad=0)
        else:
            ax.set_yticks([]);ax.text(.5,.5,'OPEN: no standalone revenue\nin the captured primary filings',ha='center',va='center',transform=ax.transAxes,fontsize=9,color=MUTED)
        ax.text(1,-.25,' / '.join(codes),ha='right',va='top',transform=ax.transAxes,fontsize=7,color=MUTED)
    footer(fig,[
      'Missing periods are gaps, not zero. FLI’s negative year and spike are retained. Revenue includes investment results; it is not a messaging budget.',
      'Point IDs: RV-{org code}-{year}; missing-period IDs: H-{org code}-{year}. Evidence: research/aggregates.csv and history_coverage.csv.',
      'Sources: primary IRS returns via Nonprofit Explorer; UK filed accounts. Snapshot: 2026-09-14 [M-SNAPSHOT].'])
    save(fig,'01-safety-revenue')

    fig=plt.figure(figsize=(12,6.3))
    title(fig,'Which institutions filed grants to these organizations?','Cash grants in the searched schedules, fiscal years ending 2019–2025 [M-START; M-GRANT-END]. Coverage varies by payer.')
    fcodes=[];fnames={}
    for r in a.values():
        if r['row_id'].startswith('MX-'):fnames[r['funder_code']]=r['funder']
    fcodes=[k for k in ['GV','CA','FL','HORIZON','NETCHOICE','PCF','PC','CRI','SV','NP','VG','TI'] if k in fnames]
    assert set(fcodes)==set(fnames),('New matrix payer needs label',set(fnames)-set(fcodes))
    data=np.array([[float(a[f'MX-{org}-{f}']['amount']) if f'MX-{org}-{f}' in a else np.nan for f in fcodes] for org in ORDER])
    ax=fig.add_axes([.265,.25,.69,.57]);cmap=plt.get_cmap('YlGnBu').copy();cmap.set_bad('#eceeeb')
    image=ax.imshow(data,aspect='auto',cmap=cmap,norm=LogNorm(vmin=np.nanmin(data),vmax=np.nanmax(data)))
    ax.set_yticks(range(len(ORDER)),[LABELS[o] for o in ORDER],fontsize=8.7)
    aliases={'GV':'Good\nVentures','CA':'Coefficient\nAction','FL':'Future\nof Life','SV':'SVCF','NP':'NPT','VG':'Vanguard','TI':'Tides','HORIZON':'Horizon','NETCHOICE':'NetChoice','PCF':'Public Citizen\nFoundation','CRI':'Responsible\nInnovation'}
    ax.set_xticks(range(len(fcodes)),[aliases.get(f,f) for f in fcodes],fontsize=8.5)
    ax.tick_params(length=0,pad=7)
    for i in range(len(ORDER)):
        for j in range(len(fcodes)):
            if not np.isnan(data[i,j]):
                v=data[i,j];lab=dollars(v)
                ax.text(j,i,lab,ha='center',va='center',fontsize=7.6,color='white' if image.norm(v)>.58 else INK)
    footer(fig,[
      'Blank cells mean no matched amount in the searched schedules, not zero funding. Color uses a logarithmic scale; dollar labels are rounded.',
      'SVCF, NPT, Vanguard and Tides are DAF sponsors; these rows do not identify donor advisers. No awards or recommendations are added.',
      'Cell IDs: MX-{org code}-{payer code}; keys and source periods: figure_index.csv. Snapshot: 2026-09-14 [M-SNAPSHOT].'])
    save(fig,'02-funder-matrix')

    fig=plt.figure(figsize=(12,6.3))
    title(fig,'Federal lobbying: company expenses and outside fees','All issues combined, USD millions. These overlapping measures must not be added. Latest year is partial [M-LDA-END; M-LDA-QUARTER].')
    labs=['Anthropic','OpenAI','Google','Meta','xAI','Microsoft','Amazon'];yrs=list(range(2019,2027))
    for x,prefix,label,cmapname in [(.12,'EX','Companies’ own expense reports','Blues'),(.585,'FE','Outside firms’ direct-client fee reports','Greens')]:
        ax=fig.add_axes([x,.29,.375,.48]);data=np.array([[float(a[f'{prefix}-{lab}-{y}']['amount'])/1e6 if a[f'{prefix}-{lab}-{y}']['amount'] else np.nan for y in yrs] for lab in labs])
        cmap=plt.get_cmap(cmapname).copy();cmap.set_bad('#eceeeb');norm=Normalize(0,np.nanmax(data));im=ax.imshow(data,aspect='auto',cmap=cmap,norm=norm)
        ax.set_title(label,fontsize=12,loc='left',weight='bold',pad=14)
        ax.set_xticks(range(len(yrs)),[str(y) if y!=2026 else '2026\nH1' for y in yrs],fontsize=9)
        ax.set_yticks(range(len(labs)),labs,fontsize=10);ax.tick_params(length=0,pad=7)
        for i in range(len(labs)):
            for j in range(len(yrs)):
                v=data[i,j];ax.text(j,i,'OPEN' if np.isnan(v) else str(Decimal(str(v)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)),ha='center',va='center',fontsize=8.3,color=MUTED if np.isnan(v) else ('white' if norm(v)>.57 else INK))
        ax.text(0,-.2,'Darker = larger within this panel; scales differ.',transform=ax.transAxes,fontsize=8,color=MUTED)
    footer(fig,[
      'Numeric amounts on latest quarterly reports only; blank amounts are not zero. No AI-only dollar allocation. Explicit intermediary-client fees are separate.',
      'Cell IDs: EX-{lab}-{year} and FE-{lab}-{year}. Public LDA API accessed 2026-09-14 [M-SNAPSHOT; D-LDA-TOS].',
      '“Senate Office of Public Records cannot vouch for the data or analyses derived from these data after the data have been retrieved from LDA.gov.”'])
    save(fig,'03-lab-lobbying')

    fig=plt.figure(figsize=(12,6.3))
    title(fig,'DAF-sponsor share of the cash grants identified here','A share of the searched grant pool, not of total organizational funding. Fiscal years ending 2019–2025; uneven coverage [M-START; M-GRANT-END].')
    ax=fig.add_axes([.285,.225,.445,.595]);ax.set_xlim(0,114);ax.set_ylim(len(ORDER)-.5,-.5)
    ax.set_yticks(range(len(ORDER)),[LABELS[o] for o in ORDER],fontsize=9)
    ax.set_xticks([0,25,50,75,100],['0%','25%','50%','75%','100%']);ax.tick_params(length=0,pad=6,labelsize=9);ax.grid(axis='x',color=GRID,lw=.7);ax.set_axisbelow(True)
    for i,org in enumerate(ORDER):
        r=a['DP-'+org]
        if r['amount']!='':
            v=float(r['amount']);ax.barh(i,v,color=TEAL,height=.67);ax.text(v+1.3,i,f'{v:.1f}%',va='center',fontsize=8.5)
        else:ax.text(1,i,'OPEN — no identified cash-grant pool',va='center',fontsize=8.5,color=MUTED)
    ax2=fig.add_axes([.765,.225,.20,.595]);ax2.set_xlim(0,1);ax2.set_ylim(len(ORDER)-.5,-.5);ax2.axis('off')
    ax2.text(.16,-1.1,'Sponsor cash',ha='center',fontsize=9,weight='bold');ax2.text(.77,-1.1,'Direct cash',ha='center',fontsize=9,weight='bold')
    for i,org in enumerate(ORDER):
        for x,prefix in [(.16,'DN'),(.77,'DD')]:
            v=a[prefix+'-'+org]['amount'];ax2.text(x,i,'—' if v=='' else dollars(float(v)),ha='center',va='center',fontsize=8.7,color=MUTED)
    footer(fig,[
      'Sponsor cash and direct cash remain separate subtotals. The percentage uses only those identified cash grants; donor and revenue totals are not inferred.',
      'A sponsor’s name does not establish the fund type or donor adviser for each grant. Confirmed DAF shares of total funding remain OPEN.',
      'Row IDs: DP-{org code}, DN-{org code}, DD-{org code}. Source-period register: coverage.csv. Snapshot: 2026-09-14 [M-SNAPSHOT].'])
    save(fig,'04-daf-sponsor-share')

    return fnames
if __name__=='__main__':build()
