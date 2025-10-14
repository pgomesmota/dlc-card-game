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

# ---------- CSS ----------
CSS = f"""
<style>
:root {{
  --accent: {BRAND_RED};
  --text: {BLACK};
  --bg: #ffffff;
}}
html, body, [data-testid="stAppViewContainer"] {{
  background: var(--bg) !important; color: var(--text);
}}
.block-container {{ padding: 10px 12px !important; }}

.page {{
  display: grid; grid-template-rows: auto auto 1fr auto; row-gap: 8px;
  min-height: calc(100vh - 20px);
}}
/* Header */
.header {{ display: flex; align-items: center; gap: 10px; }}
.header .logo img {{ width: clamp(40px, 10vw, 56px); height: auto; border-radius: 6px; }}
.header .titles h1 {{
  margin: 0; font-size: clamp(1.1rem, 4.2vw, 1.6rem);
  line-height: 1.05; font-weight: 900; white-space: nowrap;  /* single line */
}}
/* Instructions (short & clean) */
.how {{ margin: 0; font-size: clamp(0.9rem, 3.3vw, 1rem); }}
.how b {{ color: var(--accent); }}

/* Cards row: always left/right */
.cards {{
  display: grid; grid-template-columns: 1fr 1fr; gap: 10px; align-items: stretch;
}}

/* 3D flip card */
.card3d {{ perspective: 1000px; }}
.card-inner {{
  position: relative; width: 100%; height: 100%;
  transform-style: preserve-3d; transition: transform 0.6s ease;
  min-height: 120px;
}}
.card-inner.flipped {{ transform: rotateY(180deg); }}   /* facedown */
.card-face {{
  position: absolute; inset: 0; border-radius: 14px; display: grid;
  grid-template-rows: auto 1fr auto; gap: 6px; padding: 12px 10px;
  backface-visibility: hidden;
}}
/* Front (content) */
.card-front {{
  border: 1.5px solid var(--accent); background: #fff; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}}
.card-front .icon {{ font-size: clamp(20px, 5.5vw, 26px); line-height: 1; }}
.card-front .title {{
  font-size: clamp(1rem, 4.2vw, 1.35rem); font-weight: 900; letter-spacing: 0.6px; text-transform: uppercase;
}}
.card-front .hint {{
  font-size: clamp(0.72rem, 3.2vw, 0.85rem); color: var(--accent); font-weight: 800; letter-spacing: 0.6px; text-transform: uppercase;
}}
/* Back (hidden face) */
.card-back {{
  transform: rotateY(180deg);                      /* show when flipped */
  background: #fff; border: 1.5px dashed var(--accent);
  display: grid; place-items: center; text-align: center;
}}
.card-back .backmark {{
  display: grid; place-items: center; gap: 6px;
  color: var(--accent); font-weight: 900;
}}
.card-back .logo-mini {{
  width: 36px; height: 36px; border-radius: 6px; overflow: hidden; margin: 0 auto;
}}
.card-back .label {{ font-size: 0.9rem; letter-spacing: 0.6px; }}
/* Button */
.stButton > button {{
  width: 100%; padding: 11px 12px; border-radius: 12px;
  border: 2px solid var(--accent); background: var(--accent); color: #fff;
  font-weight: 800; font-size: clamp(0.92rem, 3.6vw, 1rem);
}}
.stButton > button:hover {{ filter: brightness(0.96); }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------- State ----------
if "ai_pick" not in st.session_state:
    st.session_state.ai_pick = random.choice(AI_CARDS)
if "data_pick" not in st.session_state:
    st.session_state.data_pick = random.choice(DATA_CARDS)
if "revealed" not in st.session_state:
    st.session_state.revealed = False          # start facedown

def deal_and_reveal():
    st.session_state.ai_pick = random.choice(AI_CARDS)
    st.session_state.data_pick = random.choice(DATA_CARDS)
    st.session_state.revealed = True

# ---------- UI ----------
st.markdown('<div class="page">', unsafe_allow_html=True)

# Header
st.markdown(
    f"""
<div class="header">
  <div class="logo"><img src="data:image/png;base64,{LOGO_B64}" alt="DLC logo" /></div>
  <div class="titles"><h1>Data & AI Literacy - Card Game</h1></div>
</div>
""",
    unsafe_allow_html=True,
)

# Simple instructions
st.markdown(
    """
<p class="how">
  <b>How it works:</b> Press <b>Generate card pair</b> to flip and reveal one <b>AI</b> question and one <b>DATA</b> domain.
  Connect them and share a quick point on value, risks, governance, skills, or tools (≈60–90s).
</p>
""",
    unsafe_allow_html=True,
)

# Cards (left/right). When not revealed, show the back; when revealed, show front.
flipped_class = "" if st.session_state.revealed else "flipped"
st.markdown('<div class="cards">', unsafe_allow_html=True)

# ---- AI Card ----
st.markdown(
    f"""
<div class="card3d">
  <div class="card-inner {flipped_class}">
    <!-- front -->
    <div class="card-face card-front">
      <div class="icon">🧠</div>
      <div class="title">{st.session_state.ai_pick}</div>
      <div class="hint">AI CARD</div>
    </div>
    <!-- back -->
    <div class="card-face card-back">
      <div class="backmark">
        <div class="logo-mini">
          <img src="data:image/png;base64,{LOGO_B64}" alt="DLC" style="width:100%;height:100%;object-fit:cover;" />
        </div>
        <div class="label">AI CARD</div>
      </div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---- DATA Card ----
st.markdown(
    f"""
<div class="card3d">
  <div class="card-inner {flipped_class}">
    <!-- front -->
    <div class="card-face card-front">
      <div class="icon">📊</div>
      <div class="title">{st.session_state.data_pick.upper()}</div>
      <div class="hint">DATA CARD</div>
    </div>
    <!-- back -->
    <div class="card-face card-back">
      <div class="backmark">
        <div class="logo-mini">
          <img src="data:image/png;base64,{LOGO_B64}" alt="DLC" style="width:100%;height:100%;object-fit:cover;" />
        </div>
        <div class="label">DATA CARD</div>
      </div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)

# Button: deal + reveal
st.button("🎲 Generate card pair", on_click=deal_and_reveal, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
