import os
import uuid
import sqlite3
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

# -------------------------
# Load Environment Variables
# -------------------------

load_dotenv()

# For Streamlit Cloud
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# -------------------------
# Streamlit Config
# -------------------------

st.set_page_config(
    page_title="AI SQL Task Manager",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI SQL Task Manager")

# -------------------------
# Create Database
# -------------------------

conn = sqlite3.connect("Tasks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('Pending','in_progress','completed'))
    DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

# -------------------------
# System Prompt
# -------------------------

SYSTEM_PROMPT = """
You are an intelligent SQL Task Manager.

You manage a SQLite database containing a table called tasks.

Rules:

- Use SQL tools whenever database access is required.
- Never invent task data.
- Show at most 10 tasks.
- Order results by created_at DESC.
- After INSERT, UPDATE or DELETE verify using SELECT.
- Display task lists as Markdown tables.

Table:

tasks(
id,
title,
description,
status,
created_at
)
"""
# -------------------------
# Load Agent
# -------------------------

@st.cache_resource
def load_agent():
    db = SQLDatabase.from_uri("sqlite:///Tasks.db")
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )
    toolkit = SQLDatabaseToolkit(
        db=db,
        llm=llm
    )
    memory = InMemorySaver()
    agent = create_agent(
        model=llm,
        tools=toolkit.get_tools(),
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory,
    )
    return agent
agent = load_agent()

# -------------------------
# Thread ID
# -------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}

# -------------------------
# Display Previous Messages
# -------------------------
try:
    state = agent.get_state(config)
    if state.values:
        for msg in state.values["messages"]:
            if msg.type == "human":
                with st.chat_message("user"):
                    st.markdown(msg.content)
            elif msg.type == "ai":
                if isinstance(msg.content, str) and msg.content.strip():
                    with st.chat_message("assistant"):
                        st.markdown(msg.content)
except Exception:
    pass

# -------------------------
# Chat Input
# -------------------------
prompt = st.chat_input("Manage your tasks using natural language...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = agent.invoke(
                    {
                        "messages": [
                            HumanMessage(content=prompt)
                        ]
                    },
                    config=config,
                )
                answer = response["messages"][-1].content
                st.markdown(answer)
            except Exception as e:
                st.error(str(e))
