# 与 sd-qc-engine 的交接契约

## 输入：QC 失败报告
建议字段：
- project_id / episode_id / scene_id
- shot_id / clip_id / version
- verdict：PASS / WARN / FAIL（沿用 QC 原始值）
- issue_id
- timestamp_or_range
- severity
- issue_description
- rule_reference（如有）
- evidence / observed_frame（如有）
- expected_result
- related_shots
- locked_constraints

若原报告没有某字段，不得编造；标记“未提供”。

## 输出：返修复验包
- 原 issue_id 与原始 QC 判定
- 返修版本号
- 根因诊断及证据标签
- 采用的返修策略
- 修改前/修改后预期差异
- 实际修改的提示词/时间段
- 明确保留项
- 相邻镜头需复验的连续性关系
- 声音需复验的同步点
- 未解决风险和待核验事项

## 权限边界
- `sd-repair-director` 不签发正式 PASS。
- `sd-qc-engine` 负责再次检查并给出正式判定。
- 原 QC 门禁、P0~P2、连续性台账和机检规则保持唯一权威。
- 若返修暴露剧本或分镜根因，路由回 `xiaoma-director` 或总控责任阶段。
