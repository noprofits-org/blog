# Resume prompt — poole master-graph rematch, financial pass (2026-09-18)

You are resuming an in-progress audit. Read these, in this order, before any
work: `COLD-START.md` (project background and house rules — they still bind),
`QUEUE.md`, `VALIDATION-2026-09-18.md`, `THREAD-REVIEW-2026-09-18.md`,
`IMAGE-RECONCILIATION-2026-09-18.md`, `README.md`.

## State of play

Done and validated: intake registration (51 nodes / 55 claims), version
reconciliation against the master graph (88 nodes independently counted; 36
mapped, 52 new, 15 intake-only; 103 combined entries in nodes.csv), thread
review (9 THREAD-FUND claims frozen from the author's funding post, all OPEN),
image reconciliation (88 boxes with coordinates; six earlier visual amount
readings withdrawn — amounts are OPEN, do not revive them), consistency checks
passing, original rows preserved byte-for-byte. `build.py --check` is
read-only and green.

Not done: the financial queue has not resumed; the master edge register holds
6 of ~120 edges; every graphic and thread dollar remains OPEN.

## Tasks, in order

1. **Resume the financial queue** — QUEUE.md items in order, funder-side
   primaries only (990-PF and 990 Schedule I grantee-name searches; org-side
   Schedule B is redacted post-2020 — no donor identification from c3
   filings). A graphic or thread label promotes to KEEP only with a primary
   document carrying amount, payer, payee, and period; until then it stays
   OPEN. The Tallinn ledger row (Bass M55, $184,000) stays blocked via
   jaan.info robots — try funder-side filings for the same transaction
   dimensions; otherwise documented OPEN. Do not retry robots-blocked routes.
2. **Hunt the S-code source index.** The image's `[S###]` tokens are reference
   codes (see IMAGE-RECONCILIATION-2026-09-18.md); the author claims a
   "verified network," so an index of sources plausibly exists. Work only
   public, permitted routes: the captured thread HTML (`sources/poole-master-thread.cached.html`, `thread_posts.csv` URLs), the author's profile links as captured, web/GitHub search for the handle `rookepoole` and phrases from the thread ("slow-AI", "master graph"). If found, register it as a source artifact with hash and URL; if not found after a bounded search, record the search itself in bounded-none-found form (queries, dates, routes). Never fetch x.com or jaan.info directly — documented blocks.
3. **Extend the edge register.** Freeze remaining master edges with scope and
   money_type; financial endpoints traced to primary rows before any verdict.
   Money types never summed; the author's two claim sets (graphic vs thread)
   are never added or averaged — period and scope differences stay explicit.
4. **Cross-thread consistency.** Where the author's amounts disagree across
   outputs (MIRI $2.8M vs $1.607M; AI Futures $2.08M vs $2.035M; Palisade
   $467K vs $1.133M; CAISAF $2.62M vs $3.813M), record both as drawn with
   their locators. The one claimed amount that matches a prior-audit row to
   the dollar — SFF → Tarbell $783K — may be compared against the SFF 2025
   recommendation row ($783,000 including a $200,000 conditional match,
   carried forward from the Tarbell post) as a scoped check; a published
   recommendation is not a disbursement.

## Deliverables when the pass completes

- `NOTES-POOLE.md` — house style: bounded findings, quotable sentences with
  row IDs, the claim × verdict table for everything rematched this pass
- `STATE-POOLE.md` — every OPEN with the exact public document that closes it
- Extended `build.py --check` covering the new rows; it must fail loudly on
  drift and must not auto-refresh expected values

Do NOT write blog prose, do NOT commit to git, do NOT publish, do NOT
reproduce the image. A human writes the post from your NOTES.
