# 🗓️ Deadline Manager

A simple Deadline Management app built with **FastAPI** for the backend and **Tkinter** for the frontend.

## 💡 Features

- ✅ Add deadlines with descriptions
- 📅 View all saved deadlines
- 🔔 Get notified on the day of the deadline
- 🔁 Periodic check for today’s tasks

## 🛠️ Tech Stack

- **Python**
- **FastAPI** – API backend
- **Tkinter** – GUI frontend
- **SQLite** – Local database
- **Requests** – HTTP communication between frontend & backend

## 📦 Installation

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
