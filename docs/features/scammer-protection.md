# Scammer Protection

Two systems work together to keep scammers out.

## Auto-Ban

Listens to a designated scammer broadcast channel (cross-server scammer lists) and automatically bans reported users.

Safety features:

- Staff members with tier roles are immune and can't be auto-banned
- Rate limiting between bans prevents abuse
- Banned users get a DM with the reason before the ban
- All actions logged to the log channel

Configuration: `/config_dashboard`, Scammer Auto-Ban panel (requires `manage_guild`)

## Manual Reports

Staff can manually report and ban scammers with `/scammer_report`.

| Parameter | Description |
|-----------|-------------|
| `user` | The scammer to report and ban |
| `reason` | Why they're being reported |

What happens:

1. Formatted report posted to the configured hall of shame channel
2. Optional role ping for visibility
3. User gets a DM with the ban reason
4. User is banned

Configuration: `/config_dashboard`, Scammer Report panel (requires `manage_guild`)

Required tier: 1 (Head Moderator) or higher
