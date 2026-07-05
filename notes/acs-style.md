# ACS-style authoring for the science series

Companion to `blog-authoring.md`. That file governs the *mechanics* of a post
(front matter, citations, figures, captions). This file governs the *structure
and voice* of the **ACS-style computational posts** — the ones written as a
formal note with an Abstract, Experimental Section, etc. The in-repo exemplar is
[`posts/2026-01-16-quantum-tunneling-workflow.md`](../posts/2026-01-16-quantum-tunneling-workflow.md);
match its skeleton.

Not every science post uses this structure — the essay-style posts (molar
absorptivity, pigments, Hartree–Fock) are prose-first and do **not** take ACS
sectioning. Use ACS structure when the post *is* a study: it runs calculations,
reports numbers, and interprets them. The UV–Vis push–pull post is one of these.

## 1. Canonical section order

The ACS Guide to Scholarly Communication subdivides an article into
**Introduction → Experimental Section → Results and Discussion → Conclusions**,
and these sections are **not numbered**. Our house adaptation (from the tunneling
post) wraps that core with an Abstract and provenance:

```
## Abstract
## Introduction
## Experimental Section            (a.k.a. Computational Details)
## Results and Discussion          (may split into ## Results + ## Discussion)
## Conclusions                     (optional but recommended)
## Limitations and Future Work     (optional)
## Authorship and Provenance       (house convention — AI-authored disclosure)
## References
```

For a computational post, title the methods section **Computational Details**
rather than "Experimental Section" — that is the accepted ACS variant for
theory/simulation work (there is no wet-lab bench).

## 2. The one rule that prevents the frequent error

The recurring mistake is **mixing content across sections** — putting
interpretation in Results, or data in Discussion, or restating Results in the
Conclusion. Prevent it by tagging every sentence with the question it answers and
filing it accordingly:

| Section | Answers | Contains | Never contains |
| --- | --- | --- | --- |
| Introduction | *Why?* | Motivation, prior work, the gap, the question this post closes | Your new numbers; method detail |
| Computational Details | *How?* | Level of theory, basis, functional, geometry protocol, software + versions, broadening parameters — enough to reproduce | Any result; any interpretation |
| Results | *What?* | The computed numbers and what the figures/tables literally show. Objective, factual, no "because" | Mechanism, comparison to literature, judgments |
| Discussion | *So what?* | Interpretation, trends, why the numbers came out this way, agreement/disagreement with experiment and with other functionals | Any number not already in Results |
| Conclusions | *Now what?* | One paragraph: the take-home, its significance, what it enables next | Restatement of the abstract; new data; new interpretation |

If Results and Discussion are **combined** (ACS permits this, and it often reads
better for a short computational note), the discipline still holds *within*
paragraphs: state the number, then interpret it — never interpret a number you
haven't yet stated.

## 3. Worked boundary cases (from this UV–Vis post)

**Transition energies.**
- *Computational Details:* "Vertical excitation energies were computed with
  TD-DFT (B3LYP and CAM-B3LYP) in the def2-TZVP basis at B3LYP/def2-SVP
  geometries."
- *Results:* "The lowest bright transition of benzene appears at 176 nm
  (7.03 eV, *f* = 0.58); adding the amino donor (aniline) red-shifts the lowest
  bright band to 269 nm (4.61 eV, *f* = 0.044)."
- *Discussion:* "The red shift on donor substitution reflects HOMO
  destabilization by the nitrogen lone pair, which narrows the HOMO–LUMO gap
  without lengthening the conjugated bridge."
- *Conclusions:* "A donor and an acceptor on the same benzene bridge open a
  charge-transfer band neither substituent produces alone — color engineered by
  substitution, not by chain length."

**The aniline geometry (a live example of the Results/Discussion line).**
- *Results* states the fact: "Aniline optimized to a planar (C₂ᵥ) minimum at
  B3LYP/def2-SVP."
- *Discussion* interprets and caveats it: "Gas-phase aniline is pyramidal at
  nitrogen (≈42° wag); the planar minimum here is a known small-basis/functional
  artifact that overstabilizes amino conjugation, so the donor red shift is a
  mild upper bound." The bare fact is a Result; the "known artifact, therefore
  upper bound" is Discussion. Do not merge them into a single hedged sentence in
  Results.

**Functional disagreement.** *That* B3LYP and CAM-B3LYP place the pNA
charge-transfer band at different energies is a Result (report both numbers).
*Why* — global hybrids underbind long-range CT states, corrected by
range separation — is Discussion (cite Dreuw & Head-Gordon).

## 4. Tense

ACS convention, and it also enforces the section split:
- **Past tense** for what you did and what you found: "The band appeared at
  176 nm"; "Geometries were optimized…". Use it in Computational Details and
  Results.
- **Present tense** for established facts and general truths: "Charge-transfer
  states destabilize as donor–acceptor separation grows." Use it in Introduction
  and Discussion.
- **Present tense** to refer to the paper's own exhibits: "Figure 1 shows…",
  "Table 1 lists…" — never "Figure 1 showed."

## 5. ACS conventions beyond structure

- **Numbers and units.** Space between value and unit (7.03 eV, 176 nm, not
  7.03eV). Report to justified precision; excitation energies to 0.01 eV, *f* to
  2–3 significant figures. Use unicode → for transitions (π→π*, n→π*, HOMO→LUMO).
- **Figures/tables/code.** Every one numbered, captioned, and referenced by
  number in the prose — this is already required by `blog-authoring.md` §6. ACS
  additionally wants the caption to make the exhibit **self-explanatory** without
  the body text.
- **Spectra as figures.** Per house preference, render spectra as **TikZ/pgfplots
  from the emitted data arrays** (broadened ε(λ) grid + stick list), not raster
  PNGs. Figure 1 is still the hero/OG card at 1200×630.
- **Citations.** Science series uses Pandoc `[@key]` into the shared bib
  (`blog-authoring.md` §3–4). The bib already holds the TD-DFT keys you'll need:
  `Casida1995`, `Dreuw2004`, `Laurent2013`, `Jacquemin2009`.
- **Abstract.** One paragraph, self-contained, no citations, no figure
  references. States what was done and the single most important result.
- **Provenance.** These posts are AI-authored; keep the "Authorship and
  Provenance" note the tunneling post established.

## 6. Pre-publish self-check

1. Read only the **Results** headers' paragraphs: is there a single "because,"
   "suggests," "due to," or comparison to literature? → move it to Discussion.
2. Read only the **Discussion**: does it introduce any number, band, or lifetime
   not already stated in Results? → move the number up; keep only its
   interpretation.
3. Read the **Conclusions**: does any sentence merely re-state the Abstract or
   Results? → cut or lift it to significance/next-step.
4. Is every method parameter needed to reproduce the run in **Computational
   Details** and nowhere else?
5. Tense: past for did/found, present for facts and exhibit references.

## Sources

- ACS Guide to Scholarly Communication — <https://pubs.acs.org/doi/book/10.1021/acsguide> and <https://pubs.acs.org/page/acsguide>
- JACS Author Guidelines — <https://researcher-resources.acs.org/publish/author_guidelines?coden=jacsat>
- Results vs. Discussion ("what" vs. "so what") — <https://www.cwauthors.com/article/results-versus-discussion-sections>
- Common Results/Discussion mistakes — <https://library.sacredheart.edu/c.php?g=29803&p=185933>
