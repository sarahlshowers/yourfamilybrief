#!/usr/bin/env python3
"""Render a populated Family Brief HTML deck to PDF (and optional PNG previews).

Usage:
    python3 render_pdf.py input.html output.pdf [--preview]

Pages are 1920x1080 (defined via @page in the template). Requires Playwright
with Chromium:
    pip install playwright --break-system-packages
    python3 -m playwright install chromium --with-deps
"""
import os
import subprocess
import sys
from pathlib import Path

# Headless Chromium needs libXdamage.so.1, which some sandboxes lack. It is
# never actually called in headless mode, so a stub satisfies the linker.
STUB_C = """
typedef unsigned long XID;
int XDamageQueryExtension(void* d, int* e, int* r){ if(e)*e=0; if(r)*r=0; return 0; }
XID XDamageCreate(void* d, XID w, int l){ return 0; }
void XDamageDestroy(void* d, XID x){ }
void XDamageSubtract(void* d, XID x, XID a, XID b){ }
"""


def ensure_xdamage_stub():
    libdir = Path.home() / ".stublibs"
    stub = libdir / "libXdamage.so.1"
    if not stub.exists():
        try:
            subprocess.run(["/sbin/ldconfig", "-p"], capture_output=True, text=True,
                           check=True)
        except Exception:
            pass
        probe = subprocess.run(["ldconfig", "-p"], capture_output=True, text=True)
        if "libXdamage.so.1" in probe.stdout:
            return  # real library present
        libdir.mkdir(exist_ok=True)
        src = libdir / "xdamage_stub.c"
        src.write_text(STUB_C)
        subprocess.run(["gcc", "-shared", "-fPIC", "-o", str(stub), str(src)],
                       check=True)
    os.environ["LD_LIBRARY_PATH"] = (str(libdir) + ":" +
                                     os.environ.get("LD_LIBRARY_PATH", ""))


def main():
    ensure_xdamage_stub()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    preview = "--preview" in sys.argv
    if len(args) != 2:
        print(__doc__)
        sys.exit(1)
    src, dst = Path(args[0]).resolve(), Path(args[1]).resolve()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Run:\n"
              "  pip install playwright --break-system-packages\n"
              "  python3 -m playwright install chromium --with-deps")
        sys.exit(2)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(src.as_uri())
        page.wait_for_load_state("networkidle")
        page.pdf(path=str(dst), width="1920px", height="1080px",
                 print_background=True, margin={t: "0" for t in
                                                ("top", "bottom", "left", "right")})
        print(f"PDF written: {dst}")

        if preview:
            slides = page.query_selector_all(".slide")
            for i, slide in enumerate(slides, 1):
                png = dst.with_name(f"{dst.stem}-page{i:02d}.png")
                slide.screenshot(path=str(png))
                print(f"Preview: {png}")
        browser.close()


if __name__ == "__main__":
    main()
