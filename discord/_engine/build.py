#!/usr/bin/env python3
"""Generic builder for "docs as code" Discord posts.

Usage:  python3 _engine/build.py <channel-dir>
        (defaults to the current directory if no arg is given)

Reads <channel-dir>/content.py, which must define:
    META      = {"brand": str, "default_accent": "#RRGGBB"}
    MESSAGES  = [(num, slug, accent_hex_or_None, title, footer_label, body), ...]

Writes one Components V2 payload per message to <channel-dir>/NN-slug.json:
a Container (accent bar) with a title, a divider under it, the body split on
[[SEP]] into separator-divided blocks, and a small branded footer.

Split a body into blocks with a line containing only:  [[SEP]]
"""
import importlib.util
import json
import os
import sys
import time

# Publish time as a localized Discord timestamp (<t:unix:D>) shown in every footer.
REVISED_TS = int(time.time())


def color(hexstr):
    return int(hexstr.lstrip("#"), 16)


def sep():
    return {"type": 14, "divider": True, "spacing": 2}


def load_content(channel_dir):
    path = os.path.join(channel_dir, "content.py")
    if not os.path.isfile(path):
        sys.exit(f"no content.py in {channel_dir}")
    spec = importlib.util.spec_from_file_location("content", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.META, mod.MESSAGES


def build_one(brand, accent_hex, title, footer_label, body):
    comps = [{"type": 10, "content": title}, sep()]              # title, then divider under it
    for b in [x.strip("\n") for x in body.split("[[SEP]]")]:
        comps.append({"type": 10, "content": b})
        comps.append(sep())                                      # section dividers + divider before footer
    comps.append({"type": 10, "content": f"-# **{brand}**  ·  {footer_label}  ·  Last revised <t:{REVISED_TS}:D>"})
    return {"flags": 32768, "components": [{"type": 17, "accent_color": color(accent_hex), "components": comps}]}


def main():
    channel_dir = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    meta, messages = load_content(channel_dir)
    brand = meta["brand"]
    default_accent = meta["default_accent"]
    for num, slug, accent_hex, title, footer_label, body in messages:
        payload = build_one(brand, accent_hex or default_accent, title, footer_label, body)
        chars = sum(len(c["content"]) for c in payload["components"][0]["components"] if c["type"] == 10)
        out = os.path.join(channel_dir, f"{num}-{slug}.json")
        with open(out, "w") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"{num}-{slug}.json  {chars} chars" + ("  ⚠️OVER4000" if chars > 4000 else ""))


if __name__ == "__main__":
    main()
