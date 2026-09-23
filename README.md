# Indian Fresher Job Market Analysis 2025

A data analytics project that explores the Indian fresher job market using a structured dataset
of 500 job listings. Built entirely with Python, Pandas, Plotly, and Streamlit — no machine
learning, just clean, focused data analysis and interactive visualisation.

---

## 📦 Tech Stack

| Tool / Library | Version | Purpose |
|----------------|---------|---------|
| **Python** | 3.10+ | Core programming language |
| **Pandas** | 2.0+ | Data loading, cleaning, transformation, and aggregation |
| **NumPy** | 1.26+ | Numerical operations and dtype handling |
| **Plotly Express** | 5.20+ | Interactive charts — bar, pie, box, histogram, heatmap |
| **Streamlit** | 1.35+ | Multi-page interactive web dashboard with sidebar filters |

### Why each tool was chosen

- **Pandas** handles all tabular data operations: reading the CSV, stripping whitespace,
  mapping binary flags to labels, groupby aggregations, and cross-tabulations.
- **NumPy** is used under the hood by Pandas for fast numeric operations and type coercion.
- **Plotly Express** produces fully interactive charts (hover, zoom, pan) that embed cleanly
  into Streamlit without any extra configuration.
- **Streamlit** turns Python functions into a shareable web app in minutes — sidebar filters
  instantly update every chart and KPI on the page without any JavaScript.

---

## 🗂 Dataset

**File:** `data/Indian_Fresher_Salary_Skills_2025.csv`

| Property | Value |
|----------|-------|
| Total records | 500 job listings |
| Total columns | 21 |
| Graduation cohorts covered | 2023, 2024, 2025 |
| Roles | 8 unique roles |
| Companies | 8 companies |
| Cities | 8 cities |
| States | 7 states |

### Column Reference

| Column | Type | Description |
|--------|------|-------------|
| `job_id` | String | Unique identifier for each job listing |
| `role` | String | Job role (e.g. Data Scientist, Software Engineer) |
| `company` | String | Hiring company name |
| `company_type` | String | Product-Based / Service-Based / MNC / Startup |
| `city` | String | City where the job is located |
| `state` | String | State where the job is located |
| `degree` | String | Required degree (B.Tech, M.Tech, BCA, B.Sc, B.Com, MCA) |
| `graduation_year` | Integer | Candidate's expected graduation year (2023–2025) |
| `skills` | String | Comma-separated list of required skills (up to 3) |
| `primary_skill` | String | The single most important skill for the role |
| `experience_required` | Integer | 0 = Fresher, 1 = Some prior experience required |
| `internship_experience` | Integer | 1 = Internship done, 0 = No internship |
| `remote` | Integer | 1 = Remote role, 0 = On-Site role |
| `work_type` | String | Full-Time or Internship |
| `salary_lpa` | Float | Annual salary offered in Lakhs Per Annum (LPA) |
| `stipend_if_intern` | Integer | Monthly stipend in ₹ (if work_type is Internship) |
| `selection_rounds` | Integer | Total number of selection stages (2–5) |
| `aptitude_test` | Integer | 1 = Aptitude test was part of the process |
| `coding_test` | Integer | 1 = Coding test was part of the process |
| `interview_count` | Integer | Number of interview rounds conducted |
| `offer_made` | Integer | 1 = Offer extended to candidate, 0 = No offer |

---

## 🔍 How the Data Was Analysed

The analysis is split into five focused areas, each handled by a dedicated module.

### 1. Data Cleaning — `modules/data_loader.py`

Before any analysis, the raw CSV goes through a 7-step cleaning pipeline:

1. **Whitespace stripping** — all string columns trimmed of leading/trailing spaces.
2. **Case standardisation** — categorical fields normalised to Title Case; common acronyms
   corrected (e.g. `Sql → SQL`, `Aws → AWS`, `Power Bi → Power BI`, `Mnc → MNC`).
3. **Binary flag decoding** — integer flags (0/1) mapped to readable labels:
   - `remote` → `Remote / On-Site`
   - `internship_experience` → `Yes / No`
   - `aptitude_test` → `Yes / No`
   - `coding_test` → `Yes / No`
   - `offer_made` → `Offer Made / No Offer`
4. **Skills list expansion** — the comma-separated `skills` string is parsed into a Python
   list (`skills_list`) so each skill can be counted and compared individually.
5. **Duplicate removal** — checked and confirmed 0 duplicate rows.
6. **Missing value check** — confirmed 0 missing values in any column.
7. **Dtype enforcement** — numeric columns explicitly cast to `float64` / `int64`.

---

### 2. Job Distribution Analysis — `modules/analysis.py` → `pages_app/page_jobs.py`

**What was measured:** How job listings are distributed across roles, companies, cities,
states, degrees, work types, and graduation years.

**How it was done:**
- `value_counts()` on each categorical column to get frequency and percentage share.
- Grouped bar charts and pie charts reveal dominant roles, top hiring companies, and
  location concentrations.
- A **city × role heatmap** (`px.imshow` on a pivot table) shows which cities hire most
  for each role.
- Cross-tabulations of role vs. work type and role vs. remote flag highlight flexibility
  patterns per profession.

---

### 3. Salary Analysis — `modules/analysis.py` → `pages_app/page_salary.py`

**What was measured:** How salary (LPA) varies by role, company, city, state, degree,
experience level, internship background, work type, primary skill, and graduation year.

**How it was done:**
- `groupby(...)[salary_lpa].agg([mean, median, min, max, count])` for each grouping
  variable — giving a complete picture of the salary range, not just the average.
- Box plots (`px.box`) for company type and work type show the full salary spread including
  outliers.
- A histogram (`px.histogram`) reveals the overall salary distribution shape.
- Internship vs. no-internship comparison quantifies the salary premium from prior
  work experience.

---

### 4. Skills Analysis — `modules/analysis.py` → `pages_app/page_skills.py`

**What was measured:** Which skills appear most often, which roles require which skills,
how many roles each skill spans, and which skills are associated with higher salaries.

**How it was done:**
- The `skills_list` column (a Python list per row) is **exploded** into a long-form
  DataFrame (one row per job–skill pair) using a custom `_explode_skills()` helper.
- Counting rows in the exploded frame gives the true **frequency** of each skill across
  all listings.
- A `groupby(role)` on the exploded frame finds the **top 3 skills per role**.
- Joining the exploded frame back to `salary_lpa` and taking the mean gives the
  **average salary for jobs that list each skill**.
- The primary skill column is analysed separately to identify the single most-valued
  skill per listing.

---

### 5. Selection Process & Offer Analysis — `modules/analysis.py` → `pages_app/page_selection.py`

**What was measured:** How aptitude tests, coding tests, number of selection rounds,
interview count, and internship experience influence whether an offer is made.

**How it was done:**
- `groupby(selection_rounds)[offer_made].mean()` computes the **offer rate at each
  round count**, showing the optimal selection depth.
- A `groupby([aptitude_done, coding_done])` cross-tab shows the **offer rate for every
  combination** of test types (neither / aptitude only / coding only / both).
- Grouping by `internship_done` compares offer rates and average salaries for candidates
  with and without internship experience.
- A **selection funnel** table counts total applicants → aptitude test takers → coding
  test takers → interviewed → offers made, giving a top-down view of the hiring pipeline.

---

## 🖥 Dashboard Pages

| Page | What It Shows |
|------|---------------|
| 📊 **Overview** | 8 KPI metrics, salary distribution, top role chart, top skills bar |
| 💼 **Job Distribution** | Jobs by role, company, city, state, degree, work type, heatmap |
| 💰 **Salary Analysis** | Salary by role, company, location, degree, internship, skill |
| 🛠 **Skills Analysis** | Skill frequency, top skills per role, salary by skill |
| 🎯 **Selection Process** | Offer funnel, offer rate by rounds / tests / internship |
| 🗃 **Raw Data** | Browse, inspect, and download the cleaned dataset as CSV |
| 📄 **Project Report** | Full written report with findings, insights, and limitations |

---

## ▶ How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the dashboard from inside the project folder
cd fresher_job_analysis
streamlit run app.py or python -m streamlit run app.py
```

Open **http://localhost:8501** in your browser. Use the sidebar to navigate pages and
apply filters (role, state, city, work type, remote, degree, experience, internship, skill).

---

## 📁 Project Structure

```
fresher_job_analysis/
├── app.py                        ← Streamlit entry point + global sidebar filters
├── requirements.txt              ← Python dependencies
├── README.md
├── project_report.html           ← Standalone HTML report (open in any browser)
├── data/
│   └── Indian_Fresher_Salary_Skills_2025.csv
├── modules/
│   ├── data_loader.py            ← Load CSV → clean → return DataFrame
│   ├── analysis.py               ← All KPIs, stats, groupbys, skill explosion
│   └── charts.py                 ← 30+ Plotly chart functions
└── pages_app/
    ├── page_overview.py          ← KPI summary dashboard
    ├── page_jobs.py              ← Job distribution analysis
    ├── page_salary.py            ← Salary analysis
    ├── page_skills.py            ← Skills demand analysis
    ├── page_selection.py         ← Selection process & offer analysis
    ├── page_data.py              ← Raw data explorer + CSV download
    └── page_report.py            ← Full project report (rendered in-app)
```
