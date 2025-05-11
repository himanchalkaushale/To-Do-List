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
        background-color: #f5f7fa;
    }
    .task-box {
        padding: 10px;
        margin: 10px 0;
        border-radius: 8px;
        background-color: white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .task-text {
        font-size: 16px;
    }
    .complete-btn {
        margin-right: 10px;
    }
    .delete-btn {
        color: red;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

st.title("📝 Modern To-Do List")
st.markdown("A simple yet elegant to-do list built with **Streamlit**.")

# Input new task
new_task = st.text_input("Add a new task:")
if st.button("Add Task"):
    if new_task.strip() != "":
        tasks = load_tasks()
        tasks.append({"task": new_task, "done": False})
        save_tasks(tasks)
        st.rerun()

# Load tasks
tasks = load_tasks()

# Display tasks
for idx, t in enumerate(tasks):
    status = "✅" if t["done"] else "🔲"
    task_text = f"~~{t['task']}~~" if t["done"] else t["task"]

    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col1:
        if not t["done"]:
            if st.button("✔️", key=f"complete_{idx}", help="Mark as done"):
                tasks[idx]["done"] = True
                save_tasks(tasks)
                st.rerun()
        else:
            st.write("✔️")

    with col2:
        st.markdown(f"<div class='task-text'>{task_text}</div>", unsafe_allow_html=True)

    with col3:
        if st.button("🗑️", key=f"delete_{idx}", help="Delete task"):
            tasks.pop(idx)
            save_tasks(tasks)
            st.rerun()

# Clear all button
if tasks and st.button("Clear All Tasks"):
    tasks.clear()
    save_tasks(tasks)
    st.rerun()
