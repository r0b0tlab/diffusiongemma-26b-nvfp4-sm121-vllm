#!/usr/bin/env bash
set -euo pipefail
BASE_URL=${BASE_URL:-http://127.0.0.1:30000}
MODEL=${MODEL:-/model}
OUTDIR=${OUTDIR:-benchmarks/results}
mkdir -p "$OUTDIR"
for D in 0 1024 4096 8192 16384 32768 65536; do
  IN=$((D + 128))
  echo "== depth $D input_len $IN =="
  TMP="/tmp/depth-d${D}.json"
  docker exec dgemma-vllm vllm bench serve \
    --backend openai-chat \
    --endpoint /v1/chat/completions \
    --base-url "$BASE_URL" \
    --model "$MODEL" \
    --dataset-name random \
    --random-input-len "$IN" \
    --random-output-len 256 \
    --num-prompts 4 \
    --max-concurrency 1 \
    --temperature 0 \
    --save-result \
    --save-detailed \
    --result-filename "$TMP"
  docker cp "dgemma-vllm:$TMP" "$OUTDIR/depth-d${D}.json"
done
