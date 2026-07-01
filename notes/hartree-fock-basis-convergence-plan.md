Internal planning notes — not a post, not built by Hakyll (only `posts/*` is
matched in `lib/Blog/Site.hs`). Written 2026-07-01 for follow-up work with
psi4 at the desk.

## Why

`posts/2026-07-01-hartree-fock-and-the-correlation-gap.md` makes the
correlation-gap argument (§7, Figure 3) and the Koopmans argument (§6,
Table 1 / Figure 4) with representative/schematic numbers, not numbers
computed for this specific water geometry and basis series. psi4 can produce
the real thing. Two ways to land it:

- **(A) Tighten the existing post** — swap Figure 3's schematic energy-level
  diagram for a real basis-set-convergence plot, and replace Table 1's
  "representative near-HF-limit" values with numbers computed at a stated
  basis.
- **(B) Follow-up post** — keep the existing post conceptual, and write a new
  dated post ("how much does correlation really cost, in water") that redoes
  the calculation across a basis series and shows RHF vs MP2 vs CCSD(T)
  converging. This has enough of its own narrative (basis-set convergence,
  the size of the correlation energy, MP2 vs CCSD(T)) to stand alone, and
  avoids re-touching a post that's already been reviewed once.

Leaning toward (B) with a forward link added from §7 of the existing post,
but either is easy to execute from the same calculations below — decide once
the numbers are in hand and it's clear how much they add.

## Geometry

Use the same water geometry implied by the existing post/series (experimental
$r_e$, matching the water MO-diagram post): $r_{\mathrm{OH}} = 0.9584$ Å,
$\angle_{\mathrm{HOH}} = 104.45°$. Keep it fixed (no reoptimization) across
every basis so the comparison is basis effects only, not geometry drift.

```python
import psi4

psi4.set_memory('2 GB')
water = psi4.geometry("""
0 1
O
H 1 0.9584
H 1 0.9584 2 104.45
""")
```

## Calculation 1 — RHF basis-set convergence (feeds Figure 3)

Run RHF single points across a basis series from minimal to near-complete,
and one high-level correlated method as the "exact" anchor.

Basis series: `sto-3g`, `6-31g`, `6-31g**`, `cc-pvdz`, `cc-pvtz`, `cc-pvqz`
(add `cc-pv5z` only if it finishes in reasonable time — diminishing returns
past pVQZ for this plot).

```python
bases = ["sto-3g", "6-31g", "6-31g**", "cc-pvdz", "cc-pvtz", "cc-pvqz"]
results = {}
for b in bases:
    psi4.set_options({'basis': b})
    e_scf = psi4.energy('scf')
    results[b] = e_scf
    print(b, e_scf)
```

Then one correlated anchor for the "exact" line — CCSD(T)/cc-pVQZ (or
cc-pVTZ if pVQZ CCSD(T) is too slow on the desk machine; water is small
enough pVQZ CCSD(T) should be fine):

```python
psi4.set_options({'basis': 'cc-pvqz'})
e_ccsdt = psi4.energy('ccsd(t)')
```

**Plot:** x = basis (ordered by size, e.g. number of basis functions rather
than name, so spacing is meaningful), y = energy (hartree). RHF points
converging monotonically down to the RHF/CBS-ish limit; a horizontal
reference line at `e_ccsdt` (or better, an actual CBS-extrapolated CCSD(T)
value if two large basis energies are extrapolated). The vertical gap at the
right-hand (largest-basis) end is $E_{\mathrm{corr}}$ — this replaces the
schematic Figure 3 with real numbers for a real molecule.

Also record $E_{\mathrm{corr}} = E_{\mathrm{CCSD(T)}} - E_{\mathrm{RHF}}$ at
each basis (same basis for both) to show how the *basis-set error* and the
*correlation energy* are genuinely separable quantities — the post's aside
right after Figure 3 ("both energies must be taken in the same one-particle
basis") is exactly this.

## Calculation 2 — MP2 vs CCSD(T) (feeds §7's MP2 formula)

At a couple of the mid-size bases (cc-pVDZ, cc-pVTZ), also run MP2:

```python
psi4.set_options({'basis': 'cc-pvtz'})
e_mp2 = psi4.energy('mp2')
```

Report $E_{\mathrm{corr}}^{\mathrm{MP2}}$ vs $E_{\mathrm{corr}}^{\mathrm{CCSD(T)}}$
side by side — this is the direct numeric payoff of the $E^{(2)}$ formula in
§7, and it's a natural companion bar/line chart to Figure 3's convergence plot
rather than a replacement for it.

## Calculation 3 — orbital energies for Koopmans (tightens Table 1 / Figure 4)

Run RHF at one clearly-stated basis (cc-pVTZ is a reasonable "near-HF-limit
for valence orbital energies" choice) and pull the four valence orbital
eigenvalues:

```python
psi4.set_options({'basis': 'cc-pvtz'})
e_scf, wfn = psi4.energy('scf', return_wfn=True)
eps = wfn.epsilon_a().to_array()  # hartree, ascending
# convert to eV (x27.2114), identify by symmetry/occupation which of these
# four are 2a1, 1b2, 3a1, 1b1 — psi4 with point-group symmetry on will label
# irreps directly (wfn.epsilon_a_subset("SO", "OCC") per irrep, or just read
# the output file's "Orbital Energies" block, which prints symmetry labels).
```

Replace the "$\approx$" values in Table 1 and the bars in Figure 4 with these
computed numbers, and update the caption to say "computed at RHF/cc-pVTZ"
instead of "representative near-Hartree–Fock." Keep the experimental IEs as
they are (already cited to Turner 1970 via the water post).

## Calculation 4 — a real SCF convergence trace (companion to Figure 1)

Figure 1 in the existing post is a qualitative flowchart. A real trace of
energy (or density RMS) vs. SCF iteration for water/cc-pVDZ would make it
quantitative and is nearly free to get — psi4 prints per-iteration energy and
$\Delta E$/DIIS error to the output file during `energy('scf')`. Capture the
output file, parse the "Total Energy" and "DIIS error" columns per iteration,
and plot both on a log-y axis (DIIS error should drop several orders of
magnitude in single-digit iterations once DIIS kicks in) — a good
illustration of the "guess density → iterate → converge" loop actually
happening, and of why DIIS is the practical version of the naive fixed-point
iteration the post describes.

```python
psi4.core.set_output_file('scf_trace.out', False)
psi4.set_options({'basis': 'cc-pvdz', 'e_convergence': 1e-10, 'd_convergence': 1e-10})
psi4.energy('scf')
# then grep scf_trace.out for the per-iteration "@RHF iter" lines
```

## Plotting

Same mechanism as the rest of the site: fenced ` ```tikzpicture ` blocks with
a pgfplots `axis` environment, rendered to inline SVG at build time (see
`lib/Blog/TikZ.hs`, `README.md`'s "TikZ diagrams" section). Precedent for a
real-data `axis` plot with `coordinates {...}` is
`posts/2026-06-30-reading-water-geometry-orbitals-acidity-spectra.md` (~line
197) and the Koopmans bar chart just added to
`posts/2026-07-01-hartree-fock-and-the-correlation-gap.md` (§6, ybar chart).
For a log-scale convergence trace, add `ymode=log` to the `axis` options.

No new build dependency needed — CI already installs the full TeX/dvisvgm
toolchain (`.github/workflows/deploy.yml`) and this environment has no TeX
installed at all, so diagrams here can't be test-rendered locally in this
session; they'll render (or visibly fail with an error box) on the next CI
build.

## Open decisions for when you're back at the desk

1. (A) tighten existing post vs (B) follow-up post — leaning (B), decide once
   the CCSD(T)/cc-pVQZ number is in hand and you can see whether it's a
   two-paragraph addendum or a full post's worth of content.
2. Whether to extrapolate a two-point CBS limit (e.g. cc-pVTZ/cc-pVQZ RHF
   extrapolation) for a cleaner "HF limit" line, or just show the raw
   basis-series points and let the eye extrapolate — the post's Figure 3 text
   already hedges ("the limiting value uses the Hartree–Fock basis-set
   limit"), so a real extrapolated number would tighten that language too.
3. If (B), whether it belongs in this same tag family (`quantum chemistry,
   Hartree-Fock, ...`) as a same-day-adjacent dated post, or is worth folding
   into the excited-state/basis-set post's series instead.
