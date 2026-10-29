# 📝 My Task Tracker (Streamlit Version)

A clean, beginner-friendly Task Tracker web application built using **Python** and **Streamlit**. It allows you to organize your daily tasks with real-time statistics and persistent local storage using a simple JSON file.

Developed as a Week 1 mini-project for an AI Engineering course, replacing a traditional terminal-based menu with a modern, responsive web interface.

---

## 🌟 Features

- **👁️ View Tasks**: Dedicated View Tasks tab with a **View / Refresh Tasks** button and clean card layout showing task status (`⏳ Pending` or `✅ Done (Read)`).
- **➕ Add Task**: Form to add tasks with immediate validation against empty or whitespace-only titles.
- **📊 Live Statistics**: Instantly track **Total Tasks**, **Pending Tasks**, and **Completed Tasks**.
- **✅ Mark as Read / Done**: Mark any pending task as completed with one click, or toggle back to pending.
- **🗑️ Delete Task**: Remove tasks individually without affecting others.
- **💾 JSON Persistence**: All tasks are automatically saved to `tasks.json` so your tasks remain available when you refresh or restart the app.
- **🛡️ Robust Error Handling**:
  - Starts safely with an empty list if `tasks.json` does not exist.
  - Detects malformed or corrupted JSON files and prevents accidental data overwriting.
- **🚪 Exit / Stop Session**: Includes a sidebar exit option mimicking the CLI "Exit" menu functionality.

---

## 🛠️ Technologies Used

- **Python 3.11+**: Core programming language.
- **Streamlit**: Python framework for building interactive web applications.
- **JSON (`json` module)**: Python's built-in module for file reading and writing without requiring an external database.

---

## 📁 Project File Structure

```text
Assignment 2/
├── app.py                  # Main Streamlit web application
├── mini_task_tracker.py    # Terminal command-line version
├── tasks.json              # Local JSON file storing tasks
├── requirements.txt        # Project dependencies (Streamlit)
├── HOW_TO_RUN.txt          # Quick step-by-step instructions
├── test_app.py             # Automated test suite
└── README.md               # Project documentation
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure you have Python installed on your system. You can verify this by running:

```bash
python --version
```

### 2. Install Dependencies
Install Streamlit and other requirements using:

```bash
pip install -r requirements.txt
```

---

## 💻 How to Start the Application

### 1. Streamlit Web Version:
Run the Streamlit application using:

```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### 2. Terminal CLI Version:
You can also run the terminal-based menu using:

```bash
python mini_task_tracker.py
```

---

## 🧪 Testing

Run the automated unit test suite:

```bash
python test_app.py
```

