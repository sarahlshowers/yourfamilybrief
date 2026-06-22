#!/usr/bin/env python3
"""Your Family Brief — Facebook (parent group) post graphic. Brand-exact colors."""
import cairo, math

W, H = 1080, 1350
LINEN    = (0xFA/255, 0xF5/255, 0xF2/255)
ESPRESSO = (0x3C/255, 0x2E/255, 0x30/255)
ROSE     = (0x9E/255, 0x5C/255, 0x6B/255)
TAUPE    = (0xC4/255, 0xB5/255, 0xA8/255)
WHITE    = (1, 1, 1)

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
cr = cairo.Context(surf)

# background
cr.set_source_rgb(*LINEN); cr.paint()

SERIF = "TeX Gyre Pagella"
SANS  = "TeX Gyre Adventor"

def text_w(s, face, size, slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL, tracking=0):
    cr.select_font_face(face, slant, weight); cr.set_font_size(size)
    base = cr.text_extents(s).x_advance
    return base + tracking * max(len(s) - 1, 0)

def draw_text(s, cx, y, face, size, color, slant=cairo.FONT_SLANT_NORMAL,
              weight=cairo.FONT_WEIGHT_NORMAL, tracking=0):
    """centered at cx, baseline y, optional letter tracking"""
    cr.select_font_face(face, slant, weight); cr.set_font_size(size)
    cr.set_source_rgb(*color)
    total = text_w(s, face, size, slant, weight, tracking)
    x = cx - total / 2
    if tracking == 0:
        cr.move_to(x, y); cr.show_text(s)
    else:
        for ch in s:
            cr.move_to(x, y); cr.show_text(ch)
            x += cr.text_extents(ch).x_advance + tracking

# ---- hairline frame (double) ----
cr.set_source_rgb(*TAUPE)
cr.set_line_width(1.5); cr.rectangle(44, 44, W-88, H-88); cr.stroke()
cr.set_line_width(0.8); cr.rectangle(56, 56, W-112, H-112); cr.stroke()

CX = W / 2

# ---- top wordmark ----
draw_text("YOUR FAMILY BRIEF", CX, 168, SANS, 27, ROSE, tracking=9)
# short rule
cr.set_source_rgb(*ROSE); cr.set_line_width(1.2)
cr.move_to(CX-36, 198); cr.line_to(CX+36, 198); cr.stroke()

# ---- headline (Pagella italic, espresso) ----
lines = ["The invisible work,", "finally seen."]
y = 560
for ln in lines:
    draw_text(ln, CX, y, SERIF, 92, ESPRESSO, slant=cairo.FONT_SLANT_ITALIC)
    y += 116

# ---- botanical sprig divider ----
def leaf(cr, x, y, angle, length, width, color):
    cr.save(); cr.translate(x, y); cr.rotate(angle)
    cr.move_to(0, 0)
    cr.curve_to(length*0.35, -width, length*0.75, -width*0.85, length, 0)
    cr.curve_to(length*0.75, width*0.85, length*0.35, width, 0, 0)
    cr.close_path(); cr.set_source_rgb(*color); cr.fill(); cr.restore()

sy = y - 40 + 56   # divider y
cr.set_source_rgb(*ROSE); cr.set_line_width(1.6)
cr.move_to(CX-120, sy)
cr.curve_to(CX-40, sy-14, CX+40, sy+14, CX+120, sy)
cr.stroke()
for i, t in enumerate((-0.78, -0.45, -0.12, 0.22, 0.55)):
    px = CX + t*110
    pyt = sy + math.sin((t+0.78)*2.4) * 9
    side = -1 if i % 2 == 0 else 1
    leaf(cr, px, pyt, side * (math.pi/3) + t*0.3, 34, 9, ROSE)

# ---- supporting copy (sans, wrapped, centered) ----
body = ("A 45-minute conversation. A personalized report in 48 hours. "
        "Built from everything you told me this spring.")
cr.select_font_face(SANS, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
cr.set_font_size(33)
words, cur, blines = body.split(), "", []
for wd in words:
    trial = (cur + " " + wd).strip()
    if cr.text_extents(trial).x_advance > 690 and cur:
        blines.append(cur); cur = wd
    else:
        cur = trial
blines.append(cur)
by = sy + 120
for ln in blines:
    draw_text(ln, CX, by, SANS, 33, ESPRESSO)
    by += 52

# ---- footer ----
fy = H - 170
cr.set_source_rgb(*TAUPE); cr.set_line_width(1)
cr.move_to(CX-260, fy); cr.line_to(CX+260, fy); cr.stroke()
draw_text("NOW BOOKING  ·  $75  ·  LINK IN COMMENTS", CX, fy+52, SANS, 23, ROSE, tracking=4)

surf.write_to_png("/sessions/sharp-gracious-euler/mnt/outputs/YFB_FB_PersonalFeed.png")
print("done")
