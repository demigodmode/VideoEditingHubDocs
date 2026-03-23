# Token System

When monetization is enabled, users need job tokens or a Hiring Pass subscription to submit jobs. This page covers how the token economy works. For how it fits into the broader submission flow, see [Verified Jobs](verified-jobs.md#submission-flow).

## How tokens work

1. User buys a token package from Discord's Server Shop (1, 5, or 10 tokens)
2. Discord assigns the corresponding role
3. Bot detects the role change, credits tokens to the user's database balance, sends a confirmation DM
4. 1 token consumed per approved job, at approval time, not when submitting

Tokens are tracked in the database, not by role presence. The role is just the purchase trigger.

## Hiring Pass

The Hiring Pass is a subscription role that gives unlimited submissions with no token cost. It always takes priority. If a user has both a Hiring Pass and tokens, the pass gets used and tokens aren't touched.

## Agency-only mode

When this toggle is enabled:

- Agencies go through the normal monetization gate (need tokens or Hiring Pass)
- Individuals post for free, no tokens required

This lets you monetize agency job postings while keeping it free for individual hirers.

## Checking your balance

Any user can run:

```
/vj_tokens
```

Shows available tokens, total purchased, and total consumed. If you have a Hiring Pass, it tells you that instead.

## Configuration

Token roles are mapped in `/vj_dashboard` under [Roles](../dashboards/vj-dashboard.md#roles), then the Token sub-panel. The monetization toggle and agency-only enforcement are in the [Toggles](../dashboards/vj-dashboard.md#toggles) panel.
