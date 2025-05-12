# app.py
import streamlit as st
import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import AsyncStreamBuffer
from agents import google_search_agent, arxiv_search_agent, report_agent

st.set_page_config(page_title="Literature Review Chat")

if "history" not in st.session_state:
    st.session_state.history = []

# build your team once
team = RoundRobinGroupChat(
    participants=[google_search_agent, arxiv_search_agent, report_agent],
    termination_condition=None  # or TextMentionTermination("TERMINATE")
)

def send_message(user_msg: str):
    st.session_state.history.append(("You", user_msg))
    buffer = AsyncStreamBuffer()
    # run the agents, streaming into our buffer
    async def run():
        await team.run_stream(task=user_msg, streamer=buffer)
    asyncio.run(run())
    full = buffer.get_text()  # all chunks concatenated
    st.session_state.history.append(("AI", full))

st.title("Literature Review Chat")
for role, msg in st.session_state.history:
    st.markdown(f"**{role}:** {msg}")

user_input = st.text_input("Your message", key="inp")
if st.button("Send"):
    send_message(user_input)
