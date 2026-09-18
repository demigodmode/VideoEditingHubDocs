# Editing Resources previews

Five static Components V2 guides, maintained here in the docs repository:
DaVinci Resolve, Premiere Pro, After Effects, Scene Packs, and General Resources. Each opens with
an index with consistently styled link buttons to complete sections. General
Resources holds shared asset collections, audio tools, and file-preparation help outside any one app. The five guides contain 27 cards, including a dedicated CineStudy practice-footage section.
They use the existing docs container builder and need no running bot callbacks.

## Build and verify

From the repository root:

```sh
python3 discord/editing-resources/preview.py
python3 -m unittest discover -s discord/editing-resources/tests -v
```

The default command only builds and validates in memory. It checks text and
component limits after expanding navigation links, so long jump URLs count
toward the text budget. Edit each guide's `content.py` to update its cards. `META.navigation` defines
index button labels and destinations: a section slug targets the current guide;
`@general` or `@scene-packs` targets another guide. Use this publisher's build
command to include navigation; the generic engine alone does not add it.

## Publish the authorized preview

The publisher is restricted to VEH's test forum `1480680276446154983`.
It cannot publish to the public Editing Resources forum. Use a secure executor
with `BOT_TOKEN` already in its environment, then run:

```sh
python3 discord/editing-resources/preview.py --publish-preview \
  --state /persistent/private/path/resources-preview-state.json
```

Use the **same state file on every run**. It records webhook, thread, and
message IDs, never credentials. A dedicated preview webhook is created or
reused; subsequent runs update the recorded messages. Removing a card from
source does not delete the old message automatically. Renaming a slug creates
a new message; use stable slugs while iterating.

Every existing thread and message is checked against the preview forum before
changes. The initial index briefly says that the guide is being prepared;
its final navigation is applied once all guide threads and section IDs exist. Rate-limited
requests use bounded retries. Other uncertain POST failures leave a `pending`
marker and stop, preventing automatic duplicate creation on rerun.

If a run stops with `pending`, inspect the indicated operation in the test
forum. If a message was created, record its actual IDs in the appropriate
`guides` entry; if a webhook was created, record its ID. Confirm the destination
and ownership before clearing `pending`. Do not delete the journal or blindly
clear the marker to force a retry. An interrupted PATCH is safe to rerun.

The public migration is a separate step after preview approval. Preserve the
existing public thread/message URLs where possible and the unrelated member
message in the Premiere thread. Do not use the generic `send.sh` with these
preview IDs or treat a preview approval as a release command.

## Public publication

The approved guides were published on 2026-09-18 and reposted with consistent **Video Editing Hub** sender branding and the VEH logo after user approval. `public.py` is restricted to
Editing Resources `1284644414173483040` and its original webhook
`1284707991332847687`. The active public journal now tracks the five replacement threads. The five original threads were deleted after user approval. Inspection confirmed that the supposed member reply was a type-4 Discord title-change event; no member discussion was present. Snapshots and the deletion journal remain on the host. The publisher rejects missing branding or a missing journal to prevent accidental recreation of the old migration.

For authorized future public updates, use the existing persistent journal:

```sh
python3 discord/editing-resources/public.py --publish-public \
  --state /app/data/editing-resources-public/state.json
```

Without `--publish-public`, it validates locally only. Keep public and preview
journals separate. The production snapshot is retained at
`/app/data/editing-resources-public/before.json`. Converting a classic message
to V2 cannot be reversed to embeds on the same message. Restore content as V2
if needed. Pending POST operations require reconciliation before retrying.
The ignored `local_docs/editing-resources/public-state.json` mirrors the live
journal; `verify-public.py` checks rendered cards, ownership, navigation,
sender branding and deletion of the superseded threads.

## Audit records

The working inventory, original message snapshot, per-source audit, design,
and preview IDs live in ignored `local_docs/editing-resources/`. Restricted
HTTP responses are recorded as unverified, not proof of a dead resource.
Editorial changes correct misleading labels and obsolete entries; they do not
introduce new server policy or promise compatibility/licensing for every item.
