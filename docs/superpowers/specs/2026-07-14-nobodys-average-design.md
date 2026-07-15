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
charity's 65 percent are both true, and about what has to be the case for both
to be true at once.

What has to be the case is that **501(c)(3) is not one population.** It is a
legal category doing duty as an analytic one, and it does not survive the
transfer. That is the post's conclusion, and it is a stronger claim than "the
average is misleading" — it says the bucket itself is the error, and that no
choice of summary statistic repairs it.

The third act is the payoff: revenue mix predicts runway in an **inverted U**.
Both extremes are fragile, the middle is resilient — a shape the pooled sector
number cannot express, and therefore a demonstration of the conclusion rather
than a separate finding.

### Framing the conclusion — the argument that carries it

The argument is **not** "the distribution isn't a bell curve, therefore it isn't
one population." That proves too much and a statistician will swat it: nearly
every financial variable on the 990 is savagely right-skewed, revenue and
expenses included. If non-normality dissolved categories, no category would
survive. Non-normality is *not* evidence of a mixture.

The two claims that do carry the conclusion, both verified below:

1. **A mixture of business models.** The contribution-share distribution is
   bimodal with piles at the structural extremes — 26,657 charities report
   *exactly* 0 percent contributions and 25,366 report *exactly* 100 percent.
   Those are structural zeros and ones, not measurement noise; a single smooth
   population does not produce 52,000 exact extremes. And critically the piles
   appear **at every size** (finding 4), so this is a mixture by business model,
   not a size artifact.
2. **A distinct population at the top.** Deciles 1–9 are effectively one sector
   (median contribution share ~70 percent, flat). The top 1 percent has a median
   contribution share of **2.0 percent** and holds most of the money. It is not
   the tail of this distribution; it is a different distribution.

Together: the headline 24.4 percent is not a fact about the nonprofit sector. It
is a measurement of 2,423 institutions, averaged over 240,000 organizations that
look nothing like them.

And the closing turn: **the distinction is already in the file.** `nonpfrea` —
the public-charity test each organization declares on Schedule A — separates the
piles at a median of 87.0 percent (code 07, publicly supported) against 42.2
percent (code 09, exempt-function revenue), with hospitals at 1.4 percent and
churches at 99.7 percent. So the post does not have to propose a taxonomy. It
observes that the IRS already collects one, every charity already declares it
under penalty of perjury, it ships in the same public file as the revenue lines
— and the sector averages across it anyway.

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

### The three groups, n = 242,348

| | Fee-funded (≤10%) | Donation-funded (≥90%) | Middle |
| --- | --- | --- | --- |
| Organizations | 56,619 | 81,739 | 103,990 |
| Share of all orgs | 23.4% | 33.7% | 42.9% |
| **Share of all revenue dollars** | **61.5%** | **12.5%** | 25.9% |
| Median revenue | $614,855 | $491,463 | $569,737 |
| Mean revenue | $33,412,128 | $4,707,484 | $7,669,395 |
| Median total assets | $1,251,203 | $512,764 | $1,158,034 |

Structural extremes: **26,657** charities report exactly 0% contributions;
**25,366** report exactly 100%.

### Size does NOT explain the bimodality — mechanism correction

**This refutes the mechanism assumed in the first draft of this spec, and the
prose must not revert to it.** The intuitive story — "the fee pile is giant
hospitals, the donation pile is small charities" — is **false at the median**.
Median revenue is $614,855 (fee) vs $491,463 (donation): a ratio of **1.3×**.
The typical fee-funded charity and the typical donation-funded charity are the
same size. The size difference lives entirely in the tail (mean $33.4M vs $4.7M).

So the fee/donation split is a difference in **business model**, not scale: a
similarly-sized daycare, clinic, or theater that charges for its services, next
to an advocacy group or grantmaker-supported charity that does not. Two kinds of
organization, not two sizes.

### Contribution share by revenue decile — flat, then a cliff

| Decile | Revenue range | Median contribution share | % fee-funded |
| --- | --- | --- | --- |
| 1 | $1 – $90,642 | 55.3% | 30.9% |
| 2 | $90,644 – $187,742 | 63.0% | 21.8% |
| 3 | $187,745 – $264,231 | 73.7% | 18.9% |
| 4 | $264,237 – $373,602 | 73.3% | 19.6% |
| 5 | $373,604 – $546,934 | 70.2% | 20.1% |
| 6 | $546,935 – $860,132 | 71.1% | 20.5% |
| 7 | $860,169 – $1,489,083 | 70.2% | 20.7% |
| 8 | $1,489,132 – $3,034,096 | 69.9% | 20.7% |
| 9 | $3,034,163 – $9,031,953 | 65.8% | 22.7% |
| 10 | $9,032,489 – $75.1B | **23.4%** | **37.8%** |

**Top 1% by revenue** (n = 2,423): median contribution share **2.0%**; **68.9%**
are fee-funded.

Deciles 1–9 are one sector — flat median around 70%, roughly 20% fee-funded and
34% donation-funded in every decile. Decile 10 detaches and the top 1% is
categorically different. This is the single most important table in the post: it
is what makes "different populations" an observation rather than an opinion.

### The distinction is already in the file — `nonpfrea`, n = 242,348

**Peter's question, and the post's sharpest turn.** The extract carries
`nonpfrea`, the non-private-foundation reason code: which public-charity test the
organization declares it qualifies under on Schedule A. Its two dominant values
are very nearly the two piles.

| `nonpfrea` — declared test | n | Median contribution share | % fee (≤10) | % donation (≥90) |
| --- | --- | --- | --- | --- |
| 07 — §170(b)(1)(A)(vi), publicly supported | 107,177 | 87.0% | 9.1% | 46.3% |
| 09 — §509(a)(2), exempt-function revenue | 92,654 | 42.2% | 31.1% | 24.5% |
| 02 — school | 15,473 | 17.4% | 35.9% | 18.7% |
| 12 — supporting org | 8,487 | 4.0% | 53.8% | 15.9% |
| 01 — church | 4,638 | 99.7% | 15.8% | 64.5% |
| 03 — hospital | 3,546 | 1.4% | 77.5% | 4.4% |
| 13 — supporting org | 2,402 | 1.2% | 59.2% | 11.8% |
| 14 — supporting org | 2,279 | 5.0% | 54.3% | 10.2% |
| 08 — community trust | 1,692 | 80.4% | 12.5% | 40.4% |
| 15 — supporting org | 1,449 | 0.0% | 75.4% | 6.1% |
| 06 — governmental unit | 1,430 | 73.4% | 9.5% | 26.2% |

Activity flags are sharper still:

- `operatehosptlcd == "Y"`: n = 2,235, median contribution share **1.1%**
- `operateschools170cd == "Y"`: n = 15,187, median contribution share **17.6%**

**What this does to the conclusion.** The post no longer argues that these
*should* be separate buckets. It observes that they **already are** — the IRS
collects the distinction, every charity declares it on Schedule A under penalty
of perjury, and it sits in the same public file as the revenue lines. The sector
averages across it anyway. The conclusion is not a request for a new taxonomy;
it is that there is one in the file, unused.

**Required honesty constraint — the separation is strong, not clean.** Code 09's
median is 42.2%, not near zero, and only 31.1% of 09 organizations are fee-funded
by the ≤10% definition. The reason is substantive and the prose must state it:
`nonpfrea` records which test an organization **qualifies under**, not how it is
**actually funded**. An organization can qualify via 509(a)(2) and still run
mostly on contributions. So the supportable claim is "**a strong signal the
sector's measurement apparatus ignores**" — never "a clean partition," and never
"the IRS already sorts them correctly." The hospital and church cuts are the
clean ones; 07 vs 09 is the loud but noisy one.

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
4. **The distribution is bimodal.** Piles at 0 and 100 — 26,657 exact zeros,
   25,366 exact hundreds. The mean of 56% describes nobody. Tie back to the
   sector-average reserve in the at-scale post: same failure mode, different line
   of the 990.
5. **It isn't size — it's business model.** Kill the intuitive explanation on the
   spot: median revenue differs by only 1.3× across the two piles, and the piles
   appear in every decile. This section exists to *refuse* the easy story, which
   is what licenses the conclusion later. Then the cliff: deciles 1–9 flat at
   ~70%, top 1% at 2.0%.
6. **The inverted U.** Both extremes fragile, middle resilient. State the
   correlation-not-causation caveat inline. Frame it as what stratifying buys
   you — structure the pooled number cannot express.
7. **The distinction is already in the file.** Table 1 and the `nonpfrea` story.
   The turn the post is built to deliver: the reader has by now accepted that
   these are different populations, and this section reveals the IRS has been
   coding the difference the whole time, in the same file, one column over. State
   the qualifies-under vs actually-funded caveat here, honestly and in place —
   it costs nothing and buys the section its credibility.
8. **Conclusion: they don't belong in the same bucket.** The load-bearing
   section, and the reason the post exists. 501(c)(3) is a legal category, not an
   analytic one. Make the two-claim argument from §The thesis explicitly, and
   explicitly decline the bell-curve version of it — skew is not the evidence,
   the mixture and the detached top are. Land the consequence: the sector's own
   measurement apparatus (watchdog ratios, sector averages, "the average
   nonprofit…" survey journalism) inherits the legal category without ever asking
   whether it is an analytic one, and the 24.4 percent is what that mistake
   produces. The fix is not new taxonomy — it is to stop discarding the one
   already in the file: stratify before summarizing, and make any sector
   statistic declare its weighting and its stratum or mean nothing.
9. **Close.** Cross-link the series and the noprofits.org tools
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
- **Figure 3.** Contribution share by revenue decile: **flat across deciles 1–9,
  then the cliff at decile 10, with the top 1% marked separately at 2.0%.** The
  post's most important figure — it is what turns "different populations" from an
  opinion into an observation. The flat run matters as much as the cliff, so the
  y-axis must not be scaled to hide it. Letter the flat region and the cliff;
  the caption carries the numbers.
- **Figure 4.** The inverted U: median honest reserve by contribution band, with
  the both-ends-fragile shape lettered.

`og-image` points at Figure 1.

**Table 1** — the `nonpfrea` breakdown from §The distinction is already in the
file. A table, not a figure: it is enumerable facts, and the blog's convention
already supports `**Table 1.**` with a bold caption below (§6 of the authoring
notes). Ship the eleven codes with n ≥ 1,000; do not plot them. Referenced by
number from structure section 7.

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
- **The conclusion invites the bell-curve shortcut.** The tempting sentence —
  "it's not a normal distribution, so it's not one population" — is wrong and
  must not appear in any draft. Skewness is not mixture evidence. If a draft
  reaches for it, the fix is to reach for the exact-extremes pile counts and the
  decile cliff instead.
- **The dead mechanism is seductive and will try to come back.** "Fee-funded
  means hospitals, donation-funded means food pantries" is intuitive, quotable,
  and false at the median (1.3×). Any draft sentence implying the two piles
  differ by *size* rather than by *business model* is a factual error, not a
  simplification.
- **The conclusion is a normative claim in a data series.** The post prescribes
  how the sector should measure itself, which is a step beyond describing what
  the filings say. Keep the prescription tied to the specific evidence (mixture +
  detached top + the unused code) and out of general advocacy.
- **`nonpfrea` will tempt an overclaim.** The seductive sentence is "the IRS
  already sorts charities into these groups." It does not: 07 vs 09 separates
  medians 87.0 vs 42.2, which is a strong signal and a noisy partition, because
  the code records qualification rather than realized funding. Any draft implying
  a clean sort, or that stratifying by `nonpfrea` alone would fix sector
  statistics, is overclaiming. The defensible sentence is that the signal exists,
  is free, is declared under penalty of perjury, and is discarded.
