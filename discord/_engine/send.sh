#!/usr/bin/env bash
# Publish a channel's docs-as-code posts to Discord via its webhook.
#
#   WEBHOOK_URL=https://discord.com/api/webhooks/xxx/yyy \
#     _engine/send.sh discord/vj-requirements                 # all messages
#   WEBHOOK_URL=... _engine/send.sh discord/vj-requirements 02-rates.json   # one
#
# First run for a file POSTs a new message and records its ID in the channel's
# ids.json. Later runs PATCH that same message in place. If the saved message was
# deleted, it falls back to posting a fresh one.
#
# The webhook URL is a secret — never commit it. In CI it comes from the channel's
# WEBHOOK_<CHANNEL> GitHub secret (see the workflow).
set -euo pipefail
: "${WEBHOOK_URL:?set WEBHOOK_URL (or run the GitHub Action)}"

ENGINE_DIR="$(cd "$(dirname "$0")" && pwd)"
CHANNEL_DIR="${1:?usage: send.sh <channel-dir> [file.json ...]}"
shift || true
CHANNEL_DIR="$(cd "$CHANNEL_DIR" && pwd)"

python3 "$ENGINE_DIR/build.py" "$CHANNEL_DIR" >/dev/null
cd "$CHANNEL_DIR"

IDS=ids.json
[ -f "$IDS" ] || echo '{}' > "$IDS"

shopt -s nullglob
files=("$@")
[ ${#files[@]} -eq 0 ] && files=(0*-*.json)

if [ ${#files[@]} -eq 0 ]; then
  echo "nothing to publish in $CHANNEL_DIR"
  exit 0
fi

# POST new / PATCH existing. $1 = ids.json key (the real filename); $2 = payload file
# to send (same as $1 normally, or a jump-resolved temp copy).
publish_file() {
  local f="$1" payload="$2" mid resp code newid
  mid=$(python3 -c "import json;print(json.load(open('$IDS')).get('$f',''))")
  if [ -n "$mid" ]; then
    resp=$(mktemp)
    code=$(curl -sS -o "$resp" -w '%{http_code}' -X PATCH \
      "$WEBHOOK_URL/messages/$mid?with_components=true" \
      -H 'Content-Type: application/json' --data-binary @"$payload")
    if [ "$code" = "200" ]; then echo "edited  $f ($mid)"; rm -f "$resp"; return; fi
    if [ "$code" = "404" ]; then
      echo "patch 404 for $f — message gone, posting a new one"; rm -f "$resp"
    else
      echo "patch failed ($code) for $f: $(cat "$resp")" >&2; rm -f "$resp"; exit 1
    fi
  fi
  newid=$(curl -sS -X POST "$WEBHOOK_URL?with_components=true&wait=true" \
    -H 'Content-Type: application/json' --data-binary @"$payload" \
    | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])')
  python3 -c "import json;d=json.load(open('$IDS'));d['$f']='$newid';json.dump(d,open('$IDS','w'),indent=2,ensure_ascii=False)"
  echo "posted  $f ($newid)"
}

# Glossary-style files with [[JUMP:slug]] tokens must go LAST — their links point at
# the other messages' IDs, which only exist once those are posted.
plain=(); jump=()
for f in "${files[@]}"; do
  if grep -qF '[[JUMP:' "$f"; then jump+=("$f"); else plain+=("$f"); fi
done

for f in "${plain[@]}"; do publish_file "$f" "$f"; done

if [ ${#jump[@]} -gt 0 ]; then
  meta=$(curl -sS "$WEBHOOK_URL")
  guild=$(echo "$meta"   | python3 -c 'import json,sys;print(json.load(sys.stdin).get("guild_id") or "")')
  channel=$(echo "$meta" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("channel_id") or "")')
  [ -n "$guild" ] && [ -n "$channel" ] || { echo "webhook gave no guild_id/channel_id — can't build jump links" >&2; exit 1; }
  for f in "${jump[@]}"; do
    resolved=$(mktemp)
    python3 "$ENGINE_DIR/resolve_jumps.py" "$CHANNEL_DIR" "$f" "$guild" "$channel" > "$resolved"
    publish_file "$f" "$resolved"
    rm -f "$resolved"
  done
fi
