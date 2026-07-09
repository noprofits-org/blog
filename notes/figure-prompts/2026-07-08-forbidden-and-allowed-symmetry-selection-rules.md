# Figure prompts — 2026-07-08-forbidden-and-allowed-symmetry-selection-rules

Only Figure 1 (hero / OG card) is an Illustrator "Text to Vector Graphic"
asset; Figures 2 and 3 are TikZ, baked into the post source. Workflow per
`notes/blog-authoring.md` §5: open the gear logo as the color source, run the
prompt, then add UPPERCASE condensed-sans captions in a type layer (the
generator drops free text).

## Figure 1 — hero, `/images/2026-07-08-forbidden-and-allowed-symmetry-selection-rules-hero.png`

**Canvas: 1200×630 landscape (1.91:1).** Compose left-to-right so the same
asset serves as in-post hero and OG/Twitter card. No baked-in text.

Prompt:

> Flat vector illustration, bold uniform dark-green outlines, limited palette
> of teal blue, deep teal, cream, and dark green on a cream background. A wide
> horizontal two-panel scene divided by a thin vertical rule. Both panels show
> the same setup: a bold zigzag light wave entering from the left toward a
> molecule drawn as outlined circles joined by bond lines, with a swinging
> gate or turnstile drawn between the wave and the molecule. Left panel: the
> molecule is perfectly mirror-symmetric about a dashed vertical mirror line
> through its center, the gate is closed, and the wave continues past the
> molecule as a thin, faint, pale line — almost nothing absorbed. Right panel:
> the molecule is visibly lopsided — one end drawn as a plump teal droplet,
> the other as an angular deep-teal wedge, no mirror line possible — the gate
> stands open, and the wave plunges into the molecule as a thick, bold,
> deep-teal arrow. Clean geometry, generous margins, icon style, no text, no
> gradients, no shadows.

Type layer afterwards (uppercase condensed sans, ink `#143f33`):
- Left panel: `SYMMETRIC — FORBIDDEN`
- Right panel: `ASYMMETRIC — ALLOWED`
- Gate (optional, small): `SELECTION RULE`

Palette (from the gear logo): outlines `#143f33` / `#16221d`; teal `#2f7da3`,
lifted `#5b9fc0`, deep `#1c5572`; cream `#f7f1d7`, page `#f7f4ee`.

After export: confirm 1200×630, save to
`/images/2026-07-08-forbidden-and-allowed-symmetry-selection-rules-hero.png`
(`og-image` in the post front matter already points there).

## Figures 2 and 3 — TikZ, already in the post source

- **Figure 2** — odd vs even integrand, two panels, shaded cancelling/adding
  lobes. In-source TikZ; no Illustrator asset needed.
- **Figure 3** — the intensity ladder: log-ε axis with lettered callouts A–F
  (benzene E₁ᵤ/B₁ᵤ/B₂ᵤ, CoCl₄²⁻, Co(H₂O)₆²⁺, Mn(H₂O)₆²⁺), letters defined in
  the numbered caption per house style. In-source TikZ; no Illustrator asset
  needed.
