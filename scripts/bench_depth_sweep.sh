#!/usr/bin/env bash
set -euo pipefail
BASE_URL=${BASE_URL:-http://127.0.0.1:30000}
MODEL=${MODEL:-/model}
OUTDIR=${OUTDIR:-benchmarks/results}
mkdir -p "$OUTDIR"
for D in 0 1024 4096 8192 16384 32768 65536; do
  IN=$((D + 128))
  echo "== depth $D input_len $IN =="
  vllm bench serve     --backend openai     --base-url "$BASE_URL"     --model "$MODEL"     --dataset-name random     --random-input-len "$IN"     --random-output-len 256     --num-prompts 8     --max-concurrency 1     --save-result     --result-filename "$OUTDIR/depth-d${D}.json"
done
