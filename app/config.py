import os

from dotenv import load_dotenv


load_dotenv()


SYSTEM_PROMPT = os.getenv(
    "AGENT_SYSTEM_PROMPT",
    "你是一个 helpful、可靠且简洁的 AI 助手。请用用户使用的语言回答；不确定时明确说明。",
)


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"缺少环境变量 {name}。请复制 .env.example 为 .env 并填写，"
            "或在启动前导出该变量。"
        )
    return value
