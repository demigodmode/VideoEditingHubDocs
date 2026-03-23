# VJ Review Guide

Practical guide for staff reviewing job submissions. For the full system overview including submission flow, forum publishing, and troubleshooting, see [Verified Jobs](../features/verified-jobs.md).

## The basics

Review cards show up in the review channel. Read the job details, click one of the action buttons. The bot handles DMs, forum publishing, and status tracking.

| Button | When to use |
|--------|-------------|
| **Approve** | Job is legit, well-written, reasonable budget, acceptable payment method |
| **Reject** | Scam, budget too low, bad payment method, rule violation, duplicate |
| **Hold** | Need more info, want to clarify something, want a second opinion |

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
- Crypto, gift cards, or non-standard payment
- "ASAP" with promises of big money

## Rejection reasons

When you reject or hold, you pick a reason from a dropdown:

| # | Reason | Can hold? |
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

Hold only shows the holdable reasons. "Other" opens a text box for a custom note.

## Review tips

- Use Hold over Reject when something is fixable. Holds don't add strikes
- Be consistent. Discuss edge cases with the team so budget thresholds and standards stay fair
- Aim for 24h turnaround. Faster reviews mean better experience for posters
- When in doubt, Hold. Better to pause and ask than approve something sketchy

## What happens after you act

**Approve:**

- Job publishes to the forum immediately with Apply/Close buttons
- User gets a DM with the forum link (and token balance if monetization is on)
- Review card turns green
- 1 token consumed if monetization is enabled (unless user has [Hiring Pass](../features/token-system.md#hiring-pass))

**Reject:**

- User gets +1 strike (blocked at 3)
- User gets a DM with the rejection reason
- Review card turns red

**Hold:**

- No strike added
- User gets a DM explaining what's needed
- Review card turns gold
- Approve/Reject buttons stay active for follow-up

## Privacy

- User strikes are private, don't share publicly. More on how strikes work in the [Strike System](../features/verified-jobs.md#strike-system) section
- Review discussions stay in staff channels
- Rejection reasons are sent via DM only. DM templates can be customized in the [VJ Dashboard](../dashboards/vj-dashboard.md#messages)
