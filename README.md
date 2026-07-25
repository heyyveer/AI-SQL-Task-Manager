# 🤖 AI SQL Task Manager

An AI-powered Task Management Assistant that allows users to manage tasks using natural language.

Instead of writing SQL queries manually, users can simply chat with the assistant to create, update, delete, or retrieve tasks. The application leverages LangChain Agents, LangGraph Memory, Groq LLM, and SQLite to provide an intelligent conversational interface for database operations.

---

## 🚀 Features

- ✅ Create tasks using natural language
- ✅ View all tasks
- ✅ Update task status
- ✅ Delete tasks
- ✅ SQL Agent powered by LangChain
- ✅ Conversational memory using LangGraph Checkpointer
- ✅ SQLite database integration
- ✅ Streamlit Chat UI
- ✅ Automatic SQL generation
- ✅ Markdown table output for task lists

---

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- LangGraph
- Groq LLM
- SQLite
- SQLAlchemy

---

## 🏗 Architecture

```
User
   │
   ▼
Streamlit Chat UI
   │
   ▼
LangChain SQL Agent
   │
   ▼
Groq LLM
   │
   ▼
SQLDatabase Toolkit
   │
   ▼
SQLite Database
```

---

## 📂 Project Structure

```
AI-SQL-Task-Manager/
│
├── app.py
├── Tasks.db
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-SQL-Task-Manager.git
```

Move into the project

```bash
cd AI-SQL-Task-Manager
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
```

Run the application

```bash
streamlit run app.py
```

---

## 💬 Example Prompts

Create a task

```
Create a task to learn LangGraph tomorrow.
```

Show tasks

```
Show all tasks.
```

Update task

```
Mark task 1 as completed.
```

Delete task

```
Delete task 2.
```

Pending tasks

```
Show my pending tasks.
```

---

## 📸 Demo

Streamlit -- [https://ai-sql-task-manager.streamlit.app/]

---

## 🔮 Future Improvements

- PostgreSQL support
- User Authentication
- Due Dates & Priorities
- Task Categories
- Reminder Notifications
- Multi-user Support
- Dashboard Analytics
- Docker Deployment

---

## 📚 Key Concepts Demonstrated

- AI Agents
- Tool Calling
- LangChain SQL Toolkit
- LangGraph Memory
- Prompt Engineering
- LLM Function Calling
- Conversational Database Systems
- Natural Language to SQL

---

## 👨‍💻 Author

**Veer Tiwari**

AI Engineer | Machine Learning | Generative AI

---

⭐ If you found this project useful, consider giving it a star!
