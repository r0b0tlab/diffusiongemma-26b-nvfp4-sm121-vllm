#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, time, urllib.request
from pathlib import Path


def stream_chat(base_url: str, model: str, prompt: str, max_tokens: int):
    payload = {"model": model, "messages": [{"role":"user","content":prompt}], "max_tokens": max_tokens, "temperature": 0, "stream": True}
    req = urllib.request.Request(base_url.rstrip('/') + "/chat/completions", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"})
    t0 = time.perf_counter(); chunks=[]; first=None; last=None; chars=0
    with urllib.request.urlopen(req, timeout=900) as r:
        for raw in r:
            line = raw.decode('utf-8', 'replace').strip()
            if not line or not line.startswith('data: '):
                continue
            data = line[6:]
            if data == '[DONE]':
                last = time.perf_counter(); break
            now = time.perf_counter()
            if first is None: first = now
            try:
                obj = json.loads(data)
                delta = obj.get('choices',[{}])[0].get('delta',{})
                txt = delta.get('content') or ''
                chars += len(txt)
            except Exception:
                txt = ''
            chunks.append({"t_rel_s": now-t0, "chars": len(txt)})
    last = last or time.perf_counter()
    gaps = [chunks[i]['t_rel_s'] - chunks[i-1]['t_rel_s'] for i in range(1, len(chunks))]
    return {
        "prompt_preview": prompt[:120],
        "max_tokens": max_tokens,
        "wall_s": last-t0,
        "ttft_s": (first-t0) if first else None,
        "stream_chunks": len(chunks),
        "stream_chars": chars,
        "avg_inter_chunk_s": (sum(gaps)/len(gaps)) if gaps else None,
        "max_inter_chunk_s": max(gaps) if gaps else None,
        "chunk_timeline_head": chunks[:30],
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--base-url', default='http://127.0.0.1:30000/v1')
    ap.add_argument('--model', default='/model')
    ap.add_argument('--outdir', default='benchmarks/results')
    args=ap.parse_args()
    prompts=[
        "Write a 12-item checklist for publishing an optimized vLLM NVFP4 container. Be specific.",
        "Explain block diffusion inference in practical serving terms. Include latency and throughput implications.",
        "Give a compact benchmark report template for SM121 vLLM containers.",
    ]
    rows=[]
    for i,p in enumerate(prompts):
        rec=stream_chat(args.base_url,args.model,p,512); rec['case']=i; print(json.dumps(rec)); rows.append(rec)
    out=Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    (out/'dllm-stream-metrics.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
if __name__=='__main__': main()
