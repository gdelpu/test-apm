---
name: brand-core
description: 'Reusable core rules of a visual identity: logo, colors, typography, icons, imagery, and layout. Foundation for every brand audit or refactor. Default brand: Sopra Steria. Extensible for other client brands via .apm/knowledge/brand/<client>/.'
triggers: ['brand rules', 'brand guidelines', 'visual identity', 'color palette', 'typography', 'branding foundation', 'Sopra Steria branding']
version: '2.0.0'
---

# Skill: Brand Core

## Purpose

Contains the reusable core structure for defining a visual identity. Use this as the foundation for every brand audit or refactor. Default brand values are for Sopra Steria. To override for a different client, provide assets in `.apm/knowledge/brand/<client>/` and reference a client-specific section.

## Source of Truth

Base branding decisions on the official brand guideline and official templates/assets when available. Never improvise brand elements — ask for or reference the official source.

## Core Rules Structure

### 1. Logo

- Use official source logo files only; never recreate the logo
- Select the correct variant for the background context (color, monochrome, reversed)
- Place on solid or uncluttered backgrounds for maximum clarity
- Maintain the protection area and respect minimum sizes
- Never move, resize independently, recolor, distort, or alter the logo
- In running text, write the company name with correct capitalization

### 2. Signature / Tagline

- Use official signature assets only
- Follow placement rules (left/right positioning based on context)
- Do not rewrite, restyle, or manually rebuild the signature

### 3. Primary Color System

- Define 4–8 primary colors that form the brand's core palette
- Primary colors should dominate covers, headers, and core branded areas
- Proprietary gradients are a key brand marker — use appropriately
- Use the palette with restraint; avoid too many simultaneous colors
- White / negative space should remain heavily present

### 4. Secondary Color System

- Secondary colors extend the system but do not replace the primary palette
- Use sparingly, paired with at least one primary color
- Purpose: liveliness, emphasis, selected highlights

### 5. Typography

- Define primary heading font and body text font
- Specify practical fallbacks for environments where brand fonts are unavailable
- Prefer left alignment for headings and captions
- Use justified alignment for long running text
- Aim for ~55–65 characters per line for comfortable reading
- Define line spacing guidance for print and web

### 6. Icons

- Use brand-approved icons where available
- Maintain consistent style (outline, filled, weight)
- Keep shapes simple and readable
- Optional accent patches should use approved colors

### 7. Visual Style and Composition

Define the brand's composition system:

- Key visual ingredients (logo, signature, gradient, typography, imagery)
- Core brand markers (grid, gradient, shape language)
- Cover layout rules for vertical and horizontal formats
- Proportional guidelines for logo sizing and spacing

### 8. Co-branding

- Separate both logos with a brand-appropriate visual separator
- Position initiator's logo appropriately (typically left)
- Balance logo sizes visually

### 9. Accessibility

- Ensure sufficient color contrast (4.5:1 normal text, 3:1 large text)
- Do not rely on color alone to convey meaning
- On gradients or images, ensure text sits in a safe legibility area

---

## Default Brand: Sopra Steria

The following concrete values apply when the target brand is Sopra Steria (the default). Official guideline and assets are in `.apm/knowledge/brand/soprasteria/`.

### Logo

- The classic logo uses red and orange for the swirl and black for the brand name.
- Monochrome black or white versions may be used when production constraints require it.
- Ideally place the logo on solid white; the original version may also be used on solid light backgrounds or uncluttered visuals.
- On dark backgrounds, use the white version; on solid black, the version with color swirl may also be used.
- On complex visuals, the white logo may use a black `#000000` or purple `#2A1449` drop shadow at 75% opacity, 1 mm distance, minimum size 2 mm.
- In running text, write the company name as `Sopra Steria` with capital S's.

### Signature

- Signature font for the logo lockup is Hurme Geometric Sans 3.
- In standard materials, the signature sits to the left of the logo.
- In social content, the signature is placed at the end of the carousel.

### Primary Colors

| Name | Hex |
|------|-----|
| Dark purple | `#4D1D82` |
| Light purple | `#8B1D82` |
| Red | `#CF022B` |
| Orange | `#EF7D00` |
| Off-black | `#1D1D1B` |
| Grey | `#A8A8A7` |
| Light grey | `#EDEDED` |
| White | `#FFFFFF` |

The proprietary gradient is a key brand marker and may be used as a fill, background, border, or accent. White should remain heavily present to keep the overall look light and energising.

### Secondary Colors

| Name | Hex |
|------|-----|
| Dark blue | `#007AC2` |
| Light blue | `#32ABD0` |
| Dark green / teal | `#00A188` |
| Light green | `#95C11F` |
| Pink | `#EA5599` |
| Yellow | `#F7B90C` |

Use secondary colors sparingly. Pair them with at least one primary color.

### Typography

- Main font: **Hurme Geometric Sans 3**
- Secondary font: **Hurme Geometric Sans 4** for main headings
- Office documents (Word / PowerPoint / Excel): **Tahoma**
- Line spacing: print — font size + 2 to 2.5 pt; web — font size + 4 to 6 px

### Icons

- Outline icons in dark purple `#4D1D82`
- Optional color patches: 20% tones only, smaller than the icon
- Patches centered or placed upper-right relative to the icon

### Composition

Five recurring ingredients: logo, brand signature, proprietary gradient border, title in Hurme Geometric Sans 4, visual and/or gradient.

Two core markers: a flexible composition grid and a proprietary gradient.

**Vertical cover**: logo width ≈ 1/4 of document width; title margins left and right = `3X` (where `X` = width of the swirls).

**Horizontal cover**: logo width ≈ 1/3 of document height; title margins left and right = `2X`.

### Co-branding

- Separate logos with a gradient effect line in Sopra Steria colors.
- Sopra Steria logo sits left if Sopra Steria is the initiator; right if the partner is the initiator.

### Accessibility

| Foreground | Background | Ratio | AA Normal? | AA Large? |
|---|---|---|---|---|
| White | `#4D1D82` deep purple | 10.3:1 | YES | YES |
| White | `#8B1D82` purple | 6.2:1 | YES | YES |
| White | `#CF022B` red | 5.6:1 | YES | YES |
| White | `#EF7D00` orange | 2.9:1 | NO | YES (large only) |
| `#1D1D1B` off-black | White | 18.6:1 | YES | YES |
| `#A8A8A7` mid grey | White | 2.7:1 | NO | NO |

- **Orange `#EF7D00` fails AA for normal white text** — restrict to large text, icons, or decorative use.
- **Mid grey `#A8A8A7` fails AA on white** — do not use for body text or labels.

---

## How to Apply

When making recommendations, classify each proposed change as:

- **Strict guideline requirement** — mandated by the brand manual
- **Strong recommendation** — best practice with clear brand rationale
- **Safe implementation assumption** — reasonable default when the guideline is silent

If an asset or rule is missing, do not improvise. Ask for the official asset.
