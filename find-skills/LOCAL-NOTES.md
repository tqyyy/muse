# 本地适配说明（Muse 环境）

原版 find-skills 用 `npx skills` CLI 在 skills.sh 生态里搜/装 skill。本环境没有该 CLI 运行时约定，执行时按等价路径落地：

1. 搜：先 `muse.skill_search` 查本地已装；没有再用浏览器搜 GitHub / skills.sh（关键词中英各一组）。
2. 验：按原版标准验质量——来源信誉（官方/知名作者优先）、GitHub 星数、安装量、是否 MIT/开源、是否带脚本；低于 100 星/安装量的谨慎对待并说明。
3. 报：给用户候选清单（名称、作用、星数/安装量、来源），等用户点头。
4. 装：克隆到 /tmp 检查结构 → 复制到 ~/workspace/custom-skills/<name>/（完整版含脚本）→ py_compile 语法检查（有脚本时）→ `muse.skill_search` 验证可搜到 → 记入 MEMORY.md。带脚本的仓库会触发执行风险检查，必须先向用户说明、拿到明确确认再装（用户既定流程）。
