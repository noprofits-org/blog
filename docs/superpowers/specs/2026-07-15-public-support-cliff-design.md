# One-third: the cliff a few hundred charities steer around

**Status:** approved design, not yet drafted
**Date:** 2026-07-15
**Series:** the Form 990 data series — fifth entry, after
[nobody's average](/posts/2026-07-14-nobodys-average.html).

## The thesis

There is a bright line in the tax code. A public charity relying on the
§170(b)(1)(A)(vi) support test must draw at least **one-third of its support from
the public**; fall below and it risks being reclassified as a private foundation.
Economics predicts that a threshold with real consequences produces **bunching** —
organizations that would have landed just below instead land just above.

They do. The bunching at 33⅓ percent is real, robust, and placebo-tested. It is
also **80 organizations** — which is either nothing (0.072 percent of the
population) or a lot (~12 percent of the ~670 close enough to see the line),
depending entirely on what you divide by. That is the
[nobody's average](/posts/2026-07-14-nobodys-average.html) thread arriving
somewhere new, and it is why this post belongs in the series rather than beside it.

The payoff is not the econometrics. It is **what the test actually measures**.
The 2 percent rule — any one donor's support above 2 percent of the total does not
count toward the public's share — means the charities near the cliff are not
unpopular or failing. They are **narrowly funded**. Half their support is excluded
because it came from too few people. The rule does not ask how much you raised. It
asks how many people you raised it from.

## Verified findings

All values below were computed against `calcs/data/24eoextract990.csv` (IRS SOI
annual extract, returns filed CY2024) during design and are confirmed, not
estimated. `compute.py` must reproduce them; divergence is a bug in the script.

**Population.** `subseccd == 3`, `totsupp170 > 0`, `nonpfrea == 7`, support
percentage in [0, 100]: **111,991** organizations. The support percentage is
`pubsupplesspct170 / totsupp170 * 100`.

### The cliff is invisible to almost everyone

- Median public support: **95.7%**
- Below the 33⅓ line at all: **4,323** (3.86%)
- Within 1.5 points of the line: **670** (0.60%)

### The bunching estimator

Counterfactual density fitted by a degree-5 polynomial on 0.5-point bins over
[20, 50], **excluding** a ±W window around 33.333, then observed compared to
counterfactual inside the window.

| Window | Above: observed vs counterfactual | Below: observed vs counterfactual |
| --- | --- | --- |
| ±1.0 | 267 vs 241.0 (**+10.8%**) | 187 vs 223.4 (**−16.3%**) |
| ±1.5 | 399 vs 370.3 (**+7.8%**) | 280 vs 331.4 (**−15.5%**) |
| ±2.0 | 536 vs 502.0 (**+6.8%**) | 379 vs 433.6 (**−12.6%**) |

Excess above **and** deficit below, at every window — the signature of
displacement across the line rather than a lump sitting on it.

**Headline statistic — displacement** = (excess above) + (missing below), at
bw = 0.5, degree 5, W = 1.5: **+80.1 organizations**.

### It is real — three independent checks

**Placebo.** The identical estimator at 21 fake thresholds (22–48%, excluding ±3
of the real cliff):

- placebo mean **−4.2**, sd **22.4**
- real **+80.1** → **z = +3.77**
- placebos at or above the real value: **0 of 21**. Largest placebo: +35.0.

**Bootstrap.** 400 resamples at bw = 0.5, degree 5, W = 1.5: point **+80.1**, 95%
CI **[+28.1, +129.0]**; **0/400** bootstraps ≤ 0.

**Specification robustness.** All 12 combinations of bw ∈ {0.25, 0.5, 1.0} and
degree ∈ {3, 4, 5, 6} give positive displacement, ranging **+46.9 to +95.4**.
Coarser bins attenuate it (bw = 1.0 → ~+47) exactly as expected when a
1.5-point window is smeared across 1-point bins; this is attenuation, not
instability, and the prose should say so rather than hide the spread.

### The size, and the denominator that decides it

- **80** organizations displaced
- of **111,991** in the population → **0.072%**
- of the **670** within 1.5 points of the line → **~12%**

### The mechanism: the 2 percent rule

`exceeds2pct170 / totsupp170` is the share of support excluded because it came
from donors each giving more than 2 percent of total support.

| | Near cliff (±5pt) | Typical (≥80% support) |
| --- | ---: | ---: |
| n | 2,308 | 80,940 |
| **Median share of support excluded** | **53.9%** | **0.0%** |
| Median revenue | $387,204 | $662,907 |
| Median assets | $1,266,282 | $829,810 |
| Median total support (5-yr) | $1,363,336 | $2,198,229 |

Correlation between public support % and share excluded by the 2% rule:
**−0.744**.

Near-cliff charities are **not smaller in a way that explains anything** — median
revenue $387k against $662k, same order of magnitude, and they hold *more* assets.
What separates them is donor concentration. This is the post's payoff.

#### CORRECTION — the near-cliff median is bimodal; do not quote it

**Found while rendering Figure 4, after this spec first claimed "near-cliff
charities have 53.9% of their support excluded."** That framing is wrong in
exactly the way [nobody's average](/posts/2026-07-14-nobodys-average.html) is
about. The near-cliff group is **bimodal** in donor concentration:

| Share of support excluded by the 2% rule | Near-cliff orgs |
| --- | ---: |
| 0–5% (essentially nothing excluded) | **29.5%** |
| 5–20% | 7.2% |
| 20–40% | 7.5% |
| **40–55% (where the median sits)** | **6.5%** ← the valley |
| **55–75%** | **49.2%** |
| ≥75% | 0.0% |

The median of 53.9% lands in the sparsest part of the distribution. It is a real
number and `compute.py` still asserts it, but **the post must not lean on it** —
it describes almost none of the group.

**The honest framing, which is also the stronger one:**

- **55.7%** of near-cliff charities have **≥40%** of their support excluded — the
  donor-concentration story, and it holds for a clear majority.
- **29.5%** have **<5%** excluded. Donor concentration does **not** explain these;
  they are near the line for other reasons (large non-public components in total
  support — investment income, gross receipts). **The post must say this**, not
  imply the 2% rule accounts for everyone.
- The contrast that carries the section: **86.0%** of *typical* charities have
  under 5% excluded, against 29.5% of near-cliff ones.

So: donor concentration is the **dominant** mechanism near the cliff, not the
**only** one. Say "most," never "the reason."

### The bright line and the judgment call — a null

An organization below 33⅓ may still qualify under the **facts-and-circumstances
test** if it is above **10 percent**. Same estimator at 10.0:

- displacement **+44.6**, z = **+1.73** against placebos at 5, 6, 7, 8, 13–18%
- but placebos at **5% (+45.5)** and **6% (+38.5)** are essentially as large

**This is a null and must be reported as one.** The honest sentence is "cannot be
distinguished from the placebos," never "we showed they don't respond." The
interpretation the data does support: 33⅓ is **arithmetic** — a line an
organization can compute and steer toward. The 10 percent floor gates a
**discretionary** judgment, and you cannot aim at a judgment call. Charities bunch
at the line they can calculate.

## Method notes that change the interpretation

**The ratio is a five-year measure, not an annual one.** `totsupp170` is total
support over the Schedule A Part II measuring period; it runs a median **3.70×**
a single year's revenue, consistent with a multi-year window rather than one year.
So the quantity that bunches is a **five-year aggregate** — much harder to nudge
than an annual figure. This makes the bunching more notable, not less, and the
prose should say so.

**`nonpfrea == 7` is nearly the whole population anyway.** Restricting from all
501(c)(3)s with a computable ratio (116,894) to code 07 (111,991) barely moves the
estimate, because the §170 support fields are only populated by organizations
using that test. Restrict anyway — it is the population the rule binds — but do
**not** claim the restriction sharpened the result. It didn't.

## Honesty and inference — the governing standard

Peter's standard, and it governs every sentence in this post: **assert nothing as
fact that we are unsure of.** Be transparent about exactly what was done
mathematically and what we believe it infers. Make no accusation of fraud or
wrongdoing. But do not whitewash either — if the analysis reasonably infers
something, state it as a reasonable conclusion, labelled as an inference from the
method rather than as an observation. We are scientists; if the methods or the
analysis are wrong, transparency about how the conclusion was derived is what
lets a reader catch it. **The reader decides.**

### What we observe, and what we do not

**We observe:** a displacement of ~80 organizations across the 33⅓ line — a
deficit below and an excess above — that survives 12 specifications, a bootstrap,
and 21 placebo thresholds. That is a measurement, and the post can state it
plainly.

**We do not observe the mechanism.** At least four processes produce an identical
signature in this data, and **our data cannot distinguish them**:

1. **Broadening the donor base.** An organization near the line recruits more
   small donors and crosses it. This is the rule working exactly as intended.
2. **Classification judgment at the margin.** Whether a gift is one donor or
   several, whether a grant is from a governmental unit (counted in full),
   whether a large gift qualifies as an excludable *unusual grant* — real
   judgment calls, legally available, that move the ratio.
3. **Timing.** Shifting when a large gift lands across the five-year measuring
   window.
4. **Misreporting.** Outright misstatement of the support figures.

All four yield a deficit below and an excess above. **Nothing in a single year of
as-filed aggregates separates them**, and the post must say so in the same breath
as the finding — not in a footnote.

### The inference we will state, and its limit

The honest inference the analysis supports, stated as inference: the response
concentrates at a threshold that is **arithmetic** (33⅓, computable from a
charity's own books) and is **not detectable** at the threshold that gates a
**discretionary** judgment (the 10% facts-and-circumstances floor). That contrast
is consistent with organizations *deliberately managing a number they can
compute*. That is a reasonable conclusion from how the analysis was carried out,
and it should be stated as one.

**Its limit, stated just as plainly:** "deliberately managing a number" spans
everything from lawful donor-broadening (mechanism 1 — the policy succeeding) to
misreporting (mechanism 4). **This analysis cannot tell you which, for any
organization or in aggregate**, and it is emphatically not evidence of wrongdoing
by anyone. What would distinguish them: panel data across filing years, and
Schedule B donor detail — neither of which is in this extract. Say that too.

The verbs are *steer*, *respond to*, *manage*. Never *dodge*, *game*, *cook*, or
*cheat*. Not because the benign reading is the true one — **we do not know that
either** — but because the accusatory verb asserts a mechanism the data does not
identify. The original draft of this spec claimed the bunching was "the rule
working as designed, not being gamed"; that was the same error pointing the other
way, and it is why this section exists.

### Two further constraints

1. **One year of filings; a multi-year rule.** The support ratio spans a five-year
   measuring period and reclassification follows sustained failure, not a single
   measurement. This extract is one filing year, so the post can show the
   **distribution** but can never show an organization actually losing public
   charity status, and must not imply it observed that.
2. **The 10% result is a null, not a finding.** The estimate is positive (+44.6)
   and noisy; placebos at 5% and 6% are just as large. The honest sentence is
   "cannot be distinguished from the placebos," never "we showed they don't
   respond." The bright-line/judgment-call inference above rests on this being
   *undetectable*, not on it being *zero* — and the prose must preserve that
   distinction, because the whole interpretation leans on it.

## Legal claims — verify before drafting, do not assert from memory

The post makes claims about tax rules. Each must be checked against an IRS source
and carry an inline link (nonprofit-series citation convention). **Do not write
these from memory:** the exact consequence of failing the test, the mechanics and
timing of reclassification as a private foundation, the precise operation of the
2 percent rule, and the facts-and-circumstances test's conditions. Anchor to
[IRS Publication 557](https://www.irs.gov/publications/p557) and the
[public support test guidance](https://www.irs.gov/charities-non-profits/exempt-organizations-annual-reporting-requirements-form-990-schedules-a-and-b-public-charity-support-test).
If a claim cannot be sourced, cut it — the finding does not depend on it.

## Structure — seven sections, deliberately tighter than the last post

1. **The rule.** The bright line and what falling below it risks. Sourced, linked.
2. **Almost nobody can see it.** Median 95.7%; 3.86% below; 670 within 1.5 points.
   Figure 2.
3. **It isn't about being unpopular — it's the 2% rule.** The payoff section, and
   the reason a reader who does not care about econometrics should keep reading.
   53.9% vs 0.0% excluded; correlation −0.744. Table 1.
4. **Do they steer?** The estimator, explained so a reader can follow the
   reasoning without taking it on trust: fit a counterfactual density to the
   region *excluding* a window around the line, then compare observed to
   counterfactual inside it. Missing below, excess above. Figure 1, Code 1.
   **Show the choices** — bandwidth, polynomial degree, window — and say they were
   fixed before the placebo test.
5. **Is it real?** The credibility section. Placebo 0/21, z = +3.77, bootstrap CI
   [+28, +129], 12 specifications spanning +47 to +95 (Table 2). Figure 3. Link
   the [downloadable script](/calcs/public-support-cliff/compute.py) here — the
   reader should be able to disagree with the specification and rerun it. State
   openly that a bunching estimator has researcher degrees of freedom and that the
   placebo test is precisely what disciplines them.
6. **How big? Depends what you divide by.** 0.072% or ~12%. Cross-link
   [nobody's average](/posts/2026-07-14-nobodys-average.html).
7. **What this does and does not show.** The bright line and the judgment call:
   the 10% null, and the inference it licenses — a response concentrated at the
   computable threshold and undetectable at the discretionary one, consistent with
   deliberate management of a number a charity can calculate. Then the limit, in
   the same breath: four mechanisms produce this signature, from lawful
   donor-broadening to misreporting, and **this analysis cannot distinguish them**;
   what would (panel data, Schedule B) is not in the extract. No accusation. The
   reader decides. Close + one-line caveat.

## Figures

Matplotlib, brand palette, lettered callouts only, captions carry the words.

- **Figure 1 — hero / OG card, exactly 1200×630.** Observed density around the
  cliff with the counterfactual overlaid: missing mass below, excess above, the
  line marked. The whole finding in one image.
- **Figure 2.** The full 0–100 support distribution, cliff marked — showing how far
  it sits from where charities actually live (median 95.7%).
- **Figure 3.** The placebo dot plot: real +80.1 against the 21 fake thresholds.
  The credibility figure; it is what earns the claim.
- **Figure 4.** Donor concentration — share of support excluded by the 2% rule,
  near-cliff versus typical.

**Table 1** — the near-cliff versus typical comparison from §The mechanism.

**Table 2** — the full specification grid: all 12 combinations of bandwidth and
polynomial degree, with their displacements (+46.9 to +95.4). **Publishing the
grid is the point.** A reader who suspects the headline number was the flattering
pick from a pile of specifications can see the whole pile, including the coarse
bins that attenuate it to +47. Do not report only the favourable cells.

**Code 1** — the support ratio and the displacement statistic, with the
bandwidth/degree/window choices visible rather than buried.

## Artifacts

- `calcs/public-support-cliff/compute.py` — reproduces and **asserts** every value
  in §Verified findings; writes an all-numeric intermediate.
- `calcs/public-support-cliff/figures.py` — four PNGs.
- `posts/2026-07-15-public-support-cliff.md`
- `images/2026-07-15-public-support-cliff-{hero,distribution,placebo,concentration}.png`
- `lib/Blog/Site.hs` — one new rule publishing the analysis scripts (below).

## Code availability — a requirement, not a courtesy

Peter's instruction: **save the code we used and make it available for download.**
For a post whose entire claim rests on a specification a reader cannot see from
the prose, publishing the script *is* the argument. A reader must be able to
download the exact code, disagree with the bandwidth, rerun it, and get a
different answer if we are wrong.

**Site change.** `lib/Blog/Site.hs` currently copies static assets with the
pattern at `images/*` (`route idRoute`, `compile copyFileCompiler`). Add one rule
in the same style:

```haskell
match "calcs/*/*.py" $ do
    route   idRoute
    compile copyFileCompiler
```

**Scope it exactly this way — `calcs/*/*.py`, not `calcs/**`.** The glob must
match only Python scripts one directory deep. `calcs/**` would sweep in
`calcs/data/24eoextract990.csv` (247 MB) and every `.csv.gz` intermediate, which
would bloat the deploy and publish derived data we deliberately leave untracked.

This makes every analysis script reachable at
`https://blog.noprofits.org/calcs/<post>/compute.py`, and retroactively publishes
the scripts behind the earlier posts (`below-zero/`, `who-pays/`,
`months-of-cash-at-scale/`) at no extra cost.

**Post requirement.** The methods section must link **directly to the downloadable
scripts** — `/calcs/public-support-cliff/compute.py` and `figures.py` — not merely
mention that a repository exists. The reader should be one click from the code.
Name the data source and its URL so the input is obtainable too.

**Verification.** The build check must confirm the scripts landed in `_site/` and
that no `.csv`/`.csv.gz` came with them.

## Environment — learned the hard way on the last post

**No single interpreter on this machine has both pandas and matplotlib.** This is
not a preference; it is why the sibling `figures.py` scripts are numpy-only.

- `compute.py` → `python3` (the `gwc` venv: pandas, numpy, **no** matplotlib)
- `figures.py` → `/opt/homebrew/Caskroom/miniforge/base/envs/qchem/bin/python`
  (matplotlib, numpy, **no** pandas) — read the intermediate with
  `np.genfromtxt`, so **every column it writes must be numeric**.

Intermediates stay **untracked**, matching `calcs/below-zero/` and
`calcs/who-pays/`, which track only their scripts.

## Conventions

Binding: `notes/blog-authoring.md` in full. Frontmatter `tags: nonprofits, data`;
**no `author` field**; `og-image` → the hero; title quoted if it contains a colon.
Inline links only — no `[@key]`, no reference list, no footnotes, nothing appended
to `bib/bibliography.bib`. Site-relative links. Prose over bullets. Every figure,
table, and code block gets a bold numbered caption **and** a by-number reference in
the prose. **Verify the rendered page in a browser** — the last post shipped a
green build with a code block overflowing its container, and only looking caught it.

## Delivery

Branch `post/public-support-cliff`. `stack build && stack exec blog build`, verify
the rendered page, PR into `main`. Never commit to `main`. Do not merge without
Peter.

## Open risks

- **The estimator is a researcher-degrees-of-freedom machine.** Bandwidth, degree,
  and window were chosen before the placebo test, and the placebo is what makes
  the result credible. If drafting tempts a "better" specification that raises the
  number, that is p-hacking — the spec's numbers stand.
- **The result is small in absolute terms** (~80 organizations). The post must not
  inflate it. The ~12 percent framing is legitimate only with its denominator
  stated in the same sentence.
- **Section 3 must not become a fundraising-advice column.** The 2% rule is the
  mechanism, not a how-to for engineering a support ratio.
- **The comfortable reading is as much an assertion as the accusatory one.** This
  spec originally declared the bunching benign ("the rule working as designed").
  That was unsupported. Neither the charitable nor the suspicious mechanism is
  identified by this data, and a draft that quietly settles into either has
  asserted something we do not know. The finding is the displacement; the
  mechanism is open.
- **Publishing the code raises the stakes on the code.** Once
  `/calcs/public-support-cliff/compute.py` is a URL in the post, it is part of the
  argument and will be read as such. It must run standalone against the named
  extract, assert its own numbers, and carry a docstring stating the data source,
  the filters, and the specification choices. Sloppy code is now a published
  error, not a private one.
