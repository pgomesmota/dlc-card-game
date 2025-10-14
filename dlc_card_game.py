# streamlit_app.py
import random
import streamlit as st
from base64 import b64encode

# ---------- App config ----------
st.set_page_config(
    page_title="Data & AI Literacy - Card Game",
    page_icon="🧠",
    layout="centered"
)

# ---------- Brand / theme ----------
BRAND_RED = "#E9462E"
BLACK = "#111111"

# Load logo (root: dlc-logo.png)
LOGO_PATH = "dlc-logo.png"
with open(LOGO_PATH, "rb") as f:
    LOGO_B64 = b64encode(f.read()).decode()

# ---------- Mini-decks ----------
AI_CARDS = ["WHY?", "HOW?", "WHO?", "WHEN?", "WHAT?", "WHERE?", "WHAT FOR?", "WHAT IF?", "WHICH?"]
DATA_CARDS = ["Marketing", "Communications", "Training", "Change Management", "Leadership", "Tools", "Governance", "Mindset", "Culture"]

# ---------- CSS (escaped braces for f-string) ----------
CSS = f"""
<style>
:root {{
  --accent: {BRAND_RED};
  --text: {BLACK};
  --bg: #ffffff;
}}

/* Keep things compact to avoid scroll */
html, body, [data-testid="stAppViewContainer"] {{
  background: var(--bg) !important;
  color: var(--text);
}}
/* Trim Streamlit default paddings */
[data-testid="stSidebar"], .block-container {{
  padding-top: 10px !important;
  padding-bottom: 10px !important;
}}
.block-container {{
  padding-left: 14px !important;
  padding-right: 14px !important;
}}

/* Page wrapper uses viewport to minimize scroll */
.page {{
  display: grid;
  grid-template-rows: auto auto 1fr auto;
  row-gap: 10px;
  min-height: calc(100vh - 24px);
}}

/* Header: logo + title aligned */
.header {{
  display: flex;
  align-items: center;
  gap: 12px;
}}
.header .logo img {{
  width: clamp(44px, 12vw, 60px);
  height: auto;
  border-radius: 6px;
}}
.header .titles h1 {{
  margin: 0;
  font-size: clamp(1.35rem, 5.2vw, 2rem);
  line-height: 1.15;
  font-weight: 900;
  color: var(--text);
}}

/* How it works */
.how {{
  font-size: clamp(0.9rem, 3.4vw, 1rem);
  margin: 0;
}}
.how b, .how strong {{
  color: var(--accent);
}}

/* Cards row: always two columns */
.cards {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  align-items: stretch;
}}

/* Card */
.card {{
  border-radius: 14px;
  padding: 14px 12px;
  border: 1.5px solid var(--accent);
  background: #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 6px;
  min-height: 120px;
}}
.card .icon {{
  font-size: clamp(22px, 6vw, 28px);
  line-height: 1;
}}
.card .title {{
  font-size: clamp(1.1rem, 4.8vw, 1.5rem);
  font-weight: 900;
  letter-spacing: 0.6px;
  text-transform: uppercase;           /* UPPERCASE inside cards */
}}
.card .hint {{
  font-size: clamp(0.78rem, 3.4vw, 0.9rem);
  color: var(--accent);
  font-weight: 700;
  letter-spacing: 0.6px;
  text-transform: uppercase;           /* UPPERCASE inside cards */
}}

/* Button – compact, large tap target */
.stButton > button {{
  width: 100%;
  padding: 12px 14px;
  border-radius: 12px;
  border: 2px solid var(--accent);
  background: var(--accent);
  color: #fff;
  font-weight: 800;
  font-size: clamp(0.95rem, 3.8vw, 1rem);
}}
.stButton > button:hover {{ filter: brightness(0.96); }}

/* Reduce gaps between blocks to keep on one screen */
.element-container:has(.cards) {{ margin-bottom: 6px; }}
.element-container:has(.how) {{ margin-bottom: 6px; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------- State ----------
if "ai_pick" not in st.session_state:
    st.session_state.ai_pick = random.choice(AI_CARDS)
if "data_pick" not in st.session_state:
    st.session_state.data_pick = random.choice(DATA_CARDS)

def deal_pair():
    st.session_state.ai_pick = random.choice(AI_CARDS)
    st.session_state.data_pick = random.choice(DATA_CARDS)

# ---------- UI ----------
st.markdown('<div class="page">', unsafe_allow_html=True)

# Header (aligned)
st.markdown(
    f"""
<div class="header">
  <div class="logo">
    <img src="data:image/png;base64,{LOGO_B64}" alt="DLC logo" />
  </div>
  <div class="titles">
    <h1>Data & AI Literacy - Card Game</h1>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# How it works (merged instructions + tip)
st.markdown(
    """
<p class="how">
  <strong>How it works:</strong> Tap <b>Generate card pair</b> to deal two cards side by side:
  one <b>AI</b> card (a <em>question</em>) and one <b>DATA</b> card (a <em>domain</em>).  
  In your group, connect the question to the domain and discuss implications for <b>Data & AI Literacy</b>
  (e.g., value, risks, governance, skills, tools). Keep it short and focused—aim for a 60–90 second exchange per pair.
</p>
""",
    unsafe_allow_html=True,
)

# Cards (always side-by-side)
st.markdown('<div class="cards">', unsafe_allow_html=True)

st.markdown(
    f"""
<div class="card">
  <div class="icon">🧠</div>
  <div class="title">{st.session_state.ai_pick}</div>
  <div class="hint">AI card</div>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown(
    f"""
<div class="card">
  <div class="icon">📊</div>
  <div class="title">{st.session_state.data_pick.upper()}</div>
  <div class="hint">DATA card</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)

# Button
st.button("🎲 Generate card pair", on_click=deal_pair, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
