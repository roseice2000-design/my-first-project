# storyboard.json 字段

```json
{
  "slug": "城市-楼盘-v1",            // 输出文件名
  "project": "北京懋源·云纪别墅",
  "style": {"paper": [244,239,230], "ink": [60,48,40], "accent": [139,26,26]},
  "music": "assets/bgm.mp3",         // 可选
  "shots": [
    {
      "node": "05 方向·地毯",          // 节点名，只给自己看
      "layout": "full",               // full 满版图+底部字 | split 左图右字 | card 纯文字卡 | plan 图纸完整显示
      "image": "assets/xxx.jpg",      // 相对 storyboard.json
      "duration": 6,                  // 秒
      "move": "in",                   // in 推近 | out 拉远 | left / right 平移
      "caption": "方向示意｜AI 生成，非最终方案",   // 右下角小字标注
      "text": [{"kind": "eyebrow|title|subtitle|body|caption", "text": "…"}],
      "gen": {"model": "black-forest-labs/flux-kontext-pro", "source": "assets/原图.jpg",
              "prompt": "Keep everything else exactly the same. …", "out": "gen/05.jpg"}
    }
  ]
}
```
