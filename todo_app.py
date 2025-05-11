import streamlit as st
import json
import os

# -----------------------------
# Configuration
# -----------------------------
PROBLEMS_FILE = "problems.json"
PROGRESS_FILE = "user_progress.json"

# -----------------------------
# Helper Functions
# -----------------------------

def load_problems():
    if os.path.exists(PROBLEMS_FILE):
        with open(PROBLEMS_FILE, "r") as f:
            return json.load(f)
    return []

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_progress(completed):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(list(completed), f)

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="450DSA Clone", layout="wide")
st.title("📚 450DSA Clone - Master DSA for Interviews")

# Custom CSS
st.markdown("""
<style>
    body {
        background-color: #f9f9f9;
    }
    .problem-card {
        padding: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #4A90E2;
        background-color: white;
        border-radius: 6px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .completed {
        border-left: 4px solid #27AE60;
        opacity: 0.8;
    }
    .diff-easy { color: green; font-weight: bold; }
    .diff-medium { color: orange; font-weight: bold; }
    .diff-hard { color: red; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
problems = load_problems()
progress = load_progress()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filter Problems")
categories = sorted(set(p["category"] for p in problems))
selected_category = st.sidebar.selectbox("Select Category", ["All"] + categories)

search_term = st.sidebar.text_input("Search Problem Title")

# -----------------------------
# Main View
# -----------------------------
filtered = problems

if selected_category != "All":
    filtered = [p for p in filtered if p["category"] == selected_category]

if search_term:
    filtered = [p for p in filtered if search_term.lower() in p["title"].lower()]

st.subheader(f"Showing {len(filtered)} Problems ({selected_category})")

for p in filtered:
    with st.container():
        is_completed = p["id"] in progress
        card_class = "problem-card completed" if is_completed else "problem-card"
        diff_class = {
            "Easy": "diff-easy",
            "Medium": "diff-medium",
            "Hard": "diff-hard"
        }.get(p.get("difficulty", "Easy"), "diff-easy")

        col1, col2 = st.columns([10, 1])

        with col1:
            st.markdown(f"""
            <div class="{card_class}">
                <a href="{p['link']}" target="_blank"><strong>{p['title']}</strong></a><br>
                <small>Difficulty: <span class="{diff_class}">{p.get('difficulty', 'Easy')}</span></small>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if is_completed:
                if st.button("🔁 Undo", key=f"undo_{p['id']}"):
                    progress.remove(p["id"])
                    save_progress(progress)
                    st.rerun()
            else:
                if st.button("✅ Done", key=f"done_{p['id']}"):
                    progress.add(p["id"])
                    save_progress(progress)
                    st.rerun()

# -----------------------------
# Progress Summary
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.write(f"✅ Completed: {len(progress)} / {len(problems)}")
if st.sidebar.button("🗑️ Clear Progress"):
    save_progress(set())
    st.rerun()
