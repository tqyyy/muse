# CueShot Shot Designer Starter — Demo：清晨咖啡馆看雨

> 演示说明：场景想法由本次任务自编（“清晨咖啡馆里一个人看窗外雨”），未用任何外部素材。
> 严格按 `cueshot-shot-designer-starter/SKILL.md` v0.1.0 的 Starter 工作流与输出格式产出；
> 导演匹配一段取自本地完整版 `local-cinematic-shot-design` 技能，仅作规划参考，**未写入可执行 Prompt**（Starter 合规要求：Prompt 不依赖导演名、影片名、人物或品牌）。
> 零付费：本文件为纯文字镜头方案，未调用任何生视频 API，未花积分。

## 输入（固定事实）

- 人物：一个人，约 30 岁，深灰大衣，短发，侧脸朝窗，无台词。
- 场景：清晨的咖啡馆靠窗座位，窗外下雨，窗玻璃上有雨痕。
- 动作：一个人安静地坐着，看窗外的雨；手指偶尔轻碰温热的白瓷咖啡杯。
- 情绪：安静、疏离、一点想念，不悲伤、不戏剧化。
- 道具：白瓷咖啡杯（有热气）、木桌、窗。
- 锁定：全程只有一个人；不出现第二个人；不出现可读文字招牌。

## Shot mode

**single shot（单镜头）**

选择理由：整段只有一个动作（看雨）、一个情绪变化（从发呆到被雨声轻轻拉回）、一个空间（靠窗座位）。
按 Starter 规则，2–3 镜只用于“发现—反应—行动”、对峙、环境揭示或地点/时间变化，本场景四条都不满足，拆镜只会增加人物与场景漂移风险。

## 导演匹配（规划参考，不进 Prompt）

- **首选：王家卫**——路由特征“人物疏离、碎片时间、主观色彩”与本场景完全对应：隔着雨痕玻璃看人、局部可见、时间被拉长。取用其“隔玻璃中景、偏置构图、窗外色光、缓慢漂移”四项，不取霓虹饱和色（清晨咖啡馆不适用）。
- 备选 1：Sofia Coppola——安静疏离、人物偏置、负空间充足；若想更安静、更少风格化，可改走这条。
- 备选 2：Terrence Malick——自然光、感官碎片；若想强化雨声与光线本身，可参考，但本场景人物情绪仍以王家卫更贴。

## Shot plan

- **Shot 1（唯一镜头，约 8 秒）：建立人物与雨的关系**
  - 叙事目的：呈现一个人与窗外雨之间的距离——他在室内、雨在室外，窗玻璃是两者之间的薄膜。
  - 人物位置：人物坐画面右侧三分之一处，侧脸朝左对窗；左侧留出大面积窗与雨景（负空间）。
  - 景别 / 距离：中景，腰部以上；50mm 左右的自然透视，不夸张空间、不压扁人物。
  - 角度 / 机位：平视，略低于人物视线，机位在桌对面偏右，隔着半张桌子看他。
  - 运镜：几乎不动，只在第 3–7 秒做一次极缓慢的推近（约 5% 画幅），动机是“目光被雨吸过去”，不是展示机位。
  - 光线：主光是窗外清晨冷色柔光，从左前方打在人物侧脸与杯沿；室内后方有一盏暖色小灯做暖色孤岛，照亮背景一角，不抢主体。
  - 色彩：冷雨蓝灰为主，暖灯与木桌做小面积暖色；去饱和，不用高饱和霓虹。
  - 连续性锁定：人物深灰大衣、短发、侧脸朝左；白瓷杯在右手边、杯口有热气；窗玻璃雨痕自上而下；光源方向全程左冷右暖不变。

## Model-neutral prompt

```text
Early morning in a quiet café. A person in their thirties, dark grey coat,
short hair, sits alone at a window seat in profile, facing left toward the
rain outside. Rain streaks run down the window glass between the person and
the street. A white ceramic coffee cup with faint steam sits on the wooden
table by their right hand. The person's fingers rest lightly on the cup,
then still. Cool, soft morning light from the window falls on the side of
their face and the rim of the cup; a small warm lamp glows dimly in the
background to the right. The camera is at eye level, medium shot from the
waist up, the person placed on the right third of the frame, the rainy
window filling the left. Almost static: one very slow push-in of about five
percent between the third and seventh second. No dialogue, no text, no
other people. Muted blue-grey palette with a small warm accent. Quiet,
still, a little distant.
```

## Negative constraints

- No second person entering the frame, no waiter, no passers-by inside the café.
- No dialogue, no subtitles, no readable shop signs or text on the window.
- No rain falling indoors; rain stays outside the glass.
- No face turned to camera; the person keeps looking out the window.
- No fast camera movement, no zoom jump, no cut inside the shot.
- No saturated neon colours, no high-contrast drama lighting.

## Suggested settings

- Duration: ~8 seconds（单镜头，情绪靠停留完成，不宜更长）
- Aspect ratio: 16:9（窗与人并置需要横向空间；如改竖屏，需把人物改放画面下三分之一，窗雨占上方）
- Notes:
  - 生成时最可能漂移的是三点：人物面朝方向、杯子位置、雨痕方向；三者已在 Prompt 与连续性锁定里写死，审片时先核这三点。
  - 如需切换，可直接说“改为 3 镜分镜”（对应：建立窗景 → 人物反应特写 → 手指碰杯收束）。
  - 本方案未指定生成模型；Prompt 为模型无关写法，可直接用于 Seedance / 可灵 / Runway 等（生成本身不在本次演示范围内）。

## 生成信息

- 工具：cueshot-shot-designer-starter v0.1.0（GitHub 仓 masonmosen/cueshot-starter-skills）+ 本地完整版 cinematic-shot-design 的导演档案作匹配参考
- 费用：0（纯文字方案，未调用任何付费生成 API）
- 审片对应：同一批演示的审片见 `review-room-mosen-intro.md`
