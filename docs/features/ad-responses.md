# Ad Responses

Sends templated responses automatically when new threads are created in ad forum channels. The response varies based on the creator's role (Verified vs Unverified) and which forum the thread is in.

## How it works

When someone posts in a watched forum channel, the bot checks their roles and sends the matching response template. Helps guide new posters with relevant info about the channel's rules and expectations.

## Configuration

Managed in `/config_dashboard` under the Ad Responses panel (requires `manage_guild`).

The config is rule-based. Each rule specifies:

- Which forum channel it applies to
- Which role triggers it (Verified, Unverified, or any)
- The response message template
