# Rooke Poole grant-graph intake and first rematches

Start with QUEUE.md, then rematch/. All CSV amounts are USD; blank is unknown, not zero. nodes.csv uses the required source vocabulary: poole_graphic means user-transcribed graphic lead, not inspected-image evidence. Funders, persons, fiscal sponsors, programs, and policy outputs are distinct.

edges_claims.csv is a claim register, not an additive transaction ledger. PG rows preserve the incomplete supplied claims; SFF rows freeze narrower primary follow-up claims; FLI-MUSK-ANNOUNCEMENT is an announcement/commitment. Blank grantor/date stays blank when not supplied. row_id is the one added schema field for stable citations. evidence_rows.csv contains only the first eight NGOs’ exact 2024/2025 SFF entries and their conditional components. Published recommendation totals include matching pledges: never sum published_total_usd across split rows, or add the separate pledge table, speculation annotations, prior audit records, Bass rows or Poole claims. No aggregate grant total is provided.

bass_overlap.csv and prior_overlap.csv preserve pointers into prior research. They are claim/evidence indexes, not new receipts. Sponsor/program alias mappings are search aids; they do not prove legal succession. Full Form 990/EIN rematches remain queued.

MANIFEST.csv records SHA-256 and byte size for all handoff files except itself, with source URL and capture date when available. Source metadata retains its original date. Acquisition errors are retained explicitly. Cached HTML is the source of KEEP verdicts, not web-search excerpts. The original Poole image was unavailable, so visual completeness and OCR remain OPEN.
