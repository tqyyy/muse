# boss-crawler 环境配置记录（Muse 搭建，2026-11-22）

- 虚拟环境：`~/workspace/custom-skills/boss-crawler/.venv`（Python 3.12），已按 requirements.txt 装好全部依赖，DrissionPage 4.1.1.4 已验证可导入。
- 浏览器：本机 Chrome 在 `/opt/meta-chromium/chrome`（Muse Browser 157）。跑脚本前设置环境变量 `CHROME_PATH=/opt/meta-chromium/chrome`（browser_finder.py 支持 `CHROME_PATH` / `BROWSER_PATH`）。
- LLM 配置：**未配**。流水线的推断阶段需要用户自己的 API key，填到 `assets/llm_config.json`（照 `assets/llm_config.example.json` 的格式），或用 `LLM_*` / `OPENAI_*` 环境变量。支持 OpenAI 兼容端点（DeepSeek / 通义 / 月之暗面 / 智谱 / 火山方舟 / 本地 ollama 等）。API key 走 Secure Vault 安全录入，不要写在聊天里。
- 验证命令：`.venv/bin/python scripts/utils/llm_check.py --no-call`（只查配置不花钱）。
- 注意：不要把 `assets/llm_config.json`（含真实 key）提交到 GitHub 公开仓库。
