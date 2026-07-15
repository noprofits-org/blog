# Nobody's average: who actually pays for the nonprofit sector

**Status:** approved design, not yet drafted
**Date:** 2026-07-14
**Series:** the Form 990 data series — fourth entry in the arc that runs
[months-of-cash](/posts/2026-07-06-months-of-cash.html) →
[months-of-cash-at-scale](/posts/2026-07-07-months-of-cash-at-scale.html) →
[below-zero](/posts/2026-07-11-below-zero-negative-operating-reserve.html).

## The thesis

"Nonprofits run on donations" is the sector's founding sentence. Run the census
and donations are 24.4 percent of the money. But the post is not a gotcha about
that number. It is about the fact that the 24.4 percent *and* the median
charity's 65 percent are both true, and that everything interesting lives in why.

The sector has two answers because it has two weightings. By dollars it is a
hospital. By charity it is a small donation-funded organization. Every sentence
beginning "the nonprofit sector runs on…" silently picks one and hides the
choice. This is the same failure mode as the sector-average reserve in the
at-scale post, pointed at revenue instead of the balance sheet — which is what
earns this post its slot in the arc rather than merely extending it.

The third act is the payoff: revenue mix predicts runway in an **inverted U**.
Both extremes are fragile. The middle is resilient.

## Verified findings

All figures below were computed against `calcs/data/24eoextract990.csv` (IRS SOI
annual extract, returns filed CY2024, 345,365 rows) during design. They are
confirmed, not estimated. `compute.py` must reproduce them exactly; any
divergence is a bug in the script, not a reason to edit this spec.

### Aggregate (dollar-weighted), n = 249,668 501(c)(3)s with positive revenue

| Revenue source | Amount | Share |
| --- | --- | --- |
| Contributions and grants (`totcntrbgfts`) | $754.2B | 24.4% |
| Program service revenue (`totprgmrevnue`) | $2,155.2B | 69.6% |
| Investment income (`invstmntinc`) | $73.8B | 2.4% |
| Everything else (residual) | $113.1B | 3.7% |
| **Total revenue** | **$3,096.4B** | **100%** |

The residual is reported as **one undifferentiated bucket, deliberately**. Its
largest identifiable pieces are net gains on securities sales (`netgnls`,
$46.5B) and miscellaneous revenue (`miscrevtot11e`, $42.1B; `miscrevtota`,
$29.2B), but the extract's misc line items **over-sum to ~$155B against a
$113.1B residual** — the subtotal columns overlap, so decomposing the residual
would publish double-counted numbers. Report the bucket, name its two big
components as approximate, do not build a breakdown table. The three headline
categories are clean and independently verified; the residual is not.

### Per-organization (org-weighted), n = 242,348

Contribution share of revenue, restricted to orgs whose share falls in [0, 100]:

- mean 56.0%, median **65.1%**
- p25 12.5%, p75 96.6%, p90 100%
- **33.7%** of charities are ≥90% donation-funded
- **23.4%** are ≤10% donation-funded

The distribution is **bimodal** — piles at both 0 and 100. The mean of 56%
describes almost no actual charity.

### Concentration — the reason the two answers diverge

- Top **1%** of charities hold **69.1%** of all revenue
- Top **10%** hold **91.8%**
- Bottom **50%** hold **0.94%**

### The inverted U, n = 195,437

Honest reserve (the below-zero formula) by contribution-share band:

| Contribution share | n | Median honest months | Below zero | Under 3 months |
| --- | --- | --- | --- | --- |
| 0–10% (fee-funded) | 43,898 | 5.18 | 21.5% | 39.6% |
| 10–25% | 16,345 | 5.83 | 14.9% | 34.3% |
| 25–50% | 21,943 | 7.38 | 12.7% | 29.1% |
| 50–75% | 26,060 | 8.90 | 11.8% | 26.1% |
| 75–90% | 22,350 | 9.48 | 9.4% | 24.0% |
| 90–100% (donation-funded) | 64,841 | 5.37 | 12.1% | 36.6% |

Runway peaks in the middle and collapses at both ends. Charities living on a
single revenue type — whichever type — run the thinnest. This is a correlation
across one year of filings, not a causal claim, and the prose must say so.

## Method and filters

Baseline, matching the sibling posts:

- Latest tax period per EIN (`sort_values("tax_pd").drop_duplicates("EIN", keep="last")`) — drops amended and late duplicate filings.
- `subseccd == 3` for 501(c)(3) public charities.
- `totrevenue > 0`.

Two filter notes the prose must disclose rather than bury:

1. **Per-org stats drop orgs whose contribution share falls outside [0, 100]**
   (249,668 → 242,348). Offsetting negative revenue lines — investment losses,
   net rental and sales losses — can push the ratio out of range. The ~7,300
   dropped orgs are named in the prose, not silently filtered.
2. **The reserve section reimposes the FASB reconciliation** (Part X lines
   27+28+29 == line 33 within $1K) and `cashexp > 0`, because the honest-reserve
   formula depends on line 27. That is why its n is 195,437, not 242,348. The
   at-scale post already explains why the reconciliation is necessary; this post
   links there rather than re-deriving it.

The FASB reconciliation is **not** applied to the revenue-mix sections — it is a
balance-sheet constraint and would discard valid revenue data for no reason.

## Ruled out during design

**Cost-to-raise-a-dollar is not computable from this extract.** It carries Part
IX column A totals only — no program/management/fundraising split — so the ratio
the watchdog industry rates charities on is absent from the IRS's own bulk file.
That is a real post, but it is a plumbing post about the e-file XML, and it is
not this one.

## Structure

1. **Hook.** The founding sentence, then the 24.4 percent. Establish immediately
   that the contradiction, not the number, is the subject.
2. **The census, not the survey.** Method, filters, the two disclosures above.
   Code 1 carries the arithmetic.
3. **Two true answers.** Dollar-weighted 24.4% vs org-weighted median 65.1%.
4. **Why: concentration.** Top 1% hold 69.1%. The sector average is a hospital.
5. **The distribution is bimodal.** Piles at 0 and 100; the mean describes
   nobody. Tie explicitly back to the sector-average reserve in the at-scale
   post — same failure mode, different line of the 990.
6. **The inverted U.** Both extremes fragile, middle resilient. State the
   correlation-not-causation caveat inline.
7. **Close.** Cross-link the series and the noprofits.org tools
   (search.noprofits.org, grants.noprofits.org, ProPublica Nonprofit Explorer),
   then the one-line reader caveat the nonprofit series ends on.

## Figures

Matplotlib, brand palette per `notes/blog-authoring.md` §5, **lettered callouts
only** — captions carry all words. Every figure numbered, captioned in bold, and
referenced by number in the prose (§6).

- **Figure 1 — hero / OG card, authored at 1200×630.** The two answers side by
  side: dollar-weighted revenue split vs. org-weighted distribution of
  contribution share. A data hero in the below-zero mold, not an Illustrator
  piece, so the post reproduces end to end from `figures.py`.
- **Figure 2.** The bimodal histogram of contribution share; the 0 and 100 piles
  lettered and defined in the caption.
- **Figure 3.** Contribution share by revenue-size decile — the giants are
  fee-funded, which is the mechanism behind Figure 1's divergence.
- **Figure 4.** The inverted U: median honest reserve by contribution band, with
  the both-ends-fragile shape lettered.

`og-image` points at Figure 1.

## Artifacts

- `calcs/who-pays/compute.py` — reproduces every number in "Verified findings";
  writes the gzipped intermediates `figures.py` reads. Docstring cites the data
  source and states the filters, matching the sibling scripts.
- `calcs/who-pays/figures.py` — reads the intermediates, writes four PNGs.
- `posts/2026-07-14-nobodys-average.md`
- `images/2026-07-14-nobodys-average-{hero,bimodal,by-size,inverted-u}.png`

## Conventions

Binding: `notes/blog-authoring.md`, in full. Specifically —

- Frontmatter: `tags: nonprofits, data`; **no `author` field** (the nonprofit
  series renders without a byline); `og-image` set; title quoted (it contains a
  colon).
- Citations: **inline markdown hyperlinks, no `[@key]`, no reference list, no
  footnotes.** The nonprofit series convention. Nothing is appended to
  `bib/bibliography.bib`.
- Links site-relative, never absolute.
- Voice: prose over bullets, `##` headers, bold key terms on first use, no
  in-body H1 or repeated title/byline/tags.

## Delivery

Branch `post/nobodys-average`. Verify with `stack build && stack exec site
build`, then check the rendered page: figures load, captions numbered and
referenced, card meta correct. PR into `main`; merge triggers the Pages deploy.
Never commit straight to `main`.

## Open risks

- **Figure 1 has to carry two weightings in one 1200×630 frame** and still read
  as a social card at thumbnail size. If it can't be made legible, the fallback
  is a single-panel hero on the bimodal distribution with the dollar/org split
  moved to Figure 2 — but try the two-panel first, because the divergence *is*
  the post.
- **The inverted U invites a causal read.** The prose must not let "diversified
  revenue produces resilience" stand unqualified; the data supports association
  within one filing year and nothing stronger.
