"""
default-banner.py
Generates the YFB default blog post banner (Concept A — Quiet wordmark).

Output: default-banner.png  (1200 × 480 px)

Usage:
    python3 default-banner.py

Requires:
    pip install pycairo

To use a different tagline per post, pass it as an argument:
    python3 default-banner.py "on routines, rhythms, and rest"
"""

import cairo
import sys
import math

# ─── Brand tokens ───────────────────────────────────────────────
LINEN    = (0.980, 0.961, 0.949)   # #FAF5F2
BLUSH    = (0.949, 0.867, 0.847)   # #F2DDD8
DUSTY    = (0.831, 0.659, 0.627)   # #D4A8A0
ROSE     = (0.620, 0.361, 0.420)   # #9E5C6B
TAUPE    = (0.769, 0.710, 0.659)   # #C4B5A8
ESPRESSO = (0.235, 0.180, 0.188)   # #3C2E30

# ─── Dimensions ─────────────────────────────────────────────────
W, H = 1200, 480

# ─── Text content ───────────────────────────────────────────────
WORDMARK = "YOUR FAMILY BRIEF"
TAGLINE  = sys.argv[1] if len(sys.argv) > 1 else "on family, clarity, and home"

# ─── Helpers ────────────────────────────────────────────────────

def set_color(ctx, rgb, alpha=1.0):
    ctx.set_source_rgba(*rgb, alpha)


def centered_text(ctx, text, y):
    """Draw text centered horizontally, return its width."""
    ext = ctx.text_extents(text)
    x = (W - ext.width) / 2 - ext.x_bearing
    ctx.move_to(x, y)
    ctx.show_text(text)
    return ext.width


def hairline(ctx, y, width=120):
    """Draw a centered horizontal hairline."""
    set_color(ctx, TAUPE)
    ctx.set_line_width(0.75)
    ctx.move_to((W - width) / 2, y)
    ctx.line_to((W + width) / 2, y)
    ctx.stroke()


# ─── Render ─────────────────────────────────────────────────────

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(surface)

# Background — linen
set_color(ctx, LINEN)
ctx.rectangle(0, 0, W, H)
ctx.fill()

# Bottom accent stripe — blush, 4px
set_color(ctx, BLUSH)
ctx.rectangle(0, H - 4, W, 4)
ctx.fill()

# Top hairline
hairline(ctx, H * 0.35, width=80)

# Wordmark — tracked caps, serif
# Cairo doesn't do letter-spacing natively, so we kern manually
ctx.select_font_face("TeX Gyre Pagella", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(22)
set_color(ctx, ROSE)

# Manual letter-spacing: draw each char with extra advance
def tracked_text(ctx, text, y, spacing=5):
    """Draw text with extra letter spacing, centered."""
    # Measure total width with tracking
    total = 0
    for ch in text:
        ext = ctx.text_extents(ch)
        total += ext.x_advance + spacing
    total -= spacing  # no trailing space

    x = (W - total) / 2
    for ch in text:
        ext = ctx.text_extents(ch)
        ctx.move_to(x - ext.x_bearing, y)
        ctx.show_text(ch)
        x += ext.x_advance + spacing


tracked_text(ctx, WORDMARK, H * 0.5, spacing=6)

# Tagline — italic serif, muted espresso
ctx.select_font_face("TeX Gyre Pagella", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(30)
set_color(ctx, ESPRESSO, alpha=0.38)
centered_text(ctx, TAGLINE, H * 0.62)

# Bottom hairline
hairline(ctx, H * 0.70, width=80)

# Save
out = "default-banner.png"
surface.write_to_png(out)
print(f"Saved → {out}  ({W}×{H}px)")
