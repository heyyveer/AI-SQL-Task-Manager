from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

st.set_page_config(
    page_title="TaskBot SQL Agent",
    page_icon="🤖"
)

st.title("🤖 TaskBot - SQL Agent")

SYSTEM_PROMPT = """
You are a Task Management Assistant.

You have access to a SQLite database containing a table named 'tasks'.

Rules:

- Help users create, update, delete and read tasks.
- Never make up data.
- Use SQL tools whenever database access is required.
- After INSERT/UPDATE/DELETE always verify the result with a SELECT query.
- Limit SELECT results to 10 rows.
- Order by created_at DESC.
- When displaying multiple tasks, return them as a markdown table.

Table:

tasks(
id INTEGER PRIMARY KEY,
title TEXT,
description TEXT,
status TEXT,
created_at TIMESTAMP
)
"""


@st.cache_resource
def load_agent():

    db = SQLDatabase.from_uri("sqlite:///Tasks.db")

    llm = ChatGroq(
        model="openai/gpt-oss-20b"
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
        checkpointer=memory
    )

    return agent


agent = load_agent()

config = {
    "configurable": {
        "thread_id": "streamlit-user"
    }
}

# ------------------------
# Render previous messages
# ------------------------

state = agent.get_state(config)

if state.values:

    for msg in state.values["messages"]:

        # User messages
        if msg.type == "human":

            with st.chat_message("user"):
                st.markdown(msg.content)

        # Assistant messages
        elif msg.type == "ai":

            # Skip tool-call messages
            if not msg.content:
                continue

            if isinstance(msg.content, str):

                if msg.content.strip() == "":
                    continue

                with st.chat_message("assistant"):
                    st.markdown(msg.content)

# ------------------------
# Chat
# ------------------------

prompt = st.chat_input("Ask me anything about your tasks...")

if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

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