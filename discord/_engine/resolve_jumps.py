#!/usr/bin/env python3
"""Resolve [[JUMP:slug]] tokens in a built payload into Discord message links.

Usage:  resolve_jumps.py <channel-dir> <file.json> <guild_id> <channel_id>

Prints the resolved JSON to stdout. Each [[JUMP:slug]] becomes
https://discord.com/channels/<guild>/<channel>/<message_id>, where the message id
is looked up in the channel's ids.json (the key matching NN-<slug>.json). Put the
token inside a markdown link — [Section](  [[JUMP:slug]]  ) — for a clean label.

Jump files must be published AFTER their targets, so the ids already exist.
"""
import json
import os
import re
import sys

channel_dir, fname, guild_id, channel_id = sys.argv[1:5]

with open(os.path.join(channel_dir, "ids.json")) as f:
    ids = json.load(f)


def mid_for(slug):
    for key, val in ids.items():
        if re.match(rf"^\d+-{re.escape(slug)}\.json$", key):
            return val
    sys.exit(f"no posted message for jump slug {slug!r} — publish its target first")


with open(os.path.join(channel_dir, fname)) as f:
    raw = f.read()

raw = re.sub(
    r"\[\[JUMP:([a-z0-9-]+)\]\]",
    lambda m: f"https://discord.com/channels/{guild_id}/{channel_id}/{mid_for(m.group(1))}",
    raw,
)
sys.stdout.write(raw)
