# Ticket commands

Staff reference for the `/ticket` slash commands used inside Modmail.

## Who can use these

Every `/ticket` command is staff-only, gated by the tiered permission system (see [Permissions](../getting-started/permissions.md) for who's in which tier). With two exceptions (`contact` and `unblock`), every command also requires you to be sitting in an active ticket channel. Run one anywhere else and it just tells you the action is unavailable.

Which tier each command needs. Higher tiers can do everything the lower ones can, so Admins can run anything.

| Tier | Who | Commands |
|------|-----|----------|
| 3 | Trial Moderator and up (all staff) | `info`, `history`, `summarize` |
| 2 | Moderator and up | `reply`, `anonymous_reply`, `snippet`, `edit`, `close`, `schedule_close`, `cancel_close` |
| 1 | Head Moderator and up | `contact`, `block`, `unblock`, `delete` |

The ticket dashboard itself (`/ticket_dashboard`) is Admin-only (tier 0).

## The `!` shortcuts

Most of these have a text shortcut too. Type `!r`, `!close`, etc. directly in the ticket channel instead of opening the slash command menu. The prefix defaults to `!` but is configurable per-server from the dashboard, so if someone's changed it, ask around before assuming. Unlike the slash commands, every shortcut, including `!contact`, only fires inside an active ticket channel, since it's implemented as a message listener with nowhere else to hook in.

Not every command has a shortcut. `schedule_close`, `cancel_close`, and `summarize` are slash-only.

## Replying

### `/ticket reply`
Sends a message to the member with your name attached, so they see who they're talking to.

- `text`: the message
- `attachment`: optional file

Shortcut: `!r <text>`

### `/ticket anonymous_reply`
Same as `reply`, but the member sees it as coming from the server, not from you by name.

- `text`: the message
- `attachment`: optional file

Shortcut: `!ar <text>`

### `/ticket snippet`
Sends one of the pre-written canned responses instead of typing it out. `name` autocompletes as you type. Snippets themselves are configured from the dashboard; see [Modmail Snippets](modmail-snippets.md) for the current list and what each one is for.

- `name`: snippet to send (autocompletes)
- `attachment`: optional file

Shortcut: `!s <name>`

### `/ticket edit`
Edits one of your own sent replies. Leave `message_id` off and it edits your last reply.

- `text`: new content
- `message_id`: optional, ID of the reply to edit

Shortcut: `!edit [message_id] <text>`. If you don't pass an ID it edits your last reply.

### `/ticket delete`
Deletes one of your own sent replies. Same "last one if you don't specify" behavior as edit.

- `message_id`: optional, ID of the reply to delete

Shortcut: `!delete [message_id]`

## Closing

### `/ticket close`
Closes the ticket right now. `reason` autocompletes from the close-reason presets configured in the dashboard (same place as snippets; see [Modmail Snippets](modmail-snippets.md)).

- `reason`: optional, autocompletes

Shortcut: `!close [reason]`

### `/ticket schedule_close`
Closes the ticket automatically after a delay instead of right now, useful for "give it a day in case they come back" situations. Accepts a plain-English duration like `2h`, `30 minutes`, `3d`, or `1w`, capped at 29 days. It confirms back the exact close time converted to your local timezone so you can double check it landed where you meant.

- `duration`: required, e.g. `2h`, `30 minutes`, `3d`, `1w`
- `reason`: optional, autocompletes from the same presets as `close`

No shortcut for this one.

### `/ticket cancel_close`
Cancels a close that was previously scheduled with `schedule_close`. No parameters, no shortcut.

## Info & summaries

### `/ticket summarize`
Posts an AI-generated catch-up summary of the ticket so far, handy if you're picking up a ticket someone else was handling. No parameters, no shortcut.

### `/ticket info`
Shows the ticket number, the member, and when it was opened.

Shortcut: `!info`

### `/ticket history`
Lists the member's recent tickets and their states (open, closed, etc.), so you can see if this is a repeat visitor.

Shortcut: `!logs`

## Blocking

### `/ticket block`
Blocks a member from opening new tickets. Give it a member, a member ID, or nothing at all.

- `member`: optional, pick from the member list (only shows people currently in the server)
- `member_id`: optional, paste a numeric ID by hand; use this for someone who already left, since the picker can't see them
- `reason`: optional note stored with the block

If you don't pass `member` or `member_id`, it defaults to whoever's ticket you're currently in.

Shortcut: `!block [reason]`. Always targets the current ticket's member; there's no way to pass a member/ID through the shortcut.

### `/ticket unblock`
Removes a block. Same `member` / `member_id` rules as `block`: picker for current members, ID field for people who've left, defaults to the current ticket's member if you pass neither.

Shortcut: `!unblock`. Again, always targets the current ticket's member.

## Reaching out first

### `/ticket contact`
Opens a ticket to proactively reach a member who hasn't messaged in. This is the one command (along with `unblock`, sort of) that doesn't require you to already be in a ticket, since you use it precisely because there isn't one yet.

- `member`: required, who to contact

Shortcut: `!contact <member ID or mention>`. Note the shortcut only fires inside an existing ticket channel (it's a message-listener thing), so it's not actually useful for opening the first ticket with someone. Use the slash command for that.

---

For the bigger picture on how Modmail routes and threads conversations, see the [Modmail overview](../features/modmail.md).
