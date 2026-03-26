import pandas as pd
import plotly.express as px
import streamlit as st

from database import get_connection

st.title("Visualiser")

with get_connection() as conn:
    df = pd.read_sql_query(
        """
        SELECT
            c.band,
            c.competency,
            c.sub_competency,
            a.id        AS activity_id,
            a.start_date
        FROM activity_competencies ac
        JOIN activities   a ON a.id = ac.activity_id
        JOIN competencies c ON c.id = ac.competency_id
        """,
        conn,
    )

if df.empty:
    st.info("No activities logged yet. Use the Activity Logger to add some.")
    st.stop()

# --- Sidebar filters ---
bands = ["All"] + sorted(df["band"].unique().tolist())
selected_band = st.sidebar.selectbox("Band", bands)
if selected_band != "All":
    df = df[df["band"] == selected_band]

# --- Chart ---
counts = (
    df.groupby(["competency", "sub_competency"])["activity_id"]
    .nunique()
    .reset_index()
    .rename(columns={"activity_id": "activity_count"})
)

fig = px.bar(
    counts,
    x="activity_count",
    y="sub_competency",
    color="competency",
    orientation="h",
    labels={
        "activity_count": "Number of activities",
        "sub_competency": "Sub-competency",
        "competency": "Competency",
    },
    title="Activities per sub-competency",
)
fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=max(400, len(counts) * 30))
st.plotly_chart(fig, width="stretch")

# --- Raw table ---
with st.expander("Raw activity data"):
    with get_connection() as conn:
        raw = pd.read_sql_query(
            """
            SELECT
                a.start_date,
                a.end_date,
                a.date_added,
                c.band,
                c.competency,
                c.sub_competency,
                a.situation,
                a.task,
                a.action,
                a.result,
                a.reflection
            FROM activity_competencies ac
            JOIN activities   a ON a.id = ac.activity_id
            JOIN competencies c ON c.id = ac.competency_id
            ORDER BY a.start_date DESC
            """,
            conn,
        )
    st.dataframe(raw, width="stretch", hide_index=True)
