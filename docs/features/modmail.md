# Modmail

Members DM the bot to reach staff, and staff handle the conversation from a private ticket channel in the server. There's no external ticketing site and no separate bot: it's all built into VEH.

For the full staff command list see the [Ticket Commands guide](../guides/ticket-commands.md). For managing canned replies and close reasons, see [Modmail Snippets](../guides/modmail-snippets.md).

## Opening a ticket

### What the member sees

1. **They DM the bot.** If Modmail is disabled, not fully configured, or the guild is unreachable, they get a short message explaining that (these are all configurable in the dashboard).
2. If the confirmation gate is off (this is the **default**), their first DM opens a ticket immediately and they get a "ticket created" confirmation.
3. If the confirmation gate is turned on, the bot doesn't open anything on the first DM. Instead it sends a prompt with **Open ticket** and **Cancel** buttons, asking them to confirm. Clicking **Open ticket** pops up a modal: *"Why do you want to contact staff?"* (required, up to 500 characters). Submitting the modal is what actually creates the ticket and relays their reason to staff.
4. Any messages the member sends between the initial DM and confirming go into a buffer, up to 20 messages, capped at 25 MB of attachments total. Once they confirm, those buffered messages get relayed into the new ticket channel. If something didn't fit in the buffer, the confirmation reply tells them to resend it.
5. The confirmation prompt expires after **1 hour**. Clicking it late shows an "expired, DM me again" message and nothing is created. A fresh DM starts the process over.
6. Whatever they typed in the reason modal shows up as a **"Reason for contact"** field on the ticket's header embed, so staff see it without having to scroll.

If a member already has an open ticket, none of the gate logic applies: DMs just relay straight into the existing channel, same as ever.

Non-members (people who've left the server, or who were never in it) get a configurable "members only" message instead of a ticket, unless the dashboard is set to allow non-members.

---

## The ticket channel

### Naming and header

Ticket channels are created in the configured category and named after the member (lowercased, sanitized to `a-z0-9-`, e.g. `#some-username`). If the category hits Discord's 50-channel cap, tickets fall back to a second configured category if one's set.

The first message in a new channel is a header embed: `Ticket #<id>`, the member's mention/name/ID, account creation and join dates, their role list (mentions, truncated with a count if there are too many to fit), and the reason field if the confirm gate captured one. Configured ping roles get mentioned right under the header. That's a notification, not an access grant (more on that below).

### Message relay

Member messages show up in the channel as green embeds, with author name and avatar, and the source message ID in the footer. Edits and deletes on the member's side sync live: an edited message gets an `[Edited]` marker and shows the former content, and a deleted one gets `[Deleted by member]`.

Staff replies show up as red embeds, both in the ticket channel and mirrored to the member's DM. A named reply shows the staff member's name and avatar, plus (if they have a colored role) that role's name in the footer. An anonymous reply shows "Anonymous" with the server icon on the member's side, while the staff member's real identity is still visible on the staff side so the team knows who answered.

Staff can edit or delete their own replies after sending; the change propagates to both the channel copy and the member's DM copy.

Internal notes (staff-only, never sent to the member) are also supported, for leaving context in the channel without pinging or relaying anything.

### Shortcut prefix

Staff can type a short prefix instead of full slash commands inside a ticket channel. The default is `!`, configurable per-server in the dashboard (1-4 punctuation characters, no `/` or backtick). So `!r <message>` replies, `!s <name>` sends a snippet, and so on. See the [Ticket Commands guide](../guides/ticket-commands.md) for the full shortcut list.

---

## Who can see a ticket channel

This trips people up: **ping roles and viewing access are not the same list.**

Roles you configure as "ping roles" in the dashboard get mentioned when a ticket opens, and they also get channel access, because the setup wires them into the channel's permission overwrites directly.

On top of that, **every staff permission tier role can see every ticket channel**, regardless of whether that role is in the ping list. Access comes from the server's staff tier system (Admin, Head Moderator, Moderator, Trial Moderator); see [Permissions](../getting-started/permissions.md) for how tiers map to roles.

Everyone else, `@everyone`, is explicitly denied `view_channel` on ticket channels.

So if someone can't see a ticket, check their staff tier and role assignment, not the ping role list. If you want a role to get pinged but not automatically see every ticket, that's not currently how it works: ping roles get both.

---

## Closing, transcripts & archive

Staff close a ticket with `/ticket close` (or the shortcut equivalent). Closing:

1. Optionally attaches a close reason (from the configured close-reason presets) and/or a summary.
2. Builds and uploads a full **transcript** of the ticket to the configured Modmail log channel, inside a thread named `ticket-<id>-<member>`.
3. Uploads any evidence attachments from the conversation into that same thread, each labeled with sender and timestamp.
4. Posts a closing embed in the log channel with opened/closed times, who closed it, the reason, the AI summary (if one was generated), and file counts. That embed carries an **archive status** field (`Archiving` to `Complete`) and, if archiving is interrupted mid-way, the bot resumes and reconciles on retry rather than duplicating uploads.
5. Deletes the live ticket channel and sends the member a configurable "ticket closed" DM.

The archive step is transactional in practice: it verifies every uploaded file actually landed on Discord's side before marking the close as durable, and it can pick up an incomplete close from where it left off if something failed partway.

### Scheduled auto-close

Inactivity close: if `inactivity_close_seconds` is set above 0 in the dashboard, a ticket schedules itself to close automatically after that many seconds of no activity. Any new relay (member message or staff reply) pushes the deadline back out, and it's cancelled entirely if the timer's set to 0.

Post-close cooldown: after a ticket closes, the member is on a cooldown (default 300 seconds) before they can open another one straight away. This stops a closed ticket being immediately reopened by an errant DM.

---

## AI catch-up summaries

Staff can run `/ticket summarize` (or the shortcut) mid-conversation to get an AI-generated recap of the ticket so far, useful for jumping into a ticket someone else has been handling. Summaries have a short cooldown per ticket (60 seconds) to stop spamming the AI backend, and only one summary request can be in flight per ticket at a time.

Whether the result is posted for the whole team or just shown privately depends on the **catch-up visibility** setting in the dashboard:

- `private` (default): the summary isn't posted into the channel.
- `shared`: the summary gets posted as a message in the ticket channel that everyone with access can see, and it's saved to the ticket history as an AI note.

Close-time summaries are separate and always attempted automatically when a ticket closes (if AI is enabled). That one always feeds into the closing embed in the log channel, independent of the catch-up visibility setting.

If the AI backend is disabled, unconfigured, or times out, ticket operations don't wait on it or fail because of it. Closing and summarizing degrade gracefully to "summary unavailable."

---

## Blocking a member

Staff can block a member from `/ticket block` (tier 1+). Once blocked:

- Any DM they send gets a configurable "you cannot open a ticket" reply instead of being relayed.
- This check happens before anything else, before the enabled check, before the confirm gate, before ticket routing, so a blocked member can't work around it.
- `/ticket unblock` reverses it.

Blocking doesn't touch anything else about the member's server access; it's scoped entirely to Modmail.

---

## Configuration

Everything above is tuned from the ticket dashboard (`/ticket_dashboard`, tier 0). It's a multi-panel view:

- Setup: primary ticket category, optional fallback category, the Modmail log channel, and ping roles.
- Behavior: enable/disable Modmail, typing indicators, the confirmation gate toggle, whether non-members can open tickets, timers (post-close cooldown, inactivity close), and the shortcut prefix.
- Close Reasons and Snippets: manage presets; see [Modmail Snippets](../guides/modmail-snippets.md) for details.
- Messages: every member-facing string (disabled/blocked/cooldown/created/closed messages, etc.) is editable here.
- AI: enable/disable AI summaries, timeout, minimum interval between requests, and catch-up summary visibility (private/shared).
- Retention: how many days closed-ticket metadata is kept before cleanup (1-29 days).
- Status: a read-only panel showing configuration state, AI health, and active/failed ticket counts.

The dashboard is staff-only and gated the same way as any other tier-0 command.
