# DiffusionGemma 26B A4B IT NVFP4 on SM121 vLLM

Optimized NVIDIA GB10 / SM121 vLLM container and benchmark report for `nvidia/diffusiongemma-26B-A4B-it-NVFP4`.

> Status: execution in progress. Final benchmark numbers are published only after native NVFP4 kernel proof, correctness checks, c1-c16 benchmark completion, and HTML report visual verification.

## What this repo publishes

- A reproducible vLLM OpenAI-compatible serving recipe for DiffusionGemma NVFP4 on SM121.
- A Docker image built/pinned from the day-0 vLLM DiffusionGemma support line.
- Native-backend evidence: no MARLIN/emulation for NVFP4 quant kernels.
- Full benchmark artifacts: concurrency c1/c2/c4/c5/c8/c16, depth sweep, dLLM block metrics, telemetry, and quality spot-checks.
- An interactive HTML report under `publication/html/index.html`.

## Model

- Model ID: `nvidia/diffusiongemma-26B-A4B-it-NVFP4`
- Base: Google DeepMind DiffusionGemma 26B A4B IT
- Quantization: NVIDIA ModelOpt NVFP4
- Architecture: discrete diffusion language model, 256-token canvases, Gemma 4 MoE backbone
- Parameters: 25.2B total / 3.8B active
- License: Apache-2.0 plus Gemma terms and prohibited-use policy

## Quick start

```bash
bash scripts/serve.sh
bash scripts/verify_native_kernels.sh
python3 scripts/quality_spotcheck.py --base-url http://127.0.0.1:30000/v1
```

Benchmark after serving:

```bash
bash scripts/bench_concurrency.sh
bash scripts/bench_depth_sweep.sh
python3 scripts/bench_dllm_metrics.py --base-url http://127.0.0.1:30000/v1
```

## Native publication rule

Do **not** publish or cite benchmark numbers as SM121-native if logs show MARLIN, emulation, unsupported quant kernels, failed correctness, missing telemetry, or harness failures. Fix and rerun.

## Credits

Google DeepMind (DiffusionGemma), NVIDIA (NVFP4 ModelOpt quantization), vLLM/Red Hat (day-0 dLLM integration), FlashInfer, NVIDIA CUTLASS, Hugging Face Hub, and r0b0tlab tooling.
