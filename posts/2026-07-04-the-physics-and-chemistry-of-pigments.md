---
title: "The colors on the palette are energy-level gaps: engineering pigments for permanence"
date: 2026-07-04
author: Peter Johnston
tags: pigments, color, chromophores, lightfastness, charge transfer, ligand field, band gap, conjugation, Kubelka-Munk
description: A tube of paint is an electronic-structure problem plus a scattering problem, perceived by an eye. This post builds the mechanism-first taxonomy of color — conjugated π-systems, ligand-field d–d transitions, charge transfer, and semiconductor band gaps — leading with the modern synthetic pigments engineered to fix the lightfastness failures of their historic ancestors, then puts absorption and scattering back together with Kubelka–Munk.
---

Squeeze a worm of cadmium-red-*hue* acrylic onto a palette and the tube tells a
small lie of omission. The color is a diketopyrrolopyrrole — DPP, the same red
class that paints Ferraris — and it is there *because* the cadmium it imitates is
toxic and the older organic reds it descends from faded. That single tube holds
the whole story this post is about. The red you see is a HOMO–LUMO gap of a few
electron-volts, sitting exactly where the eye can see it; the fact that it will
still be that red in a century is a separate, hard-won piece of molecular
engineering; and the reason it exists at all is that the same color physics, met
again and again across the history of painting, kept producing pigments that were
either beautiful-and-fugitive or permanent-and-poisonous. The modern palette is
the old physics, re-engineered.

The earlier posts in this series built the machinery for the first of those
claims without ever pointing it at paint. The
[fundamentals post](/posts/fundementals_of_quantum_chemistry.html) solved the
particle in a box and found that confining an electron quantizes its energy into
discrete levels whose spacing shrinks as the box grows. The
[water post](/posts/2026-06-30-reading-water-geometry-orbitals-acidity-spectra.html)
and the [Hartree–Fock post](/posts/2026-07-01-hartree-fock-and-the-correlation-gap.html)
turned those levels into molecular orbitals with computable energies, and noted
in passing that the gap between a filled and an empty orbital is what a molecule
shows to light. A pigment is where that abstraction cashes out as something you
can hold. This post answers three questions in order — *what is a pigment*, *what
molecular structures make it colored*, and *how does it physically interact with
light* — and threads one contrast through all three: lightfastness, the price some
colors pay for being made of the wrong electrons.

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
refractive index, all of which will matter enormously in §7. The binder's job is
to glue those particles to a surface and to each other, not to take them into
solution. When you thin a tube color, you are diluting a suspension, not a
solution.[@Berns2019; @Christie2014]

The boundary case is the one that plants this post's theme. A **lake** is a dye
made to behave like a pigment by precipitating it onto an inert, colorless
particulate substrate — historically aluminum hydroxide, sometimes chalk or a
metal salt. The soluble dye is *adsorbed* or chemically fixed onto the substrate
grains, and the resulting colored solid is then ground into a binder exactly like
any pigment. **Madder lake** (the dye alizarin laid down on alumina) and
**carmine** (cochineal's carminic acid, likewise laked) are the canonical
examples — gorgeous, deep, transparent reds and crimsons that were the glory of
historic palettes. They are also, not coincidentally, among the most **fugitive**
colors ever used: the very molecules that make a brilliant transparent lake are
the ones that photochemically decompose under light. Hold that thought — it is the
seed of the entire modern-versus-historic contrast, and a lake is the cleanest
place to plant it, because a lake is a dye wearing a pigment's clothing, and it
fades like the dye it is.[@Eastaugh2008; @Zollinger2003]

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
roughly **400 to 700 nm**, which in energy is about **3.1 down to 1.8 eV**. That
window is narrow and it is the whole game: a substance is colored if and only if
it has an accessible electronic transition — an energy gap between an occupied and
an empty state — that lands *inside* it. A gap larger than ~3.1 eV absorbs only in
the ultraviolet and leaves all visible light untouched (the material is white,
clear, or colorless); a gap smaller than ~1.8 eV absorbs in the infrared and, if
it absorbs *across* the whole visible range, reads as black or gray or metallic.
Color is what happens when the gap is tuned into the slot between.

So "what molecular structures produce color" is really "what physical mechanisms
put an electronic energy gap in the 1.8–3.1 eV window, and let an electron cross
it when a photon arrives." There are four that matter for pigments, and they are
genuinely different physics, not four flavors of one idea. The sections that
follow take them in turn. In each, I lead with the **modern** pigment that is the
honest current example, and use the **historic** pigment as the foil — same
mechanism, different fate under light.

## 3. Extended conjugated π-systems

This is the organic-chemistry mechanism, and it is the one that connects most
directly to the particle in a box. Take a chain or ring system of alternating
single and double bonds — a **conjugated** π-system. The π electrons are not stuck
on individual bonds; they delocalize over the whole conjugated framework, free to
roam from one end to the other. That is, to a first approximation, *exactly* an
electron in a box, where the box length $L$ is the length of the conjugated path.
The [fundamentals post](/posts/fundementals_of_quantum_chemistry.html) gave the
levels of that box,

$$
E_n = \frac{n^2 h^2}{8 m L^2},
$$

and the only new ingredient is to fill them. If the conjugated system holds $N$ π
electrons, they occupy the lowest $N/2$ levels (two per level, by Pauli), so the
highest occupied level is $n = N/2$ and the lowest empty one is $n = N/2 + 1$. The
photon that colors the molecule is the one that lifts an electron across that
HOMO–LUMO gap:

$$
\Delta E = E_{N/2+1} - E_{N/2}
        = \frac{h^2}{8 m L^2}\,(N+1).
$$

Now read what that says. Lengthen the conjugated chain and two things happen
together: you add electrons (raising $N$) but you lengthen the box faster (raising
$L^2$ in the denominator, with $L$ growing roughly in proportion to $N$). The net
effect is that $\Delta E$ *shrinks* as conjugation extends — a longer box has a
smaller gap. A short conjugated system absorbs in the ultraviolet and looks
colorless; extend it and the absorption marches down through violet, blue, green,
into the visible as a yellow, then orange, then red. **Longer box, smaller gap,
redder color.** This free-electron picture is too crude for quantitative work — it
ignores bond alternation, the real shape of the potential, and electron
correlation, all of the things the [Hartree–Fock
post](/posts/2026-07-01-hartree-fock-and-the-correlation-gap.html) was at pains to
put back — but the trend it predicts is correct and it is the reason essentially
every strong organic colorant is a large, flat, conjugated molecule.[@Christie2014; @nassau2001physics]

**Lead examples — the modern workhorses.** The high-performance organic pigments
are built to put that delocalized gap in the visible *and* to make the resulting
crystal nearly indestructible by light. **Quinacridone** (a linear five-ring
system, the magentas and violets PV19, PR122, PR202) and the **diketopyrrolopyrrole**
(**DPP**) reds and oranges (PR254, the "Ferrari red," and its family) are compact
conjugated chromophores whose molecules lock together in the solid through dense
networks of hydrogen bonds, stacking into tight, insoluble, thermally and
photochemically robust crystals. **Perylene** pigments (PR149, PR179 and
relatives) are large polycyclic π-systems with the same story. And the
**phthalocyanines** — copper phthalocyanine blue (PB15) and its chlorinated green
(PG7) — are the modern macrocyclic monarch: a huge aromatic ring wrapped around a
metal ion, with an enormous, fully allowed π→π* absorption that gives a blue or
green of ferocious tinting strength and near-total fastness. These are not
delicate. Quinacridones, DPPs, perylenes, and phthalocyanines carry the top
lightfastness ratings artists' pigments are awarded — ASTM I, blue-wool 7–8 —
because their chromophores are chemically the same kind of object as the fugitive
ones below, but engineered into crystals that shrug off the photochemistry.[@HerbstHunger2004; @Christie2014]

**Foil — the historic ancestors.** The two most important pre-industrial organic
colorants run on identical physics and fail at exactly the point the moderns are
hardened. **Indigo** is an *indigoid* chromophore — a short, cross-conjugated
system whose color comes from the same delocalized π electrons, tuned by the
molecule's donor and acceptor groups to absorb in the orange-red and look blue.
**Alizarin**, the red of **madder**, is an *anthraquinone*: a conjugated
three-ring core with hydroxyl and carbonyl groups arranged to drop the gap into
the visible. The chemistry of the absorption is, mechanistically, the same story
told in §3 so far. But laid down as lakes on alumina (§1), these molecules are
exposed, mobile, and vulnerable; light drives oxidative and photochemical
breakdown of the very π-system that produces the color, and madder lake in
particular is notoriously fugitive in thin films and tints. The payoff is the
sharpest in this slot and worth stating flatly: **the mechanism is identical, the
permanence is engineered.** Synthetic alizarin and synthetic indigo reproduce the
historic colors; the quinacridones and DPPs that displaced them in the modern
palette keep the color and add the fastness the old lakes never had.[@Zollinger2003; @HerbstHunger2004]

## 4. Ligand-field d–d transitions

The second mechanism is inorganic and lives in the partly filled $d$ shell of a
transition-metal ion. A free transition-metal ion has five $d$ orbitals that are
degenerate — all the same energy. Surround it with ligands (oxide ions, water,
the framework of a host crystal) and that degeneracy breaks: the $d$ orbitals
pointing *toward* the negatively charged ligands are pushed up in energy, those
pointing *between* them are lowered, and the set splits into groups separated by
the **crystal-field** (or ligand-field) splitting $\Delta$. For ions like Co²⁺,
Cr³⁺, Mn³⁺ and their neighbors, $\Delta$ for common oxygen environments falls
right in the visible window, so promoting an electron from a lower $d$ orbital to
an upper one — a **$d$–$d$ transition** — absorbs a visible photon and produces
color.

There is a crucial honest caveat that ties straight to how these pigments
*behave*. A $d$–$d$ transition is, strictly, **forbidden**. Both the starting and
ending orbitals are $d$ orbitals, so the transition does not change the parity
(the inversion symmetry) of the electronic state, and the **Laporte rule** forbids
electric-dipole transitions that fail to flip parity. The transition happens at
all only because vibrations and slight distortions of the metal site momentarily
break the perfect symmetry and "borrow" a little allowed character. The
consequence is that $d$–$d$ absorptions are **weak** — small molar absorptivity,
because each absorption event is improbable. Weak absorption per molecule means
**low tinting strength**: cobalt blue and viridian are relatively transparent and
mild tinters, easily overpowered when mixed, precisely because their color comes
from a forbidden transition. Keep that number in mind; in §5 and §6 the opposite
case — strong, allowed transitions — gives the opposite behavior.

**Examples.** **Cobalt blue** is Co²⁺ sitting in the tetrahedral holes of an
aluminate spinel, CoAl₂O₄; the tetrahedral ligand field tunes the $d$–$d$ gap to a
clean blue. **Chromium oxide green** (Cr₂O₃) and its hydrated, more brilliant
cousin **viridian** (hydrated Cr₂O₃) are Cr³⁺ in an oxide octahedron, the same ion
whose $d$–$d$ transitions, in a different host, make a ruby red. These are
excellent, permanent pigments — the $d$–$d$ chromophore is buried inside a robust
oxide lattice and is essentially immune to light.

This is the slot where I have to be honest that the "modern" framing bends.
Ligand-field color is dominated by inorganics, old and new; there is no
synthetic-organic swap to make here, because the mechanism is intrinsically a
metal-ion mechanism. The genuine modern story is the *engineering of the host
lattice* — designing **mixed-metal-oxide** and **spinel** pigments that place a
chosen ion in a chosen coordination to dial in hue, opacity, and durability. The
cleanest recent example is **YInMn blue**, discovered in 2009: Mn³⁺ trapped in an
unusual *trigonal-bipyramidal* oxygen coordination inside a YInO₃-type lattice,
which splits its $d$ levels so as to absorb red and green strongly and reflect a
vivid, durable blue — the first genuinely new inorganic blue chromophore in two
centuries, and a textbook case of getting a new color by engineering the ligand
field around an old ion rather than inventing a new molecule.[@SmithSubramanian2009; @nassau2001physics]

## 5. Charge-transfer transitions

The third mechanism also involves metals, but instead of an electron hopping
between two $d$ orbitals *on the same ion*, the electron jumps *from one site to
another* — from a ligand to a metal, or between two metal ions in different
oxidation states. These **charge-transfer** (CT) transitions are **fully allowed**:
the electron genuinely moves through space, the transition dipole is large, and
the absorption is intense. That is the headline difference from §4. A CT pigment
has enormous molar absorptivity and therefore **high tinting strength and deep
color from a small amount of material** — the mirror image of the weak, forbidden
$d$–$d$ pigments. Allowed transitions absorb hard; forbidden ones absorb softly;
tinting strength follows directly.

I am going to be plain about something here, because the spine of this post is
modern-pigments-first and this is the one slot where that spine honestly bends.
The canonical, best-teaching examples of charge transfer are **historic**
pigments, and forcing a modern example into the lead position would be dishonest.
Prussian blue and ultramarine remain the clearest demonstrations of the mechanism
anyone has, so I lead with them and let the modern thread be what it actually is —
the displacement of *natural* sources by *synthetic, reliably manufactured*
versions of the same materials.

**Prussian blue** is the classic **intervalence charge transfer** (IVCT). Its
structure is a cyanide-bridged framework holding iron in two oxidation states,
Fe²⁺ and Fe³⁺. A visible photon drives an electron from an Fe²⁺ site, across the
bridging cyanide, onto a neighboring Fe³⁺ — momentarily swapping which iron is
which. That intervalence jump absorbs strongly across the red and gives Prussian
blue its deep, transparent blue with an absorption maximum near 700 nm; in the
Robin–Day scheme it is a Class II mixed-valence solid, valences localized but
coupled enough for the transfer to cost a visible photon's worth of
energy.[@ItayaUchida1986] **Ultramarine** is the other great teacher, and it
carries a correction that is easy to get wrong: the chromophore is **not** the
beautiful aluminosilicate **sodalite cage** that hosts it. The cage is colorless.
The color comes from **polysulfide radical anions trapped inside it** — chiefly the
yellow-blue-absorbing **S₃⁻** radical anion, with some **S₂⁻** contributing — whose
electronic transitions (a charge-transfer-like excitation within the trapped
radical) absorb in the orange and yield ultramarine's pure blue. The cage's role
is to isolate and stabilize these otherwise-reactive radicals; destroy the cage
and you lose the color, but the cage is the host, not the chromophore.[@FleetLiu2010]
The **iron-oxide earths** — yellow **ochre** (hydrated FeO(OH)), red **sienna** and
red oxides (Fe₂O₃), brown **umber** (iron oxide with manganese) — round out the
slot, their warm colors coming from a combination of O→Fe **ligand-to-metal charge
transfer** and weaker $d$–$d$ absorption on the iron; they are the most permanent,
most stable pigments humans have ever used.

The modern thread, stated honestly, is not a new mechanism but reliable
manufacture. **Synthetic ultramarine** (made since the 1820s by firing china clay,
sulfur, and soda) reproduces the chromophore of ground lapis lazuli at a
thousandth of the cost and with controlled, reproducible color; **synthetic iron
oxides** (the "Mars" colors) give cleaner, stronger, more consistent earths than
dug ones. The CT chromophore is ancient; what modernized is the supply.

## 6. Semiconductor band-gap absorption

The fourth mechanism is the one that requires the most care to state correctly,
because it looks like the others and behaves differently. In a semiconductor, the
electronic states are not discrete molecular levels but continuous **bands** — a
filled **valence band** and an empty **conduction band**, separated by a forbidden
**band gap** $E_g$. A photon with energy *above* $E_g$ can promote an electron
across the gap and is absorbed; a photon *below* $E_g$ has nowhere to put the
electron and passes through. The critical word is *above*: a semiconductor absorbs
**everything** with energy greater than $E_g$, all the way up. So a band-gap
pigment does not have an absorption *band* — a peak that rises and falls — it has a
sharp absorption **edge**, a cutoff wavelength below which it absorbs strongly and
above which it is transparent. Get this distinction right and the colors fall out
immediately.

Slide the band gap across the visible window and watch the color change. If $E_g$
is just above the violet end (~3 eV), the material absorbs only the faint violet
and looks pale or white. Lower $E_g$ to ~2.6 eV and it starts eating blue, so it
reflects everything from green up and looks **yellow**. Lower it to ~2.3 eV and it
eats blue and green and reflects orange-and-red — **orange**. Lower it to ~2.0 eV
and only red survives — **red**. The color of a band-gap pigment is set by *where
the edge sits*, and a single chemical family that lets you tune $E_g$ gives a
whole sequence yellow→orange→red.

**Foil — the clean teaching cases.** The **cadmium** pigments are the textbook
illustration: cadmium sulfide (CdS) has a band gap that makes it a bright yellow,
and forming the solid solution **CdS₁₋ₓSeₓ** — substituting larger selenium for
sulfur — *narrows* the gap continuously, sweeping the edge from yellow through
orange to deep red as $x$ increases. One mechanism, one tunable knob, the entire
warm end of the spectrum. **Vermilion** (mercury(II) sulfide, HgS) is a band-gap
red; **chrome yellow** (lead chromate, PbCrO₄) a band-gap yellow. They are
gorgeous and they are the reason the slot needs a modern lead, because every one
of them is a heavy-metal poison — cadmium, mercury, lead.

**Lead — the genuinely modern materials story.** Here the modern example is not a
museum substitute but a live materials-science program: **reformulating away the
toxicity while keeping the band-gap color.** **Bismuth vanadate** (BiVO₄, Pigment
Yellow 184) is a non-toxic, lightfast, high-opacity yellow whose band gap of about
2.4 eV puts its absorption edge near 520 nm — reflecting a clean, strong yellow
that can stand in for cadmium and chrome yellows directly.[@Cooper2015] The
cadmium-free "**hues**" sold today are exactly this engineering: bismuth vanadate,
benzimidazolone and DPP organics (§3), and inorganic mixed oxides blended to match
the cadmium colors' hue and opacity without the cadmium. It is a real reformulation
driven by real toxicology, and it is the honest modern face of the band-gap
mechanism — not a historical footnote but a current one.

## 7. Absorption and scattering, together

Everything so far has been about **absorption** — which photons a pigment's
electrons can swallow. But a pigment in a binder does not merely absorb; it also
**scatters**, and the color you actually see is the combination of the two. Treat
absorption alone and you cannot explain why the same pigment is opaque in one
medium and transparent in another, why oil deepens color, or why titanium white is
white at all. Absorption and scattering are *independent* physical processes, and
appearance is their product.

**Subtractive perception, stated carefully.** When white light strikes a paint
film, the pigment absorbs some wavelengths and the rest are reflected back out. The
perceived color is the eye's integrated response to that **reflected** spectrum —
the light that was *not* absorbed, weighted across all wavelengths by the
sensitivities of the three cone types. It is tempting to compress this to "absorbs
red, looks green," and that shorthand is wrong often enough to be worth refusing. A
pigment that absorbs a band in the green-yellow looks magenta; one that absorbs a
broad swath looks some muddied mixture; the perceived hue is the *spectrally
integrated complement* of the absorption, not a one-word opposite. The color is in
the leftover light, summed over the whole visible range.

**Scattering as a separate contribution.** A pigment particle has a refractive
index; so does the binder around it. Whenever light crosses an interface between
two different refractive indices it bends and partly reflects, and a paint film is
packed with such interfaces — every particle surface. This is **scattering**:
**Mie** scattering when the particles are comparable in size to the wavelength of
light (the usual case for pigments, particle diameters of a few tenths of a
micron), shading toward **Rayleigh** scattering for particles much smaller than the
wavelength. The strength of the scattering is governed by the **refractive-index
contrast** between pigment and binder, $\Delta n = n_\text{pigment} -
n_\text{binder}$: a large contrast scatters light strongly and makes the film
**opaque** (high hiding power, because light is turned back before it penetrates
deep); a small contrast scatters weakly and makes the film **transparent** (light
passes through, and you see whatever is beneath). Particle size matters too — there
is an optimum particle diameter, around half the wavelength of light, that
maximizes scattering, which is why pigment manufacturers grind to a target size,
not merely "fine."

Two consequences worth naming. First, **why oil saturates color.** Linseed oil has
a refractive index of about 1.48, much higher than air's 1.00. Many pigments have
refractive indices around 1.5–2.0, so dispersing them in oil *lowers* the
index contrast $\Delta n$ relative to the same powder in air — the particles
"match" the oil more closely than they match air. Less contrast means less
scattering at the surface, so more light penetrates into the film, gets *absorbed*
by the chromophore on the way in and out, and emerges deeper and more saturated.
This is why a dry pigment powder looks pale and chalky but the instant it is wetted
with oil it "comes alive" and darkens — the absorption was always there; what
changed is that suppressing the surface scattering let the light reach it. Second,
**why titanium white is such a fierce white.** Rutile TiO₂ has a refractive index
near 2.7, enormous against any binder, giving the largest $\Delta n$ of any common
white pigment. It barely absorbs anything in the visible (its band gap is in the
UV), so it scatters *all* wavelengths almost equally and intensely — the definition
of a brilliant, high-hiding white. Titanium white is pure scattering with almost no
absorption; a saturated phthalo blue is strong absorption with comparatively modest
scattering; most pigments are somewhere between.

**The quantitative bridge: Kubelka–Munk.** To turn "absorption and scattering
combine" into a number you can predict, the standard tool is **Kubelka–Munk**
theory, a two-flux model that treats a paint film as supporting just two diffuse
light streams — one heading up toward the viewer, one down into the film — coupled
by an absorption coefficient $K$ and a scattering coefficient $S$. Solving the two
coupled equations for an optically thick film (thick enough that the background
does not show through) gives the film's diffuse reflectance $R_\infty$, and the
result inverts into the relation every colorist's software is built on:[@KubelkaMunk1931; @Berns2019]

$$
\frac{K}{S} = \frac{(1 - R_\infty)^2}{2\,R_\infty}.
$$

The power of this is that $K$ and $S$ are, to good approximation, *additive* over
the pigments in a mixture, weighted by concentration. Measure $R_\infty$ of a
masstone and a tint, extract $K/S$, and you can predict the reflectance — and thus
the color — of an arbitrary blend, which is exactly what recipe-prediction and
computer color-matching do.

But the model earns its usefulness by idealizing hard, and honesty requires the
assumptions out loud. Kubelka–Munk assumes **perfectly diffuse illumination**
inside the film; it assumes **isotropic scattering**, collapsing all of Mie
theory's angular detail into a single scalar $S$; it carries **no separate term for
the specular surface reflection** off the top of the film (the gloss), which has to
be subtracted or measured around; and it assumes a **homogeneous, optically thick**
layer. Where those break, the model breaks. It fails for **metallic and pearlescent
paints**, whose whole effect is the directional, anisotropic reflection K–M throws
away. It fails for **very strongly absorbing** films, where $K/S$ runs large, $R$
runs small, and the two-flux approximation loses accuracy. And it fails for **thin
or translucent layers** — glazes, watercolor washes — where the optically-thick
assumption is simply false and one must use the finite-thickness form of the theory
with the substrate explicitly included. K–M is the right machinery and it is an
idealization; both halves are true.

## 8. The limits

The honest accounting, gathered in one place. Three things in this post are cleaner
on the page than in reality.

First, **subtractive complementarity is not exact.** "The color seen is the
complement of the color absorbed" is a useful slogan and a real approximation, but
the perceived hue is the eye's three-cone integral over the entire reflected
spectrum (§7), and absorption bands have width, structure, and overlap. Two
pigments with quite different spectra can match in one light and diverge in another
— **metamerism** — which is precisely the failure of the slogan to be a law.

Second, **Kubelka–Munk's idealizations** (§7) mean its predicted reflectances are
engineering-grade, not exact, and degrade exactly where its assumptions do —
gloss, deep shadows, thin glazes, metallics.

Third, and this is where the post's spine lands: **lightfastness.** A chromophore
that absorbs visible photons is, by construction, a molecule that routinely sits in
electronically excited states under illumination — and an excited state is a
chemically reactive state. The same delocalized π electrons that give an organic
pigment its color can, once excited, drive bond cleavage, oxidation, or
rearrangement that destroys the chromophore: the color **fades**. This is the
physical price of the §3 mechanism, and it is why the **historic lakes were
fugitive** — madder, carmine, and the early synthetic dyes laid down as lakes
present their reactive chromophores in an exposed, mobile form, and the light that
reveals them also dismantles them.

The whole history of synthetic organic pigments is, in large part, **the history of
defeating that fugitivity** — taking the same chromophore classes and engineering
them into dense, hydrogen-bonded, insoluble crystals (the quinacridones, DPPs,
perylenes, and phthalocyanines of §3) where the excited molecule is locked in
place, its reactive pathways sterically and electronically shut down, so the color
that fades in solution holds for centuries in the solid. That is the modern-forward
through-line made concrete: identical physics, engineered permanence. But the honesty
cuts both ways. Even the best modern organics, as a class, still tend to trail the
great **inorganic** pigments — the iron oxides, the cobalt and chromium oxides, the
cadmiums — on outright permanence, because a chromophore buried in an oxide lattice
or a sulfide crystal is harder for light to reach than one held in an organic
molecule, however well packed. And the countervailing cost is **toxicity**: the most
bulletproof historic inorganics are heavy-metal compounds — cadmium, cobalt, lead,
mercury — and the reformulations of §6 (bismuth vanadate, the cadmium-free hues) are
chasing the genuinely hard target of matching their color *and* their permanence
*without* their poison. No single pigment yet wins on all three of fastness,
non-toxicity, and chroma at once; the palette is a set of compromises, and knowing
the mechanism is knowing which compromise you are making.

## The palette read as one piece

Step back and the abstractions of the earlier posts have quietly become physical
objects you can buy in a tube. The particle in a box from the
[fundamentals post](/posts/fundementals_of_quantum_chemistry.html) is a
quinacridone crystal: confine π electrons to a conjugated frame and the box length
sets the gap, and the gap *is* the color. The molecular-orbital energy levels of
the [water](/posts/2026-06-30-reading-water-geometry-orbitals-acidity-spectra.html)
and [Hartree–Fock](/posts/2026-07-01-hartree-fock-and-the-correlation-gap.html)
posts — the spacing between a filled level and an empty one — are, literally, the
hue on the palette: in an organic pigment a HOMO–LUMO gap, in a transition-metal
oxide a crystal-field splitting, in Prussian blue an intervalence jump, in cadmium
red a semiconductor band edge. Four mechanisms, one underlying statement — *put an
electronic energy gap in the 1.8–3.1 eV window* — and four engineering routes to
get there.

A tube of paint, then, is two problems stacked. It is an **electronic-structure
problem** — which photons the chromophore's energy levels let it absorb, computed
by exactly the machinery this series has been building — and it is a **scattering
problem** — how the particles, their refractive index, and their size return the
unabsorbed light, governed by Mie scattering and summarized by Kubelka–Munk. The
two are independent and the eye perceives their product. And the modern palette is
that same two-part physics, met across centuries and then deliberately
re-engineered: the identical chromophore classes that gave the old masters their
fugitive lakes and their poisonous brilliants, rebuilt into crystals chosen to
survive the very light they are made to be seen by. The colors were always
energy-level gaps. What changed is that we learned to make the gaps last.

## References
