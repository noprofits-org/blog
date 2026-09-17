# Cold-start prompt — rookepoole master-graph rematch (resume 2026-09-17)

You are resuming a paused line of investigation. Everything below is
established context; do not re-derive it. Work only from this directory and
its documented sources.

## Project context

blog.noprofits.org is a data-journalism blog. House rules, non-negotiable:
every number traces to a row ID in a CSV (row_id, amount, source_url,
snapshot_date, verbatim_quote, note); verdicts are KEEP / KILL / OPEN where
OPEN means the public evidence does not exist — never zero, never inference;
money types are never summed (grant ≠ recommendation ≠ commitment ≠ revenue
≠ lobbying fee); "none found" is bounded by exact documents searched and
dates; no motive language anywhere (the words "front group", "astroturf",
"proxy" are banned); public data only, respect robots.txt, no logins, no
contacting organizations, no git commits, no publication.

Two posts are already shipped from this line of work:
1. "What rematches, what doesn't: the Tarbell–Coefficient grant graph, row by
   row" (posts/2026-09-15-tarbell-coefficient-grant-graph.html) — rematched
   Bass TB01–TB06. Carried-forward verdicts: F1 KEEP ($5,291,930 Tarbell-named
   Coefficient awards); F2 KEEP bounded (no METR-named grant in Coefficient
   index snapshot 2026-09-11 or GVF 990-PFs through FYE June 2025); F3 OPEN
   (Anthropic stake vehicle unidentified).
2. "Who pays for the messaging" (posts/2026-09-15-who-pays-for-the-messaging.html)
   — full audit of both sides' funding. Its artifacts live at
   calcs/advocacy-audit/ (NOT this directory) and are complete; reuse its
   rows and filing captures via prior_overlap.csv instead of re-fetching.

## This directory and its state

calcs/advocacy-audit/bass-rematch/2026-09-14-rookepoole/ holds an intake and
first rematch of a community grant-graph by @rookepoole on X. README.md,
QUEUE.md, MANIFEST.csv, nodes.csv (51 nodes), edges_claims.csv (55 frozen
claims), evidence_rows.csv (20 primary SFF rows for the first 8 NGOs),
verdicts.csv (all PG-* graphic rows OPEN), bass_overlap.csv and
prior_overlap.csv (pointers into Bass-pack and prior-audit rows — indexes,
not receipts). Scripts: acquire.py, build.py (run via ../../.venv/bin/python).
Blocked routes are documented in QUEUE.md and sources/*.error.json — x.com
and jaan.info robots-block automated fetch; do not retry them.

## What changed since the pause

The ORIGINAL GRAPHIC is now available locally. Read
IMAGE-VERIFICATION-2026-09-17.md first — it records a visual pass over the
full-resolution image (media HSQiUq0WUAAXVqj, tweet
2099843861388440013, posted Sep 15: "master graph of slow-AI… 88 nodes and
120 edges"). Key facts: it is a NEWER, LARGER version than the transcription
(51 nodes, tweet 2099660837388501127); six transcribed amounts are visually
confirmed ($650K CAIS, $2.8M MIRI, $2.12M METR, $467K Palisade, $526K Encode,
$2.43M AIPI); AI Futures $2.08M, CAISAF $2.62M, Palisade $1.15M not yet
located; bracketed `[$xxM]` context totals appear on edge labels and are
undefined. The image is not ours to reproduce: local inspection only, never
republish, never commit the JPEG.

## Your tasks, in order

1. Reconcile versions. Register the master graph as the current claim set:
   diff its 88 nodes / 120 edges against nodes.csv; add new nodes/edges with
   row IDs and per-row source URLs (both tweets cited, master tweet primary);
   mark transcription-only rows as superseded, not deleted. Record the
   version lineage in each affected row's note.
2. Complete the visual reconciliation. Using the local image (ask the user
   for the file path if it has moved; expected under ~/Downloads or this
   directory), resolve the UNRESOLVED items in IMAGE-VERIFICATION-2026-09-17.md
   (AI Futures $2.08M, CAISAF $2.62M, Palisade $1.15M, the not-yet-located
   node boxes). Record confirmed-as-drawn vs not-visible per row.
3. Work QUEUE.md items 1–28 against funder-side primaries (990-PF and 990
   Schedule I grantee-name searches are the working direction; org-side
   Schedule B is redacted post-2020 — do not attempt donor identification
   from c3 filings). Promote graphic labels to KEEP only with a primary
   document; a label confirmed as drawn stays a claim.
4. The Tallinn ledger row (Bass M55, $184,000, 2024-12-06, FP-US → METR)
   remains blocked via jaan.info robots; try funder-side filings for the same
   transaction dimensions. If no primary route resolves it, it stays OPEN
   with the block documented — do not promote the Bass copy to a receipt.
5. Keep the Bass-thread linkage live: for each new KEEP, note whether the
   same edge exists in kevinnbass/metr-money-figure (use
   bass_overlap.csv; add rows as needed).

## Deliverables when the pass completes

- Updated nodes.csv / edges_claims.csv / verdicts.csv with master-graph row
  IDs and version lineage
- An IMAGE-RECONCILIATION section appended to IMAGE-VERIFICATION-2026-09-17.md
  (or a dated successor file)
- NOTES-POOLE.md in the house style: bounded findings, quotable sentences with
  row IDs, and the org × claim verdict table for everything rematched
- STATE-POOLE.md: every OPEN with the exact public document that would close
  it
- compute-style check script (extend build.py) that re-derives every
  aggregate from the CSVs and fails loudly on drift

Do NOT write blog prose, do NOT commit to git, do NOT publish. A human writes
the post from your NOTES.
