import streamlit as st

# ── NHS Identity Palette ──────────────────────────────────────────────────────
# https://www.england.nhs.uk/nhsidentity/identity-guidelines/colours/
# NHS Blue (#005EB8) and white must remain dominant.

NHS_COLOURS = [
    "#005EB8",  # NHS Blue
    "#009639",  # NHS Green
    "#41B6E6",  # NHS Light Blue
    "#003087",  # NHS Dark Blue
    "#ED8B00",  # NHS Orange
    "#00A9CE",  # NHS Aqua Blue
    "#330072",  # NHS Purple
    "#AE2573",  # NHS Pink
    "#78BE20",  # NHS Light Green
    "#0072CE",  # NHS Bright Blue
    "#006747",  # NHS Dark Green
    "#FFB81C",  # NHS Warm Yellow
]

_CSS = """
<style>
/* ── Top toolbar ──────────────────────────────────────────────────── */
header[data-testid="stHeader"] {
    background-color: #005EB8 !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #003087 !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebarNavItems"] span {
    color: white !important;
}
[data-testid="stSidebarNavItems"] a:hover span {
    color: #41B6E6 !important;
}

/* ── Headings ─────────────────────────────────────────────────────── */
h1 {
    color: #003087 !important;
    border-bottom: 3px solid #005EB8;
    padding-bottom: 0.4rem;
    margin-bottom: 1.2rem !important;
}
h2 {
    color: #005EB8 !important;
}
h3 {
    color: #0072CE !important;
}

/* ── Horizontal rules ─────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 2px solid #41B6E6 !important;
    margin: 1.2rem 0 !important;
}

/* ── Primary buttons ──────────────────────────────────────────────── */
[data-testid="baseButton-primary"],
[data-testid="stFormSubmitButton"] button {
    background-color: #005EB8 !important;
    color: white !important;
    border: 2px solid #005EB8 !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
}
[data-testid="baseButton-primary"]:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background-color: #003087 !important;
    border-color: #003087 !important;
}

/* ── Secondary buttons ────────────────────────────────────────────── */
[data-testid="baseButton-secondary"] {
    background-color: white !important;
    color: #005EB8 !important;
    border: 2px solid #005EB8 !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
}
[data-testid="baseButton-secondary"]:hover {
    background-color: #E8EDEE !important;
}

/* ── Download button ──────────────────────────────────────────────── */
[data-testid="stDownloadButton"] button {
    background-color: #425563 !important;
    color: white !important;
    border: 2px solid #425563 !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
}
[data-testid="stDownloadButton"] button:hover {
    background-color: #231f20 !important;
    border-color: #231f20 !important;
}

/* ── Alerts ───────────────────────────────────────────────────────── */
div[data-testid="stAlert"] > div[role="alert"] {
    border-radius: 4px !important;
}
.stSuccess > div[role="alert"] {
    background-color: #e6f4ec !important;
    border-left: 4px solid #009639 !important;
    color: #006747 !important;
}
.stInfo > div[role="alert"] {
    background-color: #e6f3fa !important;
    border-left: 4px solid #41B6E6 !important;
    color: #003087 !important;
}
.stWarning > div[role="alert"] {
    background-color: #fdf3e3 !important;
    border-left: 4px solid #ED8B00 !important;
    color: #231f20 !important;
}
.stError > div[role="alert"] {
    background-color: #faeaea !important;
    border-left: 4px solid #DA291C !important;
    color: #8A1538 !important;
}

/* ── Caption text ─────────────────────────────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #425563 !important;
}

/* ── Multiselect tags (full-width, NHS-coloured) ──────────────────── */
span[data-baseweb="tag"] {
    background-color: #005EB8 !important;
    color: white !important;
    width: 90% !important;
    max-width: 90% !important;
    margin-right: 0 !important;
}
span[data-baseweb="tag"] > span:first-child {
    max-width: 90% !important;
    overflow: hidden !important;
    text-overflow: unset !important;
    color: white !important;
}
span[data-baseweb="tag"] svg {
    fill: white !important;
}
</style>
"""


def apply_nhs_style() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
