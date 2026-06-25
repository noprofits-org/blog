---
title: "Astro, Apps Script, and Firebase: how site.noprofits.org is built"
date: 2026-06-25
author: Peter Johnston
tags: astro, apps script, firebase, hosting, github actions, static site, workload identity federation, serverless
description: A factual tour of the noprofits-web-engineering stack — a static Astro site on Firebase Hosting, a Google Apps Script standing in for a backend, and a keyless GitHub Actions deploy. Architecture, configuration, and data flow, with diagrams.
---

The site at `site.noprofits.org` is a marketing and lead-generation site for a
free web-design service aimed at Seattle-area nonprofits. Its source lives in the
repository `noprofits-web-engineering`. The stack has four parts:

- **Astro** builds the pages into a static `dist/` directory.
- **Firebase Hosting** (Spark/free tier) serves that directory from a CDN.
- **Google Apps Script** stands in for a backend: it receives form submissions
  and analytics beacons and writes them to a Google Sheet.
- **GitHub Actions** builds and deploys on every push to `main`, authenticating
  to Google Cloud with keyless Workload Identity Federation.

There is no application server and no database. The Google Sheet is the datastore.
This post documents each part and how they connect.

## System overview

The site runs in three planes. The static plane is the Astro build served by
Firebase Hosting. The backend plane is a single Apps Script web app reachable at a
`/exec` URL, which the browser calls directly for both lead submissions and
analytics events. A third, separate Apps Script web app renders a read-only
analytics dashboard from the same spreadsheet.

```tikzpicture
\begin{tikzpicture}[
  font=\large,
  >={Stealth[length=3mm]},
  node distance=0mm,
  box/.style={draw, rounded corners=3pt, align=center, thick,
              minimum height=15mm, minimum width=34mm},
  client/.style={draw, rounded corners=3pt, align=center, thick, fill=black!6, draw=black!55},
  host/.style={box, fill=orange!12, draw=orange!60!black},
  back/.style={box, fill=blue!9, draw=blue!55!black},
  store/.style={box, fill=green!12, draw=green!55!black},
  flow/.style={->, very thick, black!75},
  lbl/.style={font=\normalsize, align=center},
]
  % browser at the left
  \node[client, minimum height=20mm, minimum width=30mm] (br) at (0,0)
        {\textbf{Browser}\\[2pt]{\normalsize site.noprofits.org}};

  % hosting
  \node[host] (cdn) at (5.6,2.6) {\textbf{Firebase}\\\textbf{Hosting CDN}\\[2pt]{\normalsize static \texttt{dist/}}};

  % apps script endpoint
  \node[back] (exec) at (6.0,-2.4) {\textbf{Apps Script}\\\textbf{web app}\\[2pt]{\normalsize \texttt{/exec}}};

  % spreadsheet
  \node[store] (sheet) at (12.2,-2.4) {\textbf{Google Sheet}\\[2pt]{\normalsize \texttt{Leads} + \texttt{Events}}};

  % dashboard
  \node[back] (dash) at (12.2,1.4) {\textbf{Dashboard}\\\textbf{web app}\\[2pt]{\normalsize \texttt{/exec} (read)}};

  % edges
  \draw[flow] (cdn) -- node[lbl, above, sloped]{HTML / CSS / JS} (br);
  \draw[flow] (br.south) |- node[lbl, below, pos=0.7]{POST lead + analytics} (exec.west);
  \draw[flow] (exec) -- node[lbl, above]{\texttt{appendRow}} (sheet);
  \draw[flow] (sheet) -- node[lbl, right]{\texttt{openById}} (dash);
\end{tikzpicture}
```

The browser loads static assets from the CDN. The same browser POSTs lead and
analytics data to the Apps Script endpoint, which appends rows to the sheet. The
dashboard web app reads the sheet by ID and renders charts. The four corners of
the diagram are the four technologies in this post.

## Astro

The dependency list is short. `package.json` declares exactly two runtime
dependencies, `astro` (`^5.5.5`) and `@astrojs/sitemap` (`^3.2.1`), and is marked
`"type": "module"` and `private`.

`astro.config.mjs` configures pure static generation:

```js
export default defineConfig({
  site: SITE_URL,              // https://site.noprofits.org
  output: 'static',
  integrations: [sitemap(), formEndpointGuard],
});
```

`output: 'static'` means every page is rendered to HTML at build time; there is no
Astro runtime in production. The pages are `index`, `404`, `privacy`, and `stats`,
plus three SEO guide pages under `guides/`. Components (`Header`, `Footer`,
`InquiryForm`, `GuideFooterCta`) and one layout (`BaseLayout`) assemble them.
Fonts are self-hosted woff2.

### The build-time form-endpoint guard

`formEndpointGuard` is an inline integration that hooks `astro:build:start` and
**aborts the build** if `PUBLIC_FORM_ENDPOINT` does not begin with
`https://script.google.com`. The purpose is narrow: prevent shipping a site whose
lead form points at a placeholder or empty endpoint. The escape hatch for local
work is `ALLOW_PLACEHOLDER_ENDPOINT=true npm run build`.

### Content Security Policy generated from the build output

The `build` script is two steps:

```
astro build && node scripts/gen-csp.mjs
```

Astro inlines small client scripts directly into each page. A strict CSP that
allows inline scripts by hash must therefore know the hash of every script that
shipped. `gen-csp.mjs` solves this mechanically: after the build, it walks every
HTML file in `dist/`, computes the sha256 of each executable inline `<script>`
(skipping `src=` scripts and `application/ld+json`), and rewrites the
`script-src` hash allowlist inside `firebase.json` to match. Because it runs as
part of `build`, the CSP cannot drift when a bundled value — such as the form
endpoint constant — changes.

`src/data/site.ts` is the single source of truth for the site URL, contact
details, and the build-time-injected `FORM_ENDPOINT` and `DASH_URL`, each paired
with a guard (`isRealEndpoint`, `hasDashboard`) so the templates can degrade
gracefully when a value is unset.

## Firebase Hosting

`firebase.json` serves the `dist/` directory and defines no rewrites or redirects;
routing is the plain trailing-slash structure Astro emits. `.firebaserc` pins the
default project to `noprofits-web`.

```json
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "headers": [ /* cache + security headers */ ]
  }
}
```

The headers fall into two groups. **Cache headers** are tuned per asset class:

| Path | `Cache-Control` |
|------|-----------------|
| `/_astro/**` | `max-age=31536000, immutable` |
| `/fonts/**` | `max-age=604800, stale-while-revalidate` |
| images | `max-age=3600, must-revalidate` |
| `**/*.html` | `max-age=0, must-revalidate` |

Hashed Astro assets are cached for a year; HTML is never cached, so a deploy is
visible immediately.

**Security headers** apply to all paths: HSTS with preload,
`X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`,
`X-Frame-Options: DENY`, a `Permissions-Policy` that disables camera, microphone,
geolocation, and `interest-cohort`, and the CSP described above. The CSP
`connect-src` and `form-action` directives allowlist exactly
`https://script.google.com` and `https://script.googleusercontent.com` — the two
origins the Apps Script endpoint resolves to.

## Google Apps Script

There are two scripts under `apps-scripts/`, each with its own `.clasp.json` (for
`clasp` push) and `appsscript.json` (V8 runtime, `America/Los_Angeles` timezone).

The first, `leads_sheet/`, is **bound to the spreadsheet**. Its `Code.js` exposes
one `doPost` function that multiplexes three jobs by inspecting the request body.
This is the central design decision of the backend: a single deployed endpoint
does lead intake, analytics ingest, and a token-gated analytics read.

```tikzpicture
\begin{tikzpicture}[
  font=\large,
  >={Stealth[length=3mm]},
  box/.style={draw, rounded corners=3pt, align=center, thick,
              minimum height=13mm, minimum width=40mm},
  ep/.style={box, fill=blue!9, draw=blue!55!black, minimum height=16mm},
  branch/.style={box, fill=black!6, draw=black!55},
  store/.style={box, fill=green!12, draw=green!55!black},
  flow/.style={->, very thick, black!75},
  lbl/.style={font=\normalsize, align=center},
]
  \node[ep] (post) at (0,0) {\textbf{\texttt{doPost}}\\[2pt]{\normalsize one \texttt{/exec} endpoint}};

  \node[branch] (tok) at (7,3.0) {token present\\{\normalsize $\rightarrow$ dashboard JSON}};
  \node[branch] (an)  at (7,0.0) {\texttt{t} param present\\{\normalsize $\rightarrow$ analytics event}};
  \node[branch] (lead) at (7,-3.0) {otherwise\\{\normalsize $\rightarrow$ lead}};

  \node[store] (events) at (14,0.6) {\texttt{Events} tab};
  \node[store] (leads)  at (14,-3.0) {\texttt{Leads} tab\\{\normalsize + email}};

  \draw[flow] (post) -- (tok);
  \draw[flow] (post) -- (an);
  \draw[flow] (post) -- (lead);
  \draw[flow] (an)   -- node[lbl, above]{\texttt{logEvent\_}} (events);
  \draw[flow] (lead) -- node[lbl, below, sloped]{\texttt{appendRow}} (leads);
  \draw[flow] (tok.east) -| node[lbl, above, pos=0.25]{aggregate} (events.north);
\end{tikzpicture}
```

The branch is selected as follows: a `token` field (checked against the
`DASH_TOKEN` script property, fail-closed) returns aggregated analytics JSON; a
`t` parameter routes to `logEvent_`, which appends to the `Events` tab; anything
else is treated as a lead.

The lead path enforces several server-side abuse controls before it writes a row:

- a honeypot field (`np_hp`),
- a per-minute rate limit via `CacheService` (`RATE_LIMIT_PER_MIN = 12`),
- per-field length caps and a server-side email regex,
- **formula-injection neutralization** — `neutralize_` prefixes any leading
  `= + - @` with an apostrophe so a submitted value cannot become a live
  spreadsheet formula,
- a daily email cap (`DAILY_EMAIL_CAP = 60`).

Under throttling or the email cap, the lead is **still written to the sheet**;
only the notification email to the operator is suppressed. Leads are never dropped
under load. A companion file, `Outreach.js`, adds an `onOpen` custom menu to the
sheet for sending canned acknowledgement emails **manually** — deliberately not
automated, to avoid turning the deployment into an open relay.

The second script, `analytics-dashboard/`, is a **standalone** web app. Its
`doGet` opens the same spreadsheet by ID (`SHEET_ID` script property), aggregates
the `Events` tab behind a ~2-minute `CacheService` window, and server-renders
dependency-free SVG charts. It is kept separate from the lead endpoint
specifically so its access can be gated to "anyone with a Google account" while
the lead and analytics endpoint stays anonymous.

The analytics client (`src/lib/analytics.ts`) is cookieless and stores no PII. It
keeps a random per-tab session id in `sessionStorage`, records only the referrer
host, and sends events with `fetch(..., { mode: 'no-cors', keepalive: true })`. If
the endpoint is unset, every analytics call is a no-op.

## GitHub deployment

The workflow `.github/workflows/deploy.yml` ("Deploy to Firebase Hosting") runs on
`push` to `main` and on `workflow_dispatch`. It requests `contents: read` and
`id-token: write`, uses a `deploy-hosting` concurrency group with
`cancel-in-progress`, and guards the job with `if: github.ref == 'refs/heads/main'`.

```tikzpicture
\begin{tikzpicture}[
  font=\large,
  >={Stealth[length=3mm]},
  step/.style={draw, rounded corners=3pt, align=center, thick,
               fill=black!6, draw=black!55, minimum height=14mm, minimum width=30mm},
  auth/.style={step, fill=blue!9, draw=blue!55!black},
  out/.style={step, fill=orange!12, draw=orange!60!black},
  trig/.style={step, fill=green!12, draw=green!55!black},
  flow/.style={->, very thick, black!75},
  lbl/.style={font=\normalsize, align=center},
]
  \node[trig] (push) at (0,0)   {push to\\\texttt{main}};
  \node[step] (co)   at (3.6,0) {checkout\\+ Node 20};
  \node[step] (ci)   at (7.2,0) {\texttt{npm ci}};
  \node[step] (build) at (10.8,0) {\texttt{npm run}\\\texttt{build}};
  \node[auth] (wif)  at (14.4,0) {WIF auth\\{\normalsize keyless}};
  \node[out]  (dep)  at (18.0,0) {\texttt{firebase}\\\texttt{deploy}};

  \draw[flow] (push) -- (co);
  \draw[flow] (co) -- (ci);
  \draw[flow] (ci) -- (build);
  \draw[flow] (build) -- (wif);
  \draw[flow] (wif) -- (dep);

  \node[lbl] at (10.8,-1.8) {Astro build\\+ \texttt{gen-csp.mjs}};
  \node[lbl] at (14.4,-1.8) {no service-account\\key in repo};
  \node[lbl] at (18.0,-1.8) {\texttt{--only hosting}\\project \texttt{noprofits-web}};
\end{tikzpicture}
```

The steps are: `actions/checkout`, `actions/setup-node` (Node 20 with npm cache),
`npm ci`, `npm run build`, a global install of `firebase-tools@15.22.0`,
`google-github-actions/auth` (Workload Identity Federation), and finally
`firebase deploy --only hosting --project noprofits-web --non-interactive`.

Three details are worth naming:

1. **Keyless authentication.** There is no service-account JSON key in the
   repository. The deploy step obtains short-lived credentials through Workload
   Identity Federation, whose pool binds the credential to this repository and to
   `assertion.ref == 'refs/heads/main'`. That binding, not a stored secret, is the
   authoritative half of the trust.
2. **`firebase-tools` is installed before the auth step.** The credential-exporting
   auth step runs after the tool install on purpose, so a compromised
   `firebase-tools` release cannot execute with Application Default Credentials
   already in scope.
3. **Actions are pinned to commit SHAs**, with version comments, and bumped by
   Dependabot (weekly, separate `ci` and `deps` update groups).

The values the workflow needs — `GCP_WIF_PROVIDER`, `GCP_DEPLOY_SA`,
`PUBLIC_FORM_ENDPOINT`, `PUBLIC_DASH_URL` — are stored as repository **Variables**,
not Secrets. They are identifiers, not credentials: the form endpoint, for
instance, ships in the client bundle and is therefore not secret. The security of
the deploy rests entirely on the WIF binding described above.

## End to end

The full path from an edit to a served page:

```tikzpicture
\begin{tikzpicture}[
  font=\large,
  >={Stealth[length=3mm]},
  box/.style={draw, rounded corners=3pt, align=center, thick,
              minimum height=14mm, minimum width=28mm},
  dev/.style={box, fill=black!6, draw=black!55},
  ci/.style={box, fill=green!12, draw=green!55!black},
  host/.style={box, fill=orange!12, draw=orange!60!black},
  user/.style={box, fill=blue!9, draw=blue!55!black},
  flow/.style={->, very thick, black!75},
  lbl/.style={font=\normalsize, align=center},
]
  \node[dev]  (git) at (0,0)  {\texttt{git push}\\{\normalsize \texttt{main}}};
  \node[ci]   (gha) at (4.2,0) {GitHub\\Actions};
  \node[host] (fb)  at (8.4,0) {Firebase\\Hosting};
  \node[user] (vis) at (12.6,0) {Visitor};
  \node[user] (as)  at (12.6,-3.2) {Apps Script\\$\rightarrow$ Sheet};

  \draw[flow] (git) -- (gha);
  \draw[flow] (gha) -- node[lbl, above]{deploy} (fb);
  \draw[flow] (fb)  -- node[lbl, above]{serve} (vis);
  \draw[flow] (vis) -- node[lbl, right]{form /\\analytics} (as);
\end{tikzpicture}
```

A commit to `main` triggers the Actions workflow, which builds the Astro site,
regenerates the CSP from the build output, and deploys the static files to Firebase
Hosting over a keyless connection. Visitors are served those files from the CDN.
When a visitor submits the inquiry form or generates an analytics event, the
browser talks directly to the Apps Script endpoint, which writes to the Google
Sheet. No part of the running site is a server the project operates; the only code
that executes on request is in Apps Script, and the only persistent state is a
spreadsheet.
