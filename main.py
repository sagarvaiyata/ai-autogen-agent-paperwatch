import asyncio
import aioconsole
from dotenv import load_dotenv

from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

# <-- changed this from `from .agents import …` to an absolute import
from agents import (
    google_search_agent,
    arxiv_search_agent,
    report_agent,
    model_client
)

async def interactive_console(team):
    print("🖥️  LLM Agent Console")
    print(" • Type your task and press Enter.")
    print(" • Type 'TERMINATE', 'exit' or 'quit' to stop.\n")

    try:
        while True:
            task = (await aioconsole.ainput("Task> ")).strip()
            if not task or task.lower() in ("exit", "quit", "terminate"):
                print("\n👋 Goodbye!")
                break

            print("\n⏳ Thinking...\n")
            await Console(team.run_stream(task=task))
            print("\n" + "="*40 + "\n")

    except (EOFError, KeyboardInterrupt):
        print("\n\nInterrupted. Bye!")

async def main():
    load_dotenv()

    termination = TextMentionTermination("TERMINATE")
    team = RoundRobinGroupChat(
        participants=[google_search_agent, arxiv_search_agent, report_agent],
        termination_condition=termination
    )

    await interactive_console(team)
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())
