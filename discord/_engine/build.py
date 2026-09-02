#!/usr/bin/env python3
"""Generic builder for "docs as code" Discord posts.

Usage:  python3 _engine/build.py <channel-dir>
        (defaults to the current directory if no arg is given)

Reads <channel-dir>/content.py, which must define:
    META      = {"brand": str, "default_accent": "#RRGGBB", "thread_id": optional str}
    MESSAGES  = [(num, slug, accent_hex_or_None, title, footer_label, body), ...]
              = [(..., body, (button_label, button_url)), ...]   # 7th item optional

Writes one Components V2 payload per message to <channel-dir>/NN-slug.json:
a Container (accent bar) with a title, a divider under it, the body split on
[[SEP]] into separator-divided blocks, an optional link button, and a small
branded footer.

Split a body into blocks with a line containing only:  [[SEP]]

If META has "thread_id" (a forum post's starter message lives in a thread), writes
<channel-dir>/meta.json with that id, so send.sh can target the thread when editing.
"""
import importlib.util
import json
import os
import sys
import time

# Publish time as a localized Discord timestamp (<t:unix:D>) shown in every footer.
REVISED_TS = int(time.time())


def color(hexstr):
    digits = hexstr.lstrip("#")
    if len(digits) != 6 or any(c not in "0123456789abcdefABCDEF" for c in digits):
        sys.exit(f"bad accent color {hexstr!r} — need exactly 6 hex digits (e.g. #E8C84A)")
    return int(digits, 16)


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


def build_one(brand, accent_hex, title, footer_label, body, button=None):
    comps = [{"type": 10, "content": title}, sep()]              # title, then divider under it
    for b in [x.strip("\n") for x in body.split("[[SEP]]")]:
        comps.append({"type": 10, "content": b})
        comps.append(sep())                                      # section dividers + divider before footer
    if button:
        label, url = button
        comps.append({"type": 1, "components": [{"type": 2, "style": 5, "label": label, "url": url}]})
        comps.append(sep())
    comps.append({"type": 10, "content": f"-# **{brand}**  ·  {footer_label}  ·  Last revised <t:{REVISED_TS}:D>"})
    return {
        "flags": 32768,
        # TextDisplay content is real message content, not an embed description — Discord
        # parses @everyone/@here/roles in it like any other message. Suppress all of that;
        # these are informational posts, never notifications. (A literal <@user-id> mention
        # still renders as a clickable mention, it just won't ping.)
        "allowed_mentions": {"parse": []},
        # PATCHing a message doesn't clear fields you omit, it leaves them as-is. Converting
        # a legacy embed/plain-content message (e.g. an old Discohook post) to V2 needs these
        # explicitly emptied, or Discord rejects the edit: "embeds cannot be used with
        # IS_COMPONENTS_V2". Harmless no-op for a message that's already V2 or brand new.
        "embeds": [],
        "content": "",
        "components": [{"type": 17, "accent_color": color(accent_hex), "components": comps}],
    }


def main():
    channel_dir = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    meta, messages = load_content(channel_dir)
    brand = meta["brand"]
    default_accent = meta["default_accent"]
    over_limit = False
    for i, entry in enumerate(messages):
        button = None
        try:
            if len(entry) == 7:
                num, slug, accent_hex, title, footer_label, body, button = entry
            else:
                num, slug, accent_hex, title, footer_label, body = entry
        except (TypeError, ValueError):
            ident = ""
            if isinstance(entry, (tuple, list)) and len(entry) >= 2:
                ident = f" (num={entry[0]!r}, slug={entry[1]!r})"
            sys.exit(f"malformed MESSAGES entry at index {i}{ident}: expected 6 or 7 items, got {entry!r}")
        payload = build_one(brand, accent_hex or default_accent, title, footer_label, body, button)
        chars = sum(len(c["content"]) for c in payload["components"][0]["components"] if c["type"] == 10)
        out = os.path.join(channel_dir, f"{num}-{slug}.json")
        with open(out, "w") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"{num}-{slug}.json  {chars} chars")
        if chars > 4000:
            print(f"⚠️OVER4000: {num}-{slug}.json is {chars} chars", file=sys.stderr)
            over_limit = True

    if "thread_id" in meta:
        with open(os.path.join(channel_dir, "meta.json"), "w") as f:
            json.dump({"thread_id": meta["thread_id"]}, f, indent=2)

    if over_limit:
        sys.exit(1)


if __name__ == "__main__":
    main()
