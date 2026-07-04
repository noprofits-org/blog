# Design: rework of the H2O2 tunneling psi4-results post

Date: 2026-07-04
Status: approved (interactive Q&A, this session)

## Goal

Replace `posts/2026-01-16-quantum-tunneling-psi4-results.md` — a workflow
note tied to the now-absent `improved_tunnel` repo — with a self-contained
physics post in the current series voice, all numbers re-run with psi4
directly in the post's own scripts.

## Why a rework, not a touch-up

The draft has a factual error at its center: it labels its 6.70 kcal/mol
barrier *trans* (180°) and validates against an "experimental trans barrier
of ~7.4 kcal/mol". For H2O2 the high barrier (~7.3 kcal/mol, Koput 1998) is
**cis** (0°); trans is ~1.1 kcal/mol. Additionally: WKB and SCT report
identical values (the code aliased them), and the Eckart "step function at
E/V = 1" is an implementation bug presented as a method limitation — a real
Eckart barrier has smooth transmission and kappa > 1.

## Approved decisions

- **Full rewrite, current voice**, same slug and 2026-01-16 date, italic
  rebuilt-note up top (same pattern as the fundamentals rewrite).
- **Re-run everything**: relaxed MP2/cc-pVTZ torsion scan (frozen core,
  0–180° in 10° steps exploiting V(φ) symmetry), free optimization of the
  gauche minimum, frequencies at the minimum and both planar saddle points.
- **Include the tunneling splitting**: solve the periodic 1D torsional
  Schrödinger equation on the computed V(φ) (Fourier-grid Hamiltonian,
  effective moment of inertia from the computed geometries), compare the
  ground-state trans splitting to the experimental ~11 cm⁻¹.
- **kappa(T) analysis retained but corrected**: WKB through the trans
  barrier plus a properly implemented analytic Eckart; drop the aliased SCT
  and the i-PI/ring-polymer section (repo gone; cite instanton methods in
  prose only).
- Figures become computed tikz; the five h2o2_psi4_*.png images retire.
- Companion mock-workflow post (2026-01-16-quantum-tunneling-workflow.md)
  stays untouched.

## Content plan

1. Rebuilt-note + what the old post got wrong (cis/trans swap, aliased SCT,
   broken Eckart) — the errors as motivation, same as the fundamentals
   rewrite.
2. The system: H2O2 torsion, two equivalent gauche wells, two inequivalent
   barriers. Scan setup (the surviving lesson from the old post: c1
   symmetry, no_reorient; modern optking constraint).
3. The potential, computed: V(φ) figure, stationary-point table vs Koput
   1998 (gauche dihedral, trans and cis barriers in kcal/mol and cm⁻¹).
4. The splitting, measured: FGH solve → torsional doublets, ground
   splitting vs experiment; why trans (low, narrow) dominates tunneling
   even though cis is the "big" barrier.
5. kappa(T): WKB and correct Eckart transmission P(E), kappa 100–500 K,
   what the old post's step-function Eckart actually was.
6. Close: honest limits of the rigid 1D model; pointer to instanton
   methods for deep tunneling.

## Constraints

- psi4 1.11 in `qchem` env; PSI_SCRATCH set before import; np.trapezoid.
- Verify literature anchor numbers (Koput barrier heights, experimental
  splitting) against sources before quoting.
- Scan is resilient: chained geometries from the minimum outward, per-point
  JSON checkpointing, background run with progress log.
- Verify with `stack exec blog build` + visual check of every figure.
