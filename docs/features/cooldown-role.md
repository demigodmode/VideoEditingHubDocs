# Cooldown Role

Assigns a cooldown role to new members when they join, then removes it after 60 days. Helps distinguish new members from established ones.

## How it works

1. Member joins the server
2. Bot assigns the configured cooldown role immediately
3. After 60 days, bot removes the role

## Crash recovery

The bot tracks its own uptime with a heartbeat. If it detects it was offline for more than 10 minutes on startup, it automatically backfills by assigning cooldown roles to anyone who joined while the bot was down.

## Manual backfill

If you need to manually backfill a time window:

```
/backfill_cooldown start:2h
```

This backfills members who joined in the last 2 hours. You can also specify an end:

```
/backfill_cooldown start:2h end:30m
```

Backfills members who joined between 2 hours ago and 30 minutes ago.

Supports `d` (days), `h` (hours), `m` (minutes), `s` (seconds).
