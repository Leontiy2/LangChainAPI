import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

#Обійти помилку, коли немає ключа та продовжити виконання коду
# try:
#     api_key = os.getenv("OPENAI_API_KEY")
# except Exception as e:
#     print(e)
#     print("Немає ключа OPENAI_API_KEY у .env. Додай його та запусти ще раз!")

# Видасть "нашу" помилку (нас викине, просто покаже, що не так)
if not api_key:
    raise ValueError("Немає ключа OPENAI_API_KEY у .env. Додай його та запусти ще раз!")

llm = ChatOpneAI(model="gpt-4o-mini", temperature=0.7)