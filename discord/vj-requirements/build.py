#!/usr/bin/env python3
"""Source of truth for the VJ "requirements" posts in Discord.

Edit the text below, run `python3 build.py`, then publish with send.sh (locally)
or the GitHub Action. Each message becomes a Components V2 payload: one Container
(the accent bar is the old embed "color") holding Text Display blocks split by
real Separator dividers.

Split a message into blocks with a line containing only:  [[SEP]]
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

def color(hexstr):
    return int(hexstr.lstrip("#"), 16)

# order, filename, accent hex, content ([[SEP]] = divider between text blocks)
MESSAGES = [
("01", "budget", "#E8C84A", """\
# 💰 Budget Requirements

Include your **currency**. Minimums below are in **USD**.

Your budget must be a specific amount or clear range, stated **per project** — not per week or month.
> - Posting a range (e.g. $50–$100)? The **lowest** figure must meet the minimum.
> - Weekly/monthly rates or "retainers" get rejected.

⚠️ Rates go by the video's **actual length**, not the platform or label. A YouTube Short, Reel, or TikTok is judged by runtime like anything else. **If lengths vary, we use the longest one.**

-# Minimum rates are in the next post."""),

("02", "rates", "#E8C84A", """\
# 💵 Minimum Rates

Each video rate has a **Simple** and an **Advanced** tier (defined at the bottom).

### 🎞️ Video Editing
→ **Short — up to 1:00** · Simple **$15+** · Advanced **$30+**
→ **Short — 1:01 to 3:00** · Simple **$30+** · Advanced **$60+**
→ **Medium — 3:01 to 10:00** · Simple **$40+** · Advanced **$80+**
→ **Long — 10:01+** · Simple **$60+** · Advanced **$120+** (first 10 min)
> - Then **+$10/min** (Simple) or **+$20/min** (Advanced) past 10:00.
[[SEP]]
### ✂️ Clipping
-# Handing over a full stream/VOD to find and cut the best moments. (Pricing being finalized — see staff.)

### 📷 Thumbnails
> - **$10+** each

### ✍️ Scriptwriting
> - **$10+** per script (up to 500 words), then **+$10** per 500 words
[[SEP]]
### Simple vs Advanced
-# **Simple** — cuts/trims, subtitles, media sourcing, basic color grading, audio fixes, simple pan/zoom. Talking-head videos, simple shorts, podcast clips, casual vlogs.
-# **Advanced** — complex grading, motion graphics/animation, sound design, fast-paced or multi-cam, VFX, Blender/3D. Documentaries, trailers, cinematic edits, brand ads.

-# A per-second/word rate must still clear the per-project minimum at your **longest** job. e.g. "$25 per 60s, up to 3:00" is a 3-minute video → **$30+**."""),

("03", "payment", "#E8C84A", """\
# 💳 Payment Rules

The amount goes **in your post**, not in DMs. If your budget answer is "DM me" or "we'll discuss", don't post.
[[SEP]]
### ✅ Accepted
> PayPal, Stripe, Wise, Revolut, CashApp, Zelle, Venmo, Bank/Wire, UPI

### ❌ Not accepted
> - Crypto or in-game currency (Robux, V-Bucks, etc.)
> - Gift cards or vouchers
> - Revenue share, profit split, or percentage-only
> - "Based on views", "when I monetize", "paid in exposure"

-# These are unreliable and usually mean editors work for free."""),

("04", "samples", "#9B59B6", """\
# 🧪 Sample Work Policy

Sample work must be **paid**. Minimum **$10**, max **30 seconds** of footage.

> - Meets your brief → pay
> - Close but needs changes → give feedback, pay after revision
> - Doesn't match the brief → don't pay

**Free samples or unpaid trials aren't allowed. Those posts get rejected.**"""),

("05", "writing-your-post", "#1E90FF", """\
# 📝 Writing Your Post

"DM me for details" isn't a job post. Give applicants enough to decide before they reach out. Vague posts get rejected.
[[SEP]]
### 🎬 Video / Clipping / VFX
> - Content type (YouTube, TikTok, podcast, commercial, etc.)
> - Editing style, with link examples — not just "good editing"
> - Rough length and turnaround time
> - Any software or delivery-format needs

### 🎨 Thumbnails / Design
> - Quantity and format (thumbnails, banners, channel art, etc.)
> - Dimensions or platform specs if relevant
> - Style references, or the colors/mood/vibe you want
> - One final version or variations"""),

("06", "agency", "#32CD32", """\
# 🏢 Posting as an Agency

When you submit, the bot asks if you're an agency. Select yes and your agency name is collected separately — no need to write it in the description. Once tagged, future submissions post under that agency automatically.
[[SEP]]
### Put in your description
> Context about the client or project so editors know who and what they're working with. "Agency posting for a gaming channel" beats leaving it blank.

### No middlemanning
> Being an agency means you're contracted to deliver the work. Just connecting clients with editors for a cut is a ban (see **Instant bans**)."""),

("07", "instant-bans", "#E74C3C", """\
# ⛔ Instant Bans

These skip the warning and go straight to a ban:
> - **Middlemanning / dropshipping** — you must be the real client or a contracted agency
> - **Sending applicants to an external Discord** to apply, submit work, or get details
> - **AI-generated projects** where most of the content (script, footage, voice) is AI-made with minimal human input"""),
]

def build_one(hexstr, content):
    blocks = [b.strip("\n") for b in content.split("[[SEP]]")]
    comps = []
    for i, b in enumerate(blocks):
        comps.append({"type": 10, "content": b})
        if i != len(blocks) - 1:
            comps.append({"type": 14, "divider": True, "spacing": 1})
    return {"flags": 32768, "components": [{"type": 17, "accent_color": color(hexstr), "components": comps}]}

def main():
    for num, name, hexstr, content in MESSAGES:
        payload = build_one(hexstr, content)
        chars = sum(len(c["content"]) for c in payload["components"][0]["components"] if c["type"] == 10)
        with open(os.path.join(HERE, f"{num}-{name}.json"), "w") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"{num}-{name}.json  {chars} chars" + ("  ⚠️OVER4000" if chars > 4000 else ""))

if __name__ == "__main__":
    main()
