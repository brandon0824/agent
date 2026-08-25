"""Send one prompt to an OpenRouter model and print the response.

Usage:
    cp .env.example .env
    # Fill OPENROUTER_API_KEY and other settings in .env
    python openrouter_chat.py "Explain LangGraph in one sentence."

The script prints only the final ``content`` field. Reasoning details, when
returned by a reasoning model, are never printed.

The key is intentionally read from the environment and is never stored in
the source file.
"""

from __future__ import annotations

import json
import os
import sys
import argparse
import time
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener

from dotenv import load_dotenv


load_dotenv()


def required_setting(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"请在 .env 中设置 {name}。")
    return value


def ask_openrouter(messages: list[dict[str, object]]) -> dict[str, object]:
    api_key = required_setting("OPENROUTER_API_KEY")
    base_url = required_setting("OPENROUTER_BASE_URL").rstrip("/")
    model = required_setting("OPENROUTER_MODEL")
    timeout_seconds = float(os.getenv("OPENROUTER_TIMEOUT_SECONDS", "60"))
    proxy = required_setting("OPENROUTER_PROXY")

    payload = {
        "model": model,
        "messages": messages,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    # These headers are optional, but useful for OpenRouter analytics.
    if os.getenv("OPENROUTER_HTTP_REFERER"):
        headers["HTTP-Referer"] = os.environ["OPENROUTER_HTTP_REFERER"]
    if os.getenv("OPENROUTER_X_TITLE"):
        headers["X-Title"] = os.environ["OPENROUTER_X_TITLE"]

    request = Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        opener = build_opener(ProxyHandler({"http": proxy, "https": proxy}))
        with opener.open(request, timeout=timeout_seconds) as response:
            result = json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenRouter 请求失败（HTTP {exc.code}）：{detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"无法连接 OpenRouter：{exc.reason}") from exc

    try:
        return result["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"OpenRouter 返回格式异常：{result}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Call an OpenRouter chat model")
    parser.add_argument("prompt", nargs="*", help="the first user prompt")
    parser.add_argument(
        "--follow-up",
        help="optional second user prompt; preserves reasoning_details between calls",
    )
    args = parser.parse_args()
    prompt = " ".join(args.prompt).strip()
    if not prompt:
        prompt = input("请输入问题：").strip()
    if not prompt:
        raise SystemExit("问题不能为空。")

    messages: list[dict[str, object]] = [{"role": "user", "content": prompt}]
    started_at = time.perf_counter()
    assistant_message = ask_openrouter(messages)
    if args.follow_up:
        # OpenRouter reasoning models require reasoning_details to be passed
        # back unchanged when continuing a reasoning conversation.
        messages.extend(
            [
                {
                    "role": "assistant",
                    "content": assistant_message.get("content"),
                    "reasoning_details": assistant_message.get("reasoning_details"),
                },
                {"role": "user", "content": args.follow_up},
            ]
        )
        assistant_message = ask_openrouter(messages)
    elapsed_seconds = time.perf_counter() - started_at
    print(assistant_message.get("content", ""))
    print(f"\n耗时：{elapsed_seconds:.2f} 秒")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
