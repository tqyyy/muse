# CueShot Review Room Starter — Demo：审片 MOSEN 6 秒片头

> 演示说明：审片对象是 Mason 自己的成片 `mosen-intro-1101.mp4`（1280×720、30fps、6.0 秒，
> 无音频流，ffprobe 只检出 1 条 h264 视频流）。
> 审片方法：ffmpeg 以 1fps 抽 6 帧（frame_01–06，对应 0–5 秒），逐帧目视检查；
> 证据拼图见 `mosen-intro-6frames.jpg`，最清晰关键帧见 `mosen-intro-keyframe-2s.jpg`（2.0 秒，全文案入画）。
> 严格按 `cueshot-review-room-starter/SKILL.md` v0.1.0 的 Starter 工作流与输出格式产出；
> 另按本地完整版 `local-ai-director-video-review` 的规则：只写可见证据，不反推未给出的镜头参数。
> 零付费：本文件为纯文字审片，未调用任何生视频 / 视觉模型 API，未花积分。
> 审片目标：发布前质检（作 MOSEN 片头用），默认按“片头是否可用”判断。

## Decision

**Post-fix（小修后可用）**

- 片头整体可用：构图、字标、节奏都成立，无需重生成。
- 必须修的两处都是低成本后期调整（见 Issues 与 Repair prompt），不涉及重做画面。

## Visible evidence

- **0.0s（F01）：** 近乎全黑；液态金属 blob 在画面右侧中央，约占画面宽度 55%；字标只剩淡淡的 ghost（pill 与 MOSEN 隐约可见）；左上有点状尘埃。
- **1.0s（F02）：** pill“● AI 影像工作室”与大字 MOSEN 入画；英文 tagline 与中文行尚未出现；blob 轻微变大。
- **2.0s（F03）：** 全文案到齐——pill、MOSEN、斜体 `one person, one forest.`、细线、“一人之森 · AI 驱动”（最后一行仍偏暗）。
- **3.0–5.0s（F04–F06）：** 全文案 hold 住，最后一行亮度提到正常；blob 继续极缓慢推近后停住；画面布局三秒无变化。
- **全程：** 只有一次运动——海报式慢推（代码渲染的静态海报 + 推近，非实拍视频）；无人物、无对话、无音频；文字拼写全部正确（MOSEN / one person, one forest. / AI 影像工作室 / 一人之森 · AI 驱动）。

### 五模块检查

- **Character / identity：** 不适用——片头无人物，无身份连续性可判。
- **Motion / physics：** 运动只有慢推，速度均匀、无跳变、无拖影；但运动量极小，严格说是“会动的海报”而非视频镜头（见 Issues）。
- **Scene / continuity：** 连续性完好——blob 位置、字标位置、光源方向 6 秒无跳变；三秒 hold 帧之间无闪烁。
- **Cinematography / readability：** 整体可读；唯一可读性问题是 MOSEN 的字母 N 压在 blob 的亮边上（见 Issues）。
- **AI artifacts / text / logos / deformation：** 无变形、无伪影、无错字、无多余 logo；blob 边缘的彩虹色散是设计本身，不是 artifact。

## Issues

| Severity | Observation | Impact | Fix |
| --- | --- | --- | --- |
| major | 0–1 秒首帧近乎全黑，字标几乎不可见（F01）。静音自动播放或取首帧当封面时，观众第一眼什么都看不到。 | 片头钩子弱；封面帧无效。 | 把字标淡入提前 0.5 秒，或把首帧亮度抬到 F02 的水平；不要改动后续节奏。 |
| major | MOSEN 的字母 N 全程压在 blob 左侧亮边上（F02–F06），该字母的笔画与亮边重叠，对比度明显低于其余字母。 | 字标可读性打折；放大看时第一眼会先注意到 N 的边缘。 | 二选一：字标整体左移约 3% 画幅，或 blob 缩小约 5%，让 N 完全落在黑底上。 |
| minor | “一人之森 · AI 驱动”最晚入画且最暗，到约 3 秒才到正常亮度（F03–F04）。 | 中文行存在感弱于英文 tagline，品牌双语信息不对称。 | 该行淡入提前 0.5 秒，或最终亮度与英文行拉平。 |
| note | 全程无音频（文件本身无音频流）。 | 作为片头无声是可接受的设计，但不要在对外介绍里写“有声片头”。 | 如需配乐，另混一轨，不动画面。 |
| note | 运动只有海报慢推，无真实视频内容（人物、场景变化均无）。 | 作为 6 秒片头够用；但不要把它当成“视频生成”案例展示。 | README 里如实写“海报慢推 + 字标淡入”，不夸大。 |

## Repair prompt

```text
Fix the existing 6-second MOSEN intro without regenerating the scene:
1. Start the text fade-in 0.5 seconds earlier so the first frame is as legible as the 1-second frame; keep the later timing unchanged.
2. Move the whole text block left by about 3% of frame width (or shrink the blob by about 5%) so the letter N in MOSEN sits fully on black background, clear of the blob's bright rim.
3. Bring the last line "一人之森 · AI 驱动" in 0.5 seconds earlier and match its final brightness to the English tagline.
Do not change the blob, the layout, the colours, or the slow push-in. No new text, no new objects, no audio added.
```

## Re-check after repair

- [ ] 0.0 秒首帧：pill 与 MOSEN 是否清晰可读（不再近乎全黑）。
- [ ] 2.0 秒关键帧：MOSEN 的 N 是否完全落在黑底上，与亮边无重叠。
- [ ] 3.0 秒关键帧：“一人之森 · AI 驱动”亮度是否与英文 tagline 一致。
- [ ] 全程：blob 位置、字标位置、慢推速度是否与修前一致（只改三处，不动其他）。
- [ ] 导出后复核最终 MP4（不要只看工程预览），确认三处修改都已落盘。

## 生成信息

- 工具：cueshot-review-room-starter v0.1.0（GitHub 仓 masonmosen/cueshot-starter-skills）+ ffmpeg 8.1.2 抽帧（`fps=1,scale=1280:-1`）
- 审片帧：6 帧（0–5 秒，每秒 1 帧），证据拼图 `mosen-intro-6frames.jpg`
- 费用：0（纯文字审片，未调用任何付费 API）
- 关联演示：同一批的镜头方案见 `shot-designer-rainy-cafe.md`
