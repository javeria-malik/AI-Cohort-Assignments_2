import json
import os
import streamlit as st

# File path for storing task data
TASKS_FILE = "tasks.json"


def load_tasks():
    """
    Load tasks from the JSON file.
    Returns a list of task dictionaries.
    If the file does not exist, returns an empty list.
    If the file is corrupted, warns the user without overwriting data.
    """
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                st.error("Warning: 'tasks.json' does not contain a valid list. Keeping existing file safe.")
                st.session_state.file_error = True
                return []
    except json.JSONDecodeError:
        st.error("Warning: 'tasks.json' contains malformed JSON. It will not be overwritten until resolved.")
        st.session_state.file_error = True
        return []
    except Exception as error:
        st.error(f"Error loading tasks: {error}")
        st.session_state.file_error = True
        return []


def save_tasks(tasks):
    """
    Save the given list of tasks to tasks.json using json.dump().
    Prevents overwriting if the JSON file was previously detected as corrupted.
    """
    if st.session_state.get("file_error", False):
        st.error("Cannot save tasks: 'tasks.json' is corrupted. Please repair the file to prevent data loss.")
        return False

    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
        return True
    except Exception as error:
        st.error(f"Error saving tasks: {error}")
        return False


def add_task(title):
    """
    Add a new task dictionary to the task list with a 'Pending' status (done=False)
    and save the updated list to tasks.json.
    """
    clean_title = title.strip()
    if clean_title:
        new_task = {"title": clean_title, "done": False}
        st.session_state.tasks.append(new_task)
        save_tasks(st.session_state.tasks)


def complete_task(index):
    """
    Mark the task at the given index as completed / read (done=True)
    and save the updated list to tasks.json.
    """
    if 0 <= index < len(st.session_state.tasks):
        st.session_state.tasks[index]["done"] = True
        save_tasks(st.session_state.tasks)


def toggle_task(index):
    """
    Toggle task status between Done (Read) and Pending (Unread).
    """
    if 0 <= index < len(st.session_state.tasks):
        current_status = st.session_state.tasks[index].get("done", False)
        st.session_state.tasks[index]["done"] = not current_status
        save_tasks(st.session_state.tasks)


def delete_task(index):
    """
    Delete the task at the given index and save the updated list to tasks.json.
    """
    if 0 <= index < len(st.session_state.tasks):
        st.session_state.tasks.pop(index)
        save_tasks(st.session_state.tasks)


def view_tasks():
    """
    Render all tasks in a clean card layout with status labels and action buttons.
    Includes explicit View/Refresh button and working Mark as Read controls.
    """
    col_header, col_refresh = st.columns([6, 4])
    with col_header:
        st.subheader("Your Tasks")
    with col_refresh:
        if st.button("👁 View / Refresh Tasks", key="btn_view_tasks", use_container_width=True):
            st.session_state.tasks = load_tasks()
            st.toast("Tasks refreshed from tasks.json!")

    if not st.session_state.tasks:
        st.info("No tasks yet. Add your first task to get started! 🎯")
        return

    for index, task in enumerate(st.session_state.tasks):
        title = task.get("title", "")
        is_done = task.get("done", False)
        safe_key = f"{index}_{title}"

        with st.container(border=True):
            col_info, col_complete, col_delete = st.columns([5, 3, 2])

            with col_info:
                if is_done:
                    st.markdown(f"**~~{title}~~**")
                    st.caption("Status: :green[**Done (Read)**] ✅")
                else:
                    st.markdown(f"**{title}**")
                    st.caption("Status: :orange[**Pending**] ⏳")

            with col_complete:
                if not is_done:
                    st.button(
                        "✅ Mark as Read",
                        key=f"mark_read_{safe_key}",
                        on_click=complete_task,
                        args=(index,),
                        use_container_width=True,
                    )
                else:
                    st.button(
                        "⏳ Mark as Pending",
                        key=f"mark_pending_{safe_key}",
                        on_click=toggle_task,
                        args=(index,),
                        use_container_width=True,
                    )

            with col_delete:
                st.button(
                    "🗑️ Delete",
                    key=f"delete_{safe_key}",
                    on_click=delete_task,
                    args=(index,),
                    use_container_width=True,
                )


def main():
    # Page setup
    st.set_page_config(
        page_title="My Task Tracker",
        page_icon="📝",
        layout="centered",
    )

    # Initialize session state for persistent tasks in memory
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()

    if "file_error" not in st.session_state:
        st.session_state.file_error = False

    # Sidebar: About and Exit option
    with st.sidebar:
        st.header("About")
        st.write("Welcome to **My Task Tracker**! A simple, beginner-friendly task management app built with Python and Streamlit.")
        st.divider()
        st.markdown("**Features:**")
        st.markdown("- ➕ Add new tasks")
        st.markdown("- 👁 View task list & status")
        st.markdown("- ✅ Mark tasks as completed / read")
        st.markdown("- 🗑️ Delete tasks")
        st.markdown("- 💾 Automatic JSON persistence")
        st.divider()

        # Exit functionality (preserves the CLI Exit menu requirement)
        if st.button("🚪 Exit Application", use_container_width=True):
            st.session_state.exited = True

    if st.session_state.get("exited", False):
        st.info("You have closed the application. You can safely close this browser tab or restart below.")
        if st.button("▶️ Resume Application"):
            st.session_state.exited = False
            st.rerun()
        st.stop()

    # App Header
    st.title("📝 My Task Tracker")
    st.write("Organize your daily tasks in one place.")
    st.divider()

    # Task Statistics / Metrics
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for task in st.session_state.tasks if task.get("done", False))
    pending_tasks = total_tasks - completed_tasks

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Total Tasks", total_tasks)
    metric_col2.metric("Pending Tasks", pending_tasks)
    metric_col3.metric("Completed Tasks", completed_tasks)

    st.divider()

    # Main Tabs: View Tasks & Add Task
    tab_view, tab_add = st.tabs(["👁 View Tasks", "➕ Add Task"])

    with tab_view:
        view_tasks()

    with tab_add:
        st.subheader("Add a New Task")
        with st.form("add_task_form", clear_on_submit=True):
            task_title_input = st.text_input(
                "Task Title",
                placeholder="e.g., Read Python notes",
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button("➕ Add Task", use_container_width=True)

            if submitted:
                clean_title = task_title_input.strip()
                if clean_title:
                    add_task(clean_title)
                    st.success(f"Task '{clean_title}' added successfully! 🎉")
                else:
                    st.warning("Task title cannot be empty or only spaces. Please enter a valid task name.")


if __name__ == "__main__":
    main()

