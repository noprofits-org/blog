---
title: "How many months of cash? Computing a nonprofit's real reserve from the 990"
date: 2026-07-06
tags: nonprofits, data
description: The resilience number every donor should check — months of operating reserve — isn't printed anywhere on the Form 990, but four lines of the balance sheet compute it. How to do the arithmetic honestly, what the sector's distribution actually looks like, and why half of American nonprofits are three bad months from a crisis.
og-image: /images/2026-07-06-months-of-cash-hero.png
figure: '<img src="/images/2026-07-06-months-of-cash-hero.png" alt="A nonprofit runway gauge: a fuel-style dial reading in months of cash, sitting on a balance sheet, with a thin danger zone below three months.">'
figlabel: The number the form never prints
figcaption: Months of operating reserve — the single best resilience measure — has to be computed from the 990 balance sheet; the form itself never states it.
---

The most important number on a nonprofit's balance sheet is one the form never prints. The [donor's guide](/posts/2026-07-05-how-to-vet-a-charity.html) in this series called **months of operating reserve** "the resilience number" and gave the thirty-second version of the calculation; the [overhead-myth post](/posts/2026-07-06-the-overhead-myth.html) argued that the question "does it hold a real reserve?" should replace the question donors usually ask. Both posts left the actual arithmetic as a promissory note. This is that post: which lines of the [Form 990](https://www.irs.gov/forms-pubs/about-form-990) go into the number, the three corrections that separate the honest version from the naive one, and what the distribution across the sector looks like — which turns out to be the most alarming statistic in nonprofit finance.

## The question the number answers

If every donation stopped tomorrow, how long could the organization keep delivering its mission before the lights went out? That's all "months of reserve" means: expendable resources divided by monthly spending. It is the nonprofit equivalent of a startup's runway (Figure 1), and it's the first thing I compute for any organization I'm evaluating — before the program ratio, before compensation, before anything on the statement of activities. Income statements tell you how a year went. The reserve tells you whether the organization survives a *bad* year.

<figure>
  <img src="/images/2026-07-06-months-of-cash-hero.png" alt="A nonprofit runway gauge: a fuel-style dial reading in months of cash, sitting on a balance sheet, with a thin danger zone below three months.">
</figure>

**Figure 1.** The number the form never prints: months of operating reserve read like a fuel gauge, with the danger zone below the three-month line — the line half the sector sits under.

The naive version takes thirty seconds with two numbers: **net assets** (assets minus liabilities, the bottom of Part X) divided by **total expenses** (Part I, line 18), times twelve. That's the screen the donor's guide taught, and as a screen it's fine. But the naive version flatters almost every organization, sometimes wildly, because net assets include money the org can't spend and things that aren't money at all. Getting to the honest number takes three corrections, each one a single line on the same form.

## Correction one: restricted money isn't yours

Since the 2018 revision of the form, Part X splits net assets into two lines: **line 27, net assets without donor restrictions**, and **line 28, net assets with donor restrictions**. Line 28 is money a donor has fenced off — for a specified purpose, after a specified date, or permanently, as with an endowment corpus. An organization with \$10M of net assets, \$9M of it a donor-restricted endowment, does not have eight years of runway; it has whatever line 27 says it has, and the endowment can sit untouchable while the org misses payroll. So the honest calculation starts from line 27 only. (One nuance cuts the other way: funds the *board* has set aside — a board-designated reserve or quasi-endowment — still count as unrestricted and still sit in line 27, because the board can undesignate them by the same vote it used to designate them. A donor's restriction is law; a board's restriction is a policy.)

## Correction two: a building is not a reserve

Line 27 still isn't spendable, because net assets include the org's fixed assets. A food bank that owns its \$2M warehouse outright shows that warehouse in net assets, but it cannot pay staff with a loading dock. So subtract **land, buildings, and equipment** — Part X, line 10c, already net of accumulated depreciation — and add back the debt that finances them (**line 23**, secured mortgages and notes payable), since a mortgaged building ties up less of your equity than an owned one. What's left is close to what accountants call *expendable* or *liquid* unrestricted net assets: resources that are actually available, in cash or things that become cash, to absorb a shock. This is the numerator the [Nonprofit Operating Reserves Initiative](https://www.nonprofitaccountingbasics.org/nonprofit-reserves) (NORI) — a volunteer workgroup of sector accountants convened in 2008 to standardize exactly this ratio — built its definition around.

## Correction three: divide by cash expenses

The denominator needs one fix too. Total expenses (Part I line 18, which equals Part IX line 25) include **depreciation** — Part IX, line 22 — which is an accounting recognition of wear, not a check anyone writes. An organization weathering a crisis has to cover payroll and rent; it does not have to cover depreciation. Subtract line 22 from total expenses before dividing. For most small organizations this moves the answer by a few percent; for anyone who owns a building it can move it by a month or more.

The whole recipe, then, in Table 1:

| Step | Form 990 location |
| --- | --- |
| Start with net assets without donor restrictions | Part X, line 27 |
| Subtract fixed assets, net | Part X, line 10c |
| Add back the debt secured by them | Part X, line 23 |
| Divide by (total expenses − depreciation) ÷ 12 | Part I line 18; Part IX line 22 |

**Table 1.** Months of operating reserve from four lines of the 990. The result is expendable resources over monthly cash spending — the org's runway.

Run it on the food bank from the [thirteen-year walkthrough](/posts/2026-06-17-reading-a-food-banks-990.html): roughly \$549K of net assets against \$1.27M of annual expenses in fiscal 2023 gave the naive answer of about five months, and because the org rents rather than owns and holds almost nothing restricted, the honest answer lands in the same place. That's the reassuring case. The corrections matter precisely for the organizations where the naive number looks best — the ones with buildings and endowments padding the balance sheet.

## How thin the sector actually runs

Benchmark first: the [NORI workgroup's suggested floor](https://www.nonprofitaccountingbasics.org/nonprofit-reserves) is an operating reserve ratio of **25 percent — about three months** — at the lowest point of the year, with the explicit caveat that there is no one-size-fits-all number and every board should set its own policy. Three to six months is the range most advisors, including the [National Council of Nonprofits](https://www.councilofnonprofits.org/running-nonprofit/administration-and-financial-management/operating-reserves-nonprofits), treat as healthy for an operating charity.

Now the distribution. In the Nonprofit Finance Fund's [2025 State of the Nonprofit Sector Survey](https://nff.org/state-of-the-nonprofit-sector-survey/2025-state-of-the-survey-nonprofit-sector-survey/) of over 2,200 organizations, **52 percent reported three months or less of cash on hand, and 18 percent had one month or less** — and 36 percent ended 2024 with an operating deficit, the worst figure in the survey's ten-year history. This is not a new pathology: back in 2009 an Urban Institute study of Washington-area charities, [computed from these same 990 balance-sheet fields](https://www.urban.org/research/publication/washington-area-nonprofit-operating-reserves), found 57 percent below the three-month line. Half the sector has been living hand-to-mouth for at least fifteen years.

And yet [BDO's 2024 benchmarking survey](https://www.businesswire.com/news/home/20241003329446/en/Embracing-transformation-BDOs-2024-Nonprofit-Standards-Benchmarking-Survey) found that **62 percent of nonprofits hold more than seven months** of reserves. Both numbers are real; the populations differ.

<figure>
  <img src="/images/2026-07-06-months-of-cash-barbell.png" alt="The sector's reserves form a barbell: in NFF's 2025 survey of mostly small community nonprofits, 52 percent hold three months of cash or less and 18 percent hold one month or less, while BDO's 2024 survey of 250 larger established organizations finds 62 percent holding more than seven months of reserves.">
</figure>

**Figure 2.** The reserves barbell: NFF's 2025 respondents — mostly the small community organizations that dominate the sector by count — stand on thin ice, while BDO's 250 larger established organizations sit on real capital.

BDO surveyed 250 leaders of established organizations — universities, grantmakers, large public charities — while NFF's respondents skew toward the small community organizations that make up most of the sector by count. Read together they describe a barbell (Figure 2): a well-capitalized top end sitting on comfortable reserves, and a long tail of small orgs one bad quarter from insolvency. Which is exactly why you compute the number for *your* charity instead of trusting any sector average.

## Reading the answer

The donor's guide said both extremes are informative, and the reserve is where that advice bites. Near zero, the org is fragile — common for young organizations, forgivable, but you should know before you give whether you're funding a program or a rescue. Past a year or two of reserve, ask the opposite question: is this a prudent quasi-endowment with a board policy behind it, or money idling while the mission waits? The 990 helps here too — a board-designated endowment shows up in Schedule D, and an org with a real reserve *policy* will usually say so in its audited statements. And remember the lesson of the [overhead-myth post](/posts/2026-07-06-the-overhead-myth.html): a reserve is precisely the kind of organizational capacity the overhead fixation punishes. An org that builds one is doing the responsible thing even though no watchdog ratio rewards it — the starvation cycle runs on donors mistaking thin margins for virtue.

## Do it at scale, or let the machines do it

Everything above is four fields per filing, which means it automates. The [ProPublica Nonprofit Explorer](https://projects.propublica.org/nonprofits/) API returns Part X and Part IX line items for every electronically filed 990, and the earlier technical posts in this series — [mapping the IRS 990 dataset](/posts/mapping-the-irs-990-data.html) and [extracting its financial fields computationally](/posts/automating-IRS-Form-990-Data-Extraction-A-Computational-Approach.html) — are, read in this light, the plumbing for exactly this calculation across every charity at once. The [search tools at noprofits.org](https://search.noprofits.org) pull these same figures and put them next to each other, which is the whole point: the runway number nobody prints is sitting in public data, four arithmetic operations away, for every tax-exempt organization in America. Compute it before you give.

<small>This is a plain-language overview, not tax, legal, or financial advice. The line numbers above are for the post-2018 Form 990; older filings split net assets across three lines (unrestricted, temporarily restricted, permanently restricted), with line 27 as the unrestricted figure. Survey figures are as published by NFF (2025), BDO (2024), and the Urban Institute (2009) and describe different populations; example figures are from IRS Form 990 filings via the ProPublica Nonprofit Explorer API, as-filed and unaudited.</small>
