---
title: How to actually vet a charity before you donate
date: 2026-07-05
tags: nonprofits, data
description: A donor's guide to the four numbers on a Form 990 that actually tell you whether a charity is run well — where to find each one, what a healthy range looks like, and the trap hiding in every one of them.
---

Say you're about to give money to a charity, and for once you want to check under the hood first. The good news is that the data exists: every tax-exempt organization in the US files a [Form 990](https://www.irs.gov/forms-pubs/about-form-990), and every one of those returns is public. The bad news is that the 990 is a fourteen-page federal form, and nobody hands you a key to it.

You don't need the whole form. You need four numbers, and — more importantly — you need to know the trap hiding in each one, because every single one of these can be gamed or misread. This is part of a short series on reading nonprofits from the outside — it helps to first know [what kind of tax-exempt organization you're looking at](/posts/2026-07-05-501c3-vs-c4-vs-c6.html), and a companion post walks through [one food bank's returns across thirteen years](/posts/2026-06-17-reading-a-food-banks-990.html). Here I want to give you the general skill instead of one worked example.

## 1. The program expense ratio

**What it is.** Of every dollar the organization spent, how much went to the actual mission versus overhead (management and fundraising)?

**Where to find it.** Part IX, the statement of functional expenses. It splits every expense line into three columns: program services, management and general, and fundraising. Divide the program column total by total expenses.

**Healthy range.** As a rule of thumb, 65–75% or higher on program is considered fine. The BBB Wise Giving Alliance draws its line at 65%; Charity Navigator has historically wanted to see 70%+. Below ~60% and you should at least ask why.

**The trap.** This is the single most abused number in the sector, and it cuts both ways. Organizations know donors fixate on it, so they classify aggressively — a chunk of the CEO's salary gets booked as "program," a fundraising gala gets called "public education." Meanwhile a genuinely well-run org that invests in staff, systems, and evaluation can post a *lower* program ratio and be the better charity. A suspiciously high ratio (95%+) is often a sign of creative accounting or an org too small to have real infrastructure, not virtue. Accounting researchers have made this point for years — Daniel Tinkelman's work on fundraising ratios found [these numbers are weak predictors of the things donors actually care about](https://doi.org/10.1177/0148558X0602100406). Treat this number as a screen, never a verdict. (There's a whole "overhead myth" argument here that deserves its own post.)

## 2. Months of operating reserve

**What it is.** If donations stopped tomorrow, how long could the organization keep the lights on? This is the resilience number, and it's the one I look at first.

**Where to find it.** Part X gives you net assets (assets minus liabilities). Focus on the *unrestricted* portion — money not locked up by a donor's designation. Divide that by annual expenses (Part I, line 18) and multiply by twelve to get months of runway.

**Healthy range.** Three to six months of unrestricted reserve is the common benchmark for a stable operating charity.

**The trap.** Both ends are informative. Near-zero reserve means the org is one bad quarter from a crisis — common, and not disqualifying for a young or growing group, but worth knowing. At the other end, an org sitting on *years* of reserve while running annual fundraising appeals is a different question entirely: is that a prudent endowment, or money that could be doing work now? Neither extreme is automatically wrong; both should make you ask a follow-up.

Take the food bank from the companion post. In fiscal 2023 it held about \$549K in net assets against \$1.27M in expenses — roughly five months of runway. That's squarely in the healthy band, and notably it held even after the org ran a deliberate deficit that year to keep pandemic-era staff on. That's what a reserve is *for*.

## 3. Fundraising efficiency

**What it is.** How much does it cost the organization to raise a dollar?

**Where to find it.** Take the fundraising column from Part IX and divide it by total contributions (Part VIII). If it costs \$0.15 to raise \$1.00, your efficiency is 15%.

**Healthy range.** Under ~20% is generally healthy; the BBB standard says fundraising costs shouldn't exceed 35% of related contributions. Mature donor bases run cheaper; a young org building its list will spend more per dollar and that's expected.

**The trap.** Fundraising cost is lumpy and lagged. A big investment in donor acquisition this year pays off over the next five, so a single year can look terrible in isolation. And, like the program ratio, the *category* is soft — spend gets shuffled between "fundraising" and "program" depending on how flattering the org wants the picture to be. Read it as a trend across several years, not a snapshot.

## 4. Executive compensation in context

**What it is.** What the organization pays its leadership.

**Where to find it.** Part VII lists officers, directors, and highest-paid employees with their reported compensation. Schedule J has the detail for the big numbers.

**Healthy range.** There isn't a universal one — and that's the point. A \$400K salary is unremarkable at a \$200M hospital system and alarming at a \$1M community nonprofit. Judge it against the organization's *budget* and against comparable orgs of similar size and mission, not against your gut.

**The trap.** Compensation is the number outrage-farms love, precisely because the absolute figure is meaningless without the denominator. Running a large, complex nonprofit is a real executive job and pays like one — [research on nonprofit pay found it tracks organization size far more than it tracks performance](https://doi.org/10.1016/j.polsoc.2010.07.004), which is exactly why the size denominator is the whole story. The actual red flags are relational: comp that's a large fraction of total budget, pay that keeps climbing while the mission shrinks, or generous compensation flowing to board members and their relatives (Schedule L covers related-party transactions — worth a glance if something feels off).

## Putting it together

No single number condemns or blesses an organization. Each of the four has a hole in it, and the whole method is to triangulate: a low program ratio is fine *if* reserves are healthy and comp is reasonable; a scary comp figure is fine *if* the budget is large and the mission is delivering. What you're really doing is building a coherent story and checking whether any one number breaks it.

And read more than one year. A single 990 is a photograph; three or four in a row is the movie, and the movie is where the truth is — you can see a reserve being drawn down on purpose, a fundraising bet starting to pay off, or costs quietly ratcheting past revenue. That decade-long view is exactly what the [food bank walkthrough](/posts/2026-06-17-reading-a-food-banks-990.html) is about.

And if you're on the other side of this — actually *running* a small nonprofit — the companion piece on [building a back office on free tools](/posts/2026-07-05-nonprofit-back-office-free-tools.html) is about keeping that overhead low in the first place.

**Where to get the numbers.** You don't need to download PDFs. The [ProPublica Nonprofit Explorer](https://projects.propublica.org/nonprofits/) has the filings and a clean API, and the [nonprofit search tools](https://search.noprofits.org) at noprofits.org are built to pull exactly these figures and make them legible. The transparency already exists — the only hard part is that almost nobody looks.

<small>Benchmarks cited are from the BBB Wise Giving Alliance and Charity Navigator's published standards and are rules of thumb, not bright lines. Example figures are from IRS Form 990 filings for the Hunger Intervention Program (EIN 26-3716527) via the ProPublica Nonprofit Explorer API; figures are as-filed and unaudited.</small>
