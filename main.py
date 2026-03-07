# from simple_llm import llm

from tool_chain import tools
from memory import run_interactive, llm #, chat

from tool_chain import create_agent

# chat_messages = []
# chat(input("You: "), chat_messages=)
# print("Assistent:", (chat(input("You: "))))

prompt = (
    "You have access to a tool that retrieves context from a blog post. "
    "Use the tool to help answer user queries."
    "Ти корисний асистент. Коли треба рахувати - використовуй 'calculator'. "
    "Про магазин - шукай у 'faq_search'. А погоду - 'weather_api'. "
    "Спершу зрозумій запит, потім виріши, який інтсрумент доречний"
)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt= prompt,
    debug=False,
)


run_interactive(agent=agent)