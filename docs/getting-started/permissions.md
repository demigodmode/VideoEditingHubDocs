# Staff Roles & Permissions

The bot uses a tier-based permission system. Higher tiers can do everything lower tiers can.

| Tier | Role | Access |
|------|------|--------|
| 0 | Admin | Full access, all commands and dashboards |
| 1 | Head Moderator | Most commands, scammer reports |
| 2 | Moderator | Standard moderation commands |
| 3 | Trial Moderator | Basic commands only |

Users with Discord's `manage_guild` permission bypass tier checks entirely.

## How permissions are assigned

Staff roles are configured in `/config_dashboard` under the Staff Permissions panel. An admin maps Discord roles to permission tiers there.

## Checking your access

If a command tells you that you don't have permission, your role isn't mapped to a high enough tier. Ask an admin to check the staff permissions config.
