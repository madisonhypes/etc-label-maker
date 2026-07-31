#!/usr/bin/env python
"""Assemble the single-file app.html from the template + assets in build-assets/.
Re-run this whenever the template, fonts, or frame images change:
    python build.py
Then bump version.txt and upload app.html + version.txt to GitHub.
"""
import base64, pathlib, sys

ROOT = pathlib.Path(__file__).parent
A = ROOT / "build-assets"

def b64(path, mime):
    data = (A / path).read_bytes()
    return f"data:{mime};base64," + base64.b64encode(data).decode("ascii")

def main():
    version = (ROOT / "version.txt").read_text(encoding="utf-8").strip() or "0.0.0"
    html = (ROOT / "app.template.html").read_text(encoding="utf-8")

    oswald    = b64("oswald500.woff2",    "font/woff2")
    frameL    = b64("frame_large.png",    "image/png")
    frameS    = b64("frame_small.png",    "image/png")

    html = html.replace("__FONT_OSWALD__", oswald)
    html = html.replace("__VERSION__", version)
    # inject frame data URIs as JS globals
    inject = ('"use strict";\n'
              f'const FRAME_LARGE="{frameL}";\n'
              f'const FRAME_SMALL="{frameS}";')
    html = html.replace('"use strict";', inject, 1)

    out = ROOT / "app.html"
    out.write_text(html, encoding="utf-8")
    size = out.stat().st_size
    print(f"Built app.html  v{version}  {size:,} bytes")
    if size < 40_000:
        print("WARNING: app.html is under 40 KB; the launcher's validity check "
              "(MIN_SIZE) requires >=40 KB. Add more embedded assets.", file=sys.stderr)

if __name__ == "__main__":
    main()
