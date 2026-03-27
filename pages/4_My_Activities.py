from datetime import date

import pandas as pd
import streamlit as st

from database import get_connection

st.set_page_config(layout="wide")

st.title("My Activities")

st.markdown("""
<style>
/* Make each selected tag occupy its own full-width line */
span[data-baseweb="tag"] {
    width: 90% !important;
    max-width: 90% !important;
    margin-right: 0 !important;
}
span[data-baseweb="tag"] > span:first-child {
    max-width: 90% !important;
    overflow: hidden !important;
    text-overflow: unset !important;
}
</style>
""", unsafe_allow_html=True)

# Show success notification from a previous save
if st.session_state.pop("save_success", False):
    st.success("Activity updated successfully.")

# ── Load activities (one row per activity, competencies aggregated) ──────────
with get_connection() as conn:
    activities_df = pd.read_sql_query(
        """
        SELECT
            a.id,
            a.title,
            a.start_date,
            a.end_date,
            a.date_added,
            a.situation,
            a.task,
            a.action,
            a.result,
            a.reflection,
            a.notes,
            COUNT(ac.competency_id) AS sub_competency_count
        FROM activities a
        LEFT JOIN activity_competencies ac ON ac.activity_id = a.id
        GROUP BY a.id
        ORDER BY a.start_date DESC
        """,
        conn,
    )

if activities_df.empty:
    st.info("No activities logged yet. Use the Activity Logger to add some.")
    st.stop()

# ── Activity table with per-row Edit buttons ─────────────────────────────────
header_cols = st.columns([4, 2, 2, 2, 1])
for label, col in zip(["Title", "Start", "End", "# Sub-competencies", ""], header_cols):
    col.markdown(f"**{label}**")
st.divider()

for _, row in activities_df.iterrows():
    cols = st.columns([4, 2, 2, 2, 1])
    cols[0].write(row["title"] or "—")
    cols[1].write(row["start_date"])
    cols[2].write(row["end_date"])
    cols[3].write(int(row["sub_competency_count"]))
    if cols[4].button("Edit", key=f"edit_{row['id']}"):
        st.session_state["editing_id"] = int(row["id"])
        st.rerun()

st.caption(f"{len(activities_df)} {'activity' if len(activities_df) == 1 else 'activities'} logged.")

st.download_button(
    label="Export to CSV",
    data=activities_df.drop(columns=["id"]).to_csv(index=False),
    file_name="activities.csv",
    mime="text/csv",
)

# ── Edit form ─────────────────────────────────────────────────────────────────
if "editing_id" not in st.session_state:
    st.stop()

editing_id = st.session_state["editing_id"]
activity = activities_df[activities_df["id"] == editing_id].iloc[0]

st.divider()
st.subheader(f"Edit activity — {activity['start_date']}")

with get_connection() as conn:
    competencies_df = pd.read_sql_query(
        "SELECT id, band, competency, sub_competency FROM competencies ORDER BY band, competency, sub_competency",
        conn,
    )
    tagged_labels = pd.read_sql_query(
        """
        SELECT 'Band ' || c.band || ' · ' || c.competency || ' · ' || c.sub_competency AS label
        FROM activity_competencies ac
        JOIN competencies c ON c.id = ac.competency_id
        WHERE ac.activity_id = ?
        """,
        conn,
        params=(editing_id,),
    )["label"].tolist()

competencies_df["label"] = (
    "Band " + competencies_df["band"] + " · "
    + competencies_df["competency"] + " · "
    + competencies_df["sub_competency"]
)
label_to_id = dict(zip(competencies_df["label"], competencies_df["id"]))

with st.form("edit_activity_form"):
    title = st.text_input("Title", value=activity["title"], placeholder="Brief description of the activity")

    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start date", value=date.fromisoformat(activity["start_date"]))
    end_date = col2.date_input("End date", value=date.fromisoformat(activity["end_date"]))

    situation = st.text_area("Situation", value=activity["situation"], placeholder="Describe the context or background...")
    task = st.text_area("Task", value=activity["task"], placeholder="What was your responsibility or goal?")
    action = st.text_area("Action", value=activity["action"], placeholder="What did you actually do?")
    result = st.text_area("Result", value=activity["result"], placeholder="What was the outcome?")
    reflection = st.text_area("Reflection", value=activity["reflection"], placeholder="What did you learn? What would you do differently?")
    notes = st.text_area("Notes", value=activity["notes"], placeholder="Anything else that doesn't fit the STARR format...")

    selected_labels = st.multiselect(
        "Tag sub-competencies (click the box below to search/browse)",
        options=list(label_to_id.keys()),
        default=tagged_labels,
    )

    submitted = st.form_submit_button("Save changes", type="primary")

if st.button("Cancel"):
    del st.session_state["editing_id"]
    st.rerun()

if submitted:
    if end_date < start_date:
        st.error("End date cannot be before start date.")
    else:
        with get_connection() as conn:
            conn.execute(
                """UPDATE activities
                   SET start_date=?, end_date=?, title=?, situation=?, task=?, action=?, result=?, reflection=?, notes=?
                   WHERE id=?""",
                (
                    start_date.isoformat(),
                    end_date.isoformat(),
                    title,
                    situation,
                    task,
                    action,
                    result,
                    reflection,
                    notes,
                    editing_id,
                ),
            )
            conn.execute("DELETE FROM activity_competencies WHERE activity_id=?", (editing_id,))
            conn.executemany(
                "INSERT INTO activity_competencies (activity_id, competency_id) VALUES (?, ?)",
                [(editing_id, label_to_id[label]) for label in selected_labels],
            )
        del st.session_state["editing_id"]
        st.session_state["save_success"] = True
        st.rerun()
