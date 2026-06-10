#!/usr/bin/env python3
import argparse, json, re, time, urllib.request
from pathlib import Path

def post(url, payload):
    req=urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=600) as r: return json.loads(r.read())

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--base-url',default='http://127.0.0.1:30000/v1'); ap.add_argument('--model',default='/model'); ap.add_argument('--out',default='benchmarks/traces/quality-spotcheck.jsonl'); args=ap.parse_args()
    cases=[('capital','The capital of France is','Paris'),('math','Q: If there are 3 cars and each has 4 wheels, how many wheels? A:','12'),('boundary','Write exactly five bullet points about NVFP4 inference.','NVFP4')]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    passed=0
    with open(args.out,'w') as f:
        for name,prompt,expect in cases:
            t0=time.time(); data=post(args.base_url.rstrip()+'/completions', {'model':args.model,'prompt':prompt,'max_tokens':256,'temperature':0}); dt=time.time()-t0
            text=data.get('choices',[{}])[0].get('text','')
            ok=expect.lower() in text.lower()
            passed += ok
            rec={'case':name,'ok':bool(ok),'expect':expect,'wall_s':dt,'prompt':prompt,'response':text,'usage':data.get('usage',{})}
            f.write(json.dumps(rec)+'\n'); print(json.dumps({k:rec[k] for k in ['case','ok','wall_s','usage']}, indent=2))
    print(json.dumps({'passed':passed,'total':len(cases)}, indent=2))
    if passed < len(cases): raise SystemExit(1)
if __name__ == '__main__': main()
