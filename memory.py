import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="Ти дружній асистент, що відповідає просто та корисно",
    debug=False
)

def get_output(result: dict) -> str:
    # {
    # "messages": [
    #     {
    #         "role": "user",
    #         "content": "Яка погода у Kharkiv?"
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "Погода у Kharkiv: 0..+2"
    #     }
    #  ]
    #}
    messages = result.get("messages", [])
    for msg in reversed(messages):
        content = getattr(msg, "content", None)
        tool_calls = getattr(msg, "tool_calls", None) or []
        if content and not tool_calls:
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                return "".join(
                    c.get("text", str(c)) if isinstance(c, dict) else str(c)
                    for c in content
                )
    return ""

chat_messages = []
def chat(user_input: str, agent = agent) -> str:
    # Додаємо повідомлення користувача
    chat_messages.append({"role": "user", "content": user_input})

    # Викликаємо агент з усією
    result = agent.invoke({"messages": chat_messages })
    chat_messages.clear()                       # chat_messages  = []
    chat_messages.extend(result["messages"])    # [] + [{"role": "user", "content": user_input}] = [{"role": "user", "content": user_input}]

    return get_output(result)

def run_demo():
    print("Відпвідь 1:", chat("Привіт! Мене звати Лена"))
    print("Відпвідь 2:", chat("Запам'ятай, я люблю програамування"))
    print("Відпвідь 3:", chat("Нагадай, як мене звати і що мені подобається?"))


# if __name__ == "__main__":
#     run_demo()

# -----------------------------------------------------------------------------
# 5. ІНТЕРАКТИВНИЙ РЕЖИМ (спілкування в терміналі)
# -----------------------------------------------------------------------------
# while True: input() → chat() → print(). Команди виходу: exit, quit, q, /вихід
# Запуск: python step3_memory.py -i (тільки інтерактив) або python step3_memory.py (демо → пропозиція)
def run_interactive(agent=agent):
    """
    Інтерактивний чат у терміналі. Введіть повідомлення — отримаєте відповідь.
    Для виходу: exit, quit, q або /вихід
    """
    print("\n" + "=" * 60)
    print("  ІНТЕРАКТИВНИЙ РЕЖИМ - чат з агентом (пам'ять увімкнена)")
    print("  Введіть 'exit', 'quit', 'q' або '/вихід' для завершення.")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("Ви: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо побачення!")
            break

        if not user_input:
            continue

        # Команди виходу
        if user_input.lower() in ("exit", "quit", "q", "/вихід"):
            print("До побачення!")
            break

        response = chat(user_input, agent=agent)
        print(f"Бот: {response}\n")


if __name__ == "__main__":
    import sys

    # Режим: -i або --interactive - тільки інтерактивний; інакше - демо, потім пропозиція продовжити
    if "-i" in sys.argv or "--interactive" in sys.argv:
        run_interactive()
    else:
        run_demo()
        print("\n" + "-" * 40)
        try:
            choice = input("Перейти в інтерактивний режим? (y/n): ").strip().lower()
            if choice in ("y", "yes", "так", "т"):
                run_interactive()
        except (EOFError, KeyboardInterrupt):
            pass