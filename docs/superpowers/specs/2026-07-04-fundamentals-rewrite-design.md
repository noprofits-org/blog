# Design: rewrite of the fundamentals-of-quantum-chemistry post

Date: 2026-07-04
Status: approved (interactive Q&A, this session)

## Goal

Replace the 2025-04-22 lab-report draft at
`posts/fundamentals_of_quantum_chemistry.md` with a complete post in the
voice of the July 2026 series (Hartree–Fock post, correlation-gap post),
which both link to this post as their ground floor.

## Approved decisions

- **Full rewrite, current voice.** Narrative prose; drop the
  Intro/Experimental/Results/Discussion/Conclusion skeleton, the system-specs
  table, the 400-line `<details>` code listings, and all revision
  meta-commentary ("has been recalculated", "redundancy … addressed").
- **Re-run everything.** Every figure and table value computed fresh
  (numpy/scipy locally; psi4 1.11 in the `qchem` conda env). Figures become
  tikz/pgfplots blocks with computed coordinates, replacing the PNGs.
- **Retitle**, in the descriptive style of the recent posts. Slug
  `fundamentals_of_quantum_chemistry` unchanged (the HF post links to it).
- **Keep date 2025-04-22** to preserve series chronology. Drop "(DRAFT)".

## Content plan

1. **Intro** — why exactly solvable systems matter; where the post sits in
   the series; the rule: nothing schematic, every number checked against a
   closed-form answer. That accountability thread replaces the draft's
   garbled corrections narrative.
2. **Particle in a box** — wavefunctions offset by energy, densities,
   ⟨x⟩/Δx table. Lesson: confinement ⇒ quantization, E ∝ n², nodes.
3. **Harmonic oscillator** — states in the well, zero-point energy, and a
   fix to a real physics error in the draft: its Table 3 reported
   Δx·Δp = ħ/2 for all n because the code computed Δp circularly as
   ħ/(2Δx). Correct result for eigenstates is Δx·Δp = (n+½)ħ; compute ⟨p²⟩
   properly and show the ladder with ħ/2 as the floor (n=0 only).
4. **Hydrogen atom** — exact 1s radial density (most probable r = a₀ vs
   ⟨r⟩ = 1.5a₀); psi4 UHF marched up a basis ladder converging to −0.5 Eₕ;
   punchline: one electron ⇒ zero correlation energy, so the basis error is
   the *whole* error — the bridge to the correlation-gap post.
5. **Wavepackets and uncertainty** — Gaussian minimum-uncertainty packets;
   localization as superposition of momentum components.
6. **Close** — map each model to where it reappears upstairs in the series.

## Constraints

- Citations: pandoc `[@key]` against `bib/bibliography.bib`; add keys only
  if missing (Smith2020 psi4 and HelgakerJorgensenOlsen2000 exist).
- psi4 gotcha: set `PSI_SCRATCH` before import; `psi4.core.clean()` between
  jobs.
- Verify with `stack exec blog build` (local TeX toolchain renders
  tikzpicture → SVG).
- Old PNGs in `images/` referenced only by this post can be retired once the
  post no longer uses them.
