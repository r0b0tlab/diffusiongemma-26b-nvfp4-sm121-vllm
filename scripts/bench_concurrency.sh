#!/usr/bin/env bash
set -euo pipefail
BASE_URL=${BASE_URL:-http://127.0.0.1:30000}
MODEL=${MODEL:-/model}
OUTDIR=${OUTDIR:-benchmarks/results}
mkdir -p "$OUTDIR"
for C in 1 2 4 5 8 16; do
  echo "== concurrency $C =="
  vllm bench serve     --backend openai     --base-url "$BASE_URL"     --model "$MODEL"     --dataset-name random     --random-input-len 512     --random-output-len 1024     --num-prompts $((C * 4))     --max-concurrency "$C"     --save-result     --result-filename "$OUTDIR/concurrency-c${C}.json"
done
