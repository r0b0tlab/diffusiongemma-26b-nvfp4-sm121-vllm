#!/usr/bin/env python3
import argparse, json, time, urllib.request
from pathlib import Path

def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--base-url', default='http://127.0.0.1:30000/v1')
    ap.add_argument('--model', default='/model')
    ap.add_argument('--out', default='benchmarks/results/dllm-metrics.jsonl')
    args=ap.parse_args()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    prompts=[
        ('short','Answer in one sentence: why is the sky blue?'),
        ('block256','Write a 300 token explanation of block diffusion language models.'),
        ('block768','Write a detailed 900 token technical note on DiffusionGemma serving metrics.'),
    ]
    with open(args.out,'w') as f:
        for name,prompt in prompts:
            t0=time.time()
            data=post(args.base_url.rstrip('/')+'/completions', {'model':args.model,'prompt':prompt,'max_tokens':1024,'temperature':0})
            dt=time.time()-t0
            text=data.get('choices',[{}])[0].get('text','')
            usage=data.get('usage',{})
            rec={'case':name,'wall_s':dt,'chars':len(text),'usage':usage,'approx_blocks':(usage.get('completion_tokens',0)+255)//256 if usage else None,'response_preview':text[:240]}
            f.write(json.dumps(rec)+'\n'); f.flush()
            print(json.dumps(rec, indent=2))
if __name__ == '__main__': main()
