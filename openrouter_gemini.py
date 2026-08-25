"""Call the Gemini API through the configured gateway."""

from __future__ import annotations

import argparse
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()


def required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"请在 .env 中设置 {name}。")
    return value


def ask_gemini(prompt: str) -> str:
    base = required("GOOGLE_GEMINI_BASE_URL").rstrip("/")
    key = required("GEMINI_API_KEY")
    model = required("GEMINI_MODEL")
    url = f"{base}/v1beta/models/{model}:generateContent"
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=float(os.getenv("GEMINI_TIMEOUT_SECONDS", "60"))) as response:
            result = json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini 请求失败（HTTP {exc.code}）：{detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"无法连接 Gemini 服务：{exc.reason}") from exc
    try:
        parts = result["candidates"][0]["content"]["parts"]
        return "".join(part["text"] for part in parts if "text" in part)
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Gemini 返回格式异常：{result}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Call Gemini")
    parser.add_argument("prompt", nargs="*", help="要发送的问题")
    args = parser.parse_args()
    prompt = " ".join(args.prompt).strip() or input("请输入问题：").strip()
    if not prompt:
        raise SystemExit("问题不能为空。")
    print(ask_gemini(prompt))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
