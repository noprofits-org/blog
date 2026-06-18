---
title: What a food bank's tax return actually says
date: 2026-06-17
tags: nonprofits, data
---

Every tax-exempt organization in the United States files a Form 990, and every one of those returns is public. You can read the finances of any charity you donate to, volunteer for, or are simply curious about. Almost nobody does — the documents are long, the line numbers are cryptic, and the interesting story is spread across a decade of separate filings.

So let's actually read one. I'll use the [Hunger Intervention Program](https://hungerintervention.org) (HIP), a food-security nonprofit in north Seattle that I've done volunteer work for. Its returns are a small, clean example of something that happened to a lot of food programs in the last few years.

Here is HIP's total revenue against its total expenses, straight from thirteen years of 990 filings (in thousands of dollars):

```tikzpicture
\begin{axis}[
    width=11cm,
    height=8cm,
    xlabel={Fiscal year},
    ylabel={Dollars (thousands)},
    title={Hunger Intervention Program: revenue vs.\ expenses},
    grid=major,
    grid style={line width=.2pt, draw=gray!50},
    axis lines=left,
    xmin=2010.5,
    xmax=2023.5,
    ymin=0,
    ymax=1350,
    xtick={2011,2013,2015,2017,2019,2021,2023},
    xticklabel style={/pgf/number format/1000 sep=},
    legend pos=north west,
    legend style={draw=none, fill=white, fill opacity=0.85},
    tick style={color=black},
    every axis label/.style={font=\large},
    every tick label/.style={font=\large},
    title style={font=\large\bfseries},
    scaled ticks=false
]

\addplot[thick, mark=*, mark size=2pt, color=blue] coordinates {
    (2011, 58.1) (2012, 69.7) (2013, 121.0) (2014, 202.2)
    (2015, 255.6) (2016, 305.1) (2017, 278.0) (2018, 359.0)
    (2019, 558.6) (2020, 945.9) (2021, 1204.2) (2022, 1130.0)
    (2023, 1173.1)
};

\addplot[thick, mark=square*, mark size=2pt, color=red] coordinates {
    (2011, 61.8) (2012, 85.1) (2013, 109.6) (2014, 156.5)
    (2015, 221.3) (2016, 283.5) (2017, 289.5) (2018, 309.5)
    (2019, 506.7) (2020, 692.4) (2021, 1140.9) (2022, 1045.0)
    (2023, 1271.2)
};

\legend{Total revenue, Total expenses}
\end{axis}
```

The shape tells most of the story. For most of the 2010s HIP was a roughly \$300K-a-year operation growing steadily. Then the pandemic hit, demand for food assistance exploded, and so did giving: revenue went from \$559K in 2019 to \$1.2M in 2021 — more than double in two years, and about a twenty-fold increase over where the program started in 2011.

**Where the money comes from.** Almost entirely contributions. In 2023, \$1.16M of HIP's \$1.17M in revenue — about 99% — was donations and grants. Program revenue was essentially zero. That makes sense once you say it out loud: a food bank gives food away. It has no customers, only donors. That's the defining financial fact of the whole sector — these organizations don't earn their way to sustainability, they raise it, every single year.

**Where it goes.** People. Salaries grew from \$23K in 2014 to \$445K in 2023. Add payroll taxes and officer compensation and roughly half of HIP's 2023 spending — about \$650K of \$1.27M — went to the staff who actually run the program. That isn't waste; it's what scaling looks like. You cannot move a million dollars of food a year on volunteers and a part-time coordinator. The org professionalized because it had to.

**The honest wrinkle.** Look at 2023: the red line crosses above the blue. Expenses (\$1.27M) outran revenue (\$1.17M), a roughly \$98K deficit, and net assets fell from \$647K to \$549K to cover it. This is not a scandal — it's the most predictable thing in the data. The pandemic surge in giving cooled off, but the staff hired to handle the surge stayed on the payroll. A lot of nonprofits are living through exactly this normalization right now: costs that ratcheted up during 2020–21 against donations that have drifted back toward earth.

None of this required inside knowledge. It's thirteen PDFs, a few line items each, pulled from a public API. The hard part isn't access — it's that nobody reads them. That's the whole reason I build the [nonprofit data tools](https://search.noprofits.org) at noprofits.org: the transparency already exists on paper, it just needs to be made legible.

<small>Source: IRS Form 990 filings for EIN 26-3716527, via the [ProPublica Nonprofit Explorer API](https://projects.propublica.org/nonprofits/). Figures are as-filed and unaudited.</small>
