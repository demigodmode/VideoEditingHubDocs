# Docs-as-code engine

Shared machinery for managing Discord "documentation" posts as code instead of
Discohook. Each channel is a folder next to this one with its own `content.py` and
`ids.json`; this engine builds and publishes any of them.

## Onboard a channel

1. `mkdir discord/<channel>` and write `content.py`:

   ```python
   META = {"brand": "Video Editing Hub", "default_accent": "#5865F2"}
   MESSAGES = [
       ("01", "welcome", "#5865F2", "# 👋 Welcome", "Welcome", """Body...\n[[SEP]]\nMore..."""),
   ]
   ```
   `[[SEP]]` inserts a divider. Accent `None` falls back to `META["default_accent"]`.

2. Preview locally: `python3 discord/_engine/build.py discord/<channel>` and eyeball
   the generated `NN-*.json`.
3. Create the channel's Discord webhook. Add it as a GitHub secret named
   `WEBHOOK_<CHANNEL>` — uppercase, hyphens become underscores
   (e.g. channel `writing-tips` → secret `WEBHOOK_WRITING_TIPS`).
4. In `.github/workflows/publish-docs.yml`: add the channel to the `channel` dropdown
   `options`, and add one `WEBHOOK_<CHANNEL>: ${{ secrets.WEBHOOK_<CHANNEL> }}` line to `env`.
5. Actions tab → "Publish docs to Discord" → Run workflow → pick the channel. The first
   run posts all messages and records their IDs; later runs edit them in place.

## Local publish (testing)

```bash
WEBHOOK_URL='https://discord.com/api/webhooks/xxx/yyy' \
  bash discord/_engine/send.sh discord/<channel>            # all
WEBHOOK_URL='...' bash discord/_engine/send.sh discord/<channel> 02-rates.json   # one
```

Never hand-edit the `NN-*.json` files — they're generated from `content.py`.
