import streamlit as st
import os
import json

# -----------------------------
# Configuration
# -----------------------------
DATA_FILE = "tasks.json"

# -----------------------------
# Helper Functions
# -----------------------------

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# -----------------------------
# App Layout & Logic
# -----------------------------

st.set_page_config(page_title="Modern To-Do List", layout="centered")

# Custom CSS for modern look
st.markdown("""
<style>
    body {
        background-color: #f0f2f6;
    }
    .task-card {
        background-color: white;
        padding: 15px 20px;
        margin-bottom: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 6px solid #4A90E2;
    }
    .task-done {
        border-left: 6px solid #27AE60;
        opacity: 0.7;
    }
    .task-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .task-text {
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 10px;
    }
    .task-actions button {
        margin-right: 5px;
    }
    .edit-input input {
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📝 Modern To-Do List")
st.markdown("A beautiful, interactive to-do list built with **Streamlit**.")

# Input new task
with st.form("add_task_form"):
    new_task = st.text_input("Add a new task:")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_task.strip() != "":
        tasks = load_tasks()
        tasks.append({"task": new_task, "done": False})
        save_tasks(tasks)
        st.rerun()

# Load tasks
tasks = load_tasks()

# Display tasks
for idx, t in enumerate(tasks):
    card_class = "task-card task-done" if t["done"] else "task-card"

    st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([6, 3, 2])

    with col1:
        task_text = f"~~{t['task']}~~" if t["done"] else t["task"]
        st.markdown(f"<div class='task-text'>{task_text}</div>", unsafe_allow_html=True)

    with col2:
        if not t["done"]:
            if st.button(f"✔️ Complete", key=f"complete_{idx}"):
                tasks[idx]["done"] = True
                save_tasks(tasks)
                st.rerun()
        else:
            if st.button(f"🔄 Reopen", key=f"reopen_{idx}"):
                tasks[idx]["done"] = False
                save_tasks(tasks)
                st.rerun()

    with col3:
        if st.button("🗑️ Delete", key=f"delete_{idx}"):
            tasks.pop(idx)
            save_tasks(tasks)
            st.rerun()

    # Edit form inside the card
    with st.expander("✏️ Edit Task"):
        with st.form(key=f"edit_form_{idx}"):
            updated_task = st.text_input("Edit task:", value=t["task"], key=f"edit_input_{idx}")
            update_button = st.form_submit_button("Update")

            if update_button and updated_task.strip() != "":
                tasks[idx]["task"] = updated_task.strip()
                save_tasks(tasks)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Clear all button
if tasks and st.button("❌ Clear All Tasks"):
    tasks.clear()
    save_tasks(tasks)
    st.rerun()
