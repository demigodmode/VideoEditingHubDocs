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

files=("$@")
[ ${#files[@]} -eq 0 ] && files=(0*-*.json)

for f in "${files[@]}"; do
  mid=$(python3 -c "import json;print(json.load(open('$IDS')).get('$f',''))")
  if [ -n "$mid" ]; then
    code=$(curl -sS -o /dev/null -w '%{http_code}' -X PATCH \
      "$WEBHOOK_URL/messages/$mid?with_components=true" \
      -H 'Content-Type: application/json' --data-binary @"$f")
    if [ "$code" = "200" ]; then echo "edited  $f ($mid)"; continue; fi
    echo "patch $code for $f — posting a new one"
  fi
  newid=$(curl -sS -X POST "$WEBHOOK_URL?with_components=true&wait=true" \
    -H 'Content-Type: application/json' --data-binary @"$f" \
    | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])')
  python3 -c "import json;d=json.load(open('$IDS'));d['$f']='$newid';json.dump(d,open('$IDS','w'),indent=2,ensure_ascii=False)"
  echo "posted  $f ($newid)"
done
