# AGENTS.md — Agent Art Workspace

This file defines how agents should work in this repo. Read it before doing anything else. Also read `CLAUDE.md` for the full art generation spec.

## Primary Reference

**CLAUDE.md is the canonical guide** for generating SVG art in this repo. Always read it first. It covers:
- SVG format requirements (800x800, pure SVG, no JS, no external resources)
- How to structure subagent teams (5 pieces per agent, parallel)
- Color palette (exact hex values)
- Design principles (geometric primitives, asymmetric balance, layered opacity)
- How to name each piece (unique themed title + `<title>` tag in SVG)
- How to update `index.html` gallery after generation
- File naming conventions (zero-padded: `bauhaus_01.svg`, `bauhaus_251.svg`)

## Key Rules

1. **Every SVG must have a `<title>` tag** with a unique, evocative name
2. **Named themes required** — define the name and a brief visual description for each piece before writing the SVG
3. **Update `bauhaus/index.html`** after any batch generation — add new titles to the JS array and ensure the gallery renders them
4. **Commit and push** after completing a batch: `git add -A && git commit -m "..." && git push`
5. **No duplicate themes** — check existing titles in `index.html` before naming new pieces
6. **5 pieces per subagent team** — launch teams in parallel for speed

## Workflow for Batch Generation

1. Read `CLAUDE.md` fully
2. Plan named themes for all pieces in your batch (name + 1-sentence visual description each)
3. Launch parallel subagent teams (5 pieces each), passing: file names, color palette, and the specific theme + description for each piece
4. After all teams complete, update `bauhaus/index.html` titles array
5. Commit and push
6. Announce completion with `openclaw system event --text "..." --mode now`

## Gallery

- Gallery lives at `bauhaus/index.html`
- Deployed via GitHub Pages from `master` branch
- The `titles` JS array in `index.html` must match the piece numbering exactly
- Test locally: `cd bauhaus && python3 -m http.server 8000`

## Current State

- Pieces 1–250: Complete, named, in gallery
- Pieces 251–600: In progress (being regenerated with proper names)
- Total target: 600 pieces
