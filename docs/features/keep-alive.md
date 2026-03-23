# Keep Alive

Prevents forum threads from being auto-archived by Discord. Runs hourly and unarchives any non-locked threads in watched forum channels.

## Why this exists

Discord automatically archives inactive forum threads. For channels where you want threads to stay open longer, Keep Alive overrides that.

## Configuration

Managed in `/config_dashboard` under the Keep Alive panel (requires `manage_guild`).

Add or remove forum channels from the watch list. The bot checks every hour and unarchives anything Discord archived.

!!! note
    Locked threads are left alone. If a thread was intentionally locked, Keep Alive won't touch it.
