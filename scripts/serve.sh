#!/usr/bin/env bash
set -euo pipefail
IMAGE=${IMAGE:-vllm/vllm-openai:gemma4}
MODEL_DIR=${MODEL_DIR:-/home/r0b0tdgx/models/llm/nvfp4/nvidia/diffusiongemma-26B-A4B-it-NVFP4}
PORT=${PORT:-30000}
MAX_MODEL_LEN=${MAX_MODEL_LEN:-65536}
MAX_NUM_SEQS=${MAX_NUM_SEQS:-16}
GPU_UTIL=${GPU_UTIL:-0.90}
NAME=${NAME:-dgemma-vllm}

docker rm -f "$NAME" >/dev/null 2>&1 || true

docker run -d --name "$NAME" --gpus all --ipc=host --network=host   -v "$MODEL_DIR:/model:ro"   -e VLLM_USE_V2_MODEL_RUNNER=1   "$IMAGE"   vllm serve /model     --host 0.0.0.0 --port "$PORT"     --trust-remote-code     --quantization modelopt     --gpu-memory-utilization "$GPU_UTIL"     --max-model-len "$MAX_MODEL_LEN"     --max-num-seqs "$MAX_NUM_SEQS"     --attention-backend TRITON_ATTN     --enable-auto-tool-choice     --tool-call-parser gemma4     --reasoning-parser gemma4     --override-generation-config '{"max_new_tokens": null}'     --default-chat-template-kwargs '{"enable_thinking":true}'

echo "Started $NAME. Follow logs: docker logs -f $NAME"
