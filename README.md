# LangChain API — Agent Assistant

## Project overview
A small assistant built with an LLM orchestration layer, tools, and short-term memory. The app demonstrates chaining LLM calls, adding deterministic tools and keeping multi-turn context.

## Purpose
Show how to:
- wrap a model for programmatic use
- provide safe deterministic tools (calculator)
- implement short-term conversational memory
- combine tools, system prompt, and model into an agent

## Files and role

- `simple_llm.py` — initializes the LLM client and shows a minimal single-request example (loads API key from `.env` and calls the model).  
- `tool_chain.py` / calculator decorator — defines `@tool` wrappers (example: `safe_calculate`) that perform deterministic operations outside the LLM.  
- `memory.py` — implements message-based short-term memory, an agent without external tools, helper to extract agent output, demo and interactive modes.  
- `main.py` — composes model, tools, system prompt and agent; runs the interactive assistant that routes queries to tools or model as needed.

## Key behaviors
- Uses an LLM for natural language and delegates precise tasks to tools (calculator, basic questions).  
- Stores the conversation as a message list and passes it on each invoke to preserve short-term context. 

## Result
A working prototype agent demonstrating LLM calls, tool integration, and message-based memory suitable as a foundation for retrieval-augmented or fine-tuned assistants.
