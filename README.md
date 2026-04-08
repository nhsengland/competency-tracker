# Competency Tracker

A Streamlit app to help NHS Data Scientists track their professional development against a competency framework.

Log the work you do day-to-day, map it to the competencies in your framework, and over time build up a clear picture of where your strengths lie — and where the gaps are. Whether you're preparing for an appraisal, making the case for a promotion, or figuring out what you need to develop to move to the next band, this tool gives you the evidence to back it up.

## Set up

**1. Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -e .
```

**3. Run the app**

```bash
streamlit run Home.py
```

## Pages

1. **Importer** — load your competency framework from a YAML file. You only need to do this once (or whenever your framework changes).
2. **Framework Viewer** — browse the competencies and sub-competencies in your imported framework, with filters by band and competency area.
3. **Activity Logger** — record a professional activity in STARR format (Situation, Task, Action, Result, Reflection) and tag it to one or more sub-competencies. Add a title for quick reference and use the Notes field for anything that doesn't fit neatly into the STARR structure.
4. **My Activities** — view, search and edit your logged activities.
5. **Visualiser** — see charts of your activity coverage across competencies and bands, so you can spot your strengths and identify areas to focus on.

## Using in GitHub Codespaces

> **Important:** the database file (`competency_tracker_data.db`) is stored locally inside the codespace and is not committed to the repository. If your codespace is deleted, you will lose all your logged activities.
>
> Before closing or deleting a codespace, download the database file via the VS Code file explorer and keep it somewhere safe. To restore it, upload the file back into the repo root when you next open a codespace.
