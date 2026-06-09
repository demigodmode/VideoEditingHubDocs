# VJ Review Guide

Practical guide for staff reviewing job submissions. For the full system overview including submission flow, forum publishing, and troubleshooting, see [Verified Jobs](../features/verified-jobs.md). For the staff decision guide, see [VJ Hold vs Reject Guide](hold-vs-reject.md).

## The basics

Review cards show up in the review channel. Read the job details, click one of the action buttons. The bot handles DMs, forum publishing, and status tracking.

Members can also report live VJ posts from the forum. Those reports show up in the configured VJ Report channel, or fall back to the Log channel and then Review channel.

| Button | When to use |
|--------|-------------|
| **Approve** | Job is legit, complete enough to publish, reasonable budget, acceptable payment method |
| **Hold** | Something fixable is missing, unclear, or needs staff editing before approval |
| **Reject** | Job is not allowed, scammy, duplicate, unsuitable for VJ, or cannot be fixed by clarification |
| **Withdraw** | Only available after holding. Use when the submitter doesn't respond — cancels with no strike |

## Green flags

- Clear, detailed job description
- Specific budget amount
- Standard payment methods (PayPal, Venmo, CashApp, UPI)
- Realistic timeline
- Reference links or images provided

## Red flags

- Wants to move conversation off Discord quickly
- Asks for upfront fees from applicants
- Unrealistic budget (too high or suspiciously low)
- Vague "DM me for details" descriptions
- Gift cards or non-standard payment
- "ASAP" with promises of big money

!!! note "Crypto submissions"
    Crypto payment is already auto-declined by the bot in normal cases, so staff usually should not need to reject those manually.

## Rejection reasons

When you reject or hold, you pick one or more reasons from a dropdown. All selected reasons show up as a bullet list in the submitter's DM.

| Reason | Can hold? |
|--------|-----------|
| Missing client/agency disclosure | Yes |
| Budget missing or unclear | Yes |
| Deliverables too vague | Yes |
| Timeline missing | Yes |
| Requirements unrealistic | No |
| References/examples missing | Yes |
| Suspected scam | No |
| Wrong channel / not a paid job | No |
| Other (see note) | Yes |
| Monthly/weekly rate instead of per-project | Yes |
| Payment amount not disclosed | Yes |
| Unreliable payment (percentage/views) | No |
| Unrealistic expectations | No |
| Currency not specified | Yes |
| Per-project rate, not monthly/weekly rate | No |
| Game currency/crypto payment not allowed | No |
| Minimum budget requirement | Yes |
| Two separate jobs in one post | No |

Hold only shows the holdable reasons. "Other" opens a text box for a custom note.

## Hold vs Reject

The short version: **Hold fixable posts. Reject posts that should not be allowed through.**

For the full staff-facing decision guide, including editable held-submission fields and examples, see [VJ Hold vs Reject Guide](hold-vs-reject.md).

## Review tips

- You can select multiple rejection/hold reasons at once — all of them show up in the submitter's DM
- Be consistent. Discuss edge cases with the team so budget thresholds and standards stay fair
- Aim for 24h turnaround. Faster reviews mean better experience for posters
- When in doubt, Hold. Better to pause and ask than approve something sketchy

## What happens after you act

**Approve:**

- Job publishes to the forum immediately with Apply, Close, and Report buttons
- User gets a DM with the forum link (and token balance if monetization is on)
- Review card turns green
- 1 token consumed if monetization is enabled (unless user has [Hiring Pass](../features/token-system.md#hiring-pass))

**Reject:**

- User gets +1 strike (blocked at 3)
- User gets a DM with the rejection reason
- Review card turns red

**Hold:**

- No strike added
- User gets a DM explaining what's needed and how to open a ticket
- Review card turns gold
- Hold button is replaced by Withdraw. Approve/Reject stay active

**Withdraw** (after hold only):

- No strike added
- User gets a DM letting them know the submission was withdrawn and they need to re-submit
- Intake thread is archived
- Review card turns gray

## Member reports

Published VJ posts have a **Report** button. Reporters can select multiple reasons, add required details, optionally include evidence links, and optionally upload screenshots. Staff alerts include the reporter, original poster, job ID, thread link, selected reasons, details, and evidence.

Common report reasons:

- Middleman / agency concern
- Scam / suspicious behavior
- Payment issue
- Misleading or inaccurate post
- Unsafe / abusive behavior
- Spam / low-quality / not a real job
- Other

Each user can report a given job once. The original submitter cannot report their own job.

## Privacy

- User strikes are private, don't share publicly. More on how strikes work in the [Strike System](../features/verified-jobs.md#strike-system) section
- Review discussions stay in staff channels
- Rejection reasons are sent via DM only. DM templates can be customized in the [VJ Dashboard](../dashboards/vj-dashboard.md#messages)
