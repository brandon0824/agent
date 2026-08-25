# LangGraph AI Agent (Phase 1)

This repository contains a minimal command-line conversational agent built with Python, LangGraph, and LangChain. It shows how to call an OpenAI-compatible chat model from a LangGraph state graph and keep per-conversation messages with `MemorySaver`.

The current implementation focuses on the basic agent skeleton: one model node, isolated conversations, and configuration for several model providers. Tool calling, RAG, vector databases, and a web API are not included yet.

## Features

- A single-node conversation flow built with LangGraph `StateGraph`
- Conversation isolation through `thread_id`
- In-process short-term memory (cleared when the process restarts)
- OpenAI, DeepSeek, and OpenRouter support
- A standalone Gemini gateway client (`openrouter_gemini.py`)
- A configurable system prompt
- Lazy model and API-key loading, so the graph can be built or tested without credentials
- `/clear` starts a new conversation; `/exit` and `/quit` exit the CLI

## Requirements

- Python 3.11 or newer
- An API key for an OpenAI-compatible model provider

## Install and run

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
touch .env                     # Or copy your existing .env.example
python main.py
```

At least the API key for the selected provider must be present in `.env`. Once the program starts, enter prompts at `你：`.

## Configuration

### DeepSeek (example)

```env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

Set `LLM_MODEL=deepseek-reasoner` to use the reasoning model.

### OpenAI

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4o-mini
```

For a compatible endpoint, set `OPENAI_BASE_URL` as well.

### OpenRouter

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-4o-mini
```

Use an OpenRouter model identifier in `LLM_MODEL`, such as `deepseek/deepseek-chat`. `OPENROUTER_HTTP_REFERER` and `OPENROUTER_X_TITLE` are optional headers.

`AGENT_SYSTEM_PROMPT` can override the default system prompt. Never commit API keys to Git.

### Gemini gateway (standalone client)

`openrouter_gemini.py` uses the native Gemini `generateContent` API through the configured gateway. Put the following in `.env`:

```env
GOOGLE_GEMINI_BASE_URL=http://38.162.115.189:8088/antigravity
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash-medium
```

Run a one-shot prompt with:

```bash
python openrouter_gemini.py "What is 2 + 2?"
```

The script reads `.env` automatically and sends requests to `/v1beta/models/{GEMINI_MODEL}:generateContent`.

## Project layout

```text
.
├── main.py          # CLI entry point and command handling
├── app/graph.py     # Model creation and LangGraph state graph
├── app/config.py    # .env loading, system prompt, and required settings
├── openrouter_gemini.py # standalone Gemini gateway client
└── requirements.txt # Python dependencies
```

Each input is passed to the graph as a `MessagesState` message. The `assistant` node calls the model after the system prompt, and the compiled graph uses `MemorySaver` to preserve context for the same `thread_id`.

## Development and extensions

Start with `build_graph()` in `app/graph.py` to add tool nodes, conditional edges, a persistent checkpoint, RAG retrieval, or human approval steps. For production, replace in-process `MemorySaver` and add timeouts, retries, authorization, auditing, evaluation, and cost controls.

## License

This repository does not currently declare a specific open-source license. Add one before distributing it.
