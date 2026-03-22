#!/usr/bin/env python3
"""Generate Bauhaus SVG pieces 251-600 with unique named themes."""

import math
import random
import os

OUTPUT_DIR = "/home/momo/git/agent-art/bauhaus"

# Bauhaus color palette
RED        = '#E63946'
BLUE       = '#1D3557'
YELLOW     = '#F4D35E'
BLACK      = '#000000'
WHITE      = '#FFFFFF'
TEAL       = '#2A9D8F'
ORANGE     = '#E76F51'
STEEL_BLUE = '#457B9D'
CREAM      = '#FEFAE0'
WARM_GRAY  = '#A89F91'
BURGUNDY   = '#6D2E46'
FOREST     = '#264653'
SAND       = '#DDA15E'
CORAL      = '#E9C46A'
LIGHT_BLUE = '#A8DADC'

ALL_COLORS = [RED, BLUE, YELLOW, BLACK, WHITE, TEAL, ORANGE, STEEL_BLUE,
              CREAM, WARM_GRAY, BURGUNDY, FOREST, SAND, CORAL, LIGHT_BLUE]
PRIMARY    = [RED, BLUE, YELLOW]
DARK       = [BLACK, BLUE, FOREST, BURGUNDY]
WARM       = [RED, ORANGE, YELLOW, SAND, CORAL]
COOL       = [TEAL, STEEL_BLUE, LIGHT_BLUE, FOREST]

def svg_wrap(title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="800" height="800">
  <title>{title}</title>
  {body}
</svg>'''

def rect(x, y, w, h, fill, opacity=1.0, stroke=None, sw=1):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" opacity="{opacity:.2f}"{s}/>'

def circle(cx, cy, r, fill, opacity=1.0, stroke=None, sw=1):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" opacity="{opacity:.2f}"{s}/>'

def line(x1, y1, x2, y2, stroke, sw=1, opacity=1.0):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity:.2f}"/>'

def polygon(points, fill, opacity=1.0, stroke=None, sw=1):
    pts = ' '.join(f'{x},{y}' for x, y in points)
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<polygon points="{pts}" fill="{fill}" opacity="{opacity:.2f}"{s}/>'

def arc_path(cx, cy, r, start_deg, end_deg, stroke, sw=2, fill='none', opacity=1.0):
    s = math.radians(start_deg)
    e = math.radians(end_deg)
    x1 = cx + r * math.cos(s)
    y1 = cy + r * math.sin(s)
    x2 = cx + r * math.cos(e)
    y2 = cy + r * math.sin(e)
    large = 1 if (end_deg - start_deg) > 180 else 0
    return f'<path d="M {x1:.1f} {y1:.1f} A {r} {r} 0 {large} 1 {x2:.1f} {y2:.1f}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" opacity="{opacity:.2f}"/>'

def ellipse(cx, cy, rx, ry, fill, opacity=1.0, stroke=None, sw=1):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" opacity="{opacity:.2f}"{s}/>'

# ─── Style generators ────────────────────────────────────────────────────────

def style_horizontal_bands(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Low-opacity grid lines
    for x in range(0, 801, 80):
        els.append(line(x, 0, x, 800, BLACK, 0.5, 0.08))
    for y in range(0, 801, 80):
        els.append(line(0, y, 800, y, BLACK, 0.5, 0.08))
    # Bold horizontal bands
    bands = r.randint(5, 10)
    y = 0
    for i in range(bands):
        h = r.randint(40, 160)
        c = r.choice(colors)
        op = r.uniform(0.7, 1.0)
        els.append(rect(0, y, 800, h, c, op))
        y += h + r.randint(5, 30)
        if y > 800: break
    # Accent rectangles
    for _ in range(r.randint(6, 14)):
        w = r.randint(30, 200)
        h2 = r.randint(20, 100)
        x2 = r.randint(0, 760)
        y2 = r.randint(0, 760)
        els.append(rect(x2, y2, w, h2, r.choice(PRIMARY), r.uniform(0.5, 0.9)))
    # Corner anchors
    sz = r.randint(40, 80)
    for cx_, cy_ in [(0,0),(800-sz,0),(0,800-sz),(800-sz,800-sz)]:
        els.append(rect(cx_, cy_, sz, sz, r.choice(PRIMARY)))
    # Thin accent lines
    for _ in range(r.randint(5, 12)):
        y3 = r.randint(0, 800)
        els.append(line(0, y3, 800, y3, r.choice([BLACK, WHITE]), r.uniform(1, 3)))
    return '\n  '.join(els)

def style_concentric_circles(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    cx = r.randint(200, 600)
    cy = r.randint(200, 600)
    n = r.randint(8, 16)
    for i in range(n, 0, -1):
        rad = i * r.randint(25, 45)
        c = r.choice(colors)
        op = r.uniform(0.5, 1.0) if i % 2 == 0 else r.uniform(0.3, 0.8)
        els.append(circle(cx, cy, rad, c, op))
    # Structural lines
    for ang in range(0, 360, r.randint(20, 45)):
        rad2 = math.radians(ang)
        els.append(line(cx, cy, cx + 380*math.cos(rad2), cy + 380*math.sin(rad2),
                       BLACK, r.uniform(0.5, 1.5), 0.1))
    # Scattered small circles
    for _ in range(r.randint(8, 20)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(5, 30), r.choice(PRIMARY), r.uniform(0.4, 0.9)))
    # Corner rects
    for _ in range(4):
        s = r.randint(20, 60)
        els.append(rect(r.choice([0, 800-s]), r.choice([0, 800-s]), s, s, r.choice(colors)))
    # Outer ring strokes
    for i in range(3):
        els.append(circle(cx, cy, (n+i)*r.randint(25,45)+20, 'none', 1.0, r.choice([BLACK, WHITE]), r.uniform(1,3)))
    return '\n  '.join(els)

def style_diagonal_tension(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Diagonal lines
    for i in range(r.randint(8, 20)):
        offset = r.randint(-400, 400)
        c = r.choice(colors + [BLACK, WHITE])
        sw = r.uniform(1, 8)
        op = r.uniform(0.3, 0.9)
        els.append(line(offset, 0, 800+offset, 800, c, sw, op))
    # Counter-diagonal lines
    for i in range(r.randint(4, 10)):
        offset = r.randint(0, 800)
        els.append(line(offset, 0, offset-800, 800, r.choice([BLACK, WHITE]), r.uniform(0.5, 2), 0.15))
    # Large triangles
    for _ in range(r.randint(2, 5)):
        pts = [(r.randint(0,800), r.randint(0,800)) for _ in range(3)]
        els.append(polygon(pts, r.choice(PRIMARY), r.uniform(0.4, 0.8)))
    # Rectangles along diagonals
    for _ in range(r.randint(4, 10)):
        x = r.randint(0, 600)
        y = r.randint(0, 600)
        w = r.randint(20, 120)
        h = r.randint(20, 120)
        els.append(rect(x, y, w, h, r.choice(colors), r.uniform(0.5, 0.9)))
    # Small accent circles
    for _ in range(r.randint(6, 15)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(5, 25), r.choice(PRIMARY), r.uniform(0.6, 1.0)))
    return '\n  '.join(els)

def style_grid_blocks(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    cols = r.randint(4, 10)
    rows = r.randint(4, 10)
    cw = 800 // cols
    rh = 800 // rows
    for row in range(rows):
        for col in range(cols):
            if r.random() > 0.3:
                c = r.choice(colors)
                op = r.uniform(0.4, 1.0)
                els.append(rect(col*cw+1, row*rh+1, cw-2, rh-2, c, op))
    # Grid lines
    for x in range(0, 801, cw):
        els.append(line(x, 0, x, 800, BLACK, 1, 0.3))
    for y in range(0, 801, rh):
        els.append(line(0, y, 800, y, BLACK, 1, 0.3))
    # Accent circles at some intersections
    for row in range(rows+1):
        for col in range(cols+1):
            if r.random() > 0.7:
                els.append(circle(col*cw, row*rh, r.randint(5, min(cw,rh)//2),
                                 r.choice(PRIMARY), r.uniform(0.5, 0.9)))
    return '\n  '.join(els)

def style_radial_burst(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    cx = r.randint(200, 600)
    cy = r.randint(200, 600)
    n_rays = r.randint(12, 36)
    max_r = r.randint(200, 400)
    # Filled wedges
    for i in range(n_rays):
        a1 = 360 * i / n_rays
        a2 = 360 * (i+1) / n_rays
        mid = math.radians((a1+a2)/2)
        # Triangle approximation
        r1 = math.radians(a1)
        r2 = math.radians(a2)
        pts = [(cx, cy),
               (cx + max_r * math.cos(r1), cy + max_r * math.sin(r1)),
               (cx + max_r * math.cos(r2), cy + max_r * math.sin(r2))]
        c = r.choice(colors if i % 2 == 0 else [BLACK, WHITE, bg])
        els.append(polygon(pts, c, r.uniform(0.5, 1.0)))
    # Concentric rings
    for rad in range(40, max_r, r.randint(40, 80)):
        els.append(circle(cx, cy, rad, 'none', 1.0, r.choice([BLACK, WHITE]), r.uniform(0.5, 2)))
    # Center circle
    els.append(circle(cx, cy, r.randint(15, 50), r.choice(PRIMARY)))
    # Corner marks
    for px, py in [(40,40),(760,40),(40,760),(760,760)]:
        els.append(circle(px, py, r.randint(10, 30), r.choice(PRIMARY), r.uniform(0.6, 1.0)))
    return '\n  '.join(els)

def style_vertical_pillars(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Horizontal base/cap lines
    cap_y = r.randint(50, 150)
    base_y = r.randint(650, 750)
    els.append(rect(0, base_y, 800, 800-base_y, r.choice(DARK), r.uniform(0.7, 1.0)))
    els.append(rect(0, 0, 800, cap_y, r.choice(PRIMARY), r.uniform(0.6, 1.0)))
    # Pillars
    n_pillars = r.randint(4, 12)
    pw = r.randint(30, 100)
    spacing = 800 // n_pillars
    for i in range(n_pillars):
        x = i * spacing + r.randint(-10, 10)
        c = r.choice(colors)
        op = r.uniform(0.7, 1.0)
        h = base_y - cap_y - r.randint(0, 40)
        els.append(rect(x, cap_y, pw, h, c, op))
        # Shadow line
        els.append(line(x, cap_y, x, base_y, BLACK, 1, 0.2))
    # Accent elements between pillars
    for _ in range(r.randint(5, 15)):
        x = r.randint(0, 750)
        y = r.randint(cap_y, base_y)
        s = r.randint(10, 40)
        els.append(rect(x, y, s, s, r.choice(PRIMARY), r.uniform(0.5, 0.9)))
    # Thin horizontal lines
    for _ in range(r.randint(5, 15)):
        y = r.randint(cap_y, base_y)
        els.append(line(0, y, 800, y, r.choice([BLACK, WHITE]), r.uniform(0.5, 2), r.uniform(0.2, 0.6)))
    return '\n  '.join(els)

def style_arc_composition(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Background structure lines
    for x in range(0, 801, 100):
        els.append(line(x, 0, x, 800, BLACK, 0.5, 0.06))
    for y in range(0, 801, 100):
        els.append(line(0, y, 800, y, BLACK, 0.5, 0.06))
    # Bold arcs
    n_arcs = r.randint(4, 10)
    for _ in range(n_arcs):
        cx2 = r.randint(100, 700)
        cy2 = r.randint(100, 700)
        rad = r.randint(80, 350)
        start = r.randint(0, 360)
        span = r.randint(60, 270)
        c = r.choice(colors)
        sw = r.uniform(4, 20)
        els.append(arc_path(cx2, cy2, rad, start, start+span, c, sw, 'none', r.uniform(0.6, 1.0)))
    # Filled circles at arc endpoints
    for _ in range(r.randint(4, 12)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(8, 40), r.choice(PRIMARY), r.uniform(0.7, 1.0)))
    # Rectangles
    for _ in range(r.randint(3, 8)):
        w = r.randint(20, 150)
        h = r.randint(20, 150)
        els.append(rect(r.randint(0,780), r.randint(0,780), w, h,
                       r.choice(colors), r.uniform(0.4, 0.8)))
    return '\n  '.join(els)

def style_nested_squares(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    cx = r.randint(200, 600)
    cy = r.randint(200, 600)
    n = r.randint(6, 14)
    step = r.randint(25, 55)
    for i in range(n, 0, -1):
        s = i * step
        x = cx - s//2
        y = cy - s//2
        c = r.choice(colors)
        op = r.uniform(0.5, 1.0)
        # Optionally rotate
        rot = r.randint(0, 15) * i if r.random() > 0.5 else 0
        if rot:
            els.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{c}" opacity="{op:.2f}" transform="rotate({rot} {cx} {cy})"/>')
        else:
            els.append(rect(x, y, s, s, c, op))
    # Structural diagonal lines
    for ang in [45, 135]:
        rad2 = math.radians(ang)
        els.append(line(cx - 600*math.cos(rad2), cy - 600*math.sin(rad2),
                       cx + 600*math.cos(rad2), cy + 600*math.sin(rad2),
                       BLACK, 1, 0.15))
    # Cross lines
    els.append(line(cx, 0, cx, 800, BLACK, 1, 0.1))
    els.append(line(0, cy, 800, cy, BLACK, 1, 0.1))
    # Accent dots
    for _ in range(r.randint(6, 16)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(4, 20), r.choice(PRIMARY), r.uniform(0.6, 1.0)))
    return '\n  '.join(els)

def style_triangle_field(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Background grid
    for x in range(0, 801, 80):
        els.append(line(x, 0, x, 800, BLACK, 0.5, 0.07))
    for y in range(0, 801, 80):
        els.append(line(0, y, 800, y, BLACK, 0.5, 0.07))
    # Triangles
    n_tri = r.randint(8, 20)
    for _ in range(n_tri):
        # Generate triangle
        x_c = r.randint(50, 750)
        y_c = r.randint(50, 750)
        s = r.randint(40, 200)
        angle = r.randint(0, 360)
        pts = []
        for a in [0, 120, 240]:
            rad2 = math.radians(angle + a)
            pts.append((x_c + s * math.cos(rad2), y_c + s * math.sin(rad2)))
        c = r.choice(colors)
        op = r.uniform(0.4, 0.9)
        els.append(polygon(pts, c, op))
    # Bold lines
    for _ in range(r.randint(3, 8)):
        els.append(line(r.randint(0,800), r.randint(0,800),
                       r.randint(0,800), r.randint(0,800),
                       r.choice([BLACK] + PRIMARY), r.uniform(2, 6), r.uniform(0.5, 1.0)))
    # Corner elements
    for _ in range(4):
        s = r.randint(20, 60)
        els.append(circle(r.choice([s, 800-s]), r.choice([s, 800-s]), s//2,
                         r.choice(PRIMARY)))
    return '\n  '.join(els)

def style_overlapping_circles(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Large overlapping circles (Venn-like)
    n_circles = r.randint(3, 7)
    for _ in range(n_circles):
        cx2 = r.randint(100, 700)
        cy2 = r.randint(100, 700)
        rad = r.randint(100, 300)
        c = r.choice(colors)
        op = r.uniform(0.3, 0.7)
        els.append(circle(cx2, cy2, rad, c, op))
    # Ring outlines
    for _ in range(r.randint(3, 8)):
        cx2 = r.randint(100, 700)
        cy2 = r.randint(100, 700)
        rad = r.randint(50, 200)
        els.append(circle(cx2, cy2, rad, 'none', 1.0, r.choice([BLACK, WHITE]), r.uniform(1, 4)))
    # Small accents
    for _ in range(r.randint(10, 25)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(3, 20), r.choice(PRIMARY), r.uniform(0.7, 1.0)))
    # Structural lines
    for _ in range(r.randint(3, 8)):
        els.append(line(r.randint(0,800), r.randint(0,800),
                       r.randint(0,800), r.randint(0,800),
                       BLACK, r.uniform(1, 3), 0.2))
    return '\n  '.join(els)

def style_staircase(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Direction: up-right or down-right
    ascending = r.choice([True, False])
    n_steps = r.randint(5, 12)
    step_w = 800 // n_steps
    step_h = 800 // n_steps
    # Draw filled staircase
    for i in range(n_steps):
        x = i * step_w
        if ascending:
            y = (n_steps - 1 - i) * step_h
            h = 800 - y
        else:
            y = 0
            h = (i + 1) * step_h
        c = r.choice(colors)
        els.append(rect(x, y, step_w, h, c, r.uniform(0.6, 1.0)))
    # Tread/riser lines
    for i in range(1, n_steps):
        x = i * step_w
        els.append(line(x, 0, x, 800, BLACK, 1, 0.3))
        y = i * step_h
        els.append(line(0, y, 800, y, BLACK, 1, 0.3))
    # Accent elements
    for _ in range(r.randint(5, 15)):
        w = r.randint(20, 80)
        h2 = r.randint(20, 80)
        els.append(rect(r.randint(0,780), r.randint(0,780), w, h2,
                       r.choice(PRIMARY), r.uniform(0.5, 0.9)))
    # Bold diagonal
    if r.random() > 0.4:
        els.append(line(0, 800 if ascending else 0, 800, 0 if ascending else 800,
                       r.choice([BLACK, WHITE, RED]), r.uniform(3, 8), r.uniform(0.4, 0.8)))
    return '\n  '.join(els)

def style_target(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    cx = r.randint(200, 600)
    cy = r.randint(200, 600)
    n_rings = r.randint(6, 14)
    ring_w = r.randint(25, 50)
    for i in range(n_rings, 0, -1):
        rad = i * ring_w
        c = r.choice(colors if i % 2 == 0 else [WHITE, CREAM, bg])
        els.append(circle(cx, cy, rad, c))
    # Crosshair lines
    els.append(line(cx, 0, cx, 800, BLACK, r.uniform(1, 3), 0.3))
    els.append(line(0, cy, 800, cy, BLACK, r.uniform(1, 3), 0.3))
    # Tick marks
    for ang in range(0, 360, 30):
        rad3 = math.radians(ang)
        r1 = (n_rings - 1) * ring_w
        r2 = n_rings * ring_w + 10
        els.append(line(cx + r1*math.cos(rad3), cy + r1*math.sin(rad3),
                       cx + r2*math.cos(rad3), cy + r2*math.sin(rad3),
                       BLACK, 2, 0.5))
    # Center dot
    els.append(circle(cx, cy, r.randint(8, 20), r.choice(PRIMARY)))
    # Corner squares
    for px, py in [(0,0),(740,0),(0,740),(740,740)]:
        s = r.randint(40, 60)
        els.append(rect(px, py, s, s, r.choice(PRIMARY)))
    # Scattered elements
    for _ in range(r.randint(4, 10)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(5, 25), r.choice(colors), r.uniform(0.4, 0.8)))
    return '\n  '.join(els)

def style_quadrant_study(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Divide into quadrants with different treatments
    cx = r.randint(300, 500)
    cy = r.randint(300, 500)
    quad_colors = r.sample(colors, min(4, len(colors)))
    # Q1 top-left: filled rect
    els.append(rect(0, 0, cx, cy, quad_colors[0], r.uniform(0.6, 0.9)))
    # Q2 top-right: circles
    c2 = quad_colors[1]
    for _ in range(r.randint(3, 8)):
        rx = r.randint(cx, 800)
        ry = r.randint(0, cy)
        els.append(circle(rx, ry, r.randint(20, 80), c2, r.uniform(0.4, 0.8)))
    # Q3 bottom-left: diagonal stripes
    c3 = quad_colors[2]
    for i in range(0, 200, r.randint(20, 40)):
        els.append(line(0, cy+i, cx, cy+i+cx, c3, r.uniform(5, 15), r.uniform(0.5, 0.9)))
    # Q4 bottom-right: grid of small squares
    c4 = quad_colors[3] if len(quad_colors) > 3 else quad_colors[0]
    gs = r.randint(20, 50)
    for gx in range(cx, 800, gs):
        for gy in range(cy, 800, gs):
            if r.random() > 0.4:
                els.append(rect(gx+1, gy+1, gs-2, gs-2, c4, r.uniform(0.5, 1.0)))
    # Dividing lines
    els.append(line(cx, 0, cx, 800, BLACK, r.uniform(2, 5)))
    els.append(line(0, cy, 800, cy, BLACK, r.uniform(2, 5)))
    # Accent at center
    els.append(circle(cx, cy, r.randint(15, 40), r.choice(PRIMARY)))
    # Additional scattered elements
    for _ in range(r.randint(5, 15)):
        s = r.randint(5, 20)
        els.append(rect(r.randint(0,780), r.randint(0,780), s, s, r.choice(PRIMARY)))
    return '\n  '.join(els)

def style_wave_pattern(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Multiple wave bands
    n_waves = r.randint(4, 10)
    for i in range(n_waves):
        c = r.choice(colors)
        amplitude = r.randint(30, 100)
        frequency = r.uniform(1, 4)
        thickness = r.randint(20, 80)
        y_offset = i * (800 // n_waves) + 400 // n_waves
        points = []
        for x in range(0, 810, 10):
            y = y_offset + amplitude * math.sin(math.radians(x * frequency))
            points.append((x, y))
        # Draw as thick polygon band
        upper = points
        lower = [(x, y + thickness) for x, y in points]
        all_pts = upper + lower[::-1]
        pts_str = ' '.join(f'{x:.1f},{y:.1f}' for x, y in all_pts)
        els.append(f'<polygon points="{pts_str}" fill="{c}" opacity="{r.uniform(0.4,0.85):.2f}"/>')
    # Structural horizontal lines
    for _ in range(r.randint(3, 8)):
        y = r.randint(0, 800)
        els.append(line(0, y, 800, y, BLACK, r.uniform(1, 3), 0.3))
    # Accent elements
    for _ in range(r.randint(5, 15)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(5, 30), r.choice(PRIMARY), r.uniform(0.6, 1.0)))
    # Corner squares
    for px, py in [(0,0),(760,0),(0,760),(760,760)]:
        s = r.randint(20, 50)
        els.append(rect(px, py, s, s, r.choice(PRIMARY)))
    return '\n  '.join(els)

def style_scatter_field(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Background structure
    for x in range(0, 801, 100):
        els.append(line(x, 0, x, 800, BLACK, 0.5, 0.07))
    for y in range(0, 801, 100):
        els.append(line(0, y, 800, y, BLACK, 0.5, 0.07))
    # Large anchor shapes
    for _ in range(r.randint(2, 4)):
        s = r.randint(100, 250)
        x = r.randint(0, 800-s)
        y = r.randint(0, 800-s)
        if r.random() > 0.5:
            els.append(rect(x, y, s, s, r.choice(colors), r.uniform(0.5, 0.8)))
        else:
            els.append(circle(x+s//2, y+s//2, s//2, r.choice(colors), r.uniform(0.5, 0.8)))
    # Medium elements
    for _ in range(r.randint(8, 16)):
        s = r.randint(30, 80)
        x = r.randint(0, 800-s)
        y = r.randint(0, 800-s)
        els.append(rect(x, y, s, s, r.choice(PRIMARY), r.uniform(0.6, 1.0)))
    # Small elements
    for _ in range(r.randint(15, 30)):
        if r.random() > 0.5:
            els.append(circle(r.randint(0,800), r.randint(0,800),
                             r.randint(4, 15), r.choice(colors), r.uniform(0.5, 1.0)))
        else:
            s = r.randint(5, 20)
            els.append(rect(r.randint(0,795), r.randint(0,795), s, s,
                           r.choice(colors), r.uniform(0.5, 1.0)))
    # Bold structural line
    els.append(line(r.randint(0,400), 0, r.randint(400,800), 800,
                   r.choice([BLACK, WHITE, RED]), r.uniform(3, 8), r.uniform(0.5, 0.8)))
    return '\n  '.join(els)

def style_bar_chart(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Background lines
    for y in range(0, 801, 80):
        els.append(line(0, y, 800, y, BLACK, 0.5, 0.1))
    # Bars
    n_bars = r.randint(5, 15)
    bar_w = 700 // n_bars
    padding = (800 - n_bars * bar_w) // 2
    for i in range(n_bars):
        x = padding + i * bar_w + r.randint(2, 8)
        bar_h = r.randint(100, 700)
        y = 800 - bar_h
        c = r.choice(colors)
        bw = bar_w - r.randint(4, 12)
        els.append(rect(x, y, bw, bar_h, c, r.uniform(0.7, 1.0)))
        # Top accent
        els.append(rect(x, y, bw, r.randint(5, 20), r.choice(PRIMARY)))
    # Horizontal reference line
    ref_y = r.randint(200, 600)
    els.append(line(0, ref_y, 800, ref_y, BLACK, 2, 0.4))
    # Accent circles
    for _ in range(r.randint(4, 10)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(5, 25), r.choice(PRIMARY), r.uniform(0.6, 1.0)))
    return '\n  '.join(els)

def style_cross_composition(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    cx = r.randint(250, 550)
    cy = r.randint(250, 550)
    arm_w = r.randint(60, 150)
    # Cross arms
    c_cross = r.choice(PRIMARY)
    els.append(rect(0, cy - arm_w//2, 800, arm_w, c_cross, r.uniform(0.7, 1.0)))
    els.append(rect(cx - arm_w//2, 0, arm_w, 800, r.choice(colors), r.uniform(0.7, 1.0)))
    # Quadrant fills
    for qx, qy, qw, qh in [(0,0,cx-arm_w//2,cy-arm_w//2),
                             (cx+arm_w//2,0,800-cx-arm_w//2,cy-arm_w//2),
                             (0,cy+arm_w//2,cx-arm_w//2,800-cy-arm_w//2),
                             (cx+arm_w//2,cy+arm_w//2,800-cx-arm_w//2,800-cy-arm_w//2)]:
        if r.random() > 0.4:
            c = r.choice(colors)
            els.append(rect(qx, qy, qw, qh, c, r.uniform(0.2, 0.6)))
    # Center square
    s = r.randint(30, 80)
    els.append(rect(cx-s//2, cy-s//2, s, s, r.choice(PRIMARY)))
    # Concentric rings around center
    for rad in [100, 200, 300]:
        if r.random() > 0.3:
            els.append(circle(cx, cy, rad, 'none', 1.0, r.choice([BLACK, WHITE]), r.uniform(1, 3)))
    # Accent elements
    for _ in range(r.randint(5, 15)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(5, 20), r.choice(PRIMARY), r.uniform(0.6, 1.0)))
    return '\n  '.join(els)

def style_mosaic(r, title, bg, colors):
    els = [rect(0, 0, 800, 800, bg)]
    # Irregular mosaic of rectangles
    used = [[False]*8 for _ in range(8)]
    cell = 100
    for row in range(8):
        for col in range(8):
            if used[row][col]:
                continue
            # Random size (1x1 to 3x3)
            max_w = min(r.randint(1,3), 8-col)
            max_h = min(r.randint(1,3), 8-row)
            # Check all cells are free
            clear = True
            for dr in range(max_h):
                for dc in range(max_w):
                    if used[row+dr][col+dc]:
                        clear = False
                        break
            if not clear:
                max_w, max_h = 1, 1
            for dr in range(max_h):
                for dc in range(max_w):
                    used[row+dr][col+dc] = True
            x = col * cell
            y = row * cell
            w = max_w * cell - 2
            h = max_h * cell - 2
            c = r.choice(colors)
            els.append(rect(x+1, y+1, w, h, c, r.uniform(0.6, 1.0)))
    return '\n  '.join(els)

def style_concentric_forms_mixed(r, title, bg, colors):
    """Mixed circles and squares concentrically."""
    els = [rect(0, 0, 800, 800, bg)]
    cx = r.randint(200, 600)
    cy = r.randint(200, 600)
    n = r.randint(7, 14)
    for i in range(n, 0, -1):
        sz = i * r.randint(28, 48)
        if i % 2 == 0:
            els.append(circle(cx, cy, sz//2, r.choice(colors), r.uniform(0.5, 0.9)))
        else:
            els.append(rect(cx-sz//2, cy-sz//2, sz, sz, r.choice(colors), r.uniform(0.5, 0.9)))
    # Structural lines
    for ang in range(0, 360, r.randint(30, 60)):
        rad2 = math.radians(ang)
        els.append(line(cx, cy, cx+400*math.cos(rad2), cy+400*math.sin(rad2),
                       BLACK, 0.5, 0.15))
    # Accent marks
    for _ in range(r.randint(6, 16)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(4, 20), r.choice(PRIMARY), r.uniform(0.6, 1.0)))
    # Border strips
    bw = r.randint(10, 30)
    c_border = r.choice(PRIMARY)
    for x2,y2,w2,h2 in [(0,0,800,bw),(0,800-bw,800,bw),(0,0,bw,800),(800-bw,0,bw,800)]:
        els.append(rect(x2, y2, w2, h2, c_border, r.uniform(0.6, 0.9)))
    return '\n  '.join(els)

def style_geometric_landscape(r, title, bg, colors):
    """Horizon-based geometric landscape."""
    els = [rect(0, 0, 800, 800, bg)]
    # Sky
    sky_h = r.randint(250, 450)
    els.append(rect(0, 0, 800, sky_h, r.choice(COOL + [CREAM]), r.uniform(0.6, 0.9)))
    # Ground
    ground_c = r.choice(WARM + DARK)
    els.append(rect(0, sky_h, 800, 800-sky_h, ground_c, r.uniform(0.7, 1.0)))
    # Horizon line
    els.append(line(0, sky_h, 800, sky_h, BLACK, r.uniform(2, 5)))
    # Sun/moon circle
    sun_x = r.randint(100, 700)
    sun_r = r.randint(40, 100)
    els.append(circle(sun_x, sky_h - sun_r - r.randint(20, 100), sun_r, r.choice([YELLOW, CORAL, WHITE])))
    # Ground forms (buildings, hills)
    for _ in range(r.randint(3, 8)):
        bw2 = r.randint(40, 200)
        bh2 = r.randint(50, 250)
        bx = r.randint(0, 800-bw2)
        by = sky_h - r.randint(0, 100)
        els.append(rect(bx, by, bw2, 800-by, r.choice(DARK + [WARM_GRAY]), r.uniform(0.7, 1.0)))
        # Window elements
        for wx in range(bx+10, bx+bw2-10, 20):
            for wy in range(by+10, sky_h+200, 25):
                if r.random() > 0.5:
                    els.append(rect(wx, wy, 8, 12, r.choice([YELLOW, WHITE]), r.uniform(0.5, 0.9)))
    # Sky elements
    for _ in range(r.randint(3, 8)):
        w2 = r.randint(30, 120)
        h2 = r.randint(5, 20)
        els.append(rect(r.randint(0,780), r.randint(0,sky_h-20), w2, h2,
                       r.choice([WHITE, LIGHT_BLUE, CREAM]), r.uniform(0.3, 0.6)))
    return '\n  '.join(els)

def style_lattice_network(r, title, bg, colors):
    """Network of nodes and connections."""
    els = [rect(0, 0, 800, 800, bg)]
    # Background grid
    for x in range(0, 801, 80):
        els.append(line(x, 0, x, 800, BLACK, 0.5, 0.08))
    for y in range(0, 801, 80):
        els.append(line(0, y, 800, y, BLACK, 0.5, 0.08))
    # Generate nodes
    nodes = [(r.randint(50, 750), r.randint(50, 750)) for _ in range(r.randint(8, 20))]
    # Connect nodes
    for i, (x1, y1) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes):
            if i < j and r.random() > 0.5:
                dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                if dist < 350:
                    c = r.choice(colors)
                    els.append(line(x1, y1, x2, y2, c, r.uniform(1, 4), r.uniform(0.4, 0.8)))
    # Draw nodes
    for x, y in nodes:
        r_size = r.randint(8, 25)
        c = r.choice(PRIMARY)
        els.append(circle(x, y, r_size, c))
        # Halo
        els.append(circle(x, y, r_size+5, 'none', 1.0, c, 1.5))
    return '\n  '.join(els)

def style_linear_rhythm(r, title, bg, colors):
    """Rhythmic arrangement of lines and bars."""
    els = [rect(0, 0, 800, 800, bg)]
    direction = r.choice(['h', 'v'])
    n_elements = r.randint(15, 40)
    span = 800 // n_elements
    primary_c = r.choice(PRIMARY)
    accent_c = r.choice([c for c in colors if c != primary_c])
    for i in range(n_elements):
        pos = i * span
        width = r.randint(2, span - 2)
        beat = (i % r.randint(3, 7) == 0)  # Rhythmic accent
        c = primary_c if beat else r.choice([accent_c, bg])
        op = r.uniform(0.7, 1.0) if beat else r.uniform(0.3, 0.7)
        if direction == 'h':
            els.append(rect(0, pos, 800, width, c, op))
        else:
            els.append(rect(pos, 0, width, 800, c, op))
    # Bold accent
    for _ in range(r.randint(2, 5)):
        if direction == 'h':
            y = r.randint(0, 800)
            els.append(line(0, y, 800, y, r.choice([BLACK, WHITE]), r.uniform(3, 8)))
        else:
            x = r.randint(0, 800)
            els.append(line(x, 0, x, 800, r.choice([BLACK, WHITE]), r.uniform(3, 8)))
    # Cross-directional elements
    for _ in range(r.randint(3, 8)):
        if direction == 'h':
            x = r.randint(0, 800)
            els.append(line(x, 0, x, 800, r.choice(PRIMARY), r.uniform(2, 6), r.uniform(0.4, 0.8)))
        else:
            y = r.randint(0, 800)
            els.append(line(0, y, 800, y, r.choice(PRIMARY), r.uniform(2, 6), r.uniform(0.4, 0.8)))
    # Accent dots
    for _ in range(r.randint(5, 12)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(5, 20), r.choice(PRIMARY), r.uniform(0.7, 1.0)))
    return '\n  '.join(els)

def style_geometric_figure(r, title, bg, colors):
    """Bold single geometric figure as hero element."""
    els = [rect(0, 0, 800, 800, bg)]
    # Background texture
    for x in range(0, 801, r.randint(40, 100)):
        els.append(line(x, 0, x, 800, r.choice(colors), r.uniform(0.5, 2), 0.1))
    for y in range(0, 801, r.randint(40, 100)):
        els.append(line(0, y, 800, y, r.choice(colors), r.uniform(0.5, 2), 0.1))
    # Hero element
    hero = r.choice(['circle', 'rect', 'triangle'])
    hc = r.choice(PRIMARY)
    if hero == 'circle':
        r_size = r.randint(150, 300)
        cx2 = r.randint(200, 600)
        cy2 = r.randint(200, 600)
        els.append(circle(cx2, cy2, r_size, hc, 0.9))
        # Concentric rings
        for dr in [30, 60, 90]:
            els.append(circle(cx2, cy2, r_size+dr, 'none', 1.0, BLACK, r.uniform(1, 3)))
    elif hero == 'rect':
        w = r.randint(200, 500)
        h = r.randint(200, 500)
        x2 = r.randint(0, 800-w)
        y2 = r.randint(0, 800-h)
        els.append(rect(x2, y2, w, h, hc, 0.85))
        els.append(rect(x2+10, y2+10, w-20, h-20, 'none', 1.0))
    else:
        cx2, cy2 = r.randint(200,600), r.randint(200,600)
        s = r.randint(150, 300)
        pts = [(cx2, cy2-s), (cx2+s, cy2+s//2), (cx2-s, cy2+s//2)]
        els.append(polygon(pts, hc, 0.85))
    # Supporting elements
    for _ in range(r.randint(5, 15)):
        s = r.randint(10, 50)
        els.append(rect(r.randint(0,780), r.randint(0,780), s, s,
                       r.choice(colors), r.uniform(0.3, 0.7)))
    for _ in range(r.randint(3, 8)):
        els.append(circle(r.randint(0,800), r.randint(0,800),
                         r.randint(5, 25), r.choice(colors), r.uniform(0.4, 0.7)))
    # Strong framing lines
    bw = r.randint(8, 20)
    els.append(rect(0, 0, 800, bw, r.choice(PRIMARY)))
    els.append(rect(0, 800-bw, 800, bw, r.choice(PRIMARY)))
    return '\n  '.join(els)

def style_mechanical(r, title, bg, colors):
    """Mechanical / industrial abstraction."""
    els = [rect(0, 0, 800, 800, bg)]
    # Background grid
    for x in range(0, 801, 50):
        els.append(line(x, 0, x, 800, BLACK, 0.5, 0.1))
    for y in range(0, 801, 50):
        els.append(line(0, y, 800, y, BLACK, 0.5, 0.1))
    # Gear-like circle with notches
    for _ in range(r.randint(1, 3)):
        cx2 = r.randint(150, 650)
        cy2 = r.randint(150, 650)
        outer_r = r.randint(80, 180)
        inner_r = outer_r - r.randint(15, 30)
        n_teeth = r.randint(8, 24)
        pts = []
        for i in range(n_teeth * 2):
            ang = math.radians(i * 360 / (n_teeth * 2))
            rad = outer_r if i % 2 == 0 else inner_r
            pts.append((cx2 + rad * math.cos(ang), cy2 + rad * math.sin(ang)))
        c = r.choice(colors)
        els.append(polygon(pts, c, r.uniform(0.6, 0.9)))
        els.append(circle(cx2, cy2, inner_r - 10, bg))
        els.append(circle(cx2, cy2, r.randint(5, 15), r.choice(PRIMARY)))
    # Pipes/bars
    for _ in range(r.randint(3, 8)):
        x1 = r.randint(0, 800)
        y1 = r.randint(0, 800)
        x2 = r.randint(0, 800)
        y2 = y1 + r.randint(-20, 20)
        els.append(line(x1, y1, x2, y2, r.choice(DARK + [WARM_GRAY]), r.uniform(8, 20), r.uniform(0.7, 1.0)))
        # End caps
        els.append(circle(x1, y1, r.randint(5, 12), r.choice(PRIMARY)))
        els.append(circle(x2, y2, r.randint(5, 12), r.choice(PRIMARY)))
    # Bolts (small circles in grid)
    for bx in range(r.randint(50, 150), 800, r.randint(100, 200)):
        for by2 in range(r.randint(50, 150), 800, r.randint(100, 200)):
            if r.random() > 0.4:
                els.append(circle(bx, by2, r.randint(4, 10), r.choice([BLACK, WARM_GRAY])))
    return '\n  '.join(els)

def style_typographic_grid(r, title, bg, colors):
    """Grid-based typographic-inspired layout (no text)."""
    els = [rect(0, 0, 800, 800, bg)]
    # Column grid
    n_cols = r.choice([2, 3, 4, 6])
    col_w = 800 // n_cols
    gutter = r.randint(5, 20)
    # Row grid
    n_rows = r.choice([4, 5, 6, 8])
    row_h = 800 // n_rows
    # Fill cells with varying-width bars (simulating text/headlines)
    for row in range(n_rows):
        for col in range(n_cols):
            x = col * col_w + gutter//2
            y = row * row_h + gutter//2
            w = col_w - gutter
            h = row_h - gutter
            if r.random() > 0.2:
                # Sometimes span multiple cols
                span = 1
                if col + 1 < n_cols and r.random() > 0.7:
                    span = 2
                actual_w = span * col_w - gutter
                c = r.choice(colors)
                # Headline bar (thick)
                if r.random() > 0.6:
                    els.append(rect(x, y, actual_w, r.randint(h//4, h//2), c, r.uniform(0.7, 1.0)))
                    # Body bars (thin)
                    for by2 in range(y + h//2, y+h, r.randint(8, 15)):
                        bar_w = r.randint(actual_w//2, actual_w)
                        els.append(rect(x, by2, bar_w, r.randint(3, 7), r.choice([BLACK, WARM_GRAY]), 0.5))
                else:
                    els.append(rect(x, y, actual_w, h, c, r.uniform(0.4, 0.8)))
    # Column rules
    for col in range(1, n_cols):
        x = col * col_w
        els.append(line(x, 0, x, 800, BLACK, 1, 0.2))
    # Row rules
    for row in range(1, n_rows):
        y = row * row_h
        els.append(line(0, y, 800, y, BLACK, 0.5, 0.15))
    # Accent color blocks
    for _ in range(r.randint(2, 5)):
        col = r.randint(0, n_cols-1)
        row = r.randint(0, n_rows-1)
        els.append(rect(col*col_w, row*row_h, col_w, row_h, r.choice(PRIMARY), r.uniform(0.4, 0.7)))
    return '\n  '.join(els)

# Assign styles to pieces
STYLES = [
    style_horizontal_bands,
    style_concentric_circles,
    style_diagonal_tension,
    style_grid_blocks,
    style_radial_burst,
    style_vertical_pillars,
    style_arc_composition,
    style_nested_squares,
    style_triangle_field,
    style_overlapping_circles,
    style_staircase,
    style_target,
    style_quadrant_study,
    style_wave_pattern,
    style_scatter_field,
    style_bar_chart,
    style_cross_composition,
    style_mosaic,
    style_concentric_forms_mixed,
    style_geometric_landscape,
    style_lattice_network,
    style_linear_rhythm,
    style_geometric_figure,
    style_mechanical,
    style_typographic_grid,
]

# All 350 pieces with their named themes
PIECES = [
    (251, "Industrial Horizon"),
    (252, "Solar Dial"),
    (253, "Midnight Lattice"),
    (254, "Fractured Arc"),
    (255, "River Bend"),
    (256, "Geometric Storm"),
    (257, "Cathedral Grid"),
    (258, "Atomic Dance"),
    (259, "Meridian Cross"),
    (260, "Copper Coil"),
    (261, "Steel Horizon"),
    (262, "Harbor Light"),
    (263, "Prism Break"),
    (264, "Clock Face"),
    (265, "Tower Silhouette"),
    (266, "Magnetic Field"),
    (267, "Accordion Folds"),
    (268, "Polar Orbit"),
    (269, "Weave Study"),
    (270, "Signal Tower"),
    (271, "Broken Circle"),
    (272, "Cargo Net"),
    (273, "Autumn Grid"),
    (274, "Blueprint Fragment"),
    (275, "Pendulum Trace"),
    (276, "Chimney Stack"),
    (277, "Tidal Pattern"),
    (278, "War Machine"),
    (279, "Harvest Moon"),
    (280, "Ice Shelf"),
    (281, "Optical Grid"),
    (282, "Telegraph Line"),
    (283, "Deco Panel"),
    (284, "Transformer"),
    (285, "Porthole View"),
    (286, "Salt Flat"),
    (287, "Gear Mesh"),
    (288, "Velocity Lines"),
    (289, "Terrace Steps"),
    (290, "Beacon"),
    (291, "Circuit Path"),
    (292, "Crop Circle"),
    (293, "Airfield"),
    (294, "Wax Seal"),
    (295, "Labyrinth Entry"),
    (296, "Longitude Lines"),
    (297, "Brick Bond"),
    (298, "Aperture"),
    (299, "Thermal Map"),
    (300, "Midpoint"),
    (301, "Searchlight"),
    (302, "Cargo Hold"),
    (303, "Echo Chamber"),
    (304, "Refinery"),
    (305, "Navigation Chart"),
    (306, "Strata"),
    (307, "Mechanical Flower"),
    (308, "Sine Wave"),
    (309, "Library Stack"),
    (310, "Control Panel"),
    (311, "Vanishing Point"),
    (312, "Window Grid"),
    (313, "Arch Bridge"),
    (314, "Quarry"),
    (315, "Telescope Array"),
    (316, "Binary Code"),
    (317, "Suspension Point"),
    (318, "Map Contour"),
    (319, "Crane Arm"),
    (320, "Partition Wall"),
    (321, "Oscilloscope"),
    (322, "Flour Mill"),
    (323, "Brick Arch"),
    (324, "Depth Chart"),
    (325, "Spiral Galaxy"),
    (326, "Frame Study"),
    (327, "Rivet Pattern"),
    (328, "Solar Panel"),
    (329, "Broadcast"),
    (330, "Counterpoint"),
    (331, "Relief Map"),
    (332, "Spectral Line"),
    (333, "Shaft of Light"),
    (334, "Drawbridge Lift"),
    (335, "Pinwheel Cluster"),
    (336, "Engine Room"),
    (337, "Crosshatch"),
    (338, "Triptych"),
    (339, "Pressure Gauge"),
    (340, "Cliff Face"),
    (341, "Ripple Tank"),
    (342, "Cargo Crane"),
    (343, "Frequency"),
    (344, "Blueprint Grid"),
    (345, "Sounding Line"),
    (346, "Modular Units"),
    (347, "Flux"),
    (348, "Watchtower Grid"),
    (349, "Phase Shift"),
    (350, "Equilibrium"),
    (351, "Truss Work"),
    (352, "Cipher"),
    (353, "Migration Path"),
    (354, "Stack Exchange"),
    (355, "Iris Mechanism"),
    (356, "Ground Plan"),
    (357, "Dynamo"),
    (358, "Tidal Lock"),
    (359, "Switchboard"),
    (360, "Radiant Floor"),
    (361, "Calibration"),
    (362, "Slag Heap"),
    (363, "Manifold"),
    (364, "Sector Study"),
    (365, "Observation Deck"),
    (366, "Coil Spring"),
    (367, "Weather Map"),
    (368, "Cell Division"),
    (369, "Grain Silo"),
    (370, "Phase Diagram"),
    (371, "Power Grid"),
    (372, "Concave Form"),
    (373, "Axonometric View"),
    (374, "Pressure Wave"),
    (375, "Datum Line"),
    (376, "Interference Pattern"),
    (377, "Fulcrum Balance"),
    (378, "Pitch and Roll"),
    (379, "Modulation"),
    (380, "Slab Construction"),
    (381, "Thermal Column"),
    (382, "Parallax"),
    (383, "Structural Bay"),
    (384, "Resonant Frequency"),
    (385, "Bearing Surface"),
    (386, "Quay Wall"),
    (387, "Amplitude"),
    (388, "Ley Line"),
    (389, "Draft View"),
    (390, "Tension Member"),
    (391, "Masonry Bond"),
    (392, "Signal Interference"),
    (393, "Pilaster"),
    (394, "Equipotential"),
    (395, "Load Path"),
    (396, "Settlement"),
    (397, "Hard Edge"),
    (398, "Span"),
    (399, "Truss Section"),
    (400, "Centennial Mark"),
    (401, "Cantilever"),
    (402, "Void Study"),
    (403, "Lateral Force"),
    (404, "Plumb Study"),
    (405, "Diagonal Brace"),
    (406, "Rafter Pattern"),
    (407, "Compression Ring"),
    (408, "Keystone"),
    (409, "Voussoir"),
    (410, "Tympanum"),
    (411, "Colonnade"),
    (412, "Entablature"),
    (413, "Frieze Band"),
    (414, "Drum"),
    (415, "Nave Section"),
    (416, "Fluting"),
    (417, "Capital Study"),
    (418, "Plinth"),
    (419, "Soffit Pattern"),
    (420, "Engaged Column"),
    (421, "Hyperbola"),
    (422, "Catenary"),
    (423, "Parabola"),
    (424, "Ellipse Study"),
    (425, "Involute"),
    (426, "Cycloid"),
    (427, "Epitrochoid"),
    (428, "Hypocycloid"),
    (429, "Lemniscate"),
    (430, "Archimedean Spiral"),
    (431, "Logarithmic Spiral"),
    (432, "Pascals Triangle"),
    (433, "Fibonacci Sequence"),
    (434, "Golden Ratio"),
    (435, "Platonic Solid"),
    (436, "Euler Line"),
    (437, "Tessellation Study"),
    (438, "Voronoi Diagram"),
    (439, "Delaunay Mesh"),
    (440, "Convex Hull"),
    (441, "Fractal Boundary"),
    (442, "Strange Attractor"),
    (443, "Bifurcation"),
    (444, "Phase Space"),
    (445, "Limit Cycle"),
    (446, "Saddle Point"),
    (447, "Vector Field"),
    (448, "Gradient Descent"),
    (449, "Eigenform"),
    (450, "Matrix Transform"),
    (451, "Möbius Strip"),
    (452, "Klein Bottle"),
    (453, "Torus Section"),
    (454, "Hypersphere"),
    (455, "Calabi-Yau"),
    (456, "Knot Theory"),
    (457, "Braid Group"),
    (458, "Linking Number"),
    (459, "Trefoil"),
    (460, "Figure Eight Knot"),
    (461, "Seifert Surface"),
    (462, "Alexander Polynomial"),
    (463, "Chromatic Number"),
    (464, "Planar Graph"),
    (465, "Complete Graph"),
    (466, "Bipartite Graph"),
    (467, "Spanning Tree"),
    (468, "Hamiltonian Path"),
    (469, "Euler Circuit"),
    (470, "Traveling Salesman"),
    (471, "Convex Polygon"),
    (472, "Star Polygon"),
    (473, "Regular Compound"),
    (474, "Dual Polygon"),
    (475, "Polygon Triangulation"),
    (476, "Lattice Points"),
    (477, "Fundamental Domain"),
    (478, "Symmetry Group"),
    (479, "Wallpaper Pattern"),
    (480, "Frieze Symmetry"),
    (481, "Point Symmetry"),
    (482, "Glide Reflection"),
    (483, "Screw Symmetry"),
    (484, "Inversion Center"),
    (485, "Mirror Plane"),
    (486, "Rotation Group"),
    (487, "Dihedral Group"),
    (488, "Crystallographic Point Group"),
    (489, "Space Group"),
    (490, "Bravais Lattice"),
    (491, "Unit Cell"),
    (492, "Miller Index"),
    (493, "Reciprocal Lattice"),
    (494, "Brillouin Zone"),
    (495, "Wigner-Seitz Cell"),
    (496, "Band Structure"),
    (497, "Phonon Dispersion"),
    (498, "Density of States"),
    (499, "Phase Transition"),
    (500, "Crystalline Order"),
    (501, "Defect Cluster"),
    (502, "Grain Boundary"),
    (503, "Dislocation Line"),
    (504, "Vacancy Cluster"),
    (505, "Interstitial"),
    (506, "Substitution"),
    (507, "Stacking Fault"),
    (508, "Twin Boundary"),
    (509, "Antiphase Domain"),
    (510, "Precipitate"),
    (511, "Dendrite"),
    (512, "Eutectic"),
    (513, "Martensite"),
    (514, "Pearlite"),
    (515, "Bainite"),
    (516, "Spherulite"),
    (517, "Colloidal Crystal"),
    (518, "Liquid Crystal"),
    (519, "Quasicrystal"),
    (520, "Amorphous"),
    (521, "Polymer Chain"),
    (522, "Cross-Link"),
    (523, "Crystallinity"),
    (524, "Tacticity"),
    (525, "Branching"),
    (526, "Network Polymer"),
    (527, "Block Copolymer"),
    (528, "Microphase"),
    (529, "Lamellar Phase"),
    (530, "Gyroid Phase"),
    (531, "Cylinder Phase"),
    (532, "Sphere Phase"),
    (533, "Perforated Layer"),
    (534, "Double Gyroid"),
    (535, "Schwarz Surface"),
    (536, "Helicoid"),
    (537, "Catenoid"),
    (538, "Enneper Surface"),
    (539, "Costa Surface"),
    (540, "Scherk Surface"),
    (541, "Plateau Problem"),
    (542, "Weierstrass Map"),
    (543, "Bonnet Transformation"),
    (544, "Conjugate Surface"),
    (545, "Associate Family"),
    (546, "Mean Curvature"),
    (547, "Gaussian Curvature"),
    (548, "Principal Curvatures"),
    (549, "Umbilical Point"),
    (550, "Ridge Line"),
    (551, "Parabolic Line"),
    (552, "Asymptotic Line"),
    (553, "Geodesic Path"),
    (554, "Parallel Transport"),
    (555, "Holonomy"),
    (556, "Gaussian Map"),
    (557, "Shape Operator"),
    (558, "Second Fundamental Form"),
    (559, "Theorema Egregium"),
    (560, "Gauss-Bonnet"),
    (561, "Euler Characteristic"),
    (562, "Genus"),
    (563, "Orientability"),
    (564, "Fundamental Polygon"),
    (565, "Universal Cover"),
    (566, "Deck Transformation"),
    (567, "Covering Space"),
    (568, "Fiber Bundle"),
    (569, "Principal Bundle"),
    (570, "Associated Bundle"),
    (571, "Connection Form"),
    (572, "Curvature Form"),
    (573, "Chern Class"),
    (574, "Pontryagin Class"),
    (575, "Euler Class"),
    (576, "Characteristic Class"),
    (577, "Index Theorem"),
    (578, "K-Theory"),
    (579, "Cobordism"),
    (580, "Surgery Theory"),
    (581, "Handle Decomposition"),
    (582, "Morse Theory"),
    (583, "Floer Homology"),
    (584, "Donaldson Invariant"),
    (585, "Seiberg-Witten"),
    (586, "Gromov-Witten"),
    (587, "Fukaya Category"),
    (588, "Mirror Symmetry"),
    (589, "String Duality"),
    (590, "Compactification"),
    (591, "Moduli Space"),
    (592, "Teichmüller Space"),
    (593, "Mapping Class Group"),
    (594, "Dehn Twist"),
    (595, "Pseudo-Anosov"),
    (596, "Thurston Norm"),
    (597, "Hyperbolic Volume"),
    (598, "Dehn Surgery"),
    (599, "JSJ Decomposition"),
    (600, "Grand Finale"),
]

def pick_style(num):
    """Pick a style based on piece number for variety."""
    return STYLES[num % len(STYLES)]

def pick_bg_and_colors(r, num):
    """Pick background and color set."""
    bg_options = [WHITE, CREAM, BLACK, BLUE, FOREST, STEEL_BLUE]
    bg = bg_options[num % len(bg_options)]
    # Build a color set avoiding the background
    if bg in [WHITE, CREAM]:
        colors = [RED, BLUE, YELLOW, BLACK, TEAL, ORANGE, BURGUNDY, FOREST]
    elif bg in [BLACK]:
        colors = [RED, YELLOW, WHITE, TEAL, ORANGE, STEEL_BLUE, LIGHT_BLUE, CORAL]
    elif bg in [BLUE, FOREST]:
        colors = [RED, YELLOW, WHITE, TEAL, ORANGE, LIGHT_BLUE, CORAL, CREAM]
    else:
        colors = [RED, YELLOW, WHITE, BLACK, ORANGE, BURGUNDY, TEAL]
    r.shuffle(colors)
    return bg, colors

def generate_piece(num, title):
    seed = num * 31337 + 42
    r = random.Random(seed)
    bg, colors = pick_bg_and_colors(r, num)
    style_fn = pick_style(num)
    body = style_fn(r, title, bg, colors)
    return svg_wrap(title, body)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total = len(PIECES)
    for i, (num, title) in enumerate(PIECES):
        fname = f"bauhaus_{num}.svg"
        fpath = os.path.join(OUTPUT_DIR, fname)
        svg = generate_piece(num, title)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(svg)
        if (i+1) % 50 == 0 or i == total-1:
            print(f"  Generated {i+1}/{total}: {fname} — {title}")
    print(f"\nDone! Generated {total} SVG files.")
    # Print the titles list for index.html
    print("\nTitles for index.html:")
    for num, title in PIECES:
        print(f'  "{title}",')

if __name__ == '__main__':
    main()
