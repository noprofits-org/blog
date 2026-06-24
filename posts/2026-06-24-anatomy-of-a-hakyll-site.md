---
title: The anatomy of a Hakyll site, line by line
date: 2026-06-24
author: Peter Johnston
tags: haskell, hakyll, static site generator, pandoc, functional programming, build systems, tikz
description: A complete walkthrough of the Haskell that builds this blog — the Hakyll rule set, contexts, feeds, the Pandoc compiler with citations and math, and the build-time TikZ filter — explaining what every part of the configuration does and why it's there.
---

This blog is a pile of Markdown files turned into HTML by a program I wrote in
Haskell. That program is a [Hakyll](https://jaspervdj.be/hakyll/) site: a static
site generator where the *configuration is code*. There is no `config.yaml` with
a hundred knobs; instead there is a Haskell value that describes, declaratively,
how every kind of file on the site gets built.

People sometimes ask what's actually in that file. This post is the answer. We'll
walk through every piece of the build, from the four-line entry point to the
filter that compiles LaTeX diagrams to SVG at build time. By the end you should
be able to read the whole thing and know exactly what each line buys you.

## What Hakyll actually is

Hakyll is a library, not a framework you fill in. You write a `main` that hands
Hakyll a *rule set* — a description of which source files exist and how each one
should be compiled and routed. Hakyll then behaves like `make`: it builds a
dependency graph, compiles what's stale, and skips what isn't.

The core vocabulary is small:

- A **`Rules`** block is the whole recipe — the list of all the `match`/`create`
  declarations.
- **`match`** selects existing files by a glob `Pattern` (`"posts/*"`).
- **`create`** declares output files that have *no* source (like `archive.html`).
- **`route`** decides the output path (`setExtension "html"` turns
  `posts/foo.md` into `posts/foo.html`).
- **`compile`** is the pipeline that turns the source into the output, threaded
  together with `>>=`.
- A **`Context`** is the set of `$variables$` a template can see.
- A **`Compiler`** is Hakyll's build monad — it tracks dependencies for you, so
  that loading the bibliography inside a post compiler automatically makes that
  post depend on the bibliography.

That's enough to read everything below. Here is the whole build in one picture —
source files on the left, the rule set in the middle, the generated site on the
right. (Every diagram in this post is itself compiled by the TikZ filter
described at the end, so these boxes are the pipeline drawing itself.)

```tikzpicture
\begin{tikzpicture}[
  font=\small,
  >={Stealth[length=2.4mm]},
  src/.style={draw, rounded corners=2pt, align=center, fill=black!6,
              draw=black!55, minimum height=9mm, minimum width=28mm, thick},
  out/.style={draw, rounded corners=2pt, align=center, fill=green!10,
              draw=green!55!black, minimum height=9mm, minimum width=30mm, thick},
  flow/.style={->, thick, black!70},
]
  % sources
  \node[src] (posts) at (0,3)    {\texttt{posts/*.md}};
  \node[src] (idx)   at (0,1.5)  {\texttt{index.html}};
  \node[src] (bib)   at (0,0)    {\texttt{bib/*.bib, *.csl}};
  \node[src] (asset) at (0,-1.5) {\texttt{css/ js/ images/}};
  \node[src] (tpl)   at (0,-3)   {\texttt{templates/*}};

  % engine
  \node[draw, rounded corners=3pt, align=center, thick, fill=blue!7,
        draw=blue!55!black, minimum height=58mm, minimum width=30mm]
        (eng) at (5.4,0) {\textbf{siteRules}\\[3pt]\scriptsize match / create\\[1pt]
                          \scriptsize route\\[1pt]\scriptsize compile};

  % outputs
  \node[out] (ph)  at (11,3)    {\texttt{posts/*.html}};
  \node[out] (ih)  at (11,1.5)  {\texttt{index.html}};
  \node[out] (ar)  at (11,0)    {\texttt{archive.html}};
  \node[out] (fe)  at (11,-1.5) {\texttt{atom.xml / rss.xml}};
  \node[out] (st)  at (11,-3)   {static assets};

  \draw[flow] (posts) -- (eng);
  \draw[flow] (idx)   -- (eng);
  \draw[flow] (bib)   -- (eng);
  \draw[flow] (asset) -- (eng);
  \draw[flow] (tpl)   -- (eng);

  \draw[flow] (eng) -- (ph);
  \draw[flow] (eng) -- (ih);
  \draw[flow] (eng) -- (ar);
  \draw[flow] (eng) -- (fe);
  \draw[flow] (eng) -- (st);
\end{tikzpicture}
```

## The entry point

Historically a Hakyll project is one `site.hs` file. This blog has grown enough
machinery — citations, math, a TikZ-to-SVG filter — that I split it into a tiny
executable and a `blog` library. The executable is the whole of `app/site.hs`:

```haskell
-- | Entry point. All rules live in "Blog.Site"; the rest of the build logic
-- (compilers, contexts, feeds, TikZ) lives in the @blog@ library.
module Main (main) where

import Hakyll (hakyll)

import Blog.Site (siteRules)

main :: IO ()
main = hakyll siteRules
```

`hakyll` takes a `Rules ()` value and produces a full command-line program — the
one I run as `stack run site build` or `site watch`. Every bit of substance lives
in `siteRules`. Splitting it out this way means the interesting code is in a
library, which means I can write unit tests against it (the SVG-namespacing logic
in the TikZ module has tests; you can't easily test a function buried in
`Main`).

## The rule set

`Blog.Site.siteRules` is the heart of the build. It opens with two pragmas and
imports worth noting:

```haskell
{-# LANGUAGE OverloadedStrings #-}

module Blog.Site (siteRules) where

import Control.Monad (filterM)
import Hakyll

import Blog.Compilers (bibtexMathCompiler)
import Blog.Context   (postCtx)
import Blog.Feed      (feedConfiguration, feedCtx)
```

`OverloadedStrings` is what lets me write `"posts/*"` and have it be read as a
Hakyll `Pattern`, `"templates/post.html"` as an `Identifier`, and so on — the
same string literal becomes whatever type the context demands. `filterM` shows up
because of drafts, which we'll get to.

Let's take the rules in the order they fire.

### Citations: the CSL and BibTeX files

```haskell
match "bib/style.csl"        $ compile cslCompiler
match "bib/bibliography.bib" $ compile biblioCompiler
```

These two have a `compile` but no `route` — they are never written to the output
site. They exist so *other* compilers can `load` them. `cslCompiler` parses a
Citation Style Language file (it controls how `[@Maxwell]` renders — APA, IEEE,
whatever the `.csl` says), and `biblioCompiler` parses the BibTeX database of
references. The post compiler pulls both in to resolve citations.

### Static assets: images, JS, CSS

```haskell
match "images/*" $ do
    route   idRoute
    compile copyFileCompiler

match "js/*" $ do
    route   idRoute
    compile copyFileCompiler

match "css/*" $ do
    route   idRoute
    compile compressCssCompiler
```

`idRoute` is the identity route — the file lands at the same path it came from.
`copyFileCompiler` does exactly what it says: a byte-for-byte copy, no parsing,
for images and scripts. CSS gets `compressCssCompiler` instead, which strips
whitespace and comments so the stylesheets ship a little smaller. Nothing
clever — just the plumbing that gets assets onto the site.

### The standalone pages

```haskell
match (fromList ["about.rst", "contact.markdown", "colophon.markdown"]) $ do
    route   $ setExtension "html"
    compile $ pandocCompiler
        >>= loadAndApplyTemplate "templates/default.html" defaultContext
        >>= relativizeUrls
```

`fromList` builds a `Pattern` from an explicit list of files instead of a glob —
these are my three one-off pages. Notice one is `.rst` (reStructuredText) and two
are Markdown; `pandocCompiler` handles both transparently, because Pandoc reads
many formats and Hakyll picks the reader from the file extension.

The pipeline reads as a sentence once you know `>>=` is "and then feed the
result into":

1. `pandocCompiler` — render the source to an HTML fragment.
2. `loadAndApplyTemplate "templates/default.html" defaultContext` — drop that
   fragment into the site's outer template (header, nav, footer).
3. `relativizeUrls` — rewrite absolute `/css/...` links to be relative to the
   page, so the site works when served from a subdirectory or opened locally.

`defaultContext` is Hakyll's built-in set of fields: `$body$`, `$title$` (from
the file's metadata), `$url$`, and so on.

### Posts: the main event

```haskell
match "posts/*" $ do
    route $ setExtension "html"
    compile $ bibtexMathCompiler "bib/style.csl" "bib/bibliography.bib"
        >>= saveSnapshot "content"
        >>= loadAndApplyTemplate "templates/post.html"    postCtx
        >>= loadAndApplyTemplate "templates/default.html" postCtx
        >>= relativizeUrls
```

Posts get a richer compiler than the static pages, and an extra step. Walking it:

- `bibtexMathCompiler` is my own compiler (covered in detail below). It does what
  `pandocCompiler` does plus citations, math, syntax highlighting, and the TikZ
  filter.
- `saveSnapshot "content"` stashes the rendered post body *at this point* — after
  the content is rendered but **before** the page chrome is wrapped around it.
  The feeds reload this snapshot so the RSS/Atom entries contain just the
  article, not the navigation and footer.
- Two `loadAndApplyTemplate` calls nest the templates: first the post layout
  (title, date, byline, the "← All posts" link), then the site-wide default
  shell around that.
- `relativizeUrls` again.

Both templates render with `postCtx` rather than `defaultContext`, because posts
need a formatted date field. More on that in the contexts section.

### The archive page

```haskell
create ["archive.html"] $ do
    route idRoute
    compile $ do
        posts <- recentFirst =<< loadAllPublished "posts/*"
        let archiveCtx =
                listField "posts" postCtx (return posts) `mappend`
                constField "title" "Archives"            `mappend`
                defaultContext

        makeItem ""
            >>= loadAndApplyTemplate "templates/archive.html" archiveCtx
            >>= loadAndApplyTemplate "templates/default.html" archiveCtx
            >>= relativizeUrls
```

This is the first `create` — `archive.html` has no source file, so we conjure it.
The compiler:

- `loadAllPublished "posts/*"` loads every post (filtering drafts; see below) and
  `recentFirst` sorts them newest-first by date.
- `archiveCtx` is built by combining three contexts with `mappend` (`<>`). The
  key piece is `listField "posts" postCtx (return posts)`, which exposes the post
  list to the template's `$for(posts)$` loop, each post seeing `postCtx`.
  `constField "title" "Archives"` hard-codes the page title, and `defaultContext`
  supplies the rest. Contexts are a monoid: earlier fields win, so the explicit
  title beats anything `defaultContext` might have provided.
- `makeItem ""` starts from an empty body — all the visible content comes from the
  template iterating over `$posts$` — and then the archive and default templates
  are applied.

### The home page

```haskell
match "index.html" $ do
    route idRoute
    compile $ do
        posts <- recentFirst =<< loadAllPublished "posts/*"
        let indexCtx =
                listField "posts" postCtx (return posts) `mappend`
                constField "title" "Home"                `mappend`
                defaultContext

        getResourceBody
            >>= applyAsTemplate indexCtx
            >>= loadAndApplyTemplate "templates/default.html" indexCtx
            >>= relativizeUrls
```

Almost the same as the archive, with one important difference. `index.html` *does*
exist as a source file, so instead of `makeItem ""` we use `getResourceBody` to
read it and `applyAsTemplate indexCtx` to treat the file *itself* as a Hakyll
template. That means `index.html` can contain `$for(posts)$ ... $endfor$` and the
post list gets spliced straight into it, before the whole thing is wrapped in the
default layout.

### The feeds

```haskell
create ["atom.xml"] $ do
    route idRoute
    compile $ do
        posts <- fmap (take 20) . recentFirst
            =<< loadAllPublishedSnapshots "posts/*" "content"
        renderAtom feedConfiguration feedCtx posts

create ["rss.xml"] $ do
    route idRoute
    compile $ do
        posts <- fmap (take 20) . recentFirst
            =<< loadAllPublishedSnapshots "posts/*" "content"
        renderRss feedConfiguration feedCtx posts
```

Two more generated files, near-identical. This is where `saveSnapshot "content"`
pays off: `loadAllPublishedSnapshots "posts/*" "content"` reloads each post's
*body-only* snapshot, not the full templated page. `recentFirst` sorts, `take 20`
keeps the feed to the latest twenty entries, and `renderAtom`/`renderRss` emit
valid feed XML using the shared `feedConfiguration` and `feedCtx`.

### The leftovers

```haskell
match "404.html" $ do
    route idRoute
    compile copyFileCompiler

match "robots.txt" $ do
    route idRoute
    compile copyFileCompiler

match "templates/*" $ compile templateCompiler
```

The `404.html` and `robots.txt` are copied verbatim. The last line is easy to
overlook but essential: `templateCompiler` parses every file in `templates/` into
a `Template` value so that all those `loadAndApplyTemplate` calls above have
something to load. No route, because templates are build inputs, not site outputs.

### Drafts

Three of the rules above call `loadAllPublished` / `loadAllPublishedSnapshots`
instead of Hakyll's `loadAll`. Those are my helpers, and they're how a post stays
hidden until it's ready:

```haskell
isPublished :: Item a -> Compiler Bool
isPublished item = do
    draft <- getMetadataField (itemIdentifier item) "draft"
    return (draft /= Just "true")

loadAllPublished :: Pattern -> Compiler [Item String]
loadAllPublished pat = loadAll pat >>= filterM isPublished

loadAllPublishedSnapshots :: Pattern -> Snapshot -> Compiler [Item String]
loadAllPublishedSnapshots pat snap =
    loadAllSnapshots pat snap >>= filterM isPublished
```

`isPublished` reads the `draft:` field from a post's YAML frontmatter and returns
`False` only when it's exactly `"true"`. `filterM` is the monadic cousin of
`filter`: because the predicate runs in the `Compiler` monad (it has to read
metadata), ordinary `filter` won't do. The effect is that adding `draft: true` to
a post's frontmatter removes it from the home page, archive, and feeds — but the
`match "posts/*"` rule still builds the individual page, so I can preview it at
its URL while it's invisible to everyone browsing the site. That's exactly how
the [unpublish in the recent history](https://github.com/noprofits-org/blog)
worked: flip one field, the post drops out of every listing.

## The contexts

A `Context` answers the question "what `$variables$` can this template use?" The
post context is tiny:

```haskell
postCtx :: Context String
postCtx =
  dateField "date" "%B %e, %Y" `mappend`
  defaultContext
```

`dateField "date" "%B %e, %Y"` adds a `$date$` variable, formatted like
"June 24, 2026", parsed from either the filename (`2026-06-24-...`) or the
frontmatter. `mappend`-ing `defaultContext` after it gives templates everything
else — `$title$`, `$body$`, `$url$`. Because context is a left-biased monoid, the
custom `date` is the one that wins. This is the context every post, the archive,
and the home page render with.

## The feed configuration

```haskell
feedConfiguration :: FeedConfiguration
feedConfiguration = FeedConfiguration
  { feedTitle       = "noprofits.org"
  , feedDescription = "Blogs about science, nonprofits, and other fun stuff."
  , feedAuthorName  = "Peter Johnston"
  , feedAuthorEmail = "peter@noprofits.org"
  , feedRoot        = "https://blog.noprofits.org"
  }

feedCtx :: Context String
feedCtx = postCtx `mappend` bodyField "description"
```

`FeedConfiguration` is just the metadata at the top of an RSS/Atom file. The
interesting line is `feedCtx`. Feed formats require a `description` per entry, and
I want that description to be the article itself. `bodyField "description"` maps
the `$description$` variable to the item body — which, thanks to the snapshot, is
the rendered post content. Stacking it on `postCtx` means feed entries also get
the formatted date.

## The post compiler

`pandocCompiler` is fine for a plain page, but posts need more: citations, math,
syntax highlighting, and my build-time diagrams. That's `bibtexMathCompiler`:

```haskell
bibtexMathCompiler :: String -> String -> Compiler (Item String)
bibtexMathCompiler cslFileName bibFileName = do
  csl <- load $ fromFilePath cslFileName
  bib <- load $ fromFilePath bibFileName
```

It starts by `load`-ing the parsed CSL style and BibTeX database — the very items
the first two rules compiled. Loading them here is what makes every post depend on
the bibliography in Hakyll's graph: edit a reference, and posts rebuild.

```haskell
  let mathExtensions =
        [ Ext_tex_math_dollars
        , Ext_tex_math_double_backslash
        , Ext_latex_macros
        , Ext_raw_tex
        , Ext_raw_html
        , Ext_fenced_code_blocks
        , Ext_backtick_code_blocks
        , Ext_fenced_code_attributes
        ]
```

These are Pandoc extensions I turn on. The math ones let me write `$E = mc^2$`
and `\\(...\\)` and have them survive to the output as MathJax. `Ext_raw_tex` and
`Ext_raw_html` let raw markup pass through untouched. The `code_blocks` and
`fenced_code_attributes` extensions matter for the diagrams: they're what let me
tag a fenced block with `{.tikzpicture}` and have the filter recognize it.

```haskell
      defaultExtensions = writerExtensions defaultHakyllWriterOptions
      newExtensions     = foldr enableExtension defaultExtensions mathExtensions
      writerOptions = defaultHakyllWriterOptions
        { writerExtensions     = newExtensions
        , writerHTMLMathMethod = MathJax ""
        , writerHighlightStyle = Just pygments
        }
      readerOptions = defaultHakyllReaderOptions
        { readerExtensions =
            enableExtension Ext_raw_html $
              enableExtension Ext_raw_tex pandocExtensions
        }
```

`foldr enableExtension` folds the whole list of extensions onto Pandoc's
defaults. The *writer* options say: render math via MathJax, highlight code with
the `pygments` color scheme, and use the extended extension set. The *reader*
options enable raw HTML and raw TeX on the way in. Reader and writer are
configured separately because Pandoc parses to an abstract document first, then
renders — and you want raw markup preserved at both ends.

```haskell
  getResourceBody
    >>= readPandocBiblio readerOptions csl bib
    >>= \pandoc -> do
          transformed <- walkM tikzFilter pandoc
          return $ writePandocWith writerOptions (walk wrapTables transformed)
```

The actual pipeline:

1. `getResourceBody` reads the Markdown source.
2. `readPandocBiblio` parses it *and resolves the citations* against the CSL +
   BibTeX, producing a Pandoc AST with references and a bibliography.
3. `walkM tikzFilter` walks the AST and runs the TikZ filter over every block —
   `walkM` is the monadic tree-walk, needed because rendering a diagram shells
   out to LaTeX (an effect).
4. `walk wrapTables` does a second, *pure* walk that wraps every table in a
   scrolling `<div>` so wide tables don't overflow on phones:

   ```haskell
   wrapTables :: Block -> Block
   wrapTables t@Table{} = Div ("", ["table-scroll"], []) [t]
   wrapTables b         = b
   ```

5. `writePandocWith writerOptions` renders the transformed AST to HTML.

Drawn out, the post pipeline is a straight line with two side-channels: the CSL +
BibTeX items feeding into the parse, and the `"content"` snapshot tapped off
*after* rendering but *before* the templates, which is exactly what the feeds
reload:

```tikzpicture
\begin{tikzpicture}[
  font=\small,
  >={Stealth[length=2.4mm]},
  box/.style={draw, rounded corners=2pt, align=center, thick,
              minimum height=11mm, minimum width=23mm},
  stage/.style={box, fill=blue!8, draw=blue!55!black},
  io/.style={box, fill=black!7, draw=black!55},
  snap/.style={box, fill=orange!15, draw=orange!65!black},
  out/.style={box, fill=green!10, draw=green!55!black},
  flow/.style={->, thick, black!70},
]
  \node[io]    (md)  at (0,0)    {Markdown\\source};
  \node[stage] (rd)  at (3.3,0)  {readPandoc\\Biblio};
  \node[stage] (tk)  at (6.6,0)  {walkM\\tikzFilter};
  \node[stage] (wt)  at (9.9,0)  {walk\\wrapTables};
  \node[stage] (wr)  at (13.2,0) {writePandoc\\With};
  \node[out]   (pg)  at (17.2,0) {HTML\\page};

  \node[io]   (csl) at (3.3,2.3)  {CSL +\\BibTeX};
  \node[snap] (sn)  at (13.2,-2.4){\texttt{"content"}\\snapshot};
  \node[out]  (fd)  at (17.2,-2.4){atom.xml\\rss.xml};

  \draw[flow] (md) -- (rd);
  \draw[flow] (csl) -- (rd);
  \draw[flow] (rd) -- (tk);
  \draw[flow] (tk) -- (wt);
  \draw[flow] (wt) -- (wr);
  \draw[flow] (wr) -- node[above, align=center, font=\scriptsize]
                       {post.html\\default.html} (pg);
  \draw[flow] (wr) -- node[right, font=\scriptsize] {saveSnapshot} (sn);
  \draw[flow] (sn) -- node[above, font=\scriptsize] {reload} (fd);
\end{tikzpicture}
```

## The TikZ filter: LaTeX diagrams at build time

The last and most unusual piece. I want to write a diagram as TikZ/LaTeX source
*inside* a Markdown post and have it appear as a crisp, inline SVG — with no
image file ever checked into the repo. `Blog.TikZ` does that. The filter itself:

```haskell
tikzFilter :: Block -> Compiler Block
tikzFilter (CodeBlock (_, classes, _) contents)
  | "tikzpicture" `elem` classes = do
      result <- unsafeCompiler $ renderTikz (T.unpack contents)
      let html = case result of
            Right svg -> "<div class=\"tikz-figure\">" ++ inlineSvg svg ++ "</div>"
            Left err  -> "<div class=\"tikz-error\"><strong>Diagram failed to render.</strong>"
                          ++ "<pre>" ++ escapeHtml err ++ "</pre></div>"
      return $ RawBlock (Format "html") (T.pack html)
tikzFilter block = return block
```

It pattern-matches *only* code blocks tagged `.tikzpicture` and leaves every
other block alone (the catch-all last line). For a matching block it calls
`renderTikz` — wrapped in `unsafeCompiler` because compiling LaTeX is arbitrary
IO that Hakyll otherwise wouldn't allow inside a compiler. The result is either
`Right svg` (inlined into a figure) or `Left err`. That `Left` branch is
deliberate: a diagram that won't compile becomes a visible red error box rather
than aborting the entire site build. And because the match is so narrow, a post
with no diagrams never shells out at all — the site still builds on a machine with
no TeX installed.

`renderTikz` itself wraps the snippet in a `standalone` LaTeX preamble (TikZ,
pgfplots, circuitikz, mhchem, a stack of TikZ libraries), runs it through
`lualatex` in a temp directory, converts the PDF to SVG with `dvisvgm`, and reads
the result back. The whole filter — which is what rendered every figure above —
looks like this, including the graceful-failure branch that turns a broken
diagram into an error box instead of killing the build:

```tikzpicture
\begin{tikzpicture}[
  font=\small,
  >={Stealth[length=2.4mm]},
  box/.style={draw, rounded corners=2pt, align=center, thick,
              minimum height=10mm, minimum width=21mm},
  stage/.style={box, fill=blue!8, draw=blue!55!black},
  io/.style={box, fill=black!7, draw=black!55},
  ok/.style={box, fill=green!10, draw=green!55!black},
  bad/.style={box, fill=red!10, draw=red!60!black},
  flow/.style={->, thick, black!70},
  ret/.style={->, thick, green!55!black},
  rej/.style={->, thick, red!65!black, dashed},
]
  \node[io]    (cb) at (0,0)     {\texttt{.tikzpicture}\\block};
  \node[stage] (lx) at (3.4,0)   {lualatex};
  \node[stage] (dv) at (6.8,0)   {dvisvgm};
  \node[stage] (ns) at (10.2,0)  {namespace\\Ids};
  \node[ok]    (fig)at (14.2,1.2){\texttt{div.tikz-figure}\\inline SVG};
  \node[bad]   (err)at (14.2,-1.7){\texttt{div.tikz-error}\\error box};

  \draw[flow] (cb) -- node[above, font=\scriptsize] {\texttt{.tex}} (lx);
  \draw[flow] (lx) -- node[above, font=\scriptsize] {PDF} (dv);
  \draw[flow] (dv) -- node[above, font=\scriptsize] {SVG} (ns);
  \draw[ret]  (ns) -- (fig);
  \draw[rej]  (lx) to[out=-65, in=178] node[below, pos=0.35, font=\scriptsize]
                                       {fails} (err);
  \draw[rej]  (dv) to[out=-70, in=165] (err);
\end{tikzpicture}
```

I've written about
[that pipeline](/posts/2026-06-14-rich-tikz-with-dvisvgm.html) and
[reading the circuitikz source](/posts/2026-06-15-reading-the-circuitikz-source.html)
before, so I'll point at one subtle bit instead — id collisions:

```haskell
namespaceIds :: T.Text -> T.Text -> T.Text
namespaceIds prefix =
    rep "id=\""    ("id=\"" <> prefix)
  . rep "id='"     ("id='" <> prefix)
  . rep "href=\"#" ("href=\"#" <> prefix)
  . rep "href='#"  ("href='#" <> prefix)
  . rep "url(#"    ("url(#" <> prefix)
  where rep = T.replace
```

`dvisvgm` reuses glyph paths with ids like `g3-66`, and restarts that numbering
in every file. Inline two such SVGs on one page and the ids collide — a later
diagram's "R" gets drawn with an earlier one's path. `namespaceIds` prefixes
every id and every internal reference (`href="#..."`, `url(#...)`) with a
per-diagram token derived from a hash of the source, so each diagram's ids are
unique on the page. It's a pure function of text, which means it has unit tests —
the payoff from keeping the logic in a library instead of `Main`.

## Putting it together

That's the entire build. The shape of it is worth stepping back to see:

- **`app/site.hs`** — four lines, hands the rules to `hakyll`.
- **`Blog.Site`** — the rule set: what files exist, how each is compiled and
  routed, and how drafts are filtered.
- **`Blog.Context`** — the `$variables$` templates can see.
- **`Blog.Feed`** — Atom/RSS configuration.
- **`Blog.Compilers`** — the Pandoc compiler with citations, math, highlighting,
  and table wrapping.
- **`Blog.TikZ`** — Markdown code blocks compiled to inline SVG at build time.

The thing I keep coming back to with Hakyll is that the configuration is a real
program in a real language. The draft filter is `filterM` over a metadata read.
The diagram renderer is a tree-walk that shells out to LaTeX. The feed body is a
snapshot taken at exactly the right point in the pipeline. None of that needed a
plugin system or a templating DSL — it's just functions, composed with `>>=`,
type-checked before a single page is built. When the site breaks, it usually
breaks at compile time, in my editor, which is the best place for a website to
break.
