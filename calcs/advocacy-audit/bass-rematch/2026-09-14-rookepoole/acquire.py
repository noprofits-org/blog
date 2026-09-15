"""Reuse the existing audit fetcher in an isolated, dated evidence directory."""
import datetime, hashlib, importlib.util, json, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent
AUDIT = ROOT.parents[1]
SOURCES = ROOT / 'sources'
SOURCES.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location('existing_fetcher', AUDIT / 'fetch_sources.py')
fetch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch)
fetch.RAW = SOURCES
fetch.DATE = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

def reuse(name):
    src = AUDIT / 'sources' / name
    if not src.exists():
        return
    meta = src.with_name(src.name + '.meta.json')
    if meta.exists():
        expected = json.loads(meta.read_text())['sha256']
        assert hashlib.sha256(src.read_bytes()).hexdigest() == expected, name
        shutil.copy2(meta, SOURCES / meta.name)
    shutil.copy2(src, SOURCES / name)

def main():
    for pattern in ['sff-20*.html', 'sff-home.html', 'fli-funding.html', 'encode-privacy.html', 'rematch-tree.json']:
        for path in sorted((AUDIT / 'sources').glob(pattern)):
            reuse(path.name)
    shutil.copy2(AUDIT / 'fetch_sources.py', ROOT / 'existing_fetch_sources.py.txt')
    shutil.copy2(AUDIT.parents[1] / 'posts/2026-09-15-tarbell-coefficient-grant-graph.md', ROOT / 'prior-tarbell.md')
    tree = json.loads((SOURCES / 'rematch-tree.json').read_text())
    commit = tree['sha']
    jobs = [
        ['https://metr.org/about', 'metr-about.html'],
        ['https://jaan.info/philanthropy/donations.csv', 'tallinn-donations.csv'],
        ['https://survivalandflourishing.fund/2025/further-opportunities', 'sff-2025-further.html'],
        ['https://futureoflife.org/newsletter/2015-a-year-in-review/', 'fli-2015-review.html'],
        ['https://x.com/rookepoole/status/2099660837388501127', 'poole-thread.html'],
    ]
    for name in ['money_flows', 'shared_donors', 'tarbell_funding', 'redwood', 'tallinn-donations-ledger-2026-09-13']:
        jobs.append([f'https://raw.githubusercontent.com/kevinnbass/metr-money-figure/{commit}/research/{name}.csv', f'bass-{name}.csv'])
    (ROOT / 'jobs.json').write_text(json.dumps(jobs, indent=2) + '\n')
    (ROOT / 'bass-revision.json').write_text(json.dumps({'repository':'https://github.com/kevinnbass/metr-money-figure', 'tree_sha':commit, 'pin_note':'Immutable Git tree SHA from the existing cached GitHub tree response; not asserted to be a commit SHA.'}, indent=2) + '\n')
    # Serial fetches retain the original robots checks, cache, and 429 handling.
    for url, name in jobs:
        try:
            print(name, len(fetch.get(url, name)), flush=True)
        except Exception as error:
            (SOURCES / (name + '.error.json')).write_text(json.dumps({'url':url,'attempted_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':str(error)},indent=2))
            print(name, str(error), flush=True)

if __name__ == '__main__':
    main()
