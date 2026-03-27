import streamlit as st
from database import init_db

init_db()

st.set_page_config(layout="wide")

st.title("Competency Tracker")
st.markdown("""
This app helps you track your professional development as an NHS Data Scientist against your competency framework.

Log the work you do day-to-day, map it to the competencies in your framework, and over time build up a clear picture
of where your strengths lie — and where the gaps are. Whether you're preparing for an appraisal, making the case for
a promotion, or figuring out what you need to develop to move to the next band, this tool gives you the evidence to
back it up.

---

### Getting started

Use the pages in the sidebar in order:

1. **Importer** — load your competency framework from a YAML file. You only need to do this once (or whenever your framework changes).
2. **Framework Viewer** — browse the competencies and sub-competencies in your imported framework, with filters by band and competency area.
3. **Activity Logger** — record a professional activity in STARR format (Situation, Task, Action, Result, Reflection) and tag it to one or more sub-competencies. Add a title for quick reference and use the Notes field for anything that doesn't fit neatly into the STARR structure.
4. **My Activities** — view, search and edit your logged activities.
5. **Visualiser** — see charts of your activity coverage across competencies and bands, so you can spot your strengths and identify areas to focus on.

---

*This app is in early development — more features are on the way.*
""")
