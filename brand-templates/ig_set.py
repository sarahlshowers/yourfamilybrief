#!/usr/bin/env python3
"""Your Family Brief — Instagram carousel (5 slides) + story frames. Brand-exact."""
import cairo, math

LINEN    = (0xFA/255, 0xF5/255, 0xF2/255)
ESPRESSO = (0x3C/255, 0x2E/255, 0x30/255)
ROSE     = (0x9E/255, 0x5C/255, 0x6B/255)
TAUPE    = (0xC4/255, 0xB5/255, 0xA8/255)
SERIF = "TeX Gyre Pagella"
SANS  = "TeX Gyre Adventor"
IT = cairo.FONT_SLANT_ITALIC
NM = cairo.FONT_SLANT_NORMAL
OUT = "/sessions/sharp-gracious-euler/mnt/outputs/"

def make_canvas(W, H):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    cr.set_source_rgb(*LINEN); cr.paint()
    cr.set_source_rgb(*TAUPE)
    cr.set_line_width(1.5); cr.rectangle(44, 44, W-88, H-88); cr.stroke()
    cr.set_line_width(0.8); cr.rectangle(56, 56, W-112, H-112); cr.stroke()
    return surf, cr

def set_font(cr, face, size, slant=NM):
    cr.select_font_face(face, slant, cairo.FONT_WEIGHT_NORMAL); cr.set_font_size(size)

def tracked_w(cr, s, tracking):
    return cr.text_extents(s).x_advance + tracking * max(len(s)-1, 0)

def draw_centered(cr, s, cx, y, color, tracking=0):
    cr.set_source_rgb(*color)
    x = cx - tracked_w(cr, s, tracking) / 2
    if tracking == 0:
        cr.move_to(x, y); cr.show_text(s)
    else:
        for ch in s:
            cr.move_to(x, y); cr.show_text(ch)
            x += cr.text_extents(ch).x_advance + tracking

def wrap(cr, text, maxw):
    words, cur, lines = text.split(), "", []
    for wd in words:
        t = (cur + " " + wd).strip()
        if cr.text_extents(t).x_advance > maxw and cur:
            lines.append(cur); cur = wd
        else:
            cur = t
    lines.append(cur)
    return lines

def sprig(cr, cx, sy, scale=1.0):
    def leaf(x, y, angle, length, width):
        cr.save(); cr.translate(x, y); cr.rotate(angle)
        cr.move_to(0, 0)
        cr.curve_to(length*0.35, -width, length*0.75, -width*0.85, length, 0)
        cr.curve_to(length*0.75, width*0.85, length*0.35, width, 0, 0)
        cr.close_path(); cr.set_source_rgb(*ROSE); cr.fill(); cr.restore()
    cr.set_source_rgb(*ROSE); cr.set_line_width(1.6*scale)
    cr.move_to(cx-120*scale, sy)
    cr.curve_to(cx-40*scale, sy-14*scale, cx+40*scale, sy+14*scale, cx+120*scale, sy)
    cr.stroke()
    for i, t in enumerate((-0.78, -0.45, -0.12, 0.22, 0.55)):
        px = cx + t*110*scale
        py = sy + math.sin((t+0.78)*2.4) * 9 * scale
        side = -1 if i % 2 == 0 else 1
        leaf(px, py, side*(math.pi/3)+t*0.3, 34*scale, 9*scale)

def wordmark(cr, cx, y):
    set_font(cr, SANS, 27)
    draw_centered(cr, "YOUR FAMILY BRIEF", cx, y, ROSE, tracking=9)
    cr.set_source_rgb(*ROSE); cr.set_line_width(1.2)
    cr.move_to(cx-36, y+30); cr.line_to(cx+36, y+30); cr.stroke()

def dots(cr, cx, y, n, active):
    span = (n-1) * 30
    for i in range(n):
        x = cx - span/2 + i*30
        cr.set_source_rgb(*(ROSE if i == active else TAUPE))
        cr.arc(x, y, 5.5 if i == active else 4, 0, 2*math.pi); cr.fill()

# block items: (kind, text, size, color, slant)
def block_height(cr, items, maxw):
    h = 0
    for kind, text, size, color, slant in items:
        if kind == "gap":
            h += size
        elif kind == "sprig":
            h += 60
        else:
            face = SERIF if kind == "serif" else SANS
            set_font(cr, face, size, slant)
            lh = size * (1.26 if kind == "serif" else 1.55)
            h += lh * len(wrap(cr, text, maxw))
    return h

def draw_block(cr, items, cx, top, maxw):
    y = top
    for kind, text, size, color, slant in items:
        if kind == "gap":
            y += size; continue
        if kind == "sprig":
            sprig(cr, cx, y + 30); y += 60; continue
        face = SERIF if kind == "serif" else SANS
        set_font(cr, face, size, slant)
        lh = size * (1.26 if kind == "serif" else 1.55)
        for ln in wrap(cr, text, maxw):
            y += lh
            set_font(cr, face, size, slant)
            draw_centered(cr, ln, cx, y - lh*0.28, color)
    return y

def slide(fname, items, idx, n, W=1080, H=1350, maxw=760, swipe=False):
    surf, cr = make_canvas(W, H)
    cx = W/2
    wordmark(cr, cx, 168)
    bh = block_height(cr, items, maxw)
    top = 230 + ((H - 420) - bh) / 2
    draw_block(cr, items, cx, top, maxw)
    dots(cr, cx, H-130, n, idx)
    if swipe:
        set_font(cr, SANS, 22)
        draw_centered(cr, "S W I P E   →", cx, H-180, TAUPE, tracking=2)
    surf.write_to_png(OUT + fname)

S, G = "serif", "gap"
slides = [
    ([("serif", "You didn’t fail at the whiteboard.", 86, ESPRESSO, IT),
      (G, "", 44, None, NM),
      ("serif", "The whiteboard failed you.", 56, ROSE, IT)], True),
    ([("serif", "Every system died for the same reason.", 80, ESPRESSO, IT),
      (G, "", 40, None, NM),
      ("sprig", "", 0, None, NM),
      (G, "", 40, None, NM),
      ("sans", "It asked an exhausted parent to do more upkeep.", 36, ESPRESSO, NM)], False),
    ([("serif", "What if someone just… looked at all of it?", 80, ESPRESSO, IT),
      (G, "", 40, None, NM),
      ("sprig", "", 0, None, NM),
      (G, "", 40, None, NM),
      ("sans", "The schedules. The reminding.", 36, ESPRESSO, NM),
      ("sans", "The things that live only in your head.", 36, ESPRESSO, NM)], False),
    ([("serif", "A 45-minute conversation.", 62, ESPRESSO, IT),
      ("serif", "A personalized report in 48 hours.", 62, ESPRESSO, IT),
      (G, "", 40, None, NM),
      ("sprig", "", 0, None, NM),
      (G, "", 40, None, NM),
      ("sans", "What’s draining you most, plus five first steps that maintain themselves.", 36, ESPRESSO, NM)], False),
    ([("serif", "$75. One call.", 88, ESPRESSO, IT),
      ("serif", "Finally seen.", 88, ROSE, IT),
      (G, "", 44, None, NM),
      ("sans", "L I N K   I N   B I O", 30, ESPRESSO, NM)], False),
]
for i, (items, swipe) in enumerate(slides):
    slide(f"YFB_IG_Carousel_{i+1}.png", items, i, len(slides), swipe=swipe)

# ---- Story frames 1080x1920 ----
def story(fname, items, maxw=720, top_anchor=None):
    W, H = 1080, 1920
    surf, cr = make_canvas(W, H)
    cx = W/2
    wordmark(cr, cx, 210)
    bh = block_height(cr, items, maxw)
    if top_anchor is None:
        top = 280 + ((H - 560) - bh) / 2
    else:
        top = top_anchor
    draw_block(cr, items, cx, top, maxw)
    surf.write_to_png(OUT + fname)

# Frame 1 — announcement (alt to face-to-camera clip)
story("YFB_Story_1_Announcement.png", [
    ("serif", "The survey you all filled out this spring?", 84, ESPRESSO, IT),
    (G, "", 44, None, NM),
    ("serif", "It became a real thing.", 76, ROSE, IT),
    (G, "", 44, None, NM),
    ("sprig", "", 0, None, NM),
])

# Frame 2 — product card
story("YFB_Story_2_ProductCard.png", [
    ("serif", "Your Family Brief", 96, ESPRESSO, IT),
    (G, "", 46, None, NM),
    ("sprig", "", 0, None, NM),
    (G, "", 46, None, NM),
    ("sans", "A 45-minute call about how your family actually runs.", 38, ESPRESSO, NM),
    (G, "", 24, None, NM),
    ("sans", "A personalized report in 48 hours: what’s draining you + where to start.", 38, ESPRESSO, NM),
    (G, "", 52, None, NM),
    ("serif", "$75", 84, ROSE, NM),
])

# Frame 3 — link sticker frame: copy in top half, bottom open for sticker
story("YFB_Story_3_LinkFrame.png", [
    ("serif", "First spots are open now.", 88, ESPRESSO, IT),
    (G, "", 40, None, NM),
    ("sprig", "", 0, None, NM),
    (G, "", 48, None, NM),
    ("sans", "Tap below to book your session", 36, ROSE, NM),
    (G, "", 16, None, NM),
    ("sans", "↓", 64, ROSE, NM),
], top_anchor=400)

# Frame 4 — next-day reshare overlay: copy at top, bottom open for the reshared post
story("YFB_Story_4_Reshare.png", [
    ("serif", "Still thinking about this?", 84, ESPRESSO, IT),
    (G, "", 36, None, NM),
    ("serif", "It’s one call.", 72, ROSE, IT),
    (G, "", 40, None, NM),
    ("sans", "↓", 60, ROSE, NM),
], top_anchor=330)

print("done")
