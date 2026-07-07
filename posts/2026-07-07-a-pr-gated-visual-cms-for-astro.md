---
title: "Every save is a pull request: a visual, PR-gated CMS for an Astro site"
date: 2026-07-07
author: Peter Johnston
tags: astro, cms, firebase, security, github actions, static site, serverless
description: site.noprofits.org grew a content management system — a node-map editor where every routed page is a clickable node, and every save becomes a pull request. How the splice-back engine works, why a curly brace is the scariest character in an Astro template, how a CI job proves a diff is pure text, and what this design gets wrong.
og-image: /images/2026-07-07-cms-node-map-hero.png
figure: '<img src="/images/2026-07-07-cms-node-map-hero.png" alt="A site rendered as a node map of linked colored circles; one node is opened in an editing drawer whose save button points at a pull request badge.">'
figlabel: The site as a map, the save as a PR
figcaption: Every routed page is a node, every internal link an edge; clicking a node opens its text for editing, and saving opens a pull request — a human merge is the only way anything publishes.
---

The [previous post about site.noprofits.org](/posts/2026-06-25-astro-apps-script-firebase.html)
described a static [Astro](https://astro.build/) site with no server, no
database, and a Google Sheet for a backend. That architecture has one obvious
cost: changing a headline means editing an `.astro` source file, and the
people who should be able to fix a typo — future volunteer editors of a
nonprofit's site — should not need a code editor, a git tutorial, or commit
rights to do it.

Last night the site grew a content management system (CMS). It is not a
conventional one. There is still no database: the git repository is the
content store, the CMS's write primitive is a git commit, and its publish
primitive is a **pull request (PR) that a human must merge**. The editor
itself renders the site as a **node map** — one node per page, one edge per
internal hyperlink — and clicking a node opens every piece of text on that
page for editing. The whole thing is about two thousand lines with zero
runtime dependencies beyond the platform SDKs, it costs roughly nothing to
run, and its security model does not require trusting the editor, the editor
UI, or even the CMS's own GitHub credential.

The source is public in
[`noprofits-web-engineering`](https://github.com/noprofits-org/noprofits-web-engineering):
the engine and local editor under
[`tools/site-editor/`](https://github.com/noprofits-org/noprofits-web-engineering/tree/main/tools/site-editor),
the hosted variant under
[`functions/`](https://github.com/noprofits-org/noprofits-web-engineering/tree/main/functions),
and the continuous integration (CI) gate in
[`scripts/verify-content-pr.mjs`](https://github.com/noprofits-org/noprofits-web-engineering/blob/main/scripts/verify-content-pr.mjs).
This post documents how it works, what the design buys, what it costs, and
what I would build differently.

## The shape of the thing

There are two variants sharing one engine. The **local editor**
(`npm run edit`) is a single plain-Node server on `127.0.0.1:4400` that reads
the working tree and writes edits straight back to disk — a solo dev tool;
the normal git workflow reviews the changes. The **hosted editor** is one
Cloud Function on Firebase that serves the same user interface behind
Google sign-in, and instead of a filesystem it reads and writes the GitHub
repository through the API. That is the variant a non-technical editor uses,
and it is where the interesting security problems live.

The publish pipeline for the hosted variant looks like this:

```tikzpicture
\begin{tikzpicture}[
  font=\large,
  >={Stealth[length=3mm]},
  box/.style={draw, rounded corners=3pt, align=center, thick,
              minimum height=14mm, minimum width=30mm},
  client/.style={box, fill=black!6, draw=black!55},
  fn/.style={box, fill=blue!9, draw=blue!55!black},
  gh/.style={box, fill=green!12, draw=green!55!black},
  gate/.style={box, fill=yellow!22, draw=yellow!50!black},
  host/.style={box, fill=orange!12, draw=orange!60!black},
  flow/.style={->, very thick, black!75},
  lbl/.style={font=\normalsize, align=center},
]
  % top row: editing path
  \node[client] (ed) at (0,0) {\textbf{Editor}\\[1pt]{\normalsize browser, Google}\\[-2pt]{\normalsize sign-in + allowlist}};
  \node[fn] (fn) at (5.2,0) {\textbf{Cloud Function}\\[1pt]{\normalsize splice engine,}\\[-2pt]{\normalsize PAT in Secret Mgr}};
  \node[gh] (branch) at (11.2,0) {\textbf{\texttt{cms/edits}}\\[1pt]{\normalsize branch + open PR}};

  % bottom row: publish path (right to left)
  \node[gate] (ci) at (11.2,-3.4) {\textbf{CI gate}\\[1pt]{\normalsize diff must replay as}\\[-2pt]{\normalsize pure text edits}};
  \node[client] (human) at (5.2,-3.4) {\textbf{Human review}\\[1pt]{\normalsize branch protection,}\\[-2pt]{\normalsize merge = publish}};
  \node[host] (main) at (0,-3.4) {\textbf{\texttt{main} $\to$ deploy}\\[1pt]{\normalsize WIF trust exists}\\[-2pt]{\normalsize for \texttt{main} only}};

  \draw[flow] (ed) -- node[lbl, above]{save} (fn);
  \draw[flow] (fn) -- node[lbl, above]{commit + PR} (branch);
  \draw[flow] (branch) -- node[lbl, right, pos=0.25]{every push} (ci);
  \draw[flow] (ci) -- node[lbl, above]{green check} (human);
  \draw[flow] (human) -- node[lbl, above]{merge} (main);

  % the boundary annotation
  \draw[dashed, thick, red!70!black] (-2.4,-1.7) -- (13.6,-1.7)
    node[pos=0.03, below right, font=\normalsize, red!70!black, align=left]
    {nothing above this line can reach the live site};
\end{tikzpicture}
```

**Figure 1.** The publish pipeline. Saves flow left to right into a
`cms/edits` branch and an open pull request; publishing flows right to left
only through a green CI check and a human merge. The deploy workflow's
Workload Identity Federation (WIF) trust is pinned to `main`, so the CMS
branch — and therefore the CMS itself — physically cannot deploy.

Two properties fall out of this shape. First, the CMS has no publish button:
merging the PR *is* publishing, because the existing deploy workflow ships
`main` to Firebase Hosting on every push. Second, the blast radius of a fully
compromised CMS is a noisy branch and an unmerged PR — annoying, visible,
and inert.

## What the editor edits: four kinds of text block

The engine
([`extract.mjs`](https://github.com/noprofits-org/noprofits-web-engineering/blob/main/tools/site-editor/extract.mjs),
about five hundred lines, no dependencies) parses each `.astro` page into a
flat list of **editable text blocks**, each with the exact byte span it came
from. Copy lives in four places on this site, and each becomes a block kind:

```tikzpicture
\begin{tikzpicture}[
  font=\large,
  code/.style={font=\normalsize\ttfamily, anchor=west, inner sep=1.5pt},
  span/.style={font=\normalsize\ttfamily, anchor=west, inner sep=1.5pt,
               rounded corners=2pt},
  fmS/.style={span, fill=blue!14},
  txS/.style={span, fill=green!18},
  atS/.style={span, fill=orange!22},
  shS/.style={span, fill=red!14},
  tag/.style={font=\normalsize\bfseries, anchor=west},
]
  % the file
  \draw[thick, black!60, rounded corners=4pt] (-0.4,0.8) rectangle (12.6,-4.5);
  \node[code, black!50] at (-0.1,0.4) {src/pages/index.astro};

  \node[code] (l1) at (0,-0.4) {---};
  \node[code] (l2) at (0,-1.0) {const title = };
  \node[fmS]  (l2v) at (l2.east) {'Free websites for nonprofits'};
  \node[code] (l2e) at (l2v.east) {;};
  \node[code] (l3) at (0,-1.6) {---};
  \node[code] (l4) at (0,-2.2) {<h1>};
  \node[txS]  (l4v) at (l4.east) {Web design, donated};
  \node[code] at (l4v.east) {</h1>};
  \node[code] (l5) at (0,-2.8) {<img src="/team.png" alt="};
  \node[atS]  (l5v) at (l5.east) {Volunteers at work};
  \node[code] at (l5v.east) {" />};
  \node[code] (l6) at (0,-3.4) {<CtaBand heading=\{`};
  \node[atS]  (l6v) at (l6.east) {Start your project};
  \node[code] at (l6v.east) {`\} />};
  \node[code] (l7) at (0,-4.0) {<Guide set:html=\{"<p>};
  \node[shS]  (l7v) at (l7.east) {Step one: tell us\ldots};
  \node[code] at (l7v.east) {</p>"\} />};

  % legend, below the file
  \node[fmS] (k1) at (0,-5.1) {fm};
  \node[tag] at (k1.east) {\ \normalsize frontmatter string consts (title, description, og*)};
  \node[txS] (k2) at (0,-5.7) {text};
  \node[tag] at (k2.east) {\ \normalsize HTML text nodes in the template body};
  \node[atS] (k3) at (0,-6.3) {attr};
  \node[tag] at (k3.east) {\ \normalsize human-readable attributes + string-literal component props};
  \node[shS] (k4) at (0,-6.9) {shtml};
  \node[tag] at (k4.east) {\ \normalsize text nodes inside set:html string payloads};
\end{tikzpicture}
```

**Figure 2.** Block anatomy of a miniature page. The engine records the exact
source span of every highlighted region; everything outside a highlight —
markup, expressions, structure — is not editable and is never touched by a
save.

The four kinds:

- **`fm`** — frontmatter string constants (`const title = '…'` and friends),
  the strings that flow into `<title>`, meta descriptions, and Open Graph
  tags. Only plain string literals qualify; a const built with template
  interpolation is skipped rather than half-edited.
- **`text`** — ordinary HTML text nodes in the template body.
- **`attr`** — human-readable quoted attributes (`alt`, `placeholder`,
  `aria-label`, `title`) and string-literal component props
  (a call-to-action band's ``heading={`…`}``, for example).
- **`shtml`** — text nodes *inside* `set:html={"…"}` string payloads, which
  is how some longer guide pages carry their body copy. The engine decodes
  the JavaScript string, scans the HTML inside it, and edits text nodes
  within the payload.

Saving splices each changed block back at its recorded offset,
highest-offset-first so earlier spans stay valid, and re-encodes the new text
for its context. Unchanged blocks contribute zero bytes of change: saving a
page without edits leaves the file byte-identical, which matters later when a
CI job has to reason about diffs. A detail I like: the engine detects whether
each block already used named HTML entities (`&mdash;`) or literal Unicode
punctuation (`—`) and keeps whatever convention it found, so an edit doesn't
churn the file's style.

The scanner knows just enough Astro to be safe: it skips `<script>`/`<style>`
elements, balances `{…}` expressions (quote- and template-literal-aware, so a
stray `>` inside an arrow function doesn't end a tag), and refuses anything
it cannot round-trip exactly — a template literal with `${…}` interpolation
returns "not editable," not a guess.

## The character that keeps you honest: `{`

Every CMS has to answer "what if the editor types `<script>`?" — entity-encode
`< > &` and the answer is boring, the payload renders as visible text. Astro
adds a much better trap. Inside an Astro template, `{expression}` is
**JavaScript evaluated at build time**. If saved copy could smuggle a raw
brace into a template, the payload would not run in a visitor's browser — it
would run *inside the CI build*, with the build's credentials. A content
editor typing curly braces is one build away from remote code execution (RCE)
in the deploy pipeline.

So the engine's encoder treats braces as mandatory targets alongside the
HTML-significant characters: every `{` and `}` in an HTML-context block is
written as `&#123;`/`&#125;`, which renders identically and evaluates never.
Frontmatter strings get the mirror-image treatment for their context — angle
brackets are written as `\u003c`/`\u003e` escapes *inside the JavaScript
string literal*, so a title like `</script><script>…` cannot break out of a
`<title>` tag or a JSON-LD block no matter where that string is later
rendered. Attribute blocks encode their own quote character; template-literal
props escape backticks and `${`.

None of this is taken on faith:
[`security.test.mjs`](https://github.com/noprofits-org/noprofits-web-engineering/blob/main/tools/site-editor/security.test.mjs)
feeds hostile payloads — script tags, brace expressions, attribute breakouts,
`</script>` title escapes, `"}` payload escapes — through every block kind,
splices them, and then runs a **real `astro build`** over the result,
asserting that the built HTML contains zero live script tags and no evaluated
expressions. The test suite attacks the actual encoder against the actual
compiler, not a model of it.

## The hosted variant: auth in one function

The hosted editor is a single Cloud Function
([`functions/index.js`](https://github.com/noprofits-org/noprofits-web-engineering/blob/main/functions/index.js))
that does three jobs: serve the admin page, enforce authentication, and proxy
saves to GitHub. The auth chain is deliberately short. Every API call must
carry a Firebase ID token from Google sign-in; the token is verified
server-side; the account's email must be **verified** and present on a
comma-separated allowlist in the function's environment. The allowlist is
fail-closed — empty means nobody can edit. There are no cookies (so
cross-site request forgery has nothing to ride) and no CORS headers (so
cross-origin JavaScript cannot call the API at all).

The function's GitHub credential is a personal access token (PAT) for a
dedicated **non-admin machine account** with write access to this one
repository. It lives in Google Secret Manager and never reaches the browser.
The non-admin part is load-bearing: GitHub branch protection exempts
administrators by default, so an admin-owned token could push straight to
`main` and quietly defeat the whole PR gate. (A fine-grained PAT would have
been nicer than a classic one, but fine-grained PATs cannot be granted write
access to a repository owned by a *different* personal account — a limitation
that only surfaces when the write fails, because reads on a public repo
appear to work.)

Saves are also guarded against a mundane failure: every save carries the blob
SHA (Secure Hash Algorithm digest) of the file version the editor loaded, and
GitHub rejects the write atomically if the file has moved on — two editors
cannot silently clobber each other; the loser gets "reload."

## The CI gate: reproducibility as authorization

Here is the part of the design I would defend in any review. Everything above
— auth, allowlist, encoding — assumes the CMS is working as intended. The CI
gate assumes it is not. Suppose the PAT is stolen, or the function itself is
compromised: the attacker can now push arbitrary commits to `cms/edits` and
dress them up as innocent copy edits waiting for review. A tired human
skimming a diff at the end of the day is the only remaining control, and
"tired human skims diff" is not a security boundary.

So [`content-pr.yml`](https://github.com/noprofits-org/noprofits-web-engineering/blob/main/.github/workflows/content-pr.yml)
runs on every `cms/*` pull request and **re-derives the entire diff from
scratch**:

```tikzpicture
\begin{tikzpicture}[
  font=\large,
  >={Stealth[length=3mm]},
  box/.style={draw, rounded corners=3pt, align=center, thick,
              minimum height=13mm, minimum width=34mm},
  file/.style={box, fill=black!6, draw=black!55},
  eng/.style={box, fill=blue!9, draw=blue!55!black},
  ok/.style={box, fill=green!12, draw=green!55!black},
  bad/.style={box, fill=red!12, draw=red!60!black},
  flow/.style={->, very thick, black!75},
  lbl/.style={font=\normalsize, align=center},
]
  \node[file] (old) at (0,1.6)  {\textbf{old page}\\[1pt]{\normalsize from merge-base}};
  \node[file] (new) at (0,-1.6) {\textbf{new page}\\[1pt]{\normalsize from PR head}};
  \node[eng] (ex) at (5.0,0) {\textbf{extract blocks}\\[1pt]{\normalsize same count, kinds,}\\[-2pt]{\normalsize labels, order?}};
  \node[eng] (replay) at (10.0,0) {\textbf{replay edits}\\[1pt]{\normalsize applyEdits(old,}\\[-2pt]{\normalsize changed text)}};
  \node[ok]  (pass) at (14.6,1.6) {\textbf{byte-identical}\\[1pt]{\normalsize pass: pure content}};
  \node[bad] (fail) at (14.6,-1.6) {\textbf{any stray byte}\\[1pt]{\normalsize fail: do not merge}};

  \draw[flow] (old) -- (ex);
  \draw[flow] (new) -- (ex);
  \draw[flow] (ex) -- node[lbl, above]{text diffs} (replay);
  \draw[flow] (replay) -- node[lbl, above, sloped]{$=$ new file} (pass);
  \draw[flow] (replay) -- node[lbl, below, sloped]{$\neq$ new file} (fail);
\end{tikzpicture}
```

**Figure 3.** The content-PR gate. CI extracts blocks from both versions of
every changed file, requires the block *skeleton* (count, kinds, labels,
order) to be identical, replays the text differences through the same splice
engine, and fails unless the result reproduces the PR's version of the file
**byte for byte**.

The rule this enforces: a `cms/*` PR may only contain changes that are
*reproducible as pure text-block edits on routed pages*. Changed a workflow
file? Fail — only `src/pages/*.astro` is allowed. Added a component, an
attribute, an import? Fail — the block skeleton changed. Slipped one byte
outside an editable span? Fail — the replay will not reproduce it. The same
workflow also re-runs the adversarial security suite and a full site build,
so a content PR that would break the build is caught before review rather
than after merge.

I think of this as **reproducibility as authorization**: the credential
authorizes writing to a branch, but the only thing that can *pass review
automation* is the subset of writes the engine could have produced. A stolen
token keeps the ability to make noise and loses the ability to disguise code
as content. The defense does not depend on the function being honest, because
CI re-checks the claim from nothing but the diff.

The layers stack like this — each one assumes everything above it has already
failed:

```tikzpicture
\begin{tikzpicture}[
  font=\large,
  layer/.style={draw, rounded corners=5pt, thick, align=center},
]
  \node[layer, fill=red!8,    draw=red!50!black,    minimum width=158mm, minimum height=78mm] (l1) at (0,0) {};
  \node[layer, fill=orange!10, draw=orange!60!black, minimum width=132mm, minimum height=60mm] (l2) at (0,-0.75) {};
  \node[layer, fill=yellow!16, draw=yellow!55!black, minimum width=106mm, minimum height=42mm] (l3) at (0,-1.5) {};
  \node[layer, fill=blue!8,   draw=blue!55!black,   minimum width=88mm,  minimum height=24mm] (l4) at (0,-2.25) {};
  \node[layer, fill=green!14, draw=green!55!black,  minimum width=64mm,  minimum height=10mm] (l5) at (0,-2.9) {};

  \node[anchor=north, font=\large\bfseries] at (l1.north) {\rule{0pt}{5mm}auth: verified email on a fail-closed allowlist};
  \node[anchor=north, font=\large\bfseries] at (l2.north) {\rule{0pt}{5mm}encoding: saved text cannot become markup or code};
  \node[anchor=north, font=\large\bfseries] at (l3.north) {\rule{0pt}{5mm}CI proof: diff must replay as pure text edits};
  \node[anchor=north, font=\large\bfseries] at (l4.north) {\rule{0pt}{4mm}human merge behind branch protection};
  \node[font=\large\bfseries] at (l5.center) {deploy exists only for \texttt{main}};
\end{tikzpicture}
```

**Figure 4.** The layered model, outermost first. A malicious editor beats
layer one by being on the allowlist; the encoder stops their payload; a
stolen token bypasses the encoder but not the CI proof; a fooled reviewer is
still merging something CI screamed about; and even then, only `main`
deploys. Every layer has to fail before malicious *code* reaches the site.

The residual risks are worth naming because no diagram removes them: an
allowlisted editor can still write misleading *text* — no encoder prevents
lies, and the PR review is the only control; the reviewer's GitHub account is
the real trust anchor and needs two-factor authentication; and on a public
repository, every edit is a public commit with the editor's name on it —
transparency, but tell your editors before they find out.

## What this buys, and what it costs

The strengths are mostly consequences of refusing to add infrastructure.
There is no CMS database to secure, back up, or drift out of sync with the
repo — git is the content store, so history, attribution, rollback, and
review come free. The engine has zero runtime dependencies, the function fits
in the free tier at this usage volume, and the entire system is small enough
to read in a sitting. And the security story degrades loudly rather than
silently: every failure mode ends in an unmerged PR with a red check, in
public.

The costs are just as structural, and worth stating plainly:

- **It is a hand-rolled parser, not the Astro compiler.** The scanner handles
  the authoring patterns this repository actually uses. An unfamiliar pattern
  is skipped (safe, but the text becomes invisible to editors) or, worse,
  could be mis-spanned. Brittleness scales with template creativity.
- **Text only, structure frozen.** Editors cannot add a paragraph, reorder
  sections, insert an image, create a page, or change a link. This is not a
  missing feature so much as the security model itself: the CI gate *requires*
  an identical block skeleton, so the feature ceiling and the safety proof
  are the same fact. Lifting one means redesigning the other.
- **No preview.** An editor saves into a pull request sight unseen; nothing
  shows them the rendered page before a human merges. For copy tweaks this is
  tolerable; for anything layout-adjacent it is faith-based editing.
- **One shared `cms/edits` branch.** All editors' pending work piles into a
  single PR. One rejected edit holds every other edit hostage until someone
  untangles the branch.
- **Content lives inside code files.** All the escaping machinery in this
  post exists *because* copy sits in the middle of executable templates. The
  entire threat model in Figure 4 is rent paid on that decision.

## Ways to get the same result with fewer drawbacks

Three alternatives are worth taking seriously, in increasing order of
ambition.

**Use the real parser.** Astro publishes its compiler
([`@astrojs/compiler`](https://github.com/withastro/compiler), the same
WebAssembly module the build uses) with a full abstract syntax tree (AST)
API. Swapping the hand-rolled scanner for compiler-produced spans keeps the
node map, the splice-back model, and the CI gate exactly as they are, while
deleting the class of "authoring style the regex didn't anticipate" bugs.
This is the cheapest structural upgrade available.

**Move the copy out of the templates.** Astro's
[content collections](https://docs.astro.build/en/guides/content-collections/)
exist to separate content from presentation: put page copy in Markdown,
JavaScript Object Notation (JSON), or YAML data files and have templates
render it. Then a content edit touches only data files — trivially reviewable
by construction, no brace-encoding required, and the CI gate shrinks from
"replay the splice engine" to "only these paths, only these schemas." It
also unlocks adding and reordering content, which the current model
structurally cannot allow. The cost is a real refactor of every page, and
losing the "edit exactly what is in the template" property that makes the
current tool honest.

**Use an off-the-shelf git-backed CMS.** [Decap](https://decapcms.org/),
[TinaCMS](https://tina.io/), [Sveltia](https://github.com/sveltia/sveltia-cms),
and [Pages CMS](https://pagescms.org/) all implement the same publish
philosophy — commits and PRs, no CMS database — with mature editing UIs, and
most support per-editor GitHub OAuth, which dissolves the shared-PAT threat
class entirely (every edit is authored by the editor's own account, with the
editor's own permissions). What none of them will do is edit text inside
`.astro` templates: they all assume content collections. So this alternative
is really the previous one plus a free editing interface — and it gives up
the node map, which is, honestly, the part people smile at.

The pattern across all three: the current design spends its complexity
defending a decision (copy inside templates) that could instead be unmade.
Whether that trade is worth it depends on whether "editors see exactly the
page structure that exists" matters more than "editors can add a paragraph."

## What's next

The plan is foundations before features, because the two most-wanted features
are both blocked by foundations. Swapping the scanner for the Astro
compiler's AST removes the brittleness ceiling without changing the user
experience. Per-save branches (`cms/edit-<id>` instead of one shared branch)
plus Firebase preview channels would fix the pileup problem and the
no-preview problem in one move — every save becomes its own PR with its own
throwaway preview URL. After that comes the interesting design problem:
letting editors add or remove whole blocks within a whitelist, which means
teaching the CI gate to verify skeleton *transitions* instead of skeleton
identity — loosening the proof without losing it.

The longer arc: nothing in this design is specific to this site. The engine,
the function, and the workflow are a weekend away from being a template —
a drop-in, self-hosted, PR-gated visual CMS for any Astro repository, with
"your repo, a free Firebase project, and branch protection" as the entire
requirements list. That seems worth building in the open.

## Glossary

- **allowlist** — an explicit list of permitted identities; everything not on
  it is denied. The CMS allowlist is email addresses, and empty means nobody.
- **AST (abstract syntax tree)** — the structured representation of source
  code a parser produces; what the Astro compiler exposes and the hand-rolled
  scanner approximates.
- **Astro** — the static site generator that builds the site; its templates
  evaluate `{…}` expressions as JavaScript at build time.
- **blob SHA** — GitHub's content hash for a file version; sending it with a
  write makes the write atomic (the API rejects stale updates).
- **branch protection** — GitHub repository rules requiring a pull request
  and approval before `main` can change. Exempts admins unless told otherwise
  — which is why the CMS token belongs to a non-admin account.
- **CI (continuous integration)** — automation that runs on every push or
  pull request; here, the content gate, the security suite, and a full build.
- **CMS (content management system)** — software that lets people edit site
  content without editing code. This one's storage backend is git itself.
- **CORS (Cross-Origin Resource Sharing)** — headers that let a browser page
  on one origin call an API on another. The CMS emits none, so no other
  origin can call it from a browser.
- **CSP (Content Security Policy)** — a response header restricting what a
  page may load and run. The admin page pins its one inline script by hash.
- **JSON-LD (JavaScript Object Notation for Linked Data)** — structured
  metadata embedded in a `<script>` block; one of the sinks the frontmatter
  escaping protects.
- **PAT (personal access token)** — a GitHub API credential. The CMS's PAT
  belongs to a dedicated non-admin machine account and lives in Secret
  Manager.
- **PR (pull request)** — GitHub's proposed-change review unit. In this CMS,
  the PR *is* the publish mechanism: merging it deploys.
- **RCE (remote code execution)** — an attacker running arbitrary code on a
  system. Here the risk lives in CI, via Astro's build-time `{…}` evaluation
  — which is why braces are always entity-encoded.
- **Secret Manager** — Google Cloud's secret store; holds the GitHub token so
  it never appears in code, config, or the browser.
- **SHA (Secure Hash Algorithm)** — a cryptographic hash function family;
  used for GitHub blob identity and for pinning the admin page's inline
  script in its CSP.
- **splice** — replacing an exact byte range of a file with new bytes,
  leaving everything outside the range untouched.
- **WIF (Workload Identity Federation)** — keyless deploy auth: GitHub
  Actions proves its identity to Google Cloud and receives short-lived
  credentials, with trust configured for `main` only.
