#!/usr/bin/env python3
"""用可灵（国际版）把分镜里的 "kling" 字段生成视频片段——支持首尾帧，用来做“丝滑转换”。

用法: python3 kling_video.py projects/<项目>/storyboard.json [--only 3,4] [--dry-run]
凭证: Authorization: Bearer <API Key>。云端会话里由代理自动注入；本地运行设 KLING_API_KEY。
镜头字段示例:
  "kling": {"start": "assets/实景.jpg", "end": "gen/改造后.jpg",
            "prompt": "...", "duration": "5", "out": "clips/05.mp4"}
生成后把 shot.video 指向片段（回写 storyboard.json），build_video.py 会直接用视频代替静帧。
"""
import json, os, time, base64, argparse, urllib.request, urllib.error
from pathlib import Path

API = os.environ.get("KLING_API_BASE", "https://api-singapore.klingai.com")
NEG = ("warping walls, bending lines, changing window positions, changing ceiling, "
       "morphing architecture, flicker, people, text, watermark, blurry, distorted furniture")

def call(method, path, body=None):
    h = {"Content-Type": "application/json"}
    if os.environ.get("KLING_API_KEY"):
        h["Authorization"] = "Bearer " + os.environ["KLING_API_KEY"]
    r = urllib.request.Request(API + path, method=method, headers=h,
                               data=json.dumps(body).encode() if body else None)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            d = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"可灵返回 {e.code}: {e.read().decode()[:300]}")
    if d.get("code") not in (0, None):
        raise SystemExit(f"可灵错误 {d.get('code')}: {d.get('message')}")
    return d["data"]

def b64(p):  # 可灵要求纯 base64，不带 data: 前缀
    return base64.b64encode(Path(p).read_bytes()).decode()

def run(k, base):
    body = {
        "model_name": k.get("model", "kling-v2-1"),
        "mode": k.get("mode", "pro"),              # 首尾帧需要 pro 模式
        "duration": str(k.get("duration", "5")),
        "image": b64(base / k["start"]),
        "prompt": k["prompt"],
        "negative_prompt": k.get("negative", NEG),
        "cfg_scale": k.get("cfg", 0.5),
    }
    if k.get("end"):
        body["image_tail"] = b64(base / k["end"])
    task = call("POST", "/v1/videos/image2video", body)["task_id"]
    print(f"   任务 {task} 已提交，生成中…")
    while True:
        time.sleep(10)
        d = call("GET", f"/v1/videos/image2video/{task}")
        st = d.get("task_status")
        if st == "succeed":
            url = d["task_result"]["videos"][0]["url"]; break
        if st == "failed":
            raise SystemExit(f"生成失败: {d.get('task_status_msg')}")
    out = base / k["out"]; out.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, out)
    return k["out"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard"); ap.add_argument("--only"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sp = Path(a.storyboard).resolve(); sb = json.loads(sp.read_text(encoding="utf-8")); base = sp.parent
    only = {int(x) for x in a.only.split(",")} if a.only else None
    for i, s in enumerate(sb["shots"], 1):
        k = s.get("kling")
        if not k or (only and i not in only):
            continue
        print(f"[{i:02d}] {s.get('node')}  {k['start']} → {k.get('end', '(无尾帧)')}")
        if a.dry_run:
            continue
        s["video"] = run(k, base); print(f"   ✓ {s['video']}")
        sp.write_text(json.dumps(sb, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
