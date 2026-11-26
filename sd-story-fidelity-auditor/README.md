# sd-story-fidelity-auditor

版本：1.0.0  
定位：成片审片第一关——剧情忠实度审核。

## 与现有技能的关系

- `xiaoma-director`：创作剧本、分镜、初始视频提示词。
- `sd-story-fidelity-auditor`：第一道成片审核，检查有没有讲对故事。
- `sd-qc-engine`：第二道成片审核，检查连续性、剪辑、声音、机检及 P0~P2 质量门禁。
- `sd-repair-director`：根据失败报告诊断并制定返修提示词。

## 使用顺序

视频生成 → 剧情审核 → 技术/制作 QC → 必要时返修 → 重新剧情审核 → 重新 QC。

## 接入说明

如果 Muse AI 网页 App 支持独立 Skill，请将本目录导入为新 Skill。
如果只支持自定义指令，将 `SKILL.md` 作为主指令，将 `references/review-routing.md` 作为路由规则附件。
是否支持自动调用其他 Skill，取决于 Muse 当前版本。若不支持自动路由，按 `references/review-routing.md` 手动依次调用。

## 文件结构

- `SKILL.md`：技能主指令
- `references/review-routing.md`：四个 Skill 的审片顺序和路由规则
