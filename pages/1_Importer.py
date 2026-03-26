from datetime import date

import pandas as pd
import streamlit as st
import yaml

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
                    "band": str(band),
                    "competency": competency,
                    "sub_competency": sub.strip(),
                })

    df = pd.DataFrame(rows)
    st.subheader("Preview")
    st.dataframe(df, width="stretch")

    if st.button("Import", type="primary"):
        today = date.today().isoformat()
        with get_connection() as conn:
            conn.executemany(
                "INSERT INTO competencies (import_date, band, competency, sub_competency) VALUES (?, ?, ?, ?)",
                [(today, r["band"], r["competency"], r["sub_competency"]) for r in rows],
            )
        st.success(f"Imported {len(rows)} sub-competencies.")
