import pandas as pd
import streamlit as st

from database import get_connection

st.set_page_config(layout="wide")

st.title("My Activities")

with get_connection() as conn:
    df = pd.read_sql_query(
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

if df.empty:
    st.info("No activities logged yet. Use the Activity Logger to add some.")
    st.stop()

st.dataframe(df, width="stretch", hide_index=True)
st.caption(f"{df['start_date'].nunique()} activities shown.")
