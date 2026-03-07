import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import tool


load_dotenv()
# Створюємо LLM-об'єкт
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@tool(
    "colculator",
    description="Calculate math expression ('0123456789+-*/(). ')"
)
def safe_calculate(expression: str) -> str:
    # "2 + 3 * 5"
    allowed_chars = "0123456789+-*/(). "
    if not all(ch in allowed_chars for ch in expression):
        return "Error! allowed chars: '0123456789+-*/(). '"
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except Exception as e:
        return f"Error: {e}"

#-------------------------------------------
# Декоратор

# def func():
#     n = ""  # ""
#     m = 1
#     c = "12345"
#
# func = decorator_name(func)
#
# @func
# def func_new():
#     n = "qwerty"  # func() -> n = "qwerty"
#-------------------------------------------------
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

with open("data/faq.txt", "r", encoding="utf-8") as f:
    faq_text = f.read()
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
# docs = splitter.split_text(faq_text)
docs = splitter.create_documents([faq_text])

embeddings = OpenAIEmbeddings()
# vector_store = FAISS(
#     embedding_function=embeddings,
#     index=index,
#     docstore=InMemoryDocstore(),
#     index_to_docstore_id={},
# )
vector_stores = FAISS.from_documents(docs, embeddings)

@tool
def search_faq(query: str) -> str:
    """Питання/відповідь"""
    try:
        # result = vector_store.search(query)
        result = vector_stores.similarity_search(query, k=1)
        if not result:
            return "Нічого не знайдено у FAQ"
        return result[0].page_content

    except Exception as e:
        return f"Error search: {e}"


@tool
def weather_api(city: str) -> str:
    """Відповідає про погоду. Формат: Назва міста англійською"""
    data = {
        "Kharkiv": "Сонячно, 0..+2°C",
        "Kyiv": "Хмарно, -1..+1°C, вітряно",
        "Lviv": "Дощ, +2..+3°C"
    }
    return data.get(
        city,
        f"Немає даних для введеного міста, спробуйте: {', '. join(list(data.keys()))}")


# Створення агента
from langchain.agents import create_agent


tools = [safe_calculate, search_faq, weather_api]
# If desired, specify custom instructions
prompt = (
    "You have access to a tool that retrieves context from a blog post. "
    "Use the tool to help answer user queries."
    "Ти корисний асистент. Коли треба рахувати - використовуй 'calculator'. "
    "Про магазин - шукай у 'faq_search'. А погоду - 'weather_api'. "
    "Спершу зрозумій запит, потім виріши, який інтсрумент доречний"
)
# agent = create_agent(model, tools, system_prompt=prompt)
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=prompt,
    debug=True)

def get_output(result: dict) -> str:
    messages = result.get("messages", [])
    for msg in reversed(messages):
        content = getattr(msg, "content", None)
        tool_calls = getattr(msg, "tool_calls", None) or []
        if content and not tool_calls:
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                return "".join(
                    c.get("text", str(c)) if isinstance(c, dict) else str(c) for c in content
                    # for c in content:
                    #     if isinstance(c, dict):
                    #         c.get("text", str(c))
                    #     else: str(c)
                )
    return ""

if __name__ == "__main__":
    print("\n=== Калькулятор ===")
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Обчисли: (2+3)*4-5"
                }
            ]
        }
    )
    print(get_output(result))

    print("\n=== FAQ питання ===")
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Як здійснити оплату?"
                }
            ]
        }
    )
    print(get_output(result))

    print("\n=== Погода (API муляж) ===")
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Яка погода у Kharkiv?"
                }
            ]
        }
    )
    print(get_output(result))