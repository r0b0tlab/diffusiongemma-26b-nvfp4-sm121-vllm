#!/usr/bin/env python3
"""Small CUDA/torch sanity before loading the full model.
This is not a replacement for vLLM native-kernel log proof; it catches broken CUDA/SM121 basics early.
"""
import json, torch
assert torch.cuda.is_available(), 'CUDA unavailable'
cap = torch.cuda.get_device_capability()
x = torch.randn((128, 128), device='cuda', dtype=torch.bfloat16)
w = torch.randn((128, 128), device='cuda', dtype=torch.bfloat16)
y = x @ w
assert torch.isfinite(y).all()
print(json.dumps({'cuda': torch.version.cuda, 'capability': cap, 'bf16_gemm_sum': float(y.sum().cpu())}, indent=2))
