#!/usr/bin/env python3
"""按分镜表里的 "gen" 字段，用 Replicate 生成/改图（例如：在样板间实景上铺一张安静的大地毯）。

用法: python3 gen_images.py projects/<项目>/storyboard.json [--only 4,5] [--dry-run]
凭证: 环境变量 REPLICATE_API_TOKEN；在 Claude 云端会话里由代理自动注入。
每个镜头的 gen 字段示例:
  "gen": {"model": "black-forest-labs/flux-kontext-pro",
          "source": "assets/dining.jpg",
          "prompt": "Cover the fragmented green marble floor with a large calm ivory wool rug ...",
          "out": "gen/04_rug.jpg"}
生成结果写到 gen.out，并把 shot.image 指向它（会回写 storyboard.json）。
"""
import json, sys, os, time, base64, argparse, mimetypes, urllib.request
from pathlib import Path

API = "https://api.replicate.com/v1"

def req(method, url, body=None):
    h = {"Content-Type": "application/json", "Prefer": "wait"}
    tok = os.environ.get("REPLICATE_API_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    r = urllib.request.Request(url, method=method, headers=h,
                               data=json.dumps(body).encode() if body else None)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return json.loads(resp.read())

def data_uri(p):
    mt = mimetypes.guess_type(str(p))[0] or "image/jpeg"
    return f"data:{mt};base64," + base64.b64encode(Path(p).read_bytes()).decode()

def run(g, base):
    inp = {"prompt": g["prompt"], "aspect_ratio": g.get("aspect_ratio", "16:9"), "output_format": "jpg"}
    if g.get("source"):
        inp["input_image"] = data_uri(base / g["source"])
    inp.update(g.get("extra", {}))
    p = req("POST", f"{API}/models/{g['model']}/predictions", {"input": inp})
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(3); p = req("GET", p["urls"]["get"])
    if p["status"] != "succeeded":
        raise RuntimeError(p.get("error"))
    url = p["output"] if isinstance(p["output"], str) else p["output"][0]
    out = base / g["out"]; out.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, out)
    return g["out"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard"); ap.add_argument("--only"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sp = Path(a.storyboard).resolve(); sb = json.loads(sp.read_text(encoding="utf-8")); base = sp.parent
    only = {int(x) for x in a.only.split(",")} if a.only else None
    for i, s in enumerate(sb["shots"], 1):
        g = s.get("gen")
        if not g or (only and i not in only):
            continue
        print(f"[{i:02d}] {s.get('node')}: {g['prompt'][:70]}…")
        if a.dry_run:
            continue
        s["image"] = run(g, base); print(f"   ✓ {s['image']}")
        sp.write_text(json.dumps(sb, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
