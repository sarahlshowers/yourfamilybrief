#!/usr/bin/env python3
"""Your Family Brief — LinkedIn card (1200x1200). Reuses ig_set primitives."""
import ig_set as g
import cairo

W, H = 1200, 1200
surf, cr = g.make_canvas(W, H)
cx = W / 2
g.wordmark(cr, cx, 170)

items = [
    ("serif", "The household is an operations problem.", 84, g.ESPRESSO, g.IT),
    ("gap", "", 42, None, g.NM),
    ("sprig", "", 0, None, g.NM),
    ("gap", "", 42, None, g.NM),
    ("sans", "In most busy families, one parent is running an unpaid ops job. No dashboard, no backup, no recognition.", 34, g.ESPRESSO, g.NM),
    ("gap", "", 26, None, g.NM),
    ("sans", "A 45-minute working session. A personalized report in 48 hours that finally maps the load.", 34, g.ESPRESSO, g.NM),
]
maxw = 840
bh = g.block_height(cr, items, maxw)
top = 220 + ((H - 420) - bh) / 2
g.draw_block(cr, items, cx, top, maxw)

fy = H - 160
cr.set_source_rgb(*g.TAUPE); cr.set_line_width(1)
cr.move_to(cx - 280, fy); cr.line_to(cx + 280, fy); cr.stroke()
g.set_font(cr, g.SANS, 24)
g.draw_centered(cr, "NOW BOOKING  ·  $75  ·  LINK IN COMMENTS", cx, fy + 50, g.ROSE, tracking=4)

surf.write_to_png(g.OUT + "YFB_LinkedIn_Card.png")
print("done")
