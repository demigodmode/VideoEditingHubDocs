# VJ Dashboard

`/vj_dashboard` is the configuration interface for the [Verified Jobs](../features/verified-jobs.md) system. Requires Tier 0 (Admin).

Opens an ephemeral interactive message with navigation buttons for each panel.

## Panels

### Channels

| Setting | Description |
|---------|-------------|
| Info channel | Where the submit button lives |
| Review channel | Staff review queue |
| Forum channel | Where approved jobs get published |
| Log channel | Activity logs |

### Roles

**Core:**

| Setting | Description |
|---------|-------------|
| Agency role | Auto-assigned when user selects "agency" |
| Submitter roles | Required to submit (staff are exempt) |
| Blocked roles | Users with any of these roles cannot submit jobs — enforced regardless of staff status |
| Applicant roles | Required to click Apply on a job |

**Token:**

| Setting | Description |
|---------|-------------|
| Hiring Pass role | Unlimited submissions, no tokens consumed ([details](../features/token-system.md#hiring-pass)) |
| 1 Token role | Server Shop purchase, credits 1 token |
| 5 Tokens role | Server Shop purchase, credits 5 tokens |
| 10 Tokens role | Server Shop purchase, credits 10 tokens |

See [Token System](../features/token-system.md) for how token purchases and consumption work.

### Limits & Timing

| Setting | Default | Description |
|---------|---------|-------------|
| Submission cooldown | 60s | Time between submissions |
| Daily submission limit | 1 | Max submissions per day |
| Max links | 8 | Reference URLs per submission |
| Max images | 6 | Uploaded images per submission (thumbnails) |
| Max strikes | 3 | Strikes before user is blocked ([details](../features/verified-jobs.md#strike-system)) |

### Toggles

| Toggle | Description |
|--------|-------------|
| Enabled | Master on/off switch for the whole system |
| Require monetization | Enables the token/Hiring Pass gate |
| Enforce agency only | Only agencies need tokens, individuals post free ([details](../features/token-system.md#agency-only-mode)) |

### Messages

Edit DM templates sent to users during the review process:

- Approval DM - title and description (supports `{thread_url}` variable)
- Rejection DM - title and description (supports `{reason}` variable)
- Agency rejection DM
- Hold DM
- Submission confirmation

Each template has a live preview button.

### Status

Shows current configuration at a glance: all channel/role assignments, toggle states, and whether the system is fully configured.
