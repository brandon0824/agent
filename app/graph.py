import os
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph

from .config import SYSTEM_PROMPT, required_env


def create_model() -> BaseChatModel:
    """Create the default OpenAI-compatible chat model lazily."""
    # Import lazily so the graph can be compiled and tested without credentials.
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise RuntimeError(
            "缺少 langchain-openai，请运行: python -m pip install langchain-openai"
        ) from exc

    provider = os.environ.get("LLM_PROVIDER", "openai").strip().lower()
    default_headers = None
    if provider == "deepseek":
        api_key = required_env("DEEPSEEK_API_KEY")
        base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        model = os.environ.get("LLM_MODEL", "deepseek-chat")
    elif provider == "openrouter":
        api_key = required_env("OPENROUTER_API_KEY")
        base_url = os.environ.get(
            "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
        )
        model = os.environ.get("LLM_MODEL", "openai/gpt-4o-mini")
        default_headers = {
            key: value
            for key, value in {
                "HTTP-Referer": os.environ.get("OPENROUTER_HTTP_REFERER"),
                "X-Title": os.environ.get("OPENROUTER_X_TITLE"),
            }.items()
            if value
        } or None
    elif provider == "openai":
        api_key = required_env("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL") or None
        model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    else:
        raise RuntimeError(
            f"不支持的 LLM_PROVIDER: {provider}。可选值为 openai、deepseek 或 openrouter。"
        )

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        default_headers=default_headers,
        temperature=0,
    )


def build_graph(model: Optional[BaseChatModel] = None):
    """Build a stateful single-node conversational graph."""
    llm = model or create_model()

    def call_model(state: MessagesState):
        messages = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
        return {"messages": [llm.invoke(messages)]}

    workflow = StateGraph(MessagesState)
    workflow.add_node("assistant", call_model)
    workflow.add_edge(START, "assistant")
    workflow.add_edge("assistant", END)
    return workflow.compile(checkpointer=MemorySaver())
