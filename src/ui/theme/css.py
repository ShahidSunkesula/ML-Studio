"""
css.py

Global CSS for ML Studio.
"""

from src.ui.theme import colors
from src.ui.theme import spacing
from src.ui.theme import typography


GLOBAL_CSS = f"""
<style>

/* ==========================================================
   Main Layout
========================================================== */

.block-container {{
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}}



/* ==========================================================
   Buttons
========================================================== */

.stButton > button {{
    width: 100%;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
}}


/* ==========================================================
   Tabs
========================================================== */

.stTabs [role="tab"] {{
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}}

.stTabs [role="tab"][aria-selected="true"] {{
    background-color: {colors.PRIMARY};
    color: white;
}}


/* ==========================================================
   Sidebar
========================================================== */

section[data-testid="stSidebar"] {{
    border-right: 1px solid {colors.BORDER};
}}


/* ==========================================================
   DataFrames
========================================================== */

div[data-testid="stDataFrame"] {{
    border-radius: {spacing.CARD_RADIUS};
    overflow: hidden;
    border: 1px solid {colors.BORDER};
}}


/* ==========================================================
   Expanders
========================================================== */

details {{
    border-radius: {spacing.CARD_RADIUS};
    border: 1px solid {colors.BORDER};
}}


/* ==========================================================
   Inputs
========================================================== */

.stSelectbox,
.stTextInput,
.stNumberInput {{
    margin-bottom: 0.5rem;
}}


/* ==========================================================
   Progress Bar
========================================================== */

.stProgress > div > div {{
    border-radius: 10px;
}}


/* ==========================================================
   Horizontal Rule
========================================================== */

hr {{
    margin-top: 2rem;
    margin-bottom: 2rem;
}}


/* ==========================================================
   Headers
========================================================== */

h1 {{
    font-size: 2.2rem;
}}

h2 {{
    font-size: 1.4rem;
}}

h3 {{
    font-size: 1.0rem;
}}

</style>
"""