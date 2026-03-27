import pandas as pd
import streamlit as st

from database import get_connection

st.set_page_config(layout="wide")

st.title("Competency Framework Viewer")

with get_connection() as conn:
    df = pd.read_sql_query(
        "SELECT band, competency, sub_competency, import_date FROM competencies ORDER BY band, competency",
        conn,
    )

if df.empty:
    st.info("No competencies imported yet. Use the Importer page to load a framework.")
    st.stop()

bands = ["All"] + sorted(df["band"].unique().tolist())
selected_band = st.sidebar.selectbox("Band", bands)

if selected_band != "All":
    df = df[df["band"] == selected_band]

competencies = ["All"] + sorted(df["competency"].unique().tolist())
selected_competency = st.sidebar.selectbox("Competency", competencies)

if selected_competency != "All":
    df = df[df["competency"] == selected_competency]

st.dataframe(df, width="stretch", hide_index=True)
st.caption(f"{len(df)} sub-competencies shown.")
