# LangGraph AI Agent

这是第 1 阶段的最小可运行版本：一个带会话状态的命令行对话 Agent。

## 运行

```bash
python -m pip install -r requirements.txt
cp .env.example .env
# 默认使用 DeepSeek，只需填写 .env 中的 DEEPSEEK_API_KEY
python main.py
```

`/clear` 会新建会话，`/exit` 退出。当前记忆保存在进程内，重启后会清空。

## DeepSeek 配置

```env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=你的DeepSeek_API_Key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

推理模型可将 `LLM_MODEL` 改为 `deepseek-reasoner`。如使用 OpenAI，将 `LLM_PROVIDER` 改为 `openai`，并填写 `OPENAI_API_KEY`。

## OpenRouter 配置

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=你的OpenRouter_API_Key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-4o-mini
```

`LLM_MODEL` 使用 OpenRouter 的模型标识，例如 `deepseek/deepseek-chat`。`OPENROUTER_HTTP_REFERER` 和 `OPENROUTER_X_TITLE` 为可选配置。
