---
name: "ai-storyboard-director"
description: "AI Storyboard Director v5.2 — director-grade AIGC storyboard skill: turn a script into an executable cinematic shot chain (visual concept lock first, two-speed delivery: design draft then production draft), plus a review mode that checks storyboards for continuity, ungeneratable descriptions and director-TV mediocrity (导播病). 导演级分镜：剧本 → 视觉概念锁定 → 设计稿 → 生产稿镜头链；已有分镜可进审查模式。"
license: MIT
---

# AI Storyboard Director v5.2 — 入口

源仓库：62656456/ai-storyboard-director-v5.2（MIT）。本目录是完整安装：

- `standalone-compact.md` — 精编单文件版（默认用这个）：保留全部输出契约、六条铁律、受控词表与决策程序，知识库为速查版。
- `standalone-full.md` — 全量单文件版：需要完整知识深度（导演风格库、摄影词表等）时加载。
- `ai-storyboard-director5.2.skill` — 原始 skill 包文件，留档。
- `PACKAGE-README.md` / `README.md` — 原仓库说明。

## 怎么用

1. 用户给剧本要拆分镜 → 先读 `standalone-compact.md` 并按其骨架执行：读懂剧本 → 题材判断 → 定终点 → 步骤 2.5 立概念（五项强制锁定，过不了导播测试不往下走）→ 切节拍 → 归并 AG-CLIP → 关系链 → 逐镜配镜 → 接口回填 → 翻车点预测 → 因果校验。默认双速交付：先给设计稿让用户拍板，再展开生产稿。
2. 用户给已有分镜要检查 → 进审查模式（精编版 §八），查导播病、连续性、不可生成描述和输出契约缺漏，给修正版。
3. 复杂/长项目或需要导演风格装置细节时，改读 `standalone-full.md`。
4. 产出的生产稿镜头链交给下游：muse-video（前期策划）/ muse-video-prompt-skill（六段式提示词 → 生成 → 拼接 → 抽帧验证）/ cueshot-review-room-starter（审片）。
5. 只有裸剧本时脑补的光线/外形/道具一律标 假设/ASSUMED，不冒充给定事实。
