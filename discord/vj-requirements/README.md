# VJ requirements posts

The Verified Jobs "requirements" messages that sit above the submit button, managed
as code instead of Discohook. Content lives in `build.py`; it compiles to Discord
[Components V2](https://docs.discord.com/developers/components/using-message-components)
payloads (`NN-name.json`) that get posted/edited through a channel webhook.

## The 7 messages

| File | Post |
|------|------|
| `01-budget.json` | 💰 Budget Requirements |
| `02-rates.json` | 💵 Minimum Rates |
| `03-payment.json` | 💳 Payment Rules |
| `04-samples.json` | 🧪 Sample Work Policy |
| `05-writing-your-post.json` | 📝 Writing Your Post |
| `06-agency.json` | 🏢 Posting as an Agency |
| `07-instant-bans.json` | ⛔ Instant Bans |

## Editing content

1. Edit the text in `build.py` (single source of truth).
2. `python3 build.py` regenerates the JSON.
3. Publish (below). Existing posts are **edited in place** — no re-post, no re-ping.

Never hand-edit the `NN-*.json` files; they're generated.

## Publishing

**Via GitHub Actions (normal path):** Actions tab → "VJ requirements posts" → Run
workflow. It builds, posts/edits every message, and commits the message IDs back to
`ids.json`. Trigger is manual for now; flip on the `push` block in the workflow once
you trust it.

**Locally (for testing):**
```bash
WEBHOOK_URL='https://discord.com/api/webhooks/xxx/yyy' ./send.sh          # all
WEBHOOK_URL='...' ./send.sh 02-rates.json                                 # one
```

## How editing-in-place works

`ids.json` maps each file to the message the webhook created. First publish of a
file POSTs and records the ID; every publish after PATCHes that same message. Delete
a message and its next publish re-posts and updates the ID.

A webhook can only edit messages **it** created, so the first time you migrate a post
off Discohook: publish here once, then delete the old Discohook message.

## Setup (one-time)

1. In the target channel: Edit Channel → Integrations → Webhooks → New Webhook →
   Copy URL. Name/avatar it however the posts should appear.
2. Add it as a repo secret named **`WEBHOOK_VJ_REQUIREMENTS`**
   (Settings → Secrets and variables → Actions → New repository secret).
3. Run the workflow.

The webhook URL is a secret — it only ever lives in GitHub Secrets or your local env,
never in the repo.
