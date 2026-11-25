---
name: "skill-auto-router"
description: "Use when starting any conversation or receiving any task from the user — automatically search the installed skill catalog for relevant skills and invoke them BEFORE responding or acting, without waiting for the user to name or request a skill. 每次对话/任务开始时自动执行：先搜已有 skill、读中选中的 SKILL.md 并按它做事，用户不需要提醒。"
license: MIT
---

# Skill Auto Router — 自动调用 Skill 路由器

用户明确要求（2026-11-26）：每次跟 Muse 说话，Muse 自己去调用相关的 skill，不要等用户提醒。本 skill 是这一要求的执行规则，改编自 obra/superpowers 的 `using-superpowers`（已同装在本目录旁），按 Muse 的实际工具落地。

## 铁律

**任何任务型消息，先查 skill，再动手。** 哪怕只有一点可能相关，也必须先用 `muse.skill_search` 搜一遍；搜到适用的，读它的 `SKILL.md` 全文并按它执行。这不是可选项，不许用"我自己也会做"绕过。

## 执行顺序（每个任务开始时）

1. **提炼检索词**：从用户这句话里提炼 2–3 组检索词（一组贴用户原话、一组换同义词/英文术语、一组领域词），一次并行 `muse.skill_search`。
2. **涉及外部服务/账号时**（邮箱、日历、某个 App/网站），同时 `muse.connector_search` 找连接器文档。
3. **选 skill**：命中多个时，流程/方法类 skill 先行（它定做法），执行类 skill 随后；用户设过 preferred 的同类任务优先用 preferred；最具体的优先于泛用的。
4. **读全文再执行**：读中选中的 `SKILL.md`（含它指向的本地修订文件），按它的步骤做；做完按它的交付标准交付。
5. **没有命中**：不许直接说"做不了"。按顺序兜底：先按 `find-skills`（已装）去 GitHub/skills.sh 找现成的、验质量后报给用户装 → 找不到再终端/浏览器自己想办法 → 任务可复用时按 custom-connector-setup 模板沉淀成新 skill。
6. **compaction 或长任务中途**：相关 skill 的 SKILL.md 要重读，摘要不能代替原文。

## 固定调用（用户 2026-11-26 明确要求，不走搜索直接执行）

- **凡触及生成视频或修改视频的任务**（生成、重跑、改画面、剪辑、配音、字幕等一切与视频产出有关的事），动手前必须先调用 **太上老君·AI炼丹炉**（`taishang-laojun` 总控台，按任务性质再配 tslj-* 模块），读其 SKILL.md 并按它的判断框架做；同时照常并行调用技术类视频 skill（如 muse-video-prompt-skill 管生成与抽帧验证）。两者不冲突：炼丹炉管内容判断，技术 skill 管生成执行。

## 例外（这些不用先搜）

- 纯闲聊、打招呼、道谢、告别等没有任务的消息。
- 紧接着上一轮同一任务的简短确认（如"好""继续"）——沿用上一轮已加载的 skill，不重复搜。
- 用户明确说这次不要用某个 skill / 不要查。

## 红旗（出现这些念头 = 停下，先搜 skill）

- "这个简单，我直接做" → 简单任务也有 skill 定标准，先搜。
- "我记得这个 skill 怎么写的" → skill 会更新，读当前文件。
- "先问用户一句再说" → 搜 skill 排在提问之前，skill 里可能就有答案。
- "上次没用 skill 也做完了" → 上次是上次，这次照规矩来。

## 优先级

用户当下的明确指令 > 本 skill 与其他 skill > 默认行为。用户的话永远最大；skill 与用户指令冲突时听用户的，并说明冲突点。
