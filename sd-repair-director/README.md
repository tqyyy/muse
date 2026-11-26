# sd-repair-director（导演级视频返修引擎）

版本：1.0.0  
适用：漫剧老李 V7.5.0-SLIM 套装  
定位：接收 `sd-qc-engine` 的失败报告，分析根因并产出 Muse AI 可执行返修提示词，随后交回 QC 复验。

## 安装/接入
将 `sd-repair-director/` 整个目录放入你的 Skill 根目录（具体路径依你的 Muse AI/Agent 宿主而定），并确保宿主能够读取 `SKILL.md` 与 `references/`。

如果 Muse AI 网页 App 不支持导入标准 Skill 目录，则将 `SKILL.md` 内容添加为自定义 Skill/系统指令，并将 `references/` 文件作为知识文件上传。是否支持目录导入、自动路由和文件引用，取决于 Muse App 当前版本，不能仅凭本包保证。

## 与现有 Skill 的职责分工
- `xiaoma-director`：编导、剧本、分镜、初始提示词、全片制作。
- `sd-qc-engine`：成片质检、连续性台账、剪辑转场/声音 QC、正式 PASS/WARN/FAIL。
- `sd-repair-director`：失败后的根因分析、最小改动方案、返修提示词、复验交接。

本技能不修改前两个 Skill 的规则，也不复制 QC 的门禁。

## 推荐路由
1. 视频生成完成，交 `sd-qc-engine`。
2. PASS：按原流程继续。
3. FAIL 或需整改的 WARN：把完整 QC 报告、锁定剧本/分镜、失败视频和相邻镜头信息交给 `sd-repair-director`。
4. `sd-repair-director` 输出返修方案与完整 Muse 提示词。
5. 用户/自动化流程在 Muse AI 重新生成。
6. 新视频交回 `sd-qc-engine` 复验。
7. 正式判定仍由 `sd-qc-engine` 作出。

## 首次测试
先用一个失败镜头做 dry-run：
- 不生成视频；
- 要求输出问题根因表、前后镜头连续性表、返修策略和完整提示词；
- 检查是否保留剧本/台词/资产锁；
- 检查是否虚构视频观察或 Muse 参数；
- 满意后再用于实际返修。

## 文件
- `SKILL.md`：主技能定义
- `references/muse-repair-prompt-template.md`：Muse 提示词模板
- `references/repair-diagnosis-framework.md`：诊断框架
- `references/qc-handoff-contract.md`：与 QC 的交接契约
