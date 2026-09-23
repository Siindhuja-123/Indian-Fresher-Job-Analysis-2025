"""
app.py
------
Entry point for the Indian Fresher Job Analysis Streamlit dashboard.
Run with:  streamlit run app.py
"""

import sys
import os

# Make the modules package importable when run from the project root
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

# ── Page configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Indian Fresher Job Analysis 2025",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Import page modules ──────────────────────────────────────────────────────
from pages_app import (
    page_overview,
    page_jobs,
    page_salary,
    page_skills,
    page_selection,
    page_data,
    page_report,
)
from modules.data_loader import get_clean_data

# ── Cache data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return get_clean_data()

df_full = load_data()

# ── Sidebar navigation ───────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_India.svg",
    width=60,
)
st.sidebar.title("🇮🇳 Fresher Job Analysis")
st.sidebar.markdown("**Indian Fresher Salary & Skills 2025**")
st.sidebar.divider()

PAGES = {
    "📊 Overview":          "overview",
    "💼 Job Distribution":  "jobs",
    "💰 Salary Analysis":   "salary",
    "🛠 Skills Analysis":   "skills",
    "🎯 Selection Process": "selection",
    "🗃 Raw Data":           "data",
    "📄 Project Report":    "report",
}

selection = st.sidebar.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
page_key  = PAGES[selection]

# ── Global filters (sidebar) ─────────────────────────────────────────────────
st.sidebar.divider()
st.sidebar.subheader("🔍 Filters")

all_roles   = sorted(df_full["role"].unique())
all_states  = sorted(df_full["state"].unique())
all_cities  = sorted(df_full["city"].unique())
all_work    = sorted(df_full["work_type"].unique())
all_remote  = sorted(df_full["remote_work"].unique())
all_skills_flat = sorted({
    sk for sl in df_full["skills_list"] for sk in sl
})
all_degrees = sorted(df_full["degree"].unique())

sel_roles   = st.sidebar.multiselect("Role",      all_roles,   default=[])
sel_states  = st.sidebar.multiselect("State",     all_states,  default=[])
sel_cities  = st.sidebar.multiselect("City",      all_cities,  default=[])
sel_work    = st.sidebar.multiselect("Work Type", all_work,    default=[])
sel_remote  = st.sidebar.multiselect("Remote",    all_remote,  default=[])
sel_degrees = st.sidebar.multiselect("Degree",    all_degrees, default=[])
exp_filter  = st.sidebar.selectbox("Experience Required", ["All", "0 – Fresher", "1 – Some Experience"])
intern_filt = st.sidebar.selectbox("Internship Done",     ["All", "Yes", "No"])

# ── Apply filters ────────────────────────────────────────────────────────────
df = df_full.copy()

if sel_roles:
    df = df[df["role"].isin(sel_roles)]
if sel_states:
    df = df[df["state"].isin(sel_states)]
if sel_cities:
    df = df[df["city"].isin(sel_cities)]
if sel_work:
    df = df[df["work_type"].isin(sel_work)]
if sel_remote:
    df = df[df["remote_work"].isin(sel_remote)]
if sel_degrees:
    df = df[df["degree"].isin(sel_degrees)]
if exp_filter != "All":
    exp_val = 0 if "0" in exp_filter else 1
    df = df[df["experience_required"] == exp_val]
if intern_filt != "All":
    df = df[df["internship_done"] == intern_filt]

# Skill filter (applied after list explode)
sel_skill = st.sidebar.selectbox("Skill (any job listing)", ["All"] + all_skills_flat)
if sel_skill != "All":
    df = df[df["skills_list"].apply(lambda sl: sel_skill in sl)]

# Show active filter count
active = sum([
    bool(sel_roles), bool(sel_states), bool(sel_cities), bool(sel_work),
    bool(sel_remote), bool(sel_degrees),
    exp_filter != "All", intern_filt != "All", sel_skill != "All",
])
if active:
    st.sidebar.info(f"✅ {active} filter(s) active — {len(df):,} jobs shown")
else:
    st.sidebar.caption(f"Showing all {len(df):,} jobs")

# ── Route to page ────────────────────────────────────────────────────────────
if page_key == "overview":
    page_overview.show(df, df_full)
elif page_key == "jobs":
    page_jobs.show(df)
elif page_key == "salary":
    page_salary.show(df)
elif page_key == "skills":
    page_skills.show(df)
elif page_key == "selection":
    page_selection.show(df)
elif page_key == "data":
    page_data.show(df)
elif page_key == "report":
    page_report.show()
