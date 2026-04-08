import pandas as pd
import plotly.express as px
import streamlit as st

from database import get_connection
from nhs_style import apply_nhs_style, NHS_COLOURS

st.set_page_config(layout="wide")
apply_nhs_style()

st.title("Visualiser")
st.caption("Tip: hover over a bar to see the full sub-competency name.")

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

# Build a stable color map so both charts share the same competency colours
competency_list = sorted(counts["competency"].unique())
color_map = {c: NHS_COLOURS[i % len(NHS_COLOURS)] for i, c in enumerate(competency_list)}

# Truncate long labels for display; full text is shown in hover
_MAX = 70
counts["sub_competency_label"] = counts["sub_competency"].apply(
    lambda s: s if len(s) <= _MAX else s[:_MAX - 1] + "…"
)

fig = px.bar(
    counts,
    x="activity_count",
    y="sub_competency_label",
    color="competency",
    color_discrete_map=color_map,
    orientation="h",
    custom_data=["sub_competency"],
    labels={
        "activity_count": "Number of activities",
        "sub_competency_label": "Sub-competency",
        "competency": "Competency",
    },
    title="Activities per sub-competency",
)
fig.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>Activities: %{x}<extra></extra>"
)
fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    height=max(400, len(counts) * 30),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None),
)
st.plotly_chart(fig, width="stretch")

# --- Activities per competency ---
competency_counts = (
    counts.groupby("competency")["activity_count"]
    .sum()
    .reset_index()
    .sort_values("activity_count", ascending=True)
)

competency_counts["competency_label"] = competency_counts["competency"].apply(
    lambda s: s if len(s) <= _MAX else s[:_MAX - 1] + "…"
)

fig2 = px.bar(
    competency_counts,
    x="activity_count",
    y="competency_label",
    color="competency",
    color_discrete_map=color_map,
    orientation="h",
    custom_data=["competency"],
    labels={"activity_count": "Number of activities", "competency_label": "Competency"},
    title="Activities per competency",
)
fig2.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>Activities: %{x}<extra></extra>"
)
fig2.update_layout(
    height=max(300, len(competency_counts) * 40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None),
)
st.plotly_chart(fig2, width="stretch")

