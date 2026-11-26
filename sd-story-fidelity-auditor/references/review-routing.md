# 漫剧老李 V7.5.0-SLIM · 成片审片路由规则

## 推荐审片顺序

生成视频完成后，必须按以下顺序进入审片：

1. `sd-story-fidelity-auditor`：第一关，核对剧情忠实度。
2. `sd-qc-engine`：第二关，核对制作质量、连续性、剪辑、声音与机检。
3. `sd-repair-director`：只在前两关发现需要整改的问题时调用，负责诊断和制定返修方案。
4. 返修后重新从 `sd-story-fidelity-auditor` 开始，再进入 `sd-qc-engine` 复验。

## 路由判定

- 剧情 `STORY-PASS`：进入 `sd-qc-engine`。
- 剧情 `STORY-WARN`：带着待关注项进入 `sd-qc-engine`。
- 剧情 `STORY-FAIL`：
  - 根因在锁定剧本/分镜：退回 `xiaoma-director` / 总控；
  - 根因在视频生成执行：交 `sd-repair-director`；
  - 根因不明：先补证据，不允许跳过剧情审核。
- 剧情 `UNVERIFIABLE`：补齐材料后再审，不得默认通过。
- QC `PASS`：通过制作质量门禁。
- QC `WARN/FAIL`：交 `sd-repair-director` 或退回对应责任阶段；按原 QC 报告与门禁处理。

## 不可越权

- `sd-story-fidelity-auditor` 不做技术质量 PASS，不替代 QC。
- `sd-qc-engine` 不修改剧情源稿，不替代剧情审核。
- `sd-repair-director` 不擅自改剧本，不签发正式 PASS。
- `xiaoma-director` 负责剧本与分镜源头，不代替成片 QC。

## 关键原则

剧情审核不是审美审查。不得仅因剧情风格不合个人喜好判 FAIL；必须指出与锁定剧本、分镜或项目设定的具体偏差。
