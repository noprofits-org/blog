---
title: Rendering rich TikZ diagrams with dvisvgm
date: 2026-06-14
tags: tikz, rendering, haskell, hakyll
description: Swapping pdf2svg for dvisvgm — and pdflatex for lualatex — so the build can render transparency and 3D TikZ, demonstrated with an electromagnetic wave.
---

This blog renders TikZ at build time: a fenced `tikzpicture` code block is
compiled to a real figure during the Hakyll build, so the diagram in the source
*is* the diagram on the page. The original pipeline worked for line art and
`pgfplots` charts, but it quietly failed on anything richer — and the reason was
the converter, not the diagram.

## The problem with pdf2svg

The old path was `pdflatex` → PDF → `pdf2svg` → SVG. `pdf2svg` is built on
Poppler, which **rasterizes or silently drops** the PostScript-backed features
that make a diagram worth drawing: opacity, gradient fills, and many
`patterns`/`decorations`. A translucent shape came out opaque, or vanished.
`pdflatex` is also fixed-memory, so data-heavy `pgfplots` figures could hit
`TeX capacity exceeded`.

## The new pipeline

Two swaps fix it:

- **`lualatex`** instead of `pdflatex` — dynamic memory, so large diagrams stop
  overflowing.
- **`dvisvgm`** (with `mutool` as its PDF backend) instead of `pdf2svg` — it
  preserves transparency and vector detail, and `--no-fonts` turns text into
  paths so the SVG is self-contained.

The rendered SVG is now embedded **inline** (it scales crisply and respects the
page) rather than as a data-URI image, and a diagram that fails to compile is
logged and replaced with a small error box instead of aborting the whole site
build.

## Proof: a 3D electromagnetic wave

Here is the test that the old pipeline could not pass — an electromagnetic plane
wave with **translucent** field envelopes, drawn in a hand-rolled 3D basis. The
red sheet is the electric field $\vec{E}$, the blue sheet the magnetic field
$\vec{B}$, perpendicular and in phase, propagating along $\vec{v}$. Where the
sheets overlap you can see straight through both — that transparency is exactly
what `pdf2svg` used to throw away.

```tikzpicture
\begin{tikzpicture}[
  x={(1cm,-0.16cm)}, y={(0.46cm,0.32cm)}, z={(0cm,1cm)},
  >={Stealth[length=3mm]}, line cap=round, line join=round,
  Edge/.style={thick}]
  % faint ground grid on the x-y plane
  \foreach \gx in {0,1,...,8}{\draw[gray!35,line width=.3pt] (\gx,-1.8,0)--(\gx,1.8,0);}
  \foreach \gy in {-1.5,-1,...,1.5}{\draw[gray!35,line width=.3pt] (0,\gy,0)--(8,\gy,0);}
  % axes
  \draw[->,Edge] (0,0,-1.6)--(0,0,2.5) node[anchor=south]{$\vec{E}$};
  \draw[->,Edge] (-0.4,0,0)--(8.7,0,0) node[anchor=west]{$\vec{v}$};
  \draw[->,Edge] (0,-1.9,0)--(0,2.6,0) node[anchor=south west]{$\vec{B}$};
  % E field — red sheet in the x-z plane
  \fill[red,opacity=0.20] plot[variable=\x,domain=0:8,samples=160,smooth] (\x,0,{1.6*sin(\x*90)}) -- (8,0,0) -- (0,0,0) -- cycle;
  \foreach \x in {0,0.2,...,8.01}{\draw[red!65!black,opacity=0.55,line width=.4pt] (\x,0,0)--(\x,0,{1.6*sin(\x*90)});}
  \draw[red!75!black,line width=1pt] plot[variable=\x,domain=0:8,samples=200,smooth] (\x,0,{1.6*sin(\x*90)});
  % B field — blue sheet in the x-y plane
  \fill[blue,opacity=0.20] plot[variable=\x,domain=0:8,samples=160,smooth] (\x,{1.1*sin(\x*90)},0) -- (8,0,0) -- (0,0,0) -- cycle;
  \foreach \x in {0,0.2,...,8.01}{\draw[blue!65!black,opacity=0.55,line width=.4pt] (\x,0,0)--(\x,{1.1*sin(\x*90)},0);}
  \draw[blue!75!black,line width=1pt] plot[variable=\x,domain=0:8,samples=200,smooth] (\x,{1.1*sin(\x*90)},0);
\end{tikzpicture}
```

The diagram is rendered from the TikZ above on every build — no image file
checked into the repo.

*Credit: the electromagnetic-wave figure is adapted from the beautiful diagram
gallery at [diagrams.janosh.dev](https://diagrams.janosh.dev/light) (originally a
CeTZ/Typst drawing), ported here to TikZ.*
