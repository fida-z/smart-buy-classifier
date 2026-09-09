STYLES =  """
<style>

html, body, [class*="css"] {
    font-family: 'Roboto', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}

:root {
    --bg-main: #F5F9FE;         /* very light blue-white, main canvas */
    --bg-sidebar: #EAF2FC;      /* light blue-tinted sidebar */
    --bg-card: #FFFFFF;         /* metric/table cards stay clean white */
    --navy-secondary: #16335C;  /* deep navy — now used sparingly: metric box accents, sidebar border */
    --border-light: #C9DCF2;    /* soft light-blue border */
    --border-strong: #7FB0E0;   /* stronger light-blue border for hover/emphasis */
    --text-primary: #14203A;    /* near-navy, for body/heading text on white */
    --text-secondary: #5B7196;  /* muted blue-grey for secondary text */
    --accent: #2D7DD2;          /* classy light-mid blue — PRIMARY accent: headings, labels, buttons */
    --accent-value: #16335C;    /* navy — metric VALUES, for contrast against light label */
    --accent-soft: #E3EEFC;     /* pale blue fill, table headers etc. */
}

.stApp {
    background-color: var(--bg-main);
    color: var(--text-primary);
}



/* ---------- MODIFIED: Sidebar — light blue bg, navy border as secondary accent ---------- */
section[data-testid="stSidebar"] {
    background-color:  #9dc6eb;
    border-right: 1px solid var(--navy-secondary);
}

.st-emotion-cache-u1kubd > h2:nth-child(1) {
    font-size: 2rem !important;
    font-weight: 600;
}

.stForm {
    background-color: var(--bg-sidebar);
    border-width: 5px;
    border-color: var(--accent);
}


#\:r6\: {
    font-size: 2.5rem;
    color: black;
}

/* ---------- MODIFIED (v7): Metric LABEL — now targets the nested <p>, not just the outer div ---------- */
div[data-testid="stMetricLabel"] p {
    font-family: 'Roboto', sans-serif;
    font-size: 1.05rem !important;
    color: var(--accent) !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 0;
}

/* ---------- MODIFIED (v7): Metric VALUE — now targets the nested <p>, this is what was missing font-size increases before ---------- */
div[data-testid="stMetricValue"] p {
    font-family: 'Roboto', sans-serif;
    font-size: 1.75rem !important;
    color: var(--accent-value) !important;
    font-weight: 700 !important;
    line-height: 1.2;
    margin: 0;
}


.stAppToolbar {
    background-color: #9dc6eb;
}


/* ---------- UNCHANGED: Sidebar padding fix ---------- */
section[data-testid="stSidebar"] > div {
    padding-left: 1rem;
    padding-right: 1rem;
}
section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
    padding-top: 1rem !important;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 0.5rem !important;
}

/* ---------- UNCHANGED: Main section padding ---------- */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 1200px;
}

/* ---------- MODIFIED: Titles — dark navy text on light bg (was near-white on dark) ---------- */
h1 {
    font-family: 'Roboto', sans-serif;
    font-size: 1.95rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
    margin-bottom: 0.4rem !important;
    padding-bottom: 0.6rem !important;
    border-bottom: 2px solid var(--accent);
}

/* ---------- MODIFIED: Sidebar heading — primary blue text + navy underline (secondary accent) ---------- */
section[data-testid="stSidebar"] h2 {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: var(--accent) !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 1rem !important;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--navy-secondary);
}

/* ---------- MODIFIED: st.text() pseudo-headings — same primary blue treatment ---------- */
/* ---------- MODIFIED (v8): st.text() pseudo-headings — bigger font, divider now matches h1's accent divider ---------- */
[data-testid="stText"] {
    font-size: 1.3rem !important;                 /* CHANGED: was 1rem */
    font-weight: 600 !important;
    color: var(--accent) !important;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    margin-bottom: 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid var(--accent);         /* CHANGED: was 1px solid var(--border-light) — now matches h1's divider style exactly */
    display: block;
}
/* ---------- MODIFIED: general markdown text — muted blue-grey on light bg ---------- */
[data-testid="stMarkdownContainer"] p {
    font-size: 0.95rem;
    color: var(--text-secondary);
}

/* ---------- MODIFIED (v9): Metric VALUE — allow wrapping for long text values (e.g. segment labels) ---------- */
div[data-testid="stMetricValue"] p {
    font-family: 'Roboto', sans-serif;
    font-size: 1.75rem !important;
    color: var(--accent-value) !important;
    font-weight: 700 !important;
    line-height: 1.2;
    margin: 0;
    white-space: normal !important;      /* NEW: overrides Streamlit's default nowrap on metric values */
    overflow-wrap: break-word;           /* NEW: now actually takes effect since wrapping is allowed */
    word-break: break-word;              /* NEW: extra safety for very long unbroken strings */
}

/* ---------- MODIFIED (v6): Metric cards — bigger KPI-style card, left border now matches .stForm border-color (var(--accent)) ---------- */
div[data-testid="stMetric"] {
    background-color: var(--bg-card);
    border: 1px solid var(--border-light) !important;
    border-left: 4px solid var(--accent) !important;   /* CHANGED: was var(--navy-secondary) — now matches .stForm's border-color: var(--accent) */
    border-radius: 10px;
    padding: 1.25rem 1.4rem;                            /* CHANGED: was 1rem 1.1rem, more room for larger text */
    box-shadow: 0 1px 4px rgba(22,51,92,0.08);
    transition: border-color 0.15s ease;
}
div[data-testid="stMetric"]:hover {
    border-color: var(--border-strong) !important;
    border-left-color: var(--accent) !important;        /* CHANGED: was var(--navy-secondary) */
}

/* ---------- MODIFIED (v6): Metric LABEL — bumped from 0.95rem to 1.05rem, stays smaller than value ---------- */
div[data-testid="stMetricLabel"] {
    font-family: 'Roboto', sans-serif;
    font-size: 1.05rem !important;                       /* CHANGED: was 0.95rem */
    color: var(--accent) !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ---------- MODIFIED (v6): Metric VALUE — bumped from 1.15rem to 1.75rem, now the dominant KPI number ---------- */
div[data-testid="stMetricValue"] {
    font-family: 'Roboto', sans-serif;
    font-size: 1.75rem !important;                       /* CHANGED: was 1.15rem */
    color: var(--accent-value) !important;
    font-weight: 700 !important;
    line-height: 1.2;                                    /* NEW: prevents cramped look at larger size */
}

/* ---------- UNCHANGED: Metric delta ---------- */
div[data-testid="stMetricDelta"] {
    font-family: 'Roboto', sans-serif;
    font-size: 0.9rem !important;
}

/* ---------- UNCHANGED: Market Summary metric spacing (inherits label/value rules above) ---------- */
div[data-testid="column"] div[data-testid="stMetric"] {
    margin-bottom: 0.5rem;
}

/* ---------- MODIFIED: Dividers ---------- */
hr {
    border-color: var(--border-light) !important;
    margin: 1.75rem 0 !important;
}

/* ---------- MODIFIED: Form submit button — primary blue bg, white text (was blue-on-navy) ---------- */
button[kind="primary"] {
    background-color: var(--accent) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Roboto', sans-serif;
}
button[kind="primary"]:hover {
    background-color: var(--navy-secondary) !important;
}

/* ---------- MODIFIED: Input fields / selects — light bg, blue borders ---------- */
div[data-baseweb="select"] > div,
input[type="text"], input[type="number"] {
    border-radius: 6px !important;
    border-color: var(--border-light) !important;
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    font-family: 'Roboto', sans-serif;
}
div[data-baseweb="select"] > div:focus-within,
input[type="text"]:focus, input[type="number"]:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

/* ---------- MODIFIED: Sidebar widget labels ---------- */
section[data-testid="stSidebar"] label p {
    font-size: 1rem !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

/* ---------- MODIFIED: Table styling — white card, navy header text on pale blue fill ---------- */
div[data-testid="stTable"] table {
    font-family: 'Roboto', sans-serif;
    font-size: 0.9rem;
    background-color: var(--bg-card);
    color: var(--text-primary);
    border: 1px solid var(--border-light);
    border-radius: 8px;
    overflow: hidden;
}
div[data-testid="stTable"] thead th {
    background-color: var(--accent-soft) !important;
    color: var(--navy-secondary) !important;
    font-weight: 600;
    border-bottom: 1px solid var(--navy-secondary) !important;
}
div[data-testid="stTable"] tbody tr:nth-child(even) {
    background-color: rgba(45,125,210,0.04);
}
div[data-testid="stTable"] td, div[data-testid="stTable"] th {
    border-color: var(--border-light) !important;
}

/* ---------- MODIFIED: matplotlib chart container — white card, light border ---------- */
[data-testid="stPyplotGlobalUse"], .element-container:has(canvas) {
    border: 1px solid var(--border-light);
    border-radius: 10px;
    padding: 0.75rem;
    background-color: var(--bg-card);
}

</style>
"""
# ================== END CSS INJECTION BLOCK v6 ==================