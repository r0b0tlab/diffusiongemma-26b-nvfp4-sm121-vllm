#!/usr/bin/env bash
set -euo pipefail
OUT=${1:-evidence/telemetry/telemetry-$(date +%Y%m%dT%H%M%S).csv}
mkdir -p "$(dirname "$OUT")"
echo 'timestamp,temp_c,power_w,util_pct,raw' > "$OUT"
while true; do
  ts=$(date -Is)
  line=$(nvidia-smi --query-gpu=temperature.gpu,power.draw,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1 || true)
  echo "$ts,$line,"$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)"" >> "$OUT"
  sleep 1
done
