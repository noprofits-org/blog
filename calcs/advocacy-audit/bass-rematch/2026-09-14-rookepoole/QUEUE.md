# Queue

Audit folder date: 2026-09-14, the local session date. The supplied Tarbell post is dated 2026-09-15; its findings are carried forward, not re-dated.

## Completed this pass

- All 51 nodes from the supplied list and supporting leads registered. Original image completeness/OCR remains unverified.
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

9. Institute for AI Policy and Strategy (IAPS) — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
10. Centre for the Governance of AI (GovAI) — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
11. Center for Humane Technology (CHT) — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
12. Civic AI Security Program (CivAI) — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
13. PauseAI US — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
14. PauseAI Global — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
15. 80,000 Hours — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
16. Common Sense Media — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
17. Economic Security Project — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
18. Blueprint for Free Speech — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
19. Young People's Alliance Education Fund — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
20. AI Objectives Institute — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
21. Evitable — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
22. Bureau of Investigative Journalism — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
23. Alignment Research Center (ARC) — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
24. Redwood Research — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
25. Constellation — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
26. Longview Philanthropy — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
27. RAND — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.
28. Canary (Audacious) — next freeze: identify one exact grantor, receiving entity, amount, money type and period from a primary row before assigning KEEP/KILL.

## Hub and publication scope

Prior F1 KEEP: Coefficient→Tarbell TB02–TB04 $5,291,930. TB01 is a separate joint Training for Good award. F2 KEEP bounded: no direct Coefficient/GVF→METR-named grant in Coefficient index snapshot 2026-09-11 plus GVF 990-PF through FYE June 2025. F3 OPEN: Anthropic stake vehicle unidentified. These are carried-forward findings, not new rematches. `prior-tarbell.md` is the local post copy. SFF/Tarbell TB05/TB06 already occur in the prior material and are not re-added.

No complete FLI/DAF outgoing-grant scrape or all-time SFF review is claimed. The existing audit has reusable filing captures and row IDs for CAIS, CAISAF, AIPI, Encode, IAPS and FLI. `prior_overlap.csv` indexes them without promoting or totaling them again.

## Blocked / absent inputs

- `/workspace/bass-intake/codex-prompt-rookepoole-ngos.md` and `rookepoole-nodes.md`: `/workspace` is absent on this host. The chat transcription is the intake source.
- No running Python scraper was visible in the process list on this host; the existing scraper files/cache were found and reused. No other machine’s process is claimed inspected.
- https://x.com/rookepoole/status/2099660837388501127: robots disallows https://x.com/rookepoole/status/2099660837388501127. Record: `sources/poole-thread.html.error.json`.
- https://jaan.info/philanthropy/donations.csv: robots disallows https://jaan.info/philanthropy/donations.csv. Record: `sources/tallinn-donations.csv.error.json`.
- Web opening the supplied Tarbell URL failed; local published-post source was available and copied. No re-audit triggered.
- Historical SFF shorthand endpoints can fail: existing `sff-2024.html.error.json` recorded HTTP 404 for `/sff-2024`; cached canonical `/2024/recommendations` succeeded. Use metadata URLs, not guessed shorthand.

## Reproduce / extend

From this directory, run `../../.venv/bin/python acquire.py`, then `../../.venv/bin/python build.py`. The acquisition adapter imports `../../fetch_sources.py`, redirects its cache into this folder, and retains its robots policy, serial acquisition and 429 backoff. `jobs.json` records exact source URLs and scrape paths. Existing source dates and hashes are preserved. Add later NGO jobs/aliases deliberately; do not rerun the unrelated original audit pipeline. These scripts write local audit files only.
