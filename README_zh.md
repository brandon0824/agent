# LangGraph AI Agent（第 1 阶段）

这是一个使用 Python、LangGraph 和 LangChain 构建的最小命令行对话 Agent。它演示了如何用 LangGraph 状态图调用 OpenAI 兼容的大语言模型，并通过 `MemorySaver` 按会话保存消息。

当前实现聚焦于 Agent 的基础骨架：单个模型节点、会话隔离和多家模型服务商配置。暂未包含工具调用、RAG、向量数据库或 Web 接口。

## 功能

- 基于 LangGraph `StateGraph` 的单节点对话流程
- 使用 `thread_id` 隔离多个会话
- 进程内短期记忆（重启程序后清空）
- 支持 OpenAI、DeepSeek 和 OpenRouter
- 提供独立的 Gemini 网关客户端（`openrouter_gemini.py`）
- 支持自定义系统提示词
- 懒加载模型与 API 密钥，便于无密钥编译或测试图结构
- `/clear` 新建会话，`/exit` 或 `/quit` 退出

## 环境要求

- Python 3.11 或更高版本
- 一个 OpenAI 兼容模型服务的 API Key

## 安装与运行

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
touch .env                     # 或复制已有的 .env.example
python main.py
```

`.env` 至少需要填写所选服务商的 API Key。程序启动后，在 `你：` 提示符输入问题即可。

## 配置

### DeepSeek（示例）

```env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=你的DeepSeek_API_Key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

推理模型可将 `LLM_MODEL` 设置为 `deepseek-reasoner`。

### OpenAI

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=你的OpenAI_API_Key
LLM_MODEL=gpt-4o-mini
```

如果使用兼容服务，可额外设置 `OPENAI_BASE_URL`。

### OpenRouter

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=你的OpenRouter_API_Key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-4o-mini
```

`LLM_MODEL` 使用 OpenRouter 的模型标识，例如 `deepseek/deepseek-chat`。`OPENROUTER_HTTP_REFERER` 和 `OPENROUTER_X_TITLE` 为可选请求头。

还可以通过 `AGENT_SYSTEM_PROMPT` 覆盖默认系统提示词。不要把 API Key 提交到 Git 仓库。

### Gemini 网关（独立客户端）

`openrouter_gemini.py` 通过配置的网关调用 Gemini 原生 `generateContent` 接口。在 `.env` 中加入：

```env
GOOGLE_GEMINI_BASE_URL=http://38.162.115.189:8088/antigravity
GEMINI_API_KEY=你的Gemini_API_Key
GEMINI_MODEL=gemini-3.6-flash-medium
```

执行一次性提问：

```bash
python openrouter_gemini.py "2 加 2 等于几？"
```

脚本会自动读取 `.env`，并请求 `/v1beta/models/{GEMINI_MODEL}:generateContent`。

## 项目结构

```text
.
├── main.py          # CLI 入口与命令处理
├── app/graph.py     # 模型创建和 LangGraph 状态图
├── app/config.py    # .env 加载、系统提示词和必填配置
├── openrouter_gemini.py # 独立 Gemini 网关客户端
└── requirements.txt # Python 依赖
```

每轮输入都会以 `MessagesState` 的消息形式传入图，`assistant` 节点在系统提示词后调用模型，编译后的图使用 `MemorySaver` 保存同一 `thread_id` 的上下文。

## 开发与扩展

可以从 `app/graph.py` 的 `build_graph()` 开始扩展：添加 Tool 节点、条件边、持久化 checkpoint、RAG 检索或人工确认节点。生产环境应替换进程内 `MemorySaver`，并补充超时、重试、权限、审计、评测和成本控制。

## 许可证

当前仓库未声明特定开源许可证，请在分发前补充许可证信息。
