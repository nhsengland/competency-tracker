from datetime import date

import pandas as pd
import streamlit as st
import yaml

st.set_page_config(layout="wide")

from database import get_connection

st.title("Competency Importer")
st.markdown("Upload a YAML file to import a competency framework.")

uploaded = st.file_uploader("Choose a YAML file", type=["yaml", "yml"])

if uploaded:
    raw = yaml.safe_load(uploaded)

    rows = []
    for band, competencies in raw.items():
        for competency, sub_competencies in competencies.items():
            for sub in sub_competencies:
                rows.append({
                    "band": str(band).strip(),
                    "competency": competency.strip(),
                    "sub_competency": sub.strip(),
                })

    df = pd.DataFrame(rows)
    st.subheader("Preview")
    st.dataframe(df, width="stretch")

    if st.button("Import", type="primary"):
        today = date.today().isoformat()
        with get_connection() as conn:
            existing = pd.read_sql_query(
                "SELECT band, competency, sub_competency FROM competencies", conn
            )
            existing_set = {
                (r["band"].strip(), r["competency"].strip(), r["sub_competency"].strip())
                for _, r in existing.iterrows()
            }
            new_rows = [
                r for r in rows
                if (r["band"].strip(), r["competency"].strip(), r["sub_competency"].strip())
                not in existing_set
            ]
            if new_rows:
                conn.executemany(
                    "INSERT INTO competencies (import_date, band, competency, sub_competency) VALUES (?, ?, ?, ?)",
                    [(today, r["band"], r["competency"], r["sub_competency"]) for r in new_rows],
                )
        skipped = len(rows) - len(new_rows)
        msg = f"Imported {len(new_rows)} sub-competenc{'y' if len(new_rows) == 1 else 'ies'}."
        if skipped:
            msg += f" {skipped} already existed and were skipped."
        st.success(msg)
