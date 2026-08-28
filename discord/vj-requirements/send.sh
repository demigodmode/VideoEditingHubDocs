#!/usr/bin/env bash
# Publish the VJ requirements posts to Discord via a channel webhook.
#
#   WEBHOOK_URL=https://discord.com/api/webhooks/xxx/yyy ./send.sh        # all
#   WEBHOOK_URL=... ./send.sh 02-rates.json                               # one
#
# First run for a file POSTs a new message and records its ID in ids.json.
# Later runs PATCH that same message in place (edit, no re-post). If the saved
# message was deleted, it falls back to posting a fresh one.
#
# The webhook URL is a secret — never commit it. Locally, pass it as shown
# above; in CI it comes from the WEBHOOK_VJ_REQUIREMENTS GitHub secret.
set -euo pipefail
: "${WEBHOOK_URL:?set WEBHOOK_URL (or run the GitHub Action)}"
cd "$(dirname "$0")"

python3 build.py >/dev/null
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
