#!/usr/bin/env python3
"""Static site generator for the In-Clues studio deck.

Reads content/ (YAML + Markdown + image folders), renders Jinja2 templates,
and writes dist/index.html + assets. Content-driven: drop files into
content/ and rebuild.

Usage:
  python build.py                 # one-off build → dist/
  python build.py --serve         # build + serve dist/ at :8899
  python build.py --watch         # rebuild on content/templates/static change
  python build.py --serve --watch # edit-and-preview loop
"""
import argparse
import http.server
import socketserver
import threading
import time
import shutil
from pathlib import Path

import yaml
import markdown as md
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
WATCH_DIRS = [CONTENT, TEMPLATES, STATIC, ASSETS]


def load_yaml(path: Path):
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_sections():
    out = {}
    d = CONTENT / "sections"
    for p in sorted(d.glob("*.yaml")):
        out[p.stem] = load_yaml(p)
    return out


def parse_frontmatter(text: str):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return (yaml.safe_load(parts[1]) or {}, parts[2].strip())
    return ({}, text.strip())


def load_collection_md(name: str):
    d = CONTENT / "collections" / name
    items = []
    if not d.exists():
        return items
    for p in sorted(d.glob("*.md")):
        meta, body = parse_frontmatter(p.read_text(encoding="utf-8"))
        meta["body"] = body
        meta["body_html"] = md.markdown(body) if body else ""
        meta["_file"] = p.name
        items.append(meta)
    # order: explicit `order` first, then date desc, then filename
    items.sort(key=lambda m: (
        m.get("order", 10 ** 9),
        _neg_date(m.get("date")),
        m.get("_file", ""),
    ))
    return items


def _neg_date(v):
    # newest first when no explicit order; strings sort lexically (ISO dates)
    return "" if v is None else "".join(reversed(str(v)))


def load_gallery():
    d = CONTENT / "collections" / "gallery"
    caps = load_yaml(d / "_captions.yaml")
    imgs = []
    if d.exists():
        for p in sorted(d.iterdir()):
            if p.is_file() and p.suffix.lower() in IMG_EXT:
                imgs.append({"file": p.name, "caption": caps.get(p.name, "")})
    return imgs


def hero_palette(theme: str):
    purple = theme == "purple"
    return {
        "bg": "#7B77A8" if purple else "#F6F6F9",
        "fg": "#FFFFFF" if purple else "#33324A",
        "border": "rgba(255,255,255,0.6)" if purple else "#B8C2C8",
        "sub": "#FFFFFF" if purple else "#625E92",
        "is_purple": purple,
        "is_light": not purple,
    }


def build():
    site = load_yaml(CONTENT / "site.yaml")
    sections = load_sections()
    collections = {
        "articles": load_collection_md("articles"),
        "interviews": load_collection_md("interviews"),
        "testimonials": load_collection_md("testimonials"),
        "gallery": load_gallery(),
    }
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["markdown"] = lambda v: md.markdown(v) if v else ""
    html = env.get_template("base.html").render(
        site=site,
        s=sections,
        col=collections,
        hero=hero_palette(site.get("hero_theme", "light")),
    )

    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(html, encoding="utf-8")

    # custom domain for GitHub Pages
    domain = site.get("custom_domain")
    if domain:
        (DIST / "CNAME").write_text(domain.strip() + "\n", encoding="utf-8")

    # assets: brand assets + gallery images
    dist_assets = DIST / "assets"
    if dist_assets.exists():
        shutil.rmtree(dist_assets)
    shutil.copytree(ASSETS, dist_assets)
    gdir = CONTENT / "collections" / "gallery"
    if gdir.exists():
        out = dist_assets / "gallery"
        out.mkdir(parents=True, exist_ok=True)
        for p in gdir.iterdir():
            if p.is_file() and p.suffix.lower() in IMG_EXT:
                shutil.copy2(p, out / p.name)

    # static
    for name in ("styles.css", "main.js"):
        src = STATIC / name
        if src.exists():
            shutil.copy2(src, DIST / name)

    n_g = len(collections["gallery"])
    print(f"✓ built dist/index.html  (gallery: {n_g} img, "
          f"articles: {len(collections['articles'])}, "
          f"interviews: {len(collections['interviews'])}, "
          f"testimonials: {len(collections['testimonials'])})")


def _snapshot():
    latest = 0.0
    for base in WATCH_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file():
                latest = max(latest, p.stat().st_mtime)
    return latest


def watch_loop():
    last = _snapshot()
    print("watching content/ templates/ static/ assets/ … (Ctrl-C to stop)")
    while True:
        time.sleep(0.5)
        cur = _snapshot()
        if cur != last:
            last = cur
            try:
                build()
            except Exception as e:  # keep the loop alive on content errors
                print(f"! build failed: {e}")


def serve(port: int):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(DIST), **k)
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.ThreadingTCPServer(("", port), handler)
    except OSError as e:
        print(f"! port {port} is already in use ({e}).\n"
              f"  Free it, or pick another port:  python3 build.py --serve --port {port + 1}")
        return
    httpd.daemon_threads = True
    print(f"serving http://localhost:{port}/  (dist/)")
    httpd.serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build the In-Clues deck.")
    ap.add_argument("--serve", action="store_true", help="serve dist/")
    ap.add_argument("--watch", action="store_true", help="rebuild on change")
    ap.add_argument("--port", type=int, default=8899)
    args = ap.parse_args()

    build()
    if args.watch:
        threading.Thread(target=watch_loop, daemon=True).start()
    if args.serve:
        try:
            serve(args.port)
        except KeyboardInterrupt:
            pass
    elif args.watch:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
