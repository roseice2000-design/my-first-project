#!/usr/bin/env python3
"""把静帧合成为 1080p 视频：每个镜头缓慢推拉(Ken Burns) + 叠化转场 + 可选背景音乐。

用法: python3 build_video.py projects/<项目>/storyboard.json [--music bgm.mp3]
输出: projects/<项目>/build/<项目名>.mp4
依赖: ffmpeg
"""
import json, sys, subprocess, argparse
from pathlib import Path

FPS, XF = 30, 1.0  # 帧率, 叠化时长(秒)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--music")
    a = ap.parse_args()
    sb_path = Path(a.storyboard).resolve()
    sb = json.loads(sb_path.read_text(encoding="utf-8"))
    build = sb_path.parent / "build"
    frames = build / "frames"
    music = a.music or (str((sb_path.parent / sb["music"]).resolve()) if sb.get("music") else None)
    if music and not Path(music).exists():
        print(f"  ! 找不到音乐 {music}，生成无声版"); music = None

    inputs, filters, durs = [], [], []
    for i, shot in enumerate(sb["shots"]):
        dur = float(shot.get("duration", 5))
        durs.append(dur)
        n = int(dur * FPS)
        move = shot.get("move", "in")
        z = {"in": f"1+0.08*on/{n}", "out": f"1.08-0.08*on/{n}"}.get(move, "1.04")
        xexp = {"left": f"(iw-iw/zoom)*on/{n}", "right": f"(iw-iw/zoom)*(1-on/{n})"}.get(move, "iw/2-(iw/zoom/2)")
        if move in ("left", "right"):
            z = "1.06"
        if shot.get("video"):  # 可灵等生成的视频片段：直接用，不做推拉
            v = (sb_path.parent / shot["video"]).resolve()
            inputs += ["-t", str(dur), "-i", str(v)]
            filters.append(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                           f"fps={FPS},trim=0:{dur},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[v{i}]")
            continue
        inputs += ["-loop", "1", "-t", str(dur), "-i", str(frames / f"{i+1:02d}.png")]
        filters.append(f"[{i}:v]zoompan=z='{z}':x='{xexp}':y='ih/2-(ih/zoom/2)':d={n}:s=1920x1080:fps={FPS},setsar=1,format=yuv420p[v{i}]")

    last, t = "v0", durs[0]
    for i in range(1, len(durs)):
        xf = float(sb["shots"][i].get("xfade", XF)) or 0.04  # 0 = 硬接（首尾帧相同的一镜到底）
        off = t - xf
        filters.append(f"[{last}][v{i}]xfade=transition=fade:duration={xf}:offset={off:.2f}[x{i}]")
        last, t = f"x{i}", t + durs[i] - xf
    total = t
    filters.append(f"[{last}]fade=t=in:st=0:d=0.8,fade=t=out:st={total-1.2:.2f}:d=1.2[vout]")

    cmd = ["ffmpeg", "-y", "-v", "error", *inputs]
    maps = ["-map", "[vout]"]
    if music:
        cmd += ["-i", music]
        filters.append(f"[{len(durs)}:a]atrim=0:{total:.2f},afade=t=in:d=1,afade=t=out:st={total-2:.2f}:d=2[aout]")
        maps += ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
    out = build / f"{sb.get('slug', 'film')}.mp4"
    cmd += ["-filter_complex", ";".join(filters), *maps,
            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print(f"视频已生成: {out}  （约 {total:.0f} 秒）")

if __name__ == "__main__":
    main()
