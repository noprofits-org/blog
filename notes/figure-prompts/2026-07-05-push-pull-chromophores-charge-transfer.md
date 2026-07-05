# Figure prompts — 2026-07-05-push-pull-chromophores-charge-transfer

Only Figure 1 (hero / OG card) is an Illustrator "Text to Vector Graphic"
asset; Figures 2–4 are TikZ/pgfplots plots of computed data, baked into the
post source. Workflow per `notes/blog-authoring.md` §5: open the gear logo as
the color source, run the prompt, then add UPPERCASE condensed-sans captions in
a type layer (the generator drops free text).

## Figure 1 — hero, `/images/2026-07-05-push-pull-chromophores-charge-transfer-hero.png`

**Canvas: 1200×630 landscape (1.91:1).** Compose left-to-right so the same
asset serves as in-post hero and OG/Twitter card. No baked-in text.

Prompt:

> Flat vector illustration, bold uniform dark-green outlines, limited palette
> of teal blue, deep teal, cream, and dark green on a cream background. A wide
> horizontal three-part molecular diagram read left to right. Left: a small
> rounded shape resembling an electron-rich chemical group drawn as a plump
> outlined teal droplet with a plus-like glow, standing on a short bond line.
> Center: a hexagonal benzene ring drawn as a bold outlined hexagon with an
> inner circle, acting as a bridge, with short bond lines connecting it to
> both sides. Right: an electron-poor chemical group drawn as an angular
> outlined deep-teal wedge with two small circles, standing on a short bond
> line. Above the three parts, two horizontal energy-level bars: a lower cream
> bar rising in steps from the left (raised floor) and an upper deep-teal bar
> descending in steps from the right (lowered ceiling), with a bold curved
> arrow carrying a small filled electron circle from the left group across the
> hexagon to the right group through the narrowed gap between the bars. Clean
> geometry, generous margins, icon style, no text, no gradients, no shadows.

Type layer afterwards (uppercase condensed sans, ink `#143f33`):
- Left group: `DONOR`
- Center: `π BRIDGE`
- Right group: `ACCEPTOR`
- Arrow: `CHARGE TRANSFER`

Palette (from the gear logo): outlines `#143f33` / `#16221d`; teal `#2f7da3`,
lifted `#5b9fc0`, deep `#1c5572`; cream `#f7f1d7`, page `#f7f4ee`.

After export: confirm 1200×630, save to
`/images/2026-07-05-push-pull-chromophores-charge-transfer-hero.png`
(`og-image` in the post front matter already points there).
