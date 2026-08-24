import uuid

from app.graph import build_graph


def run_cli() -> None:
    print("LangGraph Agent（第 1 阶段）")
    print("输入 /exit 退出，输入 /clear 开始新对话。")
    graph = build_graph()
    thread_id = str(uuid.uuid4())

    while True:
        try:
            user_input = input("\n你：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            return
        if not user_input:
            continue
        if user_input.lower() in {"/exit", "/quit"}:
            print("再见！")
            return
        if user_input.lower() == "/clear":
            thread_id = str(uuid.uuid4())
            print("已开始新对话。")
            continue

        result = graph.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config={"configurable": {"thread_id": thread_id}},
        )
        print(f"Agent：{result['messages'][-1].content}")


if __name__ == "__main__":
    run_cli()

