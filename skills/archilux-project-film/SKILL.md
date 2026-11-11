---
name: "archilux-project-film"
description: "Archilux Living 私宅项目：把一个新项目的资料（沟通纪要、户型图、开发商实景/视频、客户需求）变成按节点组织的分镜图，再合成一支给客户看的 1 分钟左右短片。新项目要出“项目短片 / 方案视频 / 分镜图 / 方向示意图”时使用。"
---

# Archilux Living｜项目短片 SOP

范本：北京懋源·云纪别墅（`projects/beijing-yunji/`，2026-11，11 个镜头，约 55 秒）。

## 零、红线（与报价书 skill 一致）

1. **客户隐私**：姓名、家庭、对话内容不进分镜文字。资料文件夹 `assets/`、`build/` 不进 git。
2. **图片标注**：开发商实景＝“开发商样板间”；AI 改图＝“方向示意｜AI 生成，非最终方案”；参考图＝“风格参考｜非本项目设计”。别的客户家的照片永远不用。
3. **截开发商视频**时要裁掉对方字幕和 Logo。
4. 成片先给 Katie 看，确认后再发客户。

## 一、收资料（缺了就问 Katie，不要猜）

在 `projects/<城市-楼盘>/` 下建项目，放进 `assets/`：

| 资料 | 用途 | 放哪里 |
|---|---|---|
| 首次沟通纪要 PDF / 逐字稿 | 节点文字的来源 | `assets/brief.pdf` |
| 户型图（每层）| “五层空间”总览、痛点所在层 | `assets/plans/1F.jpg …` |
| 开发商实景照 / 宣传视频 | 镜头底图、AI 改图的原图 | `assets/*.jpg`，视频截帧 |
| 外立面照 | 封面 | `assets/exterior.jpg` |
| 背景音乐（有版权的）| 可选 | `assets/bgm.mp3` |

扫描版 PDF 户型图：`pdftoppm -r 150 -jpeg 图纸.pdf assets/plans/pg`，再按楼层改名。
视频截帧：`ffmpeg -ss 秒数 -i 视频.mp4 -frames:v 1 -vf "crop=iw:ih*0.76:0:0" assets/xxx.jpg`（裁掉底部字幕）。

## 二、节点（每个项目都按这个顺序，对应纪要结构）

1. **封面** — 城市＋楼盘＋A Home, Begun with Care（外立面）
2. **写在前面** — 先恭喜，尊重原设计（庭院/亮点）
3. **我听见的** — 客户要的家，一两句
4. **空间总览** — 每层户型图拼一张
5. **痛点** — 每个痛点：所在层平面 → 现状照片（一痛点一镜头）
6. **方向** — 每个方向：AI 改图示意（同角度，只改那一处）
7. **我们这样走** — 四步与交付物
8. **结语** — 一句愿景＋署名

## 三、流程（一条命令一步）

```bash
S=skills/archilux-project-film/scripts; P=projects/<项目>
python3 $S/render_frames.py $P/storyboard.json     # ① 出静帧，先给 Katie 看
python3 $S/gen_images.py $P/storyboard.json        # ② 跑 AI 改图（gen 字段），回写 image
python3 $S/render_frames.py $P/storyboard.json     # ③ 用新图重出静帧
python3 $S/kling_video.py $P/storyboard.json       # ④ 可灵首尾帧转场片段（kling 字段，可选）
python3 $S/build_video.py $P/storyboard.json [--music bgm.mp3]   # ⑤ 合成 1080p 视频
```

- 先复制 `projects/beijing-yunji/storyboard.json` 改，字段见 `templates/storyboard.schema.md`。
- 每次只改 storyboard.json，然后重跑 ①④；不手改图片。
- AI 改图用 Replicate（`black-forest-labs/flux-kontext-pro`，以实景为原图做局部改动）。提示词要写“Keep everything else exactly the same”，只改一处。先 `--dry-run` 看提示词，再 `--only 5` 单张跑。
- 静帧 3840×2160，视频 1920×1080 / 30fps，镜头 4–8 秒，叠化 1 秒，总长控制在 45–75 秒。

## 三之二、可灵（国际版）

- 接口 `api-singapore.klingai.com`，`Authorization: Bearer <API Key>`；云端会话由代理注入密钥，本地设 `KLING_API_KEY`。
- 丝滑转场做法见 `templates/丝滑转场.md`：首帧＝实景，尾帧＝改造图；空间串联时上一段尾帧＝下一段首帧，`xfade: 0` 硬接。
- App 送的免费额度不一定能用于 API，先在开发者后台确认资源包。

## 四、交付

- `build/frames/*.png`：分镜静帧（也可直接放进报价书 / 方案册）
- `build/<slug>.mp4`：成片
- 给 Katie 时附一句：哪些镜头是 AI 示意、哪些是开发商实景。
