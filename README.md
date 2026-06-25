# [NoProfits Blog]

[![Static Site Generator](https://img.shields.io/badge/Generator-Hakyll-blueviolet.svg)](https://jaspervdj.be/hakyll/)

A static blog built with [Hakyll](https://jaspervdj.be/hakyll/), featuring:

**Key Features:**

* **Technical Content Focus:** Designed for blog posts that require mathematical notation, diagrams, and academic citations.
* **LaTeX Rendering:** Beautifully renders LaTeX equations using MathJax. Perfect for math, physics, computer science, and other technical topics.
* **TikZ Diagram Support:** Embeds vector-based diagrams created with TikZ directly in your posts. Ideal for illustrations, graphs, and visualizations.
* **BibTeX Integration:** Easily include academic citations using BibTeX, with customizable citation styles.
* **Static Site Generation (Hakyll):** Fast, secure, and easy to deploy, thanks to Hakyll.
* **Archive and Index Pages:** Automatically generated archive and homepage listing of blog posts for easy navigation.
* **Customizable Design:** Styled with CSS and built using HTML templates for a flexible and consistent look.
* **Content Pages:** Includes static pages for "About," "Contact," and more.

**Technology Stack:**

* [Hakyll](https://jaspervdj.be/hakyll/) (Static Site Generator)
* [Pandoc](https://pandoc.org/) (Document Converter)
* [LaTeX](https://www.latex-project.org/) & [MathJax](https://www.mathjax.org/) (Mathematical Typesetting)
* [TikZ](https://tikz.dev/) & [PGF/TikZ](https://pgf-tikz.github.io/) (Diagram Creation)
* [BibTeX](https://www.bibtex.org/) & CSL (Citation Management)
* `pdflatex`, `pdf2svg` (Backend tools for TikZ rendering)

**Live Demo:**

* https://blog.noprofits.org

**Note:**

All science, mathematics, and chemistry-related content has been moved to a separate site at [hyperpolarizability.com](https://hyperpolarizability.com).

---

## Authoring posts

A post is a Markdown file in `posts/`, named `YYYY-MM-DD-slug.md`. The date
prefix sets the publication date and the URL, so it determines ordering.

Each post begins with a YAML frontmatter block:

```yaml
---
title: "My post title"
date: 2026-06-25
author: Peter Johnston
tags: tag one, tag two
description: One-sentence summary for the listing and feed.
---
```

`title`, `date`, `author`, `tags`, and `description` are the standard fields. Add
`draft: true` to exclude a post from the home page, archive, and feed.

**Frontmatter gotchas** — the block is parsed as YAML, so a few characters in
values bite:

* **A colon in the title (or any value) breaks the parse.** `title: Astro: a
  tour` fails with *"mapping values are not allowed in this context"* and aborts
  the whole build. Wrap the value in double quotes: `title: "Astro: a tour"`.
  This is the single most common authoring error — quote any value containing
  `:`, and likewise values that start with `[`, `{`, `>`, `|`, `#`, `*`, `&`, or
  a quote.
* The build fails on the *first* bad post and names it, so read the
  `[ERROR] posts/...` line and the line/column it cites.

**TikZ diagrams** go in fenced ` ```tikzpicture ` blocks and are rendered to
inline SVG at build time. The LaTeX preamble loads a fixed set of libraries
(`arrows.meta`, `calc`, `patterns`, `decorations.*`, `matrix`, `backgrounds`,
`pgfplots`, `circuitikz`) — notably **not** `positioning`, so place nodes with
explicit coordinates (`at (x,y)`) rather than `below=…of`. A block that fails to
compile is replaced with a visible error box and logged; it does not abort the
build, so a green build does not by itself prove every diagram rendered — check
the page.

---