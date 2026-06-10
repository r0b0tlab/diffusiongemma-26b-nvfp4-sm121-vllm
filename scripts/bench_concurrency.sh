#!/usr/bin/env bash
set -euo pipefail
BASE_URL=${BASE_URL:-http://127.0.0.1:30000}
MODEL=${MODEL:-/model}
OUTDIR=${OUTDIR:-benchmarks/results}
mkdir -p "$OUTDIR"
for C in 1 2 4 5 8 16; do
  echo "== concurrency $C =="
  TMP="/tmp/concurrency-c${C}.json"
  docker exec dgemma-vllm vllm bench serve \
    --backend openai-chat \
    --endpoint /v1/chat/completions \
    --base-url "$BASE_URL" \
    --model "$MODEL" \
    --dataset-name random \
    --random-input-len 512 \
    --random-output-len 1024 \
    --num-prompts $((C * 4)) \
    --max-concurrency "$C" \
    --temperature 0 \
    --save-result \
    --save-detailed \
    --result-filename "$TMP"
  docker cp "dgemma-vllm:$TMP" "$OUTDIR/concurrency-c${C}.json"
done
