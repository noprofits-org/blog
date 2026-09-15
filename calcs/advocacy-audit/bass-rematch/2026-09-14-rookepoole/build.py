"""Deterministic CSV/rematch handoff from frozen claims and cached primary HTML."""
import csv, hashlib, json, pathlib, re
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent
S = ROOT / 'sources'
AUDIT = ROOT.parents[1]
THREAD = 'https://x.com/rookepoole/status/2099660837388501127'
DATE = '2026-09-14'

def write_csv(name, rows, fields=None):
    with (ROOT/name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields or list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

def read_csv(path):
    return list(csv.DictReader(path.open()))

def meta(name):
    return json.loads((S/(name+'.meta.json')).read_text())

def soup(name):
    return BeautifulSoup((S/name).read_bytes(), 'lxml')

def slug(name):
    return re.sub('[^a-z0-9]+','-',name.lower()).strip('-')

NGOS = [
 ('METR','Model Evaluation and Threat Research',2120000,'METR'),
 ('MIRI','Machine Intelligence Research Institute',2800000,'MIRI'),
 ('Center for AI Safety (CAIS)','Center for AI Safety',650000,'CAIS'),
 ('CAIS Action Fund','Center for AI Safety Action Fund',2620000,'CAISAF'),
 ('AI Futures Project','AI Futures Project',2080000,'AIFP'),
 ('AI Policy Institute (AIPI)','AI Policy Institute',2430000,'AIPI'),
 ('Palisade Research','Palisade Research',None,'PALISADE'),
 ('Encode AI','Encode AI Corporation',526000,'ENCODE'),
 ('Institute for AI Policy and Strategy (IAPS)','Institute for AI Policy and Strategy',None,'IAPS'),
 ('Centre for the Governance of AI (GovAI)','Centre for the Governance of AI',None,'GOVAI'),
 ('Center for Humane Technology (CHT)','Center for Humane Technology',None,'CHT'),
 ('Civic AI Security Program (CivAI)','Civic AI Security Program',None,'CIVAI'),
 ('PauseAI US','PauseAI US',None,'PAUSEUS'),
 ('PauseAI Global','PauseAI Global',None,'PAUSEGLOBAL'),
 ('80,000 Hours','80,000 Hours',None,'80K'),
 ('Common Sense Media','Common Sense Media',None,'CSM'),
 ('Economic Security Project','Economic Security Project',None,'ESP'),
 ('Blueprint for Free Speech','Blueprint for Free Speech',None,'BFFS'),
 ("Young People's Alliance Education Fund","Young People's Alliance Education Fund",None,'YPA'),
 ('AI Objectives Institute','AI Objectives Institute',None,'AOI'),
 ('Evitable','Evitable',None,'EVITABLE'),
 ('Bureau of Investigative Journalism','Bureau of Investigative Journalism',None,'BIJ'),
 ('Alignment Research Center (ARC)','Alignment Research Center',None,'ARC'),
 ('Redwood Research','Redwood Research',None,'REDWOOD'),
 ('Constellation','Constellation',None,'CONSTELLATION'),
 ('Longview Philanthropy','Longview Philanthropy',None,'LONGVIEW'),
 ('RAND','RAND Corporation',None,'RAND'),
 ('Canary (Audacious)','Canary project',None,'CANARY'),
]
nodes=[]
def node(name, normalized=None, category='ngo', source='poole_graphic', amount=None, notes=''):
    if source=='poole_graphic':
        notes='User transcription only; original graphic unavailable; OCR and exact label unverified. '+notes
    nodes.append(dict(name=name,normalized_name=normalized or name,category=category,source=source,graphic_amount_usd_claimed=amount if amount is not None else '',notes=notes))

for name, normalized, amount, code in NGOS:
    source='bass_pack' if code=='ARC' else 'poole_graphic'
    notes='Approximate claimed amount; grantor, date and money type absent from transcription. ' if amount else ''
    if code=='PALISADE': notes='Two distinct graphic claims: approximately $467,000 and $1,150,000; no combined amount entered. '
    if code=='ENCODE': notes+='Possible OCR Encide AI. Official cached privacy page names Encode AI Corporation; Encode Justice label and March On Foundation in SFF 2024 retained separately in evidence. '
    if code=='CONSTELLATION': notes+='Ambiguous label; legal entity unresolved. '
    if code in ['RAND','CANARY']: notes+='Conditional lead in brief; RAND recipient and Canary/Audacious project/initiative are not interchangeable. '
    node(name,normalized,source=source,amount=amount,notes=notes)
for name in ['Future of Life Institute','Survival and Flourishing Fund']:
    node(name,category='funder',notes='SFF is a recommendation platform; legal paying vehicle must be established per edge.' if 'Survival' in name else '')
for name in ['Jaan Tallinn','Vitalik Buterin','Elon Musk']:
    node(name,category='person',notes='Funding, investment and governance claims require separate evidence.')
for name in ['Good Ventures Foundation','Coefficient Giving','National Philanthropic Trust','Silicon Valley Community Foundation','Players Philanthropy Fund','Vanguard Charitable']:
    node(name,category='funder',source='prior',notes='Prior Bass/Tarbell orbit; no new money attributed. '+('EIN 46-1008520 supplied in brief.' if name=='Good Ventures Foundation' else ''))
node('Tarbell Center','Tarbell Center for AI Journalism',source='prior',notes='Prior TB01–TB06/F1–F3 retained; no repeat rematch or new total here.')
node('Anthropic',category='lab',source='prior',notes='Investor and stake leads only; no payroll attribution from grants.')
for name in ['Facing the Frontier','FLI Digital Media Accelerator','Protect What\'s Human']:
    node(name,category='media',source='poole_thread',notes='User-supplied amplification/program lead; original thread unavailable; standalone legal entity not established.')
for name in ['UK ASI Security Bill','US superintelligence-ban effort','UK AI kill-switch amendment']:
    node(name,category='policy',source='poole_thread',notes='Policy output only; no NGO/grant row without spending evidence and, if relevant, Schedule C.')
for name in ['Ashgro','Epistea, z.s.','The Hack Foundation','March On Foundation']:
    node(name,category='other',source='prior',notes='Sponsor/receiving-entity lead. Preserve exact period-specific receiving-charity label; do not assign sponsor-wide funding to a program.')

edges=[]; verdicts=[]
def edge(rid, grantor, grantee, amount, period, kind, source, sentence):
    edges.append(dict(grantor=grantor,grantee=grantee,amount_usd_claimed='' if amount is None else amount,date_or_year=period,money_type=kind,claim_source_url=source,freeze_sentence=sentence,row_id=rid))

for name, norm, amount, code in NGOS:
    if code=='PALISADE': amounts=[467000,1150000]
    else: amounts=[amount]
    for index, value in enumerate(amounts,1):
        rid=f'PG-{code}-{index}'
        sentence=(f'The user-supplied transcription of the Poole graphic dated 14 September 2026 attributes approximately ${value:,} to {name}' if value is not None else f'The user-supplied transcription lists {name} as a funding-network lead')+'; grantor, grant date, filing year and money type are unspecified.'
        edge(rid,'',norm,value,'','unknown',THREAD,sentence)
        verdicts.append(dict(row_id=rid,verdict='OPEN',reason='Original graphic unavailable and transaction dimensions unspecified; a different scoped primary row cannot confirm or contradict this claim.',source_url=THREAD,source_file='sources/poole-thread.html.error.json'))
edge('PG-MUSK-FLI','Elon Musk','Future of Life Institute',10000000,'2015','unknown',THREAD,'The supplied lead claims Elon Musk gave FLI $10,000,000 in 2015; legal payer and disbursement timing are unspecified.')
verdicts.append(dict(row_id='PG-MUSK-FLI',verdict='OPEN',reason='FLI confirms an announced donation; receipt date and legal payer remain unresolved for the cash-gift interpretation.',source_url=meta('fli-2015-review.html')['url'],source_file='sources/fli-2015-review.html'))
for person in ['Vitalik Buterin','Jaan Tallinn']:
    for grantee in ['Future of Life Institute','Survival and Flourishing Fund']:
        edge('PG-'+slug(person+'-'+grantee).upper(),person,grantee,None,'','unknown',THREAD,f'The supplied lead proposes a {person} funding relationship with {grantee}; amount, year and legal paying/receiving entity remain unspecified.')

aliases={
 'METR':['Model Evaluation and Threat Research','Model Evaluation & Threat Research (METR)'],
 'MIRI':['Machine Intelligence Research Institute','Machine Intelligence Research Institute (MIRI)'],
 'CAIS':['Center for AI Safety, Inc.','Center for AI Safety (CAIS)'],
 'CAISAF':['Center for AI Safety Action Fund, Inc.','Center for AI Safety Action Fund (CAIS AF)'],
 'AIFP':['AI Futures Project'], 'AIPI':['The AI Policy Institute','AI Policy Institute (AIPI)'],
 'PALISADE':['Palisade Research'], 'ENCODE':['Encode Justice','Encode AI Corporation'],
}
evidence=[]
for year in [2024,2025]:
    fn=f'sff-{year}.html'; document=soup(fn)
    pledge_terms={}
    for grid in document.select('[columns]'):
        n=int(grid['columns']); cells=grid.find_all('div',class_='in-grid',recursive=False)
        headers=[c.get_text(' ',strip=True) for c in cells[:n]]
        if 'Matching Pledge Deadline' not in headers: continue
        for ri in range(1,len(cells)//n):
            terms=dict(zip(headers,[c.get_text(' ',strip=True) for c in cells[ri*n:(ri+1)*n]]))
            pledge_terms[terms['Organization']]=terms
    for gi,grid in enumerate(document.select('[columns]')):
        n=int(grid['columns']); cells=grid.find_all('div',class_='in-grid',recursive=False)
        headers=[c.get_text(' ',strip=True) for c in cells[:n]]
        if 'Total Funding Rec.' not in headers: continue # pledge table repeats a subset
        for ri in range(1,len(cells)//n):
            values=[c.get_text(' ',strip=True) for c in cells[ri*n:(ri+1)*n]]
            fields=dict(zip(headers,values)); org=fields['Organization']
            code=next((k for k,v in aliases.items() if org in v),None)
            if not code: continue
            raw=fields['Total Funding Rec.']; total=int(re.search(r'\$([\d,]+)',raw)[1].replace(',',''))
            match=re.search(r'Matching:\s*\{\$([\d,]+)\}',raw)
            pledge=int(match[1].replace(',','')) if match else 0
            # The page says matching pledges are inside the total. Never add them again.
            parts=[('recommendation',total-pledge)] + ([('commitment',pledge)] if pledge else [])
            for kind, amount in parts:
                rid=f'SFF-{year}-G{gi}-R{ri}-'+('MATCH' if kind=='commitment' else 'REC')
                scope='conditional matching pledge included in the total recommendation' if kind=='commitment' else ('non-matching portion of the published recommendation, derived as total minus included matching pledge' if pledge else 'published funding recommendation')
                sentence=f'SFF’s {year} round lists Jaan Tallinn as source of a ${amount:,} {scope} for {org}, with receiving charity {fields["Receiving Charity"]}; this does not establish a cash payment or filing year.'
                edge(rid,'Jaan Tallinn (SFF recommendation)',org,amount,str(year),kind,meta(fn)['url'],sentence)
                evidence.append(dict(row_id=rid,org_code=code,amount_usd=amount,money_type=kind,year=year,grantor=fields['Source'],project_name=org,receiving_charity=fields['Receiving Charity'],source_url=meta(fn)['url'],source_file='sources/'+fn,source_locator=f'grid {gi}; data row {ri}; Total Funding Rec.',snapshot_date=meta(fn)['snapshot_date'],published_total_usd=total,included_matching_pledge_usd=pledge,raw_amount_cell=raw,raw_cells_json=json.dumps(fields),derivation=f'{total} - {pledge}' if kind=='recommendation' and pledge else 'Exact source amount',freeze_sentence=sentence))
                terms=pledge_terms.get(org,{}) if kind=='commitment' else {}
                evidence[-1].update(matching_rate=terms.get('Matching Rate',''),matching_deadline=terms.get('Matching Pledge Deadline',''))
                if kind=='commitment':
                    assert int(re.search(r'\$([\d,]+)',terms['Matching Pledge Amount'])[1].replace(',',''))==amount
                verdicts.append(dict(row_id=rid,verdict='KEEP',reason='Primary table confirms this bounded recommendation/conditional pledge; no paid grant inferred.',source_url=meta(fn)['url'],source_file='sources/'+fn))

# Preserve author row IDs for overlap; this is a claim index, not new primary evidence.
overlaps=[]
for path in sorted(S.glob('bass-*.csv')):
    for lineno,row in enumerate(read_csv(path),2):
        if 'row_id' not in row: continue
        if re.search(r'METR|Model Evaluation|Tarbell|Survival and Flourishing|Machine Intelligence|Palisade|Center for AI Safety|Encode|AI Policy Institute',json.dumps(row),re.I):
            overlaps.append(dict(bass_row_id=row['row_id'],bass_file=path.name,source_csv_line=lineno,original_row_json=json.dumps(row),status='Claim-pack cross-reference only; primary rematch required unless explicitly linked in a rematch note.'))

(ROOT/'rematch').mkdir(exist_ok=True)
for name,norm,amount,code in NGOS[:8]:
    claims=[r for r in edges if r['row_id'].startswith('PG-'+code+'-')]
    found=[r for r in evidence if r['org_code']==code]
    lines=[f'# {name}', '',f'Audit date: {DATE}. Status: first bounded SFF edges finished; graphic claim OPEN.', '', '## Frozen graphic claim', '']
    lines += [f'- **{r["row_id"]}** — {r["freeze_sentence"]}' for r in claims]
    lines += ['', '## Verdicts', '', '| Row | Verdict | Reason | Source |','| --- | --- | --- | --- |']
    for r in claims:
        lines.append(f'| {r["row_id"]} | OPEN | Grantor, period and money type missing; original image unavailable. | [Thread]({THREAD}); `sources/poole-thread.html.error.json` |')
    for r in found:
        lines.append(f'| {r["row_id"]} | KEEP | ${r["amount_usd"]:,} {r["money_type"]}, {r["year"]}; receiving entity **{r["receiving_charity"]}**. | [Primary page]({r["source_url"]}); `{r["source_file"]}`; {r["source_locator"]} |')
    lines+=['', '## Frozen primary claims', '']+[f'- **{r["row_id"]}** — {r["freeze_sentence"]}' for r in found]
    lines+=['','## Scope and gaps','','Searched the SFF 2024 and 2025 main recommendation tables captured 2026-09-14, using the exact project aliases recorded in build.py. Amounts in parentheses are speculation annotations, not additional awards. Matching pledges are included in the published total: the non-matching component and pledge are separated in evidence_rows.csv. The separate pledge table repeats the same pledge and is not another edge. No all-time total or payment total is calculated.','', 'The graphic amount remains OPEN: a differently scoped primary amount is not enough for KILL. Obtain the original arrow, legend, date range and fiscal-sponsor labels; then check FLI grant schedules and the relevant SFF rounds. Full funding history and legal identity audit are unfinished.']
    if code=='METR':
        text=soup('metr-about.html').get_text(' ',strip=True)
        assert 'Survival and Flourishing Fund' in text
        lines += ['', '## Bass / Tarbell overlap', '', 'Bass **M38** is the same SFF 2024 $204,000 recommendation rematched above. **M39** splits 2025 into $120,000 and a $428,000 matching pledge, also rematched above. Reuse these row IDs when joining to Bass; do not add the Bass rows again. M35–M37 concern ARC/ARC Evals and are not automatically METR receipts. M52/M53/M55 are Tallinn-ledger claims: primary retrieval was robots-disallowed, so they remain unrematched here.', '', '[METR About](https://metr.org/about), cached as `sources/metr-about.html`, confirms the SFF recommendation relationship but provides no matching dollar total. No payroll or donor-to-lab attribution follows. Prior F2 remains bounded to its original Coefficient/GVF corpus and cutoff; F3 remains OPEN.']
    if code=='ENCODE':
        lines+=['','## Name check','','The official [privacy notice](https://encodeai.org/privacy-policy/), cached as `sources/encode-privacy.html`, names Encode AI Corporation. The 2024 recommendation instead names Encode Justice and March On Foundation as receiving charity. The 2025 row names Encode AI Corporation as recipient. These are period-specific records; this audit does not establish legal succession or merge the sponsors.']
    (ROOT/'rematch'/f'{slug(norm)}.md').write_text('\n'.join(lines)+'\n')

fli_text=soup('fli-funding.html').get_text(' ',strip=True)
assert '2021' in fli_text and 'Vitalik Buterin' in fli_text and 'no formal or informal role' in fli_text
(ROOT/'rematch/future-of-life-institute.md').write_text('''# Future of Life Institute

Audit date: 2026-09-14. Hub claims only; outgoing NGO grant schedules remain queued.

| Frozen sentence | Verdict | Reason and primary source |
| --- | --- | --- |
| In 2015, FLI reported Musk’s announcement of a $10,000,000 donation to establish its AI safety research grants program. | KEEP | Confirms the announcement/commitment, not a dated bank receipt or legal payer. [2015 review](https://futureoflife.org/newsletter/2015-a-year-in-review/), `sources/fli-2015-review.html`. |
| PG-MUSK-FLI: Musk paid FLI $10,000,000 in 2015. | OPEN | Cash timing/legal payer not resolved by the announcement; obtain the relevant primary grant schedule or receipt disclosure. Same source. |
| FLI’s finances page says Vitalik Buterin made an unconditional contribution in 2021. | KEEP | Amount is undisclosed in this page. [Finances](https://futureoflife.org/about-us/finances/), `sources/fli-funding.html`. |
| As of the cached 2026-09-14 finances page, Buterin has a formal or informal decision-making role at FLI. | KILL | The organization expressly states he has no such role. This is a narrowly dated self-disclosure verdict, not a conclusion about every historical period. Same source. |
| The supplied graphic lead’s unspecified Buterin board claim is established. | OPEN | Original graphic, wording and date unavailable; the current-role finding cannot settle an unspecified historical claim. Same source and thread retrieval error. |
| FLI’s finances page says Tallinn has served on its board since founding. | KEEP | Attributed organizational disclosure; no gift amount inferred. Same source. |

No dollar value was assigned to the Buterin gift. No FLI-to-METR absence claim is made from these pages. Next: inspect funder-side Schedule I/foreign-grant detail for each exact grantee and fiscal sponsor, preserving year and legal recipient.
''')
edge('FLI-MUSK-ANNOUNCEMENT','Elon Musk','Future of Life Institute',10000000,'2015','commitment',meta('fli-2015-review.html')['url'],'In its 2015 review, FLI reported Musk’s announcement of a $10,000,000 donation for an AI safety research grant program; payment timing and legal payer are not established here.')
assert 'Musk announced a donation of $10 million to FLI' in soup('fli-2015-review.html').get_text(' ',strip=True)
verdicts.append(dict(row_id='FLI-MUSK-ANNOUNCEMENT',verdict='KEEP',reason='FLI annual review confirms the announcement; no cash timing or legal payer inferred.',source_url=meta('fli-2015-review.html')['url'],source_file='sources/fli-2015-review.html'))
for row in edges:
    if row['row_id'] not in {v['row_id'] for v in verdicts}:
        verdicts.append(dict(row_id=row['row_id'],verdict='OPEN',reason='Lead has no frozen amount or period; dated primary disclosure findings are separately scoped in the FLI hub note.',source_url=row['claim_source_url'],source_file='sources/poole-thread.html.error.json'))

write_csv('nodes.csv',nodes)
write_csv('edges_claims.csv',edges)
write_csv('evidence_rows.csv',evidence)
write_csv('verdicts.csv',verdicts)
write_csv('bass_overlap.csv',overlaps)

remaining='\n'.join(f'{i}. {name} — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.' for i,(name,_,_,_) in enumerate(NGOS[8:],9))
errors=[]
for path in S.glob('*.error.json'):
    error=json.loads(path.read_text());errors.append(f'- {error["url"]}: {error["error"]}. Record: `sources/{path.name}`.')
(ROOT/'QUEUE.md').write_text(f'''# Queue

Audit folder date: {DATE}, the local session date. The supplied Tarbell post is dated 2026-09-15; its findings are carried forward, not re-dated.

## Completed this pass

- All {len(nodes)} nodes from the supplied list and supporting leads registered. Original image completeness/OCR remains unverified.
- Top eight NGO entries: frozen graphic claims and exact SFF 2024/2025 edges with primary table locators. Graphic amounts remain OPEN.
- FLI hub note: Musk announcement, Buterin gift/current-role disclosure, Tallinn board disclosure.
- Bass M38/M39 linked to the same METR SFF evidence; prior Tarbell findings preserved.

## Next work in order

1. METR: next exact claim is Bass M55, Tallinn’s ledger records $184,000 on 2024-12-06 via FP-US to Model Evaluation and Threat Research. Primary ledger access is blocked; do not promote the Bass copy to a receipt. Check funder-side filing routes and legal recipient, then resolve the graphic’s ~$2.12M period and grantor.
2. MIRI: rematch a funder-side filing/ledger edge; exclude AI Impacts/Eisenstat program earmarks received through MIRI or Ashgro from MIRI general support.
3. CAIS: resolve the ~$650k graphic arrow, date and funder; reuse existing audit CAIS rows only after matching their primary locator.
4. CAIS Action Fund: keep it distinct from CAIS; same next-step requirements for ~$2.62M.
5. AI Futures Project: preserve Epistea as the 2024 receiving charity and the 2025 program label; matching pledge is not payment.
6. AIPI: preserve Hack Foundation receiving-charity labels; investigate ~$2.43M without adding sponsor revenue.
7. Palisade: separately freeze the ~$467k and ~$1.15M arrows; do not sum them before identifying scope/type.
8. Encode: compare original image spelling with official notice and distinguish 2024 Encode Justice/March On from the 2025 Encode AI Corporation row.

{remaining}

## Hub and publication scope

Prior F1 KEEP: Coefficient→Tarbell TB02–TB04 $5,291,930. TB01 is a separate joint Training for Good award. F2 KEEP bounded: no direct Coefficient/GVF→METR-named grant in Coefficient index snapshot 2026-09-11 plus GVF 990-PF through FYE June 2025. F3 OPEN: Anthropic stake vehicle unidentified. These are carried-forward findings, not new rematches. `prior-tarbell.md` is the local post copy. SFF/Tarbell TB05/TB06 already occur in the prior material and are not re-added.

No complete FLI/DAF outgoing-grant scrape or all-time SFF review is claimed. The existing audit has reusable filing captures and row IDs for CAIS, CAISAF, AIPI, Encode, IAPS and FLI. `prior_overlap.csv` indexes them without promoting or totaling them again.

## Blocked / absent inputs

- `/workspace/bass-intake/codex-prompt-rookepoole-ngos.md` and `rookepoole-nodes.md`: `/workspace` is absent on this host. The chat transcription is the intake source.
- No running Python scraper was visible in the process list on this host; the existing scraper files/cache were found and reused. No other machine’s process is claimed inspected.
{chr(10).join(errors)}
- Web opening the supplied Tarbell URL failed; local published-post source was available and copied. No re-audit triggered.
- Historical SFF shorthand endpoints can fail: existing `sff-2024.html.error.json` recorded HTTP 404 for `/sff-2024`; cached canonical `/2024/recommendations` succeeded. Use metadata URLs, not guessed shorthand.

## Reproduce / extend

From this directory, run `../../.venv/bin/python acquire.py`, then `../../.venv/bin/python build.py`. The acquisition adapter imports `../../fetch_sources.py`, redirects its cache into this folder, and retains its robots policy, serial acquisition and 429 backoff. `jobs.json` records exact source URLs and scrape paths. Existing source dates and hashes are preserved. Add later NGO jobs/aliases deliberately; do not rerun the unrelated original audit pipeline. These scripts write local audit files only.
''')

prior=[]
for fn in ['recommendations.csv','grants.csv','project_grants.csv','disclosures.csv','entities.csv','awards.csv']:
    path=AUDIT/'research'/fn
    if not path.exists():continue
    for row in read_csv(path):
        if row.get('org_id') in ['CAIS','CAISAF','AIPI','ENCODE','IAPS','FLI']:
            prior.append(dict(prior_file=str(path),prior_row_id=row.get('row_id',''),org_id=row['org_id'],source_url=row.get('source_url',''),note='Previously covered evidence lead only; no new total or verdict assigned.'))
write_csv('prior_overlap.csv',prior)

(ROOT/'README.md').write_text('''# Rooke Poole grant-graph intake and first rematches

Start with QUEUE.md, then rematch/. All CSV amounts are USD; blank is unknown, not zero. nodes.csv uses the required source vocabulary: poole_graphic means user-transcribed graphic lead, not inspected-image evidence. Funders, persons, fiscal sponsors, programs, and policy outputs are distinct.

edges_claims.csv is a claim register, not an additive transaction ledger. PG rows preserve the incomplete supplied claims; SFF rows freeze narrower primary follow-up claims; FLI-MUSK-ANNOUNCEMENT is an announcement/commitment. Blank grantor/date stays blank when not supplied. row_id is the one added schema field for stable citations. evidence_rows.csv contains only the first eight NGOs’ exact 2024/2025 SFF entries and their conditional components. Published recommendation totals include matching pledges: never sum published_total_usd across split rows, or add the separate pledge table, speculation annotations, prior audit records, Bass rows or Poole claims. No aggregate grant total is provided.

bass_overlap.csv and prior_overlap.csv preserve pointers into prior research. They are claim/evidence indexes, not new receipts. Sponsor/program alias mappings are search aids; they do not prove legal succession. Full Form 990/EIN rematches remain queued.

MANIFEST.csv records SHA-256 and byte size for all handoff files except itself, with source URL and capture date when available. Source metadata retains its original date. Acquisition errors are retained explicitly. Cached HTML is the source of KEEP verdicts, not web-search excerpts. The original Poole image was unavailable, so visual completeness and OCR remain OPEN.
''')

# Validate semantics and source integrity before hashing the final handoff.
assert len({n['normalized_name'] for n in nodes})==len(nodes)
assert len({r['row_id'] for r in edges})==len(edges)
assert {r['row_id'] for r in edges}=={r['row_id'] for r in verdicts}
assert {r['org_code'] for r in evidence}==set(aliases)
assert all(r['money_type'] in ['award','recommendation','commitment','unknown'] for r in edges)
for row in evidence:
    assert (ROOT/row['source_file']).exists()
    assert row['amount_usd']>=0
    if row['money_type']=='recommendation':
        assert row['amount_usd']+row['included_matching_pledge_usd']==row['published_total_usd']
for path in S.glob('*.meta.json'):
    data=json.loads(path.read_text()); source=path.with_name(path.name.removesuffix('.meta.json'))
    assert source.exists() and hashlib.sha256(source.read_bytes()).hexdigest()==data['sha256'],path
(ROOT/'VALIDATION.md').write_text(f'# Validation\n\nPassed: {len(nodes)} unique nodes, {len(edges)} unique frozen claim IDs, {len(evidence)} primary SFF component rows covering all eight first-priority NGOs; typed money categories, non-negative amounts, included-pledge reconciliation, source existence and every cached-source SHA-256 match. CSVs round-trip through Python csv.DictReader. No graphic amount was treated as a receipt.\n')
for path in ROOT.glob('*.csv'):
    if path.name!='MANIFEST.csv': read_csv(path)
manifest=[]
for path in sorted(ROOT.rglob('*')):
    if not path.is_file() or path.name=='MANIFEST.csv' or '__pycache__' in path.parts:continue
    metadata_path=path.with_name(path.name+'.meta.json')
    m=json.loads(metadata_path.read_text()) if metadata_path.exists() else {}
    data=path.read_bytes()
    manifest.append(dict(path=str(path.relative_to(ROOT)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),source_url=m.get('url',''),snapshot_date=m.get('snapshot_date',''),role='primary_or_claim_source_see_filename' if path.parent==S else 'handoff'))
write_csv('MANIFEST.csv',manifest)
print(f'{len(nodes)} nodes; {len(edges)} claims; {len(evidence)} primary rows; {len(manifest)} hashed files')
