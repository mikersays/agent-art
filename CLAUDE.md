# Agent Art

This repo contains collections of generative SVG art created by AI agents. Each collection lives in its own directory with an `index.html` gallery page.

## Project Structure

```
agent-art/
├── index.html              # Root redirect to default collection
├── bauhaus/                # Bauhaus collection (110 pieces)
│   ├── index.html          # Gallery page
│   └── bauhaus_*.svg       # Art pieces
└── <future-collection>/    # New collections follow same pattern
```

## How to Generate Art

### Creating SVG Art Pieces

All art is pure SVG — no external resources, no JavaScript, no raster images. Each piece is a self-contained `.svg` file.

**Canvas**: Always 800x800 pixels (square ratio):
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="800" height="800">
```

**Element count**: Aim for 20-60+ SVG elements per piece for visual richness. Use basic SVG primitives: `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<polygon>`, `<path>`, `<polyline>`.

**Layering**: Use `opacity` (0.1-1.0) for transparency and layering effects. Place background elements first, foreground last.

**No text elements**: Avoid `<text>` — express everything through geometry.

### Using Subagent Teams for Batch Generation

To generate art at scale, use parallel subagent teams. Each team generates 5 pieces:

1. **Define a color palette** for the collection (6-8 colors)
2. **Create unique themes** for each piece — give each a name and detailed visual description
3. **Launch 5-10 agents in parallel**, each responsible for 5 pieces
4. **Each agent prompt must include**:
   - Output directory path
   - Exact file names (e.g., `piece_31.svg` through `piece_35.svg`)
   - Canvas dimensions (800x800)
   - The color palette with hex values
   - Unique theme/description per piece with compositional guidance
   - Instruction to use Write tool, pure SVG only, 20+ elements per piece

Example agent prompt structure:
```
Generate 5 unique [STYLE]-style SVG art images in [PATH].
Name them [prefix]_31.svg through [prefix]_35.svg. Each 800x800 pixels.

Color palette: [list colors with hex codes]

Make each one UNIQUE with 20+ elements:

31. "[Title]" - [Detailed visual description of composition, shapes, arrangement]
32. "[Title]" - [...]
...

Use the Write tool. Pure SVG only, no external resources.
```

### Creating a Gallery Page

Each collection needs an `index.html` gallery page. Key features:
- Minimalist design with light background (#f5f5f0)
- CSS grid layout: `repeat(auto-fill, minmax(280px, 1fr))`
- Cards with hover lift effect and box-shadow
- Click-to-fullscreen overlay (dark background, 90vmin max size)
- Title array in JS matching file numbering
- `onerror` handler on images to gracefully handle missing files
- Helvetica Neue / sans-serif font stack
- Uppercase letter-spaced headings

### Serving Locally

```bash
cd <collection-dir> && python3 -m http.server 8000 --bind 0.0.0.0
```

### File Naming

- Numbers 1-99: two-digit zero-padded (`piece_01.svg` through `piece_99.svg`)
- Numbers 100+: three-digit (`piece_100.svg`, `piece_101.svg`, etc.)

## Bauhaus Style Reference

### Color Palette
| Name        | Hex       | Usage                          |
|-------------|-----------|--------------------------------|
| Red         | `#E63946` | Primary accent, bold forms     |
| Blue        | `#1D3557` | Primary, backgrounds, depth    |
| Yellow      | `#F4D35E` | Primary accent, highlights     |
| Black       | `#000000` | Structure, outlines, contrast  |
| White       | `#FFFFFF` | Backgrounds, negative space    |
| Teal        | `#2A9D8F` | Secondary accent               |
| Orange      | `#E76F51` | Warm accent                    |
| Steel Blue  | `#457B9D` | Cool secondary                 |
| Cream       | `#FEFAE0` | Soft backgrounds               |
| Warm Gray   | `#A89F91` | Neutral, subtle fills          |
| Burgundy    | `#6D2E46` | Deep warm accent               |
| Forest      | `#264653` | Dark cool accent               |
| Sand        | `#DDA15E` | Warm neutral                   |
| Coral       | `#E9C46A` | Golden accent                  |
| Light Blue  | `#A8DADC` | Soft cool accent               |

### Design Principles
- **Geometric primitives only**: circles, rectangles, triangles, lines, arcs
- **Asymmetric balance**: compositions feel balanced but not symmetric
- **Bold, clean forms**: no gradients, no blur filters, no decorative curves
- **Primary color dominance**: red, blue, yellow as main colors; others as accents
- **Structural lines**: thin lines (0.5-3px) create underlying grid/structure
- **Layered opacity**: overlapping shapes with varying opacity create depth
- **Strong compositional anchors**: one or two dominant shapes, supported by smaller elements

### Common Compositional Techniques
- Background grid lines at low opacity (0.05-0.15) for structure
- Corner accent shapes (small squares, circles) to frame composition
- Concentric forms (nested circles/squares) for focal points
- Diagonal lines for dynamic tension
- Horizontal/vertical bars for rhythm
- Scattered small shapes for visual texture
- Arc paths (`<path d="M... A...">`) for curved elements

## Deployment

- GitHub Pages auto-deploys from `master` branch via `.github/workflows/pages.yml`
- Push to `master` triggers deploy
