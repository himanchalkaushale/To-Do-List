import streamlit as st
import os
import json
import re  # For JS parsing

# -----------------------------
# Configuration
# -----------------------------
DATA_FILE = "tasks.json"
PROBLEMS_JS_FILE = "450DSAFinal.js"  # Optional for DSA clone

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

def load_problems_from_js():
    if not os.path.exists(PROBLEMS_JS_FILE):
        return []
    with open(PROBLEMS_JS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract JSON-like array
    start_idx = content.find("[")
    end_idx = content.rfind("]") + 1
    if start_idx == -1 or end_idx == -1:
        st.error("Invalid file format: Missing [ or ] in JS file.")
        return []

    json_like = content[start_idx:end_idx]

    # Convert JS syntax to JSON
    json_like = json_like.replace("'", '"')
    json_like = re.sub(r'(\w+):', r'"\1":', json_like)  # Quote keys
    json_like = re.sub(r',\s*([}\]])', r'\1', json_like)  # Remove trailing commas

    try:
        problems = json.loads(json_like)
        for i, p in enumerate(problems):
            p["id"] = int(p.get("id", i + 1))
        return problems
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JS file: {e}")
        st.code(json_like)
        return []

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Modern To-Do List", layout="centered")

# Custom CSS
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
    .task-text {
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 10px;
    }
    .full-width {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📝 Modern To-Do List")
st.markdown("A beautiful, interactive to-do list built with **Streamlit**.")

# -----------------------------
# Input New Task (Full Width)
# -----------------------------
with st.form("add_task_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        new_task = st.text_input("Add a new task:", key="new_task_input", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("➕ Add")

    if submitted and new_task.strip() != "":
        tasks = load_tasks()
        tasks.append({"task": new_task, "done": False})
        save_tasks(tasks)
        st.rerun()

# -----------------------------
# Load Tasks
# -----------------------------
tasks = load_tasks()

# -----------------------------
# Display Tasks
# -----------------------------
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

    # Edit Form
    with st.expander("✏️ Edit Task"):
        with st.form(key=f"edit_form_{idx}"):
            updated_task = st.text_input("Edit task:", value=t["task"], key=f"edit_input_{idx}", label_visibility="collapsed")
            update_button = st.form_submit_button("💾 Update")

            if update_button and updated_task.strip() != "":
                tasks[idx]["task"] = updated_task.strip()
                save_tasks(tasks)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Clear All Button
# -----------------------------
if tasks and st.button("❌ Clear All Tasks", use_container_width=True):
    tasks.clear()
    save_tasks(tasks)
    st.rerun()
