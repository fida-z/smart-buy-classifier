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
    color: black;
}

div[data-testid="stMetricLabel"] p {
    font-family: 'Roboto', sans-serif;
    font-size: 1.05rem !important;
    color: var(--accent) !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 0;
}

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

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 1200px;
}

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

[data-testid="stText"] {
    font-size: 1.3rem !important;                 
    font-weight: 600 !important;
    color: var(--accent) !important;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    margin-bottom: 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid var(--accent);         
    display: block;
}

[data-testid="stMarkdownContainer"] p {
    font-size: 0.95rem;
    color: var(--text-secondary);
}

div[data-testid="stMetricValue"] p {
    font-family: 'Roboto', sans-serif;
    font-size: 1.25 rem !important;
    color: var(--accent-value) !important;
    font-weight: 700 !important;
    line-height: 1.2;
    margin: 0;
    white-space: normal !important;      
    overflow-wrap: break-word;           
    word-break: break-word;              
}

div[data-testid="stMetric"] {
    background-color: var(--bg-card);
    border: 1px solid var(--border-light) !important;
    border-left: 4px solid var(--accent) !important;   
    border-radius: 10px;
    padding: 1.25rem 1.4rem;                            
    box-shadow: 0 1px 4px rgba(22,51,92,0.08);
    transition: border-color 0.15s ease;
}
div[data-testid="stMetric"]:hover {
    border-color: var(--border-strong) !important;
    border-left-color: var(--accent) !important;        


    div[data-testid="stMetricLabel"] {
    font-family: 'Roboto', sans-serif;
    font-size: 1.05rem !important;                       
    color: var(--accent) !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

div[data-testid="stMetricValue"] {
    font-family: 'Roboto', sans-serif;
    font-size: 1.75rem !important;                       
    color: var(--accent-value) !important;
    font-weight: 700 !important;
    line-height: 1.2;                                    
}

div[data-testid="stMetricDelta"] {
    font-family: 'Roboto', sans-serif;
    font-size: 0.9rem !important;
}

div[data-testid="column"] div[data-testid="stMetric"] {
    margin-bottom: 0.5rem;
}

hr {
    border-color: var(--border-light) !important;
    margin: 1.75rem 0 !important;
}

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

section[data-testid="stSidebar"] label p {
    font-size: 1rem !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

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

[data-testid="stPyplotGlobalUse"], .element-container:has(canvas) {
    border: 1px solid var(--border-light);
    border-radius: 10px;
    padding: 0.75rem;
    background-color: var(--bg-card);
}

</style>
"""
