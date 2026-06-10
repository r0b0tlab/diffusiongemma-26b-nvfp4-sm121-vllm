#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, time, urllib.request
from pathlib import Path

# 64000 stays below --max-model-len 65536 after chat-template overhead.
DEPTHS = [0, 1024, 4096, 8192, 16384, 32768, 64000]

def post(url, payload, timeout=900):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"})
    t = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    return time.perf_counter() - t, data

def filler_tokens(n: int) -> str:
    if n <= 0:
        return ""
    # Cheap deterministic token-ish filler. Actual tokenizer count is measured by vLLM usage.
    return (" context" * n)[: n * 8]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:30000/v1")
    ap.add_argument("--model", default="/model")
    ap.add_argument("--outdir", default="benchmarks/results")
    ap.add_argument("--max-output-tokens", type=int, default=128)
    args = ap.parse_args()
    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    rows = []
    for depth in DEPTHS:
        content = (
            "You are benchmarking long-context serving. Read the filler and answer only 'ok'.\n"
            + filler_tokens(depth)
            + "\nQuestion: Reply with ok."
        )
        payload = {"model": args.model, "messages": [{"role":"user", "content": content}], "max_tokens": args.max_output_tokens, "temperature": 0}
        err = None; data = None
        try:
            wall, data = post(args.base_url.rstrip('/') + "/chat/completions", payload)
        except Exception as e:
            wall = None; err = repr(e)
        usage = (data or {}).get("usage") or {}
        text = ""
        if data:
            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        row = {"depth_requested": depth, "ok": err is None, "wall_s": wall, "error": err, "prompt_tokens": usage.get("prompt_tokens",0), "completion_tokens": usage.get("completion_tokens",0), "text_preview": text[:200]}
        print(json.dumps(row))
        rows.append(row)
    (out / "chat-depth-sweep.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
