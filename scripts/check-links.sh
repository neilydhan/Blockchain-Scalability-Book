#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
command -v curl >/dev/null 2>&1 || { echo "error: curl is required" >&2; exit 1; }
mapfile -t urls < <(python3 - "$root" <<'PY'
from pathlib import Path
import re,sys
root=Path(sys.argv[1])
urls=set()
for p in [root/'README.md',root/'PUBLISHING.md',*sorted((root/'chapters').glob('*.md'))]:
    urls.update(u.rstrip('.,') for u in re.findall(r'https?://[^\s)>]+',p.read_text()))
print('\n'.join(sorted(urls)))
PY
)
fail=0
for url in "${urls[@]}"; do
  code=$(curl -L -I --retry 1 --connect-timeout 8 --max-time 25 -A 'Mozilla/5.0' -o /dev/null -sS -w '%{http_code}' "$url") || code=000
  case "$code" in
    2*|3*|401|403) printf 'ok   %s %s\n' "$code" "$url" ;;
    *) printf 'FAIL %s %s\n' "$code" "$url"; fail=1 ;;
  esac
done
exit "$fail"
