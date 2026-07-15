---
title: "One-third: the cliff a few hundred charities steer around"
date: 2026-07-15
tags: nonprofits, data
description: "There is a bright line in the tax code: draw less than a third of your support from the public and you stop being a public charity. Almost no charity can see it — the median sits at 96 percent. But among the few hundred close enough to see it, the distribution bends, and it bends at the number they can compute."
og-image: /images/2026-07-15-public-support-cliff-hero.png
---

Most tax rules are dials. You pay a little more, you deduct a little less, the
consequence scales with the number. A few are not dials. A few are cliffs, where
one side of a line means one thing and the other side means something else
entirely, and the difference between 33.2 and 33.4 is the difference between two
regimes.

The [public support test](https://www.irs.gov/charities-non-profits/exempt-organizations-annual-reporting-requirements-form-990-schedules-a-and-b-public-charity-support-test)
is a cliff. Economists have a prediction about what people do at cliffs, and the
prediction is testable, and the [IRS publishes the data](https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data)
to test it with. This post runs the test. The answer is yes — measurably,
robustly, and about eighty organizations' worth (Figure 1).

<figure>
  <img src="/images/2026-07-15-public-support-cliff-hero.png" alt="Histogram of charities by public support percentage from 24 to 44 percent, with a dashed counterfactual curve. The bars in the one and a half points below the 33 percent line sit below the curve; the bars just above the line sit above it, jumping from about 99 charities to about 132 across the line.">
</figure>

**Figure 1.** The bend, which the rest of this post is about. Charities by public
support, with **A** the one-third line and **D** a counterfactual density fitted to
the neighbourhood *excluding* the shaded window. **B**, the bins in the 1.5 points
below the line, sit *under* the counterfactual — 280 organizations where 331 were
expected. **C**, the bins just above, sit *over* it — 399 where 370 were expected.
The last bin below the line holds 99 charities; the first bin above holds 132. Same
asset as the social card.

## The rule

A charity that wants to be treated as a **public charity** rather than a private
foundation generally has to show the public actually supports it. One of the
routes — the one most donation-funded charities take — is the support test under
§170(b)(1)(A)(vi): the organization must "receive at least one-third of its
support from contributions from the general public," a figure
[measured over a five-year period](https://www.irs.gov/charities-non-profits/exempt-organizations-annual-reporting-requirements-form-990-schedules-a-and-b-public-charity-support-test)
covering the current and four prior tax years.

Miss it and there is one more chance: the
[10 percent facts-and-circumstances test](https://www.irs.gov/charities-non-profits/exempt-organizations-annual-reporting-requirements-form-990-schedules-a-and-b-facts-and-circumstances-public-support-test),
for organizations above 10 percent but below a third, which requires showing that
"under all the facts and circumstances, it normally receives a substantial part of
its support from governmental units or the general public." Hold that phrase — it
matters later. Miss both, and per the
[Schedule A instructions](https://www.irs.gov/instructions/i990sa) the
organization "is a private foundation as of the beginning of the … tax year for
filing purposes."

That reclassification is not cosmetic. Private foundations pay an
[excise tax on net investment income](https://www.irs.gov/charities-non-profits/private-foundations/tax-on-net-investment-income),
face a
[mandatory annual payout](https://www.irs.gov/charities-non-profits/private-foundations/taxes-on-failure-to-distribute-income-private-foundations)
enforced by a 30 percent tax on income they fail to distribute, and — this is the
one that stings — their donors generally deduct up to
[30 percent of adjusted gross income instead of 50](https://www.irs.gov/publications/p526).
The organization keeps doing exactly what it did the day before. Its donors just
get a worse deal for doing it.

So: a bright line, a real penalty, and a number every charity computes about
itself. That is the setup for one of the most-studied phenomena in public
economics — **bunching**. If a threshold matters, and people can see where they
stand relative to it, the distribution around it stops being smooth. Organizations
that would have landed just below turn up just above instead.

## Almost nobody can see it

Before testing that, a deflating fact.

<figure>
  <img src="/images/2026-07-15-public-support-cliff-distribution.png" alt="Distribution of public support across 111,991 charities. A tall spike sits at 95 to 100 percent, the bulk of the sector. The 33 percent cliff is marked far to the left, in a nearly empty stretch of the distribution.">
</figure>

**Figure 2.** The cliff and the crowd. Public support for all 111,991 charities
using this test: **A** marks the one-third line; **B** marks the median, at 95.7
percent. Almost the entire sector lives in the right-hand spike, several dozen
points from the line that supposedly disciplines it.

This post looks at the **111,991** organizations that declare the
§170(b)(1)(A)(vi) test on Schedule A and report a computable support ratio. The
median one draws **95.7 percent** of its support from the public. Only **4,323**
of them — **3.86 percent** — sit below the one-third line at all. Only **670**,
six-tenths of one percent, are within a point and a half of it.

For the overwhelming majority of American charities, the public support test is
not a constraint. It is scenery. They clear it by sixty points without thinking
about it, the way you clear a speed limit while parked.

Which means anything we find at the cliff is a fact about a very small
neighbourhood — and Figure 2 is worth remembering when we get to the size of the
effect.

## It isn't about being unpopular — it's the 2 percent rule

Here is the part I did not expect, and the part worth a reader's time even if
bunching estimators leave them cold.

You would assume a charity near the one-third line is one the public doesn't much
support. Unloved, struggling to raise money. That is not what the data says, and
Table 1 is the refutation. The near-cliff charities are not smaller in any way that
explains their position — median revenue **$387,204** against **$662,907** for
typical charities, the same order of magnitude, and they actually hold *more*
assets ($1,266,282 against $829,810).

What separates them is **who** gave, not how much.

The support test does not count all contributions as public. Per the
[Schedule A instructions](https://www.irs.gov/instructions/i990sa), when one
donor's gifts across the five-year window exceed **2 percent of total support**,
only the first 2 percent counts toward the public's share; the excess is stripped
out. And "one donor" is construed broadly — "all contributions made by a donor and
by any person or persons standing in a relationship to the donor … will be treated
as made by one person," so a family or a related company cannot split a gift into
smaller pieces.

The consequence is that the test measures **breadth, not amount**. A charity that
raises $2 million from four devoted donors can fail it. A charity that raises
$50,000 from six hundred people sails through. The rule is not asking how much you
raised. It is asking how many people you raised it from.

<figure>
  <img src="/images/2026-07-15-public-support-cliff-concentration.png" alt="Two overlaid distributions of the share of support excluded by the 2 percent rule. Typical charities pile at zero, with almost nothing excluded. Charities near the cliff are split: a group at zero and a much larger group with 55 to 75 percent of their support excluded.">
</figure>

**Figure 3.** Where the cliff-dwellers come from. Share of support stripped out by
the 2 percent rule: **A**, typical charities (support ≥ 80 percent), 86.0 percent
of which have under 5 percent excluded; **B**, the second mode among near-cliff
charities, half of which have 55–75 percent of their support excluded because it
came from too few people.

| | Near the cliff (±5 pt) | Typical (support ≥ 80%) |
| --- | ---: | ---: |
| Organizations | 2,308 | 80,940 |
| **Under 5% of support excluded** | **29.5%** | **86.0%** |
| **40% or more excluded** | **55.7%** | 4.1% |
| Median revenue | $387,204 | $662,907 |
| Median total assets | $1,266,282 | $829,810 |

**Table 1.** Near-cliff charities against typical ones. They are not smaller. They
are narrowly funded: a majority have at least 40 percent of their support
disqualified by the 2 percent rule, against a sector where seven-eighths have
essentially none.

Across all 111,991 organizations, the correlation between public support and the
share stripped by the 2 percent rule is **−0.744**. That is most of the story of
who stands near the cliff.

**But not all of it, and Figure 3 shows why.** The near-cliff group is *bimodal*:
**55.7 percent** have 40 percent or more of their support excluded — the donor
concentration story — while **29.5 percent** have essentially *nothing* excluded.
Those organizations are near the line for other reasons entirely: their total
support includes large non-public components that dilute the ratio from the other
direction. Donor concentration is the **dominant** mechanism near the cliff. It is
not the only one, and the median of that bimodal group (53.9 percent) lands in a
valley holding just 6.5 percent of it — a number describing almost no one, which is
[a mistake this series has written about](/posts/2026-07-14-nobodys-average.html)
and very nearly repeated here.

## Do they steer?

Now the test. If the line changes behaviour, the distribution should be *missing*
organizations just below it and *carrying extra* just above.

To say "missing" and "extra" you need a counterfactual: what would the
neighbourhood look like if the line weren't there? The standard approach (Code 1)
is to fit a smooth curve to the density **excluding** a window around the
threshold, and then ask that curve what the window should have held.

```python
# Bin width, polynomial degree, window half-width.
# Frozen before the placebo test was run.
BW, DEG, W = 0.5, 5, 1.5

# Fit the density OUTSIDE a window around the line, then ask
# that curve what the window should have held.
excl = (mid > CLIFF - W) & (mid < CLIFF + W)
cf = np.polyval(np.polyfit(mid[~excl], cnt[~excl], DEG), mid)

displacement = (observed_above - cf_above) + (cf_below - observed_below)
```

**Code 1.** The estimator, with its three arbitrary choices made in public: bin
width, polynomial degree, and window. The [full script](/calcs/public-support-cliff/compute.py)
is downloadable, and Table 2 reports what happens when the first two are changed.

That is the dashed curve in Figure 1, and the two shaded regions are the answer.
Below the line, 280 organizations where the curve expects 331 — **15.5 percent
missing**. Above it, 399 where the curve expects 370 — **7.8 percent extra**.

Both halves of the signature are there, and both matter. An excess above the line
alone could be a lump of organizations that genuinely belong there. A deficit below
paired with an excess above is **displacement** — the shape you get when
organizations move across a line rather than pile onto it. Widen or narrow the
window and it persists: a 16.3 percent deficit and 10.8 percent excess at ±1
point, 12.6 and 6.8 at ±2.

Adding the two halves together gives the headline: **about 80 organizations**
sitting above the line that the smooth curve says should be below it.

One thing worth knowing before you decide how impressed to be. The ratio being
bent here is **not one year's fundraising** — it is a five-year aggregate, running
a median 3.70 times a single year's revenue. Whatever is happening, it is not a
charity nudging one year's books. It is a five-year total that ends up on the
right side of a line.

## Is it real?

Eighty organizations out of 111,991 is a small number extracted from a wiggle in a
curve, using a method with three arbitrary choices in it. Healthy scepticism says:
you can find a wiggle anywhere if you look with a flexible enough curve.

Correct. So here is the check that matters, and it is the one that earns everything
above — run the identical estimator at thresholds where **no rule exists**. If the
method manufactures 80-organization bumps out of noise, it will manufacture them at
27 percent and 41 percent too. Figure 4 runs it at 21 of them.

<figure>
  <img src="/images/2026-07-15-public-support-cliff-placebo.png" alt="Displacement estimated at 22 fake thresholds and the real one. The 21 placebo thresholds scatter between minus 55 and plus 35 organizations around zero. The real one-third cliff sits alone at plus 80.">
</figure>

**Figure 4.** The test that earns the claim. **A** is the real cliff, +80.1
organizations. **B** is the largest of 21 placebo thresholds from 22 to 48 percent,
at +35.0. The placebos scatter around zero (mean −4.2); the real one does not sit
among them.

The placebos average **−4.2** with a standard deviation of **22.4**. The real cliff
is **+80.1** — **3.77 standard deviations** above the placebo distribution, and
**not one of the 21** reaches it. Bootstrapping the estimate over 400 resamples
gives a 95 percent interval of **[+28, +129]**, with zero of the 400 landing at or
below nothing.

And because the specification is the obvious place to hide a thumb:

| Bin width | deg 3 | deg 4 | deg 5 | deg 6 |
| --- | ---: | ---: | ---: | ---: |
| **0.25 pt** | +95.4 | +93.0 | +86.5 | +85.8 |
| **0.5 pt** | +88.9 | +87.0 | **+80.1** | +79.7 |
| **1.0 pt** | +56.9 | +46.9 | +48.5 | +47.7 |

**Table 2.** Every specification tried, not the flattering ones. All 12 give a
positive displacement, from **+46.9 to +95.4**; the bolded cell is the one reported
above. Coarse 1-point bins attenuate the estimate by roughly half — expected, since
a 1.5-point window smeared across 1-point bins blurs the very thing being measured.

The reported specification (0.5-point bins, degree 5, ±1.5) was fixed **before** the
placebo test was run, which is the only reason the placebo test means anything —
choosing the specification after seeing which one maximises the answer is how you
get a result that replicates in nobody else's hands. The
[whole script is downloadable](/calcs/public-support-cliff/compute.py), including
the [figure code](/calcs/public-support-cliff/figures.py); the bootstrap seed is
pinned so the interval above comes out the same on your machine. Disagree with the
bandwidth, change it, and see what you get.

## How big? It depends what you divide by

Eighty organizations. Out of 111,991 charities, that is **0.072 percent** —
seven-hundredths of one percent. A rounding error. Nothing.

Except: how many charities could possibly respond to this line? From Figure 2, only
**670** are within a point and a half of it. Everyone else is at 96 percent, sixty
points clear, with nothing to respond to. Measured against the organizations that
can actually see the cliff, eighty is around **12 percent**.

Same eighty organizations. Same data. One denominator says a rounding error, the
other says one in eight. This is the [previous post in this series](/posts/2026-07-14-nobodys-average.html)
arriving somewhere new: the number was never the argument, the denominator was, and
a statistic that won't tell you what it divided by isn't telling you anything. The
honest sentence names both — *eighty organizations, which is a twelfth of those
close enough for the rule to reach.*

## What this does and does not show

Recall the second chance from the first section: a charity below one-third can
still qualify under the facts-and-circumstances test, by showing that "under all
the facts and circumstances, it normally receives a substantial part of its
support" from the public. That test has a 10 percent floor. So the same rule
contains a second threshold — and it is a threshold of a completely different kind.
One-third is **arithmetic**: a charity computes it from its own books and knows
exactly where it stands. The 10 percent floor gates a **judgment**, weighed by
someone else, on the totality of the circumstances.

Run the same estimator at 10 percent and it returns **+44.6** — which looks like
something until you put it beside its own placebos. Fake thresholds at 5 and 6
percent return **+45.5** and **+38.5**. The whole low-support region is noisy at
this sample size, and the 10 percent estimate is **1.73 standard deviations** out —
indistinguishable from the noise around it. **That is a null, and it should be read
as one**: not evidence that nobody responds to the facts-and-circumstances test,
just an absence of evidence that they do.

With that caveat sitting in plain view, the inference this analysis supports is
narrow and worth stating precisely. **The response is concentrated at the threshold
charities can calculate, and undetectable at the threshold that turns on someone
else's judgment.** That is what you would expect if organizations are deliberately
managing a number they can compute — you cannot aim at a facts-and-circumstances
determination the way you can aim at a fraction. It is a reasonable conclusion from
the way this analysis was carried out, and it is an inference, not an observation.

Now the limit, which deserves as much prominence as the finding. **We do not
observe the mechanism, and this data cannot identify it.** At least four
different processes produce exactly the signature in Figure 1:

1. **Broadening the donor base** — an organization near the line recruits more
   small donors and crosses it. This is the rule doing precisely what it was
   written to do.
2. **Classification judgment** — whether a grant comes from a governmental unit
   (counted in full), whether two gifts are one donor or two, whether a large gift
   qualifies as an excludable unusual grant. Real judgment calls, legally
   available, that move the ratio without moving a dollar.
3. **Timing** — when a large gift lands inside a five-year window that rolls.
4. **Misreporting** — the support figures simply being wrong.

Every one of them puts a deficit below the line and an excess above it. One year of
as-filed aggregates, which is what this extract is, **separates none of them**. So
this post is not in a position to tell you that charities are gaming the public
support test, and it is not telling you that. It is equally not in a position to
tell you the bunching is all benign donor-broadening — that would be just as much
an assertion about a mechanism nobody here has measured. What would actually
distinguish them: following the same organizations across filing years, and the
Schedule B donor detail that says who gave what. Neither is in this file. Both
exist.

What is left is a measurement, and it is a real one: at a line in the tax code
where the arithmetic bites, the distribution of American charities has a bend in
it, and the bend is not there at 27 percent or 41 percent. Around eighty
organizations, one in twelve of those close enough to see the line, are on the
comfortable side of it when a smooth curve says they should not be. Why they are
there is a question this data cannot answer, and you now have the same numbers I do
— [the script](/calcs/public-support-cliff/compute.py), the specification grid, and
the placebos. Draw your own conclusion.

If you are looking at one specific organization rather than a hundred thousand,
none of this transfers: an aggregate bend says nothing whatever about any
individual charity, including one sitting at 34 percent. The
[search tools at noprofits.org](https://search.noprofits.org) and the
[ProPublica Nonprofit Explorer](https://projects.propublica.org/nonprofits/) will
show you its Schedule A, which is where its own answer lives.

<small>This is a plain-language overview, not tax, legal, or financial advice.
Figures are computed from the IRS SOI annual extract of Form 990 data (returns
filed in calendar year 2024, mostly fiscal 2023), as-filed and unaudited;
organizations filing the 990-EZ or 990-N are not included. The population is the
111,991 filers declaring the §170(b)(1)(A)(vi) test with a support ratio
computable from the extract. The analysis script
(<a href="/calcs/public-support-cliff/compute.py">calcs/public-support-cliff/</a>
in this site's repository) contains the full method, asserts every number in this
post, and pins its random seed. The bunching estimate is an aggregate statistical
result and is not evidence of wrongdoing by any organization; as described above,
this analysis cannot identify the mechanism behind it and makes no claim about
any individual filer.</small>
