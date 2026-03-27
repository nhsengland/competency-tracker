from datetime import date, datetime

import pandas as pd
import streamlit as st

from database import get_connection

st.set_page_config(layout="wide")

st.title("Activity Logger")
st.markdown("Record a professional activity in STARR format and tag it to one or more sub-competencies.")

with get_connection() as conn:
    competencies_df = pd.read_sql_query(
        "SELECT id, band, competency, sub_competency FROM competencies ORDER BY band, competency, sub_competency",
        conn,
    )

if competencies_df.empty:
    st.warning("No competencies found. Please import a framework first.")
    st.stop()

competencies_df["label"] = (
    "Band " + competencies_df["band"] + " · "
    + competencies_df["competency"] + " · "
    + competencies_df["sub_competency"]
)
label_to_id = dict(zip(competencies_df["label"], competencies_df["id"]))

with st.form("activity_form"):
    title = st.text_input("Title", placeholder="Brief description of the activity")

    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start date", value=date.today())
    end_date = col2.date_input("End date", value=date.today())

    situation = st.text_area("Situation", placeholder="Describe the context or background...")
    task = st.text_area("Task", placeholder="What was your responsibility or goal?")
    action = st.text_area("Action", placeholder="What did you actually do?")
    result = st.text_area("Result", placeholder="What was the outcome?")
    reflection = st.text_area("Reflection", placeholder="What did you learn? What would you do differently?")
    notes = st.text_area("Notes", placeholder="Anything else that doesn't fit the STARR format...")

    selected_labels = st.multiselect(
        "Tag sub-competencies",
        options=list(label_to_id.keys()),
    )

    submitted = st.form_submit_button("Save activity", type="primary")

if submitted:
    if not selected_labels:
        st.error("Please tag at least one sub-competency.")
    elif end_date < start_date:
        st.error("End date cannot be before start date.")
    elif not all([situation, task, action, result, reflection]):
        st.error("Please fill in all STARR fields.")
    else:
        date_added = datetime.now().isoformat(timespec="seconds")
        with get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO activities
                   (date_added, start_date, end_date, title, situation, task, action, result, reflection, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    date_added,
                    start_date.isoformat(),
                    end_date.isoformat(),
                    title,
                    situation,
                    task,
                    action,
                    result,
                    reflection,
                    notes,
                ),
            )
            activity_id = cursor.lastrowid
            conn.executemany(
                "INSERT INTO activity_competencies (activity_id, competency_id) VALUES (?, ?)",
                [(activity_id, label_to_id[label]) for label in selected_labels],
            )
        st.success(f"Activity saved and tagged to {len(selected_labels)} sub-competency(ies).")
