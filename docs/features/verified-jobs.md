# Verified Jobs

Moderated job board for paid video editing work. Users submit jobs, staff reviews them, and approved jobs get published to a forum with apply/close buttons.

This page covers the full system end to end. If you're a reviewer, the [Review Guide](../guides/review-guide.md) is the quick-reference version focused on what you need day to day. For configuration, see the [VJ Dashboard](../dashboards/vj-dashboard.md) reference.

## Submission Flow

### What the user sees

1. **Click the Submit button** in the info channel
2. **Pre-checks run** - system enabled, user has required submitter role (staff are exempt), user doesn't have a blocked role, not blocked by strikes, not on cooldown, no duplicate drafts
3. **Monetization gate** (if enabled, see [Token System](token-system.md) for full details):
    - Users with a Hiring Pass role skip this entirely
    - Otherwise the user needs at least 1 job token (purchased from Server Shop)
    - In agency-only mode, only agencies need tokens. Individuals post free
4. **Dropdowns**:
    - Job type: Video Editor, Thumbnail, Clipper, VFX Artist
    - Content format (video jobs only): Long Form, Medium Form, Short Form
    - Payment timing: Upfront, Partial Upfront, After Completion
    - Sample work policy: No Sample Required, Paid Sample
    - Agency status: Yes / No (skipped if user already has the agency role — they're locked to agency)
5. **Modal opens** with fields for description, payment method, budget, and reference URLs. Thumbnail jobs get a FileUpload component for up to 6 images instead of URLs
6. **Auto-validation** checks for:
    - Crypto keywords or wallet addresses (Bitcoin/Ethereum)
    - External contact info (email, phone, Telegram, WhatsApp)
    - Invalid budget ("TBD", "negotiable" without numbers)
    - Bad payment methods (gift cards, in-game currency, "exposure")
    - Percentage-based or unreliable payment (revenue share, "based on views", "when I get monetized")
    - Hidden payment amounts ("DM me for price", "ask in DM")
    - Profanity
7. **Duplicate detection** warns if 85%+ similar to a recent submission from the last 7 days
8. **Preview** shows how the job will appear. User can edit, cancel, or submit

If validation fails, the user gets a DM explaining why and the submission doesn't enter the queue.

### Image uploads (thumbnail jobs)

Discord's FileUpload in modals creates temporary attachments that expire immediately. The bot downloads them and re-uploads to the review thread, creating permanent Discord CDN URLs that persist through to the forum post. If upload fails, a fallback notice in the forum thread asks the user to upload manually.

---

## Review Workflow

Validated submissions appear in the review channel as embed cards.

### Review card contents

- Job type badge, content format, agency status
- Hiring Entity (agency name or "Hiring for myself")
- Budget and Payment Method
- Payment Timing (Upfront / Partial Upfront / After Completion)
- Sample Work (Required or Not Required)
- Description (full job details)
- Timeline (if provided)
- Submitter mention and request ID in the footer

### Review buttons

| Button | What it does |
|--------|-------------|
| **Approve** | Publishes to forum, sends approval DM, consumes 1 token if monetization is on and user has no Hiring Pass |
| **Reject** | Adds 1 strike, sends rejection DM with reason(s). User blocked at 3 strikes (configurable) |
| **Hold** | Pauses for clarification, sends hold DM with ticket instructions. No strike. Once held, the Hold button is replaced by Withdraw |
| **Withdraw** | Only appears after a hold. Cancels the submission with no strike — use when you don't hear back from the submitter. Sends the submitter a DM and archives the intake thread |
| **Mark as Agency** | Only shows when agency-only enforcement is on. Assigns agency role to the submitter |

Only one reviewer can claim a submission. If someone else already acted on it, the button tells you.

For a practical breakdown of when to approve, reject, or hold (with green/red flags and tips), see the [Review Guide](../guides/review-guide.md).

### Rejection and hold reasons

Staff can select multiple reasons at once. All selected reasons show up as a bullet list in the submitter's DM.

| # | Reason | Holdable? |
|---|--------|-----------|
| 1 | Missing client/agency disclosure | Yes |
| 2 | Budget missing or unclear | Yes |
| 3 | Payment terms missing | Yes |
| 4 | Deliverables too vague | Yes |
| 5 | Timeline missing | Yes |
| 6 | Requirements unrealistic | No |
| 7 | References/examples missing | Yes |
| 8 | Suspected scam | No |
| 9 | Wrong channel / not a paid job | No |
| 10 | Other (see note) | Yes |
| 11 | Monthly/weekly rate instead of per-project | Yes |
| 12 | Payment amount not disclosed | Yes |
| 13 | Unreliable payment (percentage/views) | No |
| 14 | Unrealistic expectations | No |
| 15 | Currency not specified | Yes |
| 16 | Per-project rate, not monthly/weekly rate | No |
| 17 | Game currency/crypto payment not allowed | No |
| 18 | Minimum budget requirement | Yes |
| 19 | Two separate jobs in one post | No |

"Other" opens a modal for a custom note. The hold dropdown only shows holdable reasons.

---

## After Approval

### Forum post structure

1. **Thread created** with title: "Need {Job Type} - {Budget} - by @username"
2. **Main embed** with all job details including payment timing and sample work policy
3. **First reply** with "How to Apply" instructions and a safety notice
4. **Second reply** (if any) with reference links and/or uploaded images
5. **Fallback notice** on thumbnail jobs prompting the user to upload images to the thread if needed

The thread gets auto-tagged with the matching forum tag based on job type.

### Buttons on the forum post

- **Apply** - user applies to the job. Requires configured applicant role(s) if set. Tracked in the database so nobody can apply twice. Applicant count shown in footer
- **Close** - only the job submitter can use this. Archives and locks the thread

---

## Token System

Quick summary here. The [Token System](token-system.md) page has the full breakdown.

When monetization is enabled (`require_monetization` toggle), users need tokens or a Hiring Pass to submit jobs. Users buy token packages from Discord's Server Shop, and 1 token gets consumed per approved job. Users with a Hiring Pass role get unlimited submissions instead. In agency-only mode, only agencies need tokens and individuals post free.

Users can check their balance with `/vj_tokens`.

---

## Strike System

- +1 strike per rejection (not per hold)
- Blocked at 3 strikes (configurable via `max_strikes`)
- Blocked users see an error when clicking Submit
- Staff can check strikes with `/vj_config check_strikes @user`
- Staff can reset strikes to 0 with `/vj_config reset_strikes @user`
- Staff can decrement by a specific amount with `/vj_config reset_strikes @user amount:N`

---

## Commands

| Command | Tier | Description |
|---------|------|-------------|
| `/vj_dashboard` | 0 | Open the configuration dashboard ([reference](../dashboards/vj-dashboard.md)) |
| `/vj_config deploy_button` | 0 | Deploy the submit button to the info channel |
| `/vj_config check_strikes @user` | 0 | Check a user's strike count |
| `/vj_config reset_strikes @user [amount:N]` | 0 | Reset a user's strikes to 0, or decrement by N if `amount` is provided |
| `/vj_stats [time_range] [reviewer]` | 0 | View reviewer performance stats |
| `/vj_tokens` | any | Check your token balance |

---

## Common Scenarios

### Legitimate job with minor issues
Put it on Hold with the relevant reason. User gets a DM asking for clarification and is directed to open a ticket. Once they respond, approve or reject. If you don't hear back after 48 hours, use the Withdraw button to cancel without issuing a strike.

### Obvious scam
Reject with "Suspected scam". User gets a strike. Auto-validation catches most of these but some slip through.

### Agency without role
If agency-only enforcement is on, use the Mark as Agency button on the review card. Otherwise the role gets auto-assigned when they select "Yes" in the agency dropdown. Once a user has the agency role, they can't submit as an individual — the agency dropdown is skipped entirely on future submissions.

### Thumbnail job with no images
Either Hold for "References/examples missing", or approve anyway. The fallback notice in the forum thread guides them to upload images.

### Duplicate submission
Check if the original job is still open. If yes, reject as duplicate. If the original is closed, the new one is fine to approve.

### DM notification failed
Normal. Some users have DMs disabled. The job still processes, no action needed.

### User complaining about auto-rejection
Auto-validation can have false positives. Check what triggered it (crypto keywords, contact info patterns, budget format, payment method, percentage-based pay, "DM for price"). Ask the user to rephrase and resubmit.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Submit button not working | Check system is enabled ([Status panel](../dashboards/vj-dashboard.md#status)). Check user strikes. Check cooldown settings |
| Review buttons not responding | Check your permissions. Someone else may have already reviewed it. Check log channel |
| Forum post not created after approval | Check forum channel is configured (Status panel). Check bot permissions in the forum. Check logs |
| Images not showing | They auto-embed from URLs, give it a few seconds. If user skipped upload, the fallback notice handles it |
| Wrong stats in /vj_stats | Stats are per-reviewer and real-time. Check if you're filtering by timeframe |
