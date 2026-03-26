import streamlit as st
from database import init_db

init_db()

st.set_page_config(layout="wide")

st.title("Competency Tracker")
st.markdown("""
Welcome! Use the pages in the sidebar to:

- **Importer** — load a competency framework from a YAML file
- **Viewer** — browse imported competencies
- **Activity Logger** — record a professional activity in STARR format
- **Visualiser** — see your activity coverage across competencies
""")
