---
title: "The colors on the palette are energy-level gaps: engineering pigments for permanence"
date: 2026-07-04
author: Peter Johnston
tags: pigments, color, chromophores, lightfastness, charge transfer, ligand field, band gap, conjugation, Kubelka-Munk
description: A tube of paint is an electronic-structure problem plus a scattering problem, perceived by an eye. This post builds the mechanism-first taxonomy of color — conjugated π-systems, ligand-field d–d transitions, charge transfer, and semiconductor band gaps — leading with the modern synthetic pigments engineered to fix the lightfastness failures of their historic ancestors, then puts absorption and scattering back together with Kubelka–Munk.
---

A tube labeled cadmium-red-*hue* usually contains no cadmium. The colorant is a
diketopyrrolopyrrole (DPP), a synthetic organic red substituted for cadmium
sulfoselenide because cadmium is toxic and the organic reds that preceded cadmium
pigments — madder, carmine — faded under light. That substitution is this post's
subject. A pigment's color is a HOMO–LUMO gap of a few electron-volts positioned
where the eye can detect it. Its permanence is a separate property, achieved only
by deliberate molecular engineering. Historically, the same color-producing
physics kept yielding pigments that were either vivid and fugitive or permanent
and toxic; the modern synthetic palette is built to avoid both failure modes at
once.

The earlier posts in this series built the machinery for the first of those
claims without pointing it at paint. The
[fundamentals post](/posts/fundementals_of_quantum_chemistry.html) solved the
particle in a box and found that confining an electron quantizes its energy into
discrete levels whose spacing shrinks as the box grows. The
[water post](/posts/2026-06-30-reading-water-geometry-orbitals-acidity-spectra.html)
and the [Hartree–Fock post](/posts/2026-07-01-hartree-fock-and-the-correlation-gap.html)
turned those levels into molecular orbitals with computable energies, and
established that the gap between a filled and an empty orbital is what a
molecule shows to light. A pigment is that abstraction applied to a physical,
purchasable material. This post answers three questions in order — *what is a
pigment*, *what molecular structures make it colored*, and *how does it
physically interact with light* — and returns repeatedly to lightfastness: why
a chromophore that absorbs visible light is also, for the chemical reasons given
in §8, prone to degrading under it.

## 1. Pigment, dye, and lake

The first distinction is not about color at all; it is about solubility, and it is
operational. A **dye** is a colorant that dissolves — its molecules disperse
individually into the medium, bound to a substrate or floating free in solution,
each molecule surrounded by solvent. A **pigment** is a colorant that does *not*
dissolve: it stays as discrete solid particles, suspended in but chemically aloof
from the binder that carries it — gum, oil, acrylic emulsion, egg yolk. The same
chromophore can play either role depending on how it is presented to the medium;
what makes a paint a *pigment* paint is that the colored matter remains a
particulate phase with its own surfaces, its own crystal structure, and its own
refractive index, all of which will matter in §7. The binder's job is to glue
those particles to a surface and to each other, not to take them into solution.
When you thin a tube color, you are diluting a suspension, not a
solution.[@Berns2019; @Christie2014]

A **lake** is the boundary case between dye and pigment: a dye made to behave
like a pigment by precipitating it onto an inert, colorless particulate substrate
— historically aluminum hydroxide, sometimes chalk or a metal salt. The soluble
dye is *adsorbed* or chemically fixed onto the substrate grains, and the
resulting colored solid is ground into a binder exactly like any pigment.
**Madder lake** (the dye alizarin laid down on alumina) and **carmine**
(cochineal's carminic acid, likewise laked) are the canonical examples — deep,
transparent reds and crimsons used throughout historic palettes. They are also,
not coincidentally, among the most **fugitive** colors ever used: the same
molecules that make a brilliant transparent lake photochemically decompose under
light. A lake's chromophore is chemically still the dissolved dye — laking
changes how the colorant is dispersed, not its intrinsic photostability — which
is why lakes fade like the dyes they are made from. This fragility recurs through
the rest of the post as lightfastness.[@Eastaugh2008; @Zollinger2003]

One more boundary, then we set it aside. Not all color is pigmentation. The blue
of a morpho butterfly, the green of a beetle's shell, the flash of an opal — these
are **structural colors**, produced by interference and diffraction from
nanoscale physical architecture, with no light-absorbing molecule involved at all.
Tilt the wing and the color shifts; grind it to powder and the color dies, because
you have destroyed the structure that made it. That is a wave-optics phenomenon,
not a chromophore, and although it shares the visible spectrum with everything
below, it is a different subject. Everything else in this post is about color that
survives grinding: molecules and crystals that *absorb* particular photons.

## 2. What makes a molecule colored

A material has a color in the ordinary sense when it selectively absorbs some of
the visible photons that fall on it and returns the rest. Visible light spans
roughly **400 to 700 nm**, which in energy is about **3.1 down to 1.8 eV** — a
narrow window, and the entire constraint on what can be colored: a substance is
colored if and only if it has an accessible electronic transition — an energy gap
between an occupied and an empty state — that lands *inside* it (Figure 1). A gap
larger than ~3.1 eV absorbs only in the ultraviolet and leaves all visible light
untouched (the material is white, clear, or colorless); a gap smaller than ~1.8 eV
absorbs in the infrared and, if it absorbs *across* the whole visible range, reads
as black, gray, or metallic. Color requires the gap to fall between those two
limits.

```tikzpicture
\draw[thick,Stealth-] (0,0) -- (11,0);
\node[left,font=\small] at (0,0.15) {$E$ (eV), increasing $\leftarrow$};
\fill[blue!6] (3,-0.9) rectangle (8,0.9);
\draw[thick,blue!50!black] (3,-0.9) rectangle (8,0.9);
\node[above,font=\small\bfseries] at (5.5,1.05) {visible: 1.8--3.1 eV};
\draw[dashed] (3,0.9) -- (3,-1.1);
\node[below,font=\scriptsize] at (3,-1.2) {3.1 eV};
\draw[dashed] (8,0.9) -- (8,-1.1);
\node[below,font=\scriptsize] at (8,-1.2) {1.8 eV};
\node[align=center,font=\scriptsize] at (1.3,-1.7) {gap $>3.1$ eV\\UV only\\\textbf{colorless}};
\node[align=center,font=\scriptsize] at (9.6,-1.7) {gap $<1.8$ eV\\IR $+$ all visible\\\textbf{black / metallic}};
\draw[->,thick,orange!80!black] (4.3,-0.6) -- (4.3,0.6);
\node[align=center,below,font=\scriptsize] at (4.3,-1.05) {$\Delta E\approx2.6$ eV\\violet absorbed\\\textbf{yellow}};
\draw[->,thick,red!70!black] (6.8,-0.6) -- (6.8,0.6);
\node[align=center,below,font=\scriptsize] at (6.8,-1.05) {$\Delta E\approx2.0$ eV\\blue--green absorbed\\\textbf{red}};
```

*Figure 1.* The visible window, 1.8–3.1 eV. A material is colored only if it has
an electronic transition whose energy falls inside this band; gaps above 3.1 eV
absorb only ultraviolet light (colorless), gaps below 1.8 eV absorb infrared and,
if broad, most of the visible range too (black, gray, or metallic). Two example
gaps inside the window are marked with the color each produces.

So "what molecular structures produce color" reduces to "what physical
mechanisms put an electronic energy gap in the 1.8–3.1 eV window, and let an
electron cross it when a photon arrives." Four mechanisms matter for pigments,
and they are genuinely different physics, not variations on one idea. Each of
the next four sections covers one mechanism, gives a modern pigment that uses
it, and compares it with a historic pigment that uses the same mechanism but
lacks the engineered permanence.

## 3. Extended conjugated π-systems

This is the organic-chemistry mechanism, and it connects most directly to the
particle in a box. Take a chain or ring system of alternating single and double
bonds — a **conjugated** π-system. The π electrons are not confined to
individual bonds; they delocalize over the whole conjugated framework. That is,
to a first approximation, an electron in a box, where the box length $L$ is the
length of the conjugated path. The
[fundamentals post](/posts/fundementals_of_quantum_chemistry.html) gave the
levels of that box,

$$
E_n = \frac{n^2 h^2}{8 m L^2},
$$

and the remaining step is to fill them. If the conjugated system holds $N$ π
electrons, they occupy the lowest $N/2$ levels (two per level, by Pauli), so the
highest occupied level is $n = N/2$ and the lowest empty one is $n = N/2 + 1$.
The photon that colors the molecule lifts an electron across that HOMO–LUMO gap:

$$
\Delta E = E_{N/2+1} - E_{N/2}
        = \frac{h^2}{8 m L^2}\,(N+1).
$$

Lengthening the conjugated chain does two things at once: it adds electrons
(raising $N$) and it lengthens the box (raising $L^2$ in the denominator), with
$L$ growing roughly in proportion to $N$. The net effect is that $\Delta E$
shrinks as conjugation extends (Figure 2) — a longer box has a smaller gap. A
short conjugated system absorbs in the ultraviolet and looks colorless;
extending it moves the absorption down through violet, blue, and green, into the
visible as yellow, then orange, then red: longer box, smaller gap, redder color.
This free-electron picture ignores bond alternation, the real shape of the
potential, and electron correlation — the corrections the [Hartree–Fock
post](/posts/2026-07-01-hartree-fock-and-the-correlation-gap.html) worked
through — but the trend it predicts is correct, and it is why essentially every
strong organic colorant is a large, flat, conjugated molecule.[@Christie2014;
@nassau2001physics]

```tikzpicture
\begin{scope}[xshift=0cm]
  \node[font=\small\bfseries] at (1,6.9) {short conjugated chain};
  \draw[->] (-0.3,0) -- (-0.3,6.1) node[above,font=\scriptsize] {$E$};
  \draw[thick] (0.2,0.65) -- (1.6,0.65);
  \draw[thick] (0.2,2.6) -- (1.6,2.6) node[right] {HOMO};
  \draw[thick,gray] (0.2,5.85) -- (1.6,5.85) node[right] {LUMO};
  \draw[->,thick,purple] (2.1,2.6) -- (2.1,5.85);
  \node[right,align=left,font=\scriptsize] at (2.2,4.2) {$\Delta E$ large\\(UV, colorless)};
\end{scope}
\begin{scope}[xshift=7cm]
  \node[font=\small\bfseries] at (1,6.9) {long conjugated chain};
  \draw[->] (-0.3,0) -- (-0.3,6.1) node[above,font=\scriptsize] {$E$};
  \draw[thick] (0.2,0.16) -- (1.6,0.16);
  \draw[thick] (0.2,0.65) -- (1.6,0.65);
  \draw[thick] (0.2,1.46) -- (1.6,1.46);
  \draw[thick] (0.2,2.6) -- (1.6,2.6) node[right] {HOMO};
  \draw[thick,gray] (0.2,4.06) -- (1.6,4.06) node[right] {LUMO};
  \draw[->,thick,purple] (2.1,2.6) -- (2.1,4.06);
  \node[right,align=left,font=\scriptsize] at (2.2,3.3) {$\Delta E$ small\\(visible, colored)};
\end{scope}
```

*Figure 2.* Particle-in-a-box levels for a short versus a long conjugated chain,
scaled by $E_n \propto n^2/L^2$. Filled levels are occupied $\pi$ electrons up to
the HOMO; the LUMO is the lowest empty level. Doubling the box length while
adding electrons still shrinks the HOMO–LUMO gap, moving absorption from the
ultraviolet into the visible.

**Modern examples.** The high-performance organic pigments put that delocalized
gap in the visible and make the resulting crystal resistant to light.
**Quinacridone** (a linear five-ring system; the magentas and violets PV19,
PR122, PR202) and the **diketopyrrolopyrrole** (**DPP**) reds and oranges
(PR254 and its family) are compact conjugated chromophores whose molecules lock
together through dense networks of hydrogen bonds, stacking into tight,
insoluble, thermally and photochemically robust crystals. **Perylene** pigments
(PR149, PR179, and relatives) are large polycyclic π-systems with the same
structure. The **phthalocyanines** — copper phthalocyanine blue (PB15) and its
chlorinated green (PG7) — are macrocyclic: a large aromatic ring wrapped around
a metal ion, with a fully allowed π→π* absorption that gives a blue or green of
high tinting strength and near-total fastness. Quinacridones, DPPs, perylenes,
and phthalocyanines carry the top lightfastness ratings artists' pigments are
awarded — ASTM I, blue-wool 7–8 — because the chromophore is chemically the same
kind of object as the fugitive pigments below, engineered into a crystal that
resists the photochemistry that would otherwise degrade it.[@HerbstHunger2004;
@Christie2014]

**Historic precedents.** **Indigo** and **alizarin** run on the same physics and
fail at the point the modern pigments above were engineered to fix. Indigo is an
*indigoid* chromophore — a short, cross-conjugated system whose color comes from
the same delocalized π electrons, tuned by donor and acceptor groups to absorb
in the orange-red and appear blue. **Alizarin**, the red of **madder**, is an
*anthraquinone*: a conjugated three-ring core with hydroxyl and carbonyl groups
arranged to bring the gap into the visible. Mechanistically the absorption is
the story told above. But laid down as lakes on alumina (§1), these molecules
are exposed and mobile; light drives oxidative and photochemical breakdown of
the same π-system that produces the color, and madder lake in particular is
notoriously fugitive in thin films and tints. The mechanism is identical; the
permanence is engineered. Synthetic alizarin and synthetic indigo reproduce the
historic colors, but it is the quinacridones and DPPs — unrelated in structure,
equivalent in physics — that displaced them, by keeping the color and adding the
fastness the old lakes never had.[@Zollinger2003; @HerbstHunger2004]

## 4. Ligand-field d–d transitions

The second mechanism is inorganic, and lives in the partly filled $d$ shell of a
transition-metal ion. A free transition-metal ion has five $d$ orbitals that are
degenerate — all the same energy. Surrounding it with ligands (oxide ions,
water, the framework of a host crystal) breaks that degeneracy: the $d$
orbitals pointing *toward* the negatively charged ligands are pushed up in
energy, those pointing *between* them are lowered, and the set splits into
groups separated by the **crystal-field** (or ligand-field) splitting $\Delta$.
For ions such as Co²⁺, Cr³⁺, and Mn³⁺, $\Delta$ for common oxygen environments
falls in the visible window, so promoting an electron from a lower $d$ orbital
to an upper one — a **$d$–$d$ transition** — absorbs a visible photon and
produces color.

A selection rule governs how these pigments behave in practice: a $d$–$d$
transition is, strictly, **forbidden**. Both the starting and ending orbitals
are $d$ orbitals, so the transition does not change the parity (the inversion
symmetry) of the electronic state, and the **Laporte rule** forbids
electric-dipole transitions that fail to flip parity. The transition happens at
all only because vibrations and slight distortions of the metal site
momentarily break the perfect symmetry and "borrow" a little allowed character.
The consequence is that $d$–$d$ absorptions are **weak** — low molar
absorptivity, because each absorption event is improbable. Weak absorption per
molecule means **low tinting strength**: cobalt blue and viridian are
relatively transparent, easily overpowered when mixed, because their color
comes from a forbidden transition. §5 and §6 show the opposite case — strong,
allowed transitions producing the opposite behavior.

**Examples.** **Cobalt blue** is Co²⁺ sitting in the tetrahedral holes of an
aluminate spinel, CoAl₂O₄; the tetrahedral ligand field tunes the $d$–$d$ gap to
a clean blue. **Chromium oxide green** (Cr₂O₃) and its hydrated, more brilliant
relative **viridian** are Cr³⁺ in an oxide octahedron — the same ion that, in a
different host, makes a ruby red. These are excellent, permanent pigments: the
$d$–$d$ chromophore is buried inside a robust oxide lattice and is essentially
immune to light.

Ligand-field color is dominated by inorganic pigments, historic and modern
alike; there is no organic-for-inorganic swap to describe here, because the
mechanism is intrinsically tied to a metal ion. The modern development is in
the *host lattice*: mixed-metal-oxide and spinel pigments engineered to place a
chosen ion in a chosen coordination, dialing in hue, opacity, and durability.
**YInMn blue**, discovered in 2009, is the clearest recent example: Mn³⁺
trapped in an unusual *trigonal-bipyramidal* oxygen coordination inside a
YInO₃-type lattice, which splits its $d$ levels to absorb red and green
strongly and reflect a vivid, durable blue (Figure 3). The trigonal-bipyramidal
site has no center of inversion, so the Laporte rule that makes octahedral
cobalt and chromium $d$–$d$ transitions weak is relaxed: the transition becomes
symmetry-allowed, which is why YInMn is an intense, strong-tinting blue rather
than a pale one. The same selection rule that explains the weakness of cobalt
blue explains the strength of YInMn — it is the first new inorganic blue
chromophore in two centuries, produced by engineering the ligand field around
an existing ion rather than inventing a new molecule.[@SmithSubramanian2009;
@nassau2001physics]

```tikzpicture
\begin{scope}[xshift=0cm]
  \node[font=\small\bfseries,align=center] at (1.6,5.3) {octahedral site\\(cobalt, chromium)};
  \draw[thick] (-0.8,3.9) -- (0.4,3.9); \node[left,font=\scriptsize] at (-0.8,3.9) {free ion};
  \draw[thick] (1.8,1.1) -- (3.0,1.1) node[right] {$t_{2g}$};
  \draw[thick] (1.8,3.0) -- (3.0,3.0) node[right] {$e_g$};
  \draw[dashed,gray] (0.4,3.9) -- (1.8,3.0);
  \draw[dashed,gray] (0.4,3.9) -- (1.8,1.1);
  \draw[<->] (3.7,1.1) -- (3.7,3.0) node[midway,right] {$\Delta_{\mathrm{oct}}$};
  \draw[->,dashed,thick,gray] (2.4,1.3) -- (2.4,2.8);
  \node[align=center] at (2.4,0.4) {inversion center present\\\textbf{Laporte-forbidden}\\weak, pale color};
\end{scope}
\begin{scope}[xshift=7.5cm]
  \node[font=\small\bfseries,align=center] at (1.6,5.3) {trigonal-bipyramidal site\\(YInMn blue)};
  \draw[thick] (-0.8,3.9) -- (0.4,3.9); \node[left,font=\scriptsize] at (-0.8,3.9) {free ion};
  \draw[thick] (1.8,1.1) -- (3.0,1.1) node[right] {lower $d$ set};
  \draw[thick] (1.8,3.0) -- (3.0,3.0) node[right] {upper $d$ set};
  \draw[dashed,gray] (0.4,3.9) -- (1.8,3.0);
  \draw[dashed,gray] (0.4,3.9) -- (1.8,1.1);
  \draw[<->] (4.9,1.1) -- (4.9,3.0) node[midway,right] {$\Delta$};
  \draw[->,thick,red] (2.4,1.3) -- (2.4,2.8);
  \node[align=center] at (2.4,0.4) {no inversion center\\\textbf{Laporte-allowed}\\strong, intense color};
\end{scope}
```

*Figure 3.* Crystal-field splitting for an octahedral site (cobalt blue,
viridian) versus the trigonal-bipyramidal site in YInMn blue. Both split the
free ion's degenerate $d$ orbitals into two sets separated by $\Delta$, but only
the octahedral site retains an inversion center: its $d$–$d$ transition is
Laporte-forbidden and weak, while the noncentrosymmetric YInMn site makes the
same kind of transition Laporte-allowed and strong.

## 5. Charge-transfer transitions

The third mechanism also involves metals, but instead of an electron hopping
between two $d$ orbitals *on the same ion*, the electron jumps *from one site to
another* — from a ligand to a metal, or between two metal ions in different
oxidation states. These **charge-transfer** (CT) transitions are **fully
allowed**: the electron genuinely moves through space, the transition dipole is
large, and the absorption is intense. That is the key difference from §4. A CT
pigment has high molar absorptivity and therefore **high tinting strength and
deep color from a small amount of material** — the reverse of the weak,
forbidden $d$–$d$ pigments of §4.

The clearest examples of charge transfer are historic pigments — Prussian blue
and ultramarine — and both are covered directly below. The modern development
for this mechanism is not a new chromophore but reliable synthetic manufacture
of the same ones, described after the examples.

**Prussian blue** is the classic **intervalence charge transfer** (IVCT). Its
structure is a cyanide-bridged framework holding iron in two oxidation states,
Fe²⁺ and Fe³⁺. A visible photon drives an electron from an Fe²⁺ site, across the
bridging cyanide, onto a neighboring Fe³⁺ — momentarily swapping which iron is
which. That intervalence jump absorbs strongly across the red and gives Prussian
blue its deep, transparent blue with an absorption maximum near 700 nm; in the
Robin–Day scheme it is a Class II mixed-valence solid, valences localized but
coupled enough for the transfer to cost a visible photon's worth of
energy.[@ItayaUchida1986]

**Ultramarine** is the other major example, and its chromophore is often
misidentified: it is **not** the aluminosilicate **sodalite cage** that hosts
it. The cage is colorless. The color comes from **polysulfide radical anions
trapped inside it** — chiefly the **S₃⁻** radical anion, with some **S₂⁻**
contributing — whose electronic transitions (a charge-transfer-like excitation
within the trapped radical) absorb in the orange and yield ultramarine's blue.
The cage isolates and stabilizes these otherwise-reactive radicals; destroy the
cage and the color is lost, but the cage is the host, not the
chromophore.[@FleetLiu2010] The **iron-oxide earths** — yellow **ochre**
(hydrated FeO(OH)), red **sienna** and red oxides (Fe₂O₃), brown **umber** (iron
oxide with manganese) — round out this mechanism, their warm colors coming from
a combination of O→Fe **ligand-to-metal charge transfer** and weaker $d$–$d$
absorption on the iron; they are among the most permanent pigments humans have
ever used.

The modern development for this mechanism is reliable manufacture, not a new
chromophore. **Synthetic ultramarine** (made since the 1820s by firing china
clay, sulfur, and soda) reproduces the chromophore of ground lapis lazuli at a
fraction of the cost, with controlled, reproducible color. **Synthetic iron
oxides** (the "Mars" colors) give cleaner, stronger, more consistent earths than
dug ones. The CT chromophore itself is unchanged; what modernized is the supply.

## 6. Semiconductor band-gap absorption

The fourth mechanism looks similar to the others but behaves differently,
because it produces an absorption edge rather than an absorption band. In a
semiconductor, the electronic states are not discrete molecular levels but
continuous **bands** — a filled **valence band** and an empty **conduction
band**, separated by a forbidden **band gap** $E_g$ (Figure 4). A photon with
energy above $E_g$ promotes an electron across the gap and is absorbed; a
photon below $E_g$ has nowhere to put the electron and passes through. A
semiconductor absorbs everything with energy greater than $E_g$, all the way up
— so a band-gap pigment does not have an absorption *band* that rises and
falls, it has a sharp absorption **edge**: a cutoff wavelength below which it
absorbs strongly and above which it is transparent.

Moving the band gap across the visible window changes the color directly. If
$E_g$ is just above the violet end (~3 eV), the material absorbs only the faint
violet and looks pale or white. Lowering $E_g$ to ~2.6 eV means it starts eating
blue, so it reflects everything from green up and looks **yellow**. At ~2.3 eV
it eats blue and green and reflects orange-and-red — **orange**. At ~2.0 eV
only red survives — **red**. The color of a band-gap pigment is set by where
the edge sits, and a single chemical family with a tunable $E_g$ gives the
whole sequence yellow→orange→red (Figure 4).

```tikzpicture
\begin{scope}[xshift=0cm]
  \node[font=\small\bfseries] at (1.3,5.2) {band-gap absorption};
  \fill[blue!12] (0,0) rectangle (2.6,1.4);
  \draw[thick] (0,0) rectangle (2.6,1.4);
  \node at (1.3,0.7) {valence band};
  \fill[orange!12] (0,3.0) rectangle (2.6,4.4);
  \draw[thick] (0,3.0) rectangle (2.6,4.4);
  \node at (1.3,3.7) {conduction band};
  \draw[<->] (3.5,1.4) -- (3.5,3.0) node[midway,right] {$E_g$};
  \draw[->,thick,violet] (0.6,1.4) -- (0.6,3.0);
  \node[left,align=right,font=\scriptsize] at (0.5,2.2) {$h\nu>E_g$\\absorbed};
  \draw[->,thick,gray] (2.0,1.05) -- (2.0,1.75);
  \node[right,align=left,font=\scriptsize] at (2.9,1.05) {$h\nu<E_g$\\transmitted};
\end{scope}
\begin{scope}[xshift=6.4cm,yshift=1.4cm]
  \node[font=\small\bfseries] at (2,3.7) {\ce{CdS_{1-x}Se_x}: tuning $E_g$};
  \shade[left color=yellow!80!white,right color=red!70!black] (0,0) rectangle (4,0.8);
  \draw[thick] (0,0) rectangle (4,0.8);
  \foreach \x in {0,2,4} {
    \draw (\x,0) -- (\x,0.9);
  }
  \node[below,align=center,font=\scriptsize] at (0,-0.1) {\ce{CdS}\\$x=0$\\$E_g\approx2.4$ eV};
  \node[below,align=center,font=\scriptsize] at (2,-0.1) {$x=0.5$\\$E_g\approx2.0$ eV};
  \node[below,align=center,font=\scriptsize] at (4,-0.1) {\ce{CdSe}\\$x=1$\\$E_g\approx1.7$ eV};
\end{scope}
```

*Figure 4.* Left: band-gap absorption. A photon with energy above $E_g$
promotes an electron from the valence band to the conduction band and is
absorbed; a photon below $E_g$ passes through. Right: substituting selenium for
sulfur in CdS₁₋ₓSeₓ narrows $E_g$ continuously, sweeping the absorption edge —
and the reflected color — from yellow through orange to red as $x$ increases.

**Historic examples.** The **cadmium** pigments are the clearest illustration:
cadmium sulfide (CdS) has a band gap that makes it a bright yellow, and forming
the solid solution **CdS₁₋ₓSeₓ** — substituting larger selenium for sulfur —
narrows the gap continuously, sweeping the edge from yellow through orange to
deep red as $x$ increases (Figure 4). **Vermilion** (mercury(II) sulfide, HgS)
is a band-gap red; **chrome yellow** (lead chromate, PbCrO₄) a band-gap yellow.
All three are toxic — cadmium, mercury, lead — which is why this mechanism
needed a modern replacement.

**Modern replacements.** Here the modern work is reformulating away the
toxicity while keeping the band-gap color. **Bismuth vanadate** (BiVO₄, Pigment
Yellow 184) is a non-toxic, lightfast, high-opacity yellow whose band gap of
about 2.4 eV puts its absorption edge near 520 nm, reflecting a clean, strong
yellow that substitutes directly for cadmium and chrome yellows.[@Cooper2015]
The cadmium-free "**hues**" sold today combine this engineering: bismuth
vanadate, benzimidazolone and DPP organics (§3), and inorganic mixed oxides
blended to match the cadmium colors' hue and opacity without the cadmium.

| Mechanism | Physical origin | Selection rule / strength | Historic example | Modern example |
|:----------|:-----------------|:---------------------------|:-------------------|:------------------|
| Conjugated π-system (§3) | HOMO–LUMO gap of delocalized π electrons | Allowed; strength grows with conjugation length | Indigo, alizarin (madder) | Quinacridone, DPP, phthalocyanine |
| Ligand-field $d$–$d$ (§4) | Crystal-field splitting of a transition-metal ion's $d$ orbitals | Laporte-forbidden; weak, low tinting strength | Cobalt blue, viridian | YInMn blue (Laporte-allowed site) |
| Charge transfer (§5) | Electron transfer between two sites (ligand→metal or metal→metal) | Fully allowed; strong, high tinting strength | Prussian blue, ultramarine, iron oxides | Same chromophores, synthetic manufacture |
| Semiconductor band gap (§6) | Valence-to-conduction-band promotion above $E_g$ | Absorption edge, not a band; strength set by edge position | Cadmium yellows/reds, vermilion, chrome yellow | Bismuth vanadate, cadmium-free hues |

*Table 1.* The four mechanisms that place an electronic energy gap in the
1.8–3.1 eV visible window, compared by physical origin, transition strength,
and representative pigments.

With all four color-producing mechanisms in hand, the next question is how a
pigment's absorbed and unabsorbed light actually reaches the eye.

## 7. Absorption and scattering, together

Everything so far has been about **absorption** — which photons a pigment's
electrons can absorb. But a pigment in a binder does not merely absorb; it also
**scatters**, and the color actually seen is the combination of the two.
Absorption alone cannot explain why the same pigment is opaque in one medium and
transparent in another, why oil deepens color, or why titanium white is white
at all. Absorption and scattering are *independent* physical processes, and
appearance is their product.

**Subtractive perception, stated carefully.** When white light strikes a paint
film, the pigment absorbs some wavelengths and the rest are reflected back out.
The perceived color is the eye's integrated response to that **reflected**
spectrum — the light that was *not* absorbed, weighted across all wavelengths
by the sensitivities of the three cone types. The shorthand "absorbs red, looks
green" is frequently wrong: a pigment that absorbs a band in the green-yellow
looks magenta, and one that absorbs a broad swath looks a muddied mixture. The
perceived hue is the spectrally integrated complement of the absorption, not a
one-word opposite.

**Scattering as a separate contribution.** A pigment particle has a refractive
index; so does the binder around it. Whenever light crosses an interface between
two different refractive indices it bends and partly reflects, and a paint film
is packed with such interfaces — every particle surface. This is
**scattering**: **Mie** scattering when the particles are comparable in size to
the wavelength of light (the usual case for pigments, particle diameters of a
few tenths of a micron), shading toward **Rayleigh** scattering for particles
much smaller than the wavelength. The strength of the scattering is governed by
the **refractive-index contrast** between pigment and binder, $\Delta n =
n_\text{pigment} - n_\text{binder}$: a large contrast scatters light strongly
and makes the film **opaque** (high hiding power, because light is turned back
before it penetrates deep); a small contrast scatters weakly and makes the film
**transparent** (light passes through, and you see whatever is beneath).
Particle size matters too — there is an optimum particle diameter, around half
the wavelength of light, that maximizes scattering, which is why pigment
manufacturers grind to a target size, not merely "fine."

Two consequences follow. First, **why oil saturates color.** Linseed oil has a
refractive index of about 1.48, much higher than air's 1.00. Many pigments have
refractive indices around 1.5–2.0, so dispersing them in oil *lowers* the index
contrast $\Delta n$ relative to the same powder in air — the particles match the
oil more closely than they match air. Less contrast means less scattering at the
surface, so more light penetrates into the film, gets *absorbed* by the
chromophore on the way in and out, and emerges deeper and more saturated. This
is why a dry pigment powder looks pale and chalky but the instant it is wetted
with oil it darkens — the absorption was always there; what changed is that
suppressing the surface scattering let the light reach it. Second, **why
titanium white is such an intensely opaque white.** Rutile TiO₂ has a
refractive index near 2.7, enormous against any binder, giving the largest
$\Delta n$ of any common white pigment. It barely absorbs anything in the
visible (its band gap is in the UV), so it scatters *all* wavelengths almost
equally and intensely — the definition of a brilliant, high-hiding white.
Titanium white is pure scattering with almost no absorption; a saturated
phthalo blue is strong absorption with comparatively modest scattering; most
pigments are somewhere between.

**The quantitative bridge: Kubelka–Munk.** To turn "absorption and scattering
combine" into a number, the standard tool is **Kubelka–Munk** theory, a
two-flux model that treats a paint film as two diffuse light streams — one
toward the viewer, one into the film — coupled by an absorption coefficient $K$
and a scattering coefficient $S$ (Figure 5). Solving the two coupled equations
for an optically thick film (thick enough that the background does not show
through) gives the film's diffuse reflectance $R_\infty$, and the result
inverts into the relation colorist software is built
on:[@KubelkaMunk1931; @Berns2019]

```tikzpicture
\node[align=center,font=\small\bfseries] at (2,4.75) {viewer};
\node[align=center,font=\scriptsize] at (2,4.3) {air};
\fill[blue!7] (0,1.2) rectangle (4,4.0);
\draw[thick] (0,1.2) rectangle (4,4.0);
\node[align=center,font=\small] at (2,2.6) {film\\$K$ absorption\\$S$ scattering\\per unit thickness};
\node[below,font=\scriptsize] at (2,1.1) {substrate};
\draw[->,thick,red] (0.7,1.4) -- (0.7,3.8);
\node[right,font=\scriptsize] at (0.7,1.65) {$I$ (up)};
\draw[->,thick,blue] (3.3,3.8) -- (3.3,1.4);
\node[left,font=\scriptsize] at (3.3,3.55) {$J$ (down)};
\node[below,align=center,font=\scriptsize] at (2,0.5) {two coupled diffuse fluxes, $I$ toward the viewer and $J$ into the film};
```

*Figure 5.* Kubelka–Munk's two-flux model: an upward diffuse flux $I$ carries
light back to the viewer and a downward diffuse flux $J$ carries light into the
film, coupled by an absorption coefficient $K$ and a scattering coefficient $S$
per unit thickness.

$$
\frac{K}{S} = \frac{(1 - R_\infty)^2}{2\,R_\infty}.
$$

$K$ and $S$ are, to good approximation, additive over the pigments in a
mixture, weighted by concentration. Measuring $R_\infty$ of a masstone and a
tint gives $K/S$, from which the reflectance — and thus the color — of an
arbitrary blend can be predicted; this is what recipe-prediction and computer
color-matching do.

Kubelka–Munk's usefulness comes from several idealizing assumptions, which also
set its limits. It assumes **perfectly diffuse illumination** inside the film;
**isotropic scattering**, collapsing Mie theory's angular detail into a single
scalar $S$; **no separate term for specular surface reflection** off the top of
the film (gloss), which must be subtracted or measured around; and a
**homogeneous, optically thick** layer. It fails for **metallic and pearlescent
paints**, whose effect depends on the directional, anisotropic reflection K–M
discards. It fails for **very strongly absorbing** films, where $K/S$ runs
large, $R$ runs small, and the two-flux approximation loses accuracy. And it
fails for **thin or translucent layers** — glazes, watercolor washes — where the
optically-thick assumption does not hold, requiring the finite-thickness form
of the theory with the substrate included.

## 8. The limits

Three simplifications made earlier in this post are worth stating explicitly.

First, **subtractive complementarity is not exact.** "The color seen is the
complement of the color absorbed" is a useful approximation, but the perceived
hue is the eye's three-cone integral over the entire reflected spectrum (§7),
and absorption bands have width, structure, and overlap. Two pigments with
different spectra can match under one light source and diverge under another —
**metamerism** — which is exactly where the approximation breaks down.

Second, **Kubelka–Munk's idealizations** (§7) mean its predicted reflectances
are engineering-grade, not exact, and degrade precisely where its assumptions
do: gloss, deep shadows, thin glazes, metallics.

Third, **lightfastness.** A chromophore that absorbs visible photons is, by
construction, a molecule that routinely sits in electronically excited states
under illumination, and an excited state is a chemically reactive one. The same
delocalized π electrons that give an organic pigment its color can, once
excited, drive bond cleavage, oxidation, or rearrangement that destroys the
chromophore — the color **fades**. This is the physical price of the §3
mechanism, and it is why the historic lakes were fugitive: madder, carmine, and
the early synthetic dyes laid down as lakes present their reactive chromophores
in an exposed, mobile form, and the light that reveals the color also degrades
it.

Much of the history of synthetic organic pigments is the history of defeating
that fugitivity — taking the same chromophore classes and engineering them into
dense, hydrogen-bonded, insoluble crystals (the quinacridones, DPPs, perylenes,
and phthalocyanines of §3) where the excited molecule is locked in place and
its reactive pathways are sterically and electronically shut down, so a color
that fades in solution holds for centuries in the solid. This does not extend
uniformly across all pigment classes, however: even the best modern organics,
as a class, still tend to trail the great **inorganic** pigments — the iron
oxides, the cobalt and chromium oxides, the cadmiums — on outright permanence,
because a chromophore buried in an oxide lattice or a sulfide crystal is harder
for light to reach than one held in an organic molecule, however well packed.
And permanence trades against **toxicity**: the most durable historic
inorganics are heavy-metal compounds — cadmium, cobalt, lead, mercury — and the
reformulations of §6 (bismuth vanadate, the cadmium-free hues) are chasing the
genuinely hard target of matching their color *and* their permanence *without*
their toxicity. No single pigment yet wins on all three of fastness,
non-toxicity, and chroma at once; the palette is a set of engineering
compromises, and knowing the mechanism behind a color is knowing which
compromise it represents.

## The palette read as one piece

The abstractions from the earlier posts in this series correspond directly to
physical pigments. The particle in a box from the [fundamentals
post](/posts/fundementals_of_quantum_chemistry.html) is a quinacridone crystal:
confining π electrons to a conjugated frame sets the box length, and the box
length sets the gap that is the color. The molecular-orbital energy levels from
the [water](/posts/2026-06-30-reading-water-geometry-orbitals-acidity-spectra.html)
and [Hartree–Fock](/posts/2026-07-01-hartree-fock-and-the-correlation-gap.html)
posts — the spacing between a filled level and an empty one — are the hue on
the palette: a HOMO–LUMO gap in an organic pigment, a crystal-field splitting in
a transition-metal oxide, an intervalence jump in Prussian blue, a semiconductor
band edge in cadmium red. Four mechanisms, one requirement — an electronic
energy gap in the 1.8–3.1 eV window (Table 1) — and four different physical
routes to satisfy it.

A tube of paint is two separable problems. It is an **electronic-structure
problem**: which photons the chromophore's energy levels let it absorb,
computed by the same machinery this series has built. And it is a **scattering
problem**: how the particles' refractive index and size return the unabsorbed
light, governed by Mie scattering and summarized by Kubelka–Munk (§7). The two
are independent, and the eye perceives their product. The modern palette applies
the same two-part physics that produced the fugitive lakes and toxic brilliants
of the historic palette, but engineers the chromophore's host — the crystal, the
lattice, the coordination site — to survive the light it is made to be seen by.

## References
