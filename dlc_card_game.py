# streamlit_app.py
import random
import streamlit as st

# ---------- Brand / assets ----------
BRAND_RED = "#E9462E"  # DLC red
BLACK = "#111111"
LOGO_PATH = "/mnt/data/de31a37a-11e6-4fc0-a566-b321e6971d63.png"  # DLC logo

# ---------- App config ----------
st.set_page_config(
    page_title="Data & AI Literacy - Card Game",
    page_icon=LOGO_PATH,  # use DLC logo as page icon
    layout="centered"
)

# ---------- Data: the two mini-decks ----------
AI_CARDS = [
    "WHY?", "HOW?", "WHO?", "WHEN?", "WHAT?", "WHERE?",
    "WHAT FOR?", "WHAT IF?", "WHICH?"
]

DATA_CARDS = [
    "Marketing", "Communications", "Training", "Change Management",
    "Leadership", "Tools", "Governance", "Mindset", "Culture"
]

# ---------- Styles ----------
CARD_CSS = f"""
<style>
:root {{
  --accent: {BRAND_RED};
  --text: {BLACK};
  --bg: #ffffff;
}}
html, body, [data-testid="stAppViewContainer"] {{
  background: var(--bg) !important;
  color: var(--text);
  margin: 0 !important;
  padding: 0 !important;
}}
[data-testid="stElementContainer"] {{
  padding: 0 !important;
  margin: 0 !important;
}}
/* Header */
.header {{
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 0.6rem;
  flex-wrap: wrap;
}}
.header img {{
  width: 80px;
  height: auto;
  border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}}
.header-content h1 {{
  margin: 0;
  font-size: clamp(1.6rem, 4.6vw, 2.4rem);
  line-height: 1.15;
  color: var(--text);
  font-weight: 800;
}}
.header-content p {{
  margin: 6px 0 0 0;
  font-size: clamp(0.95rem, 3.2vw, 1.05rem);
  color: var(--text);
}}
.header-content b, .header-content .accent {{
  color: var(--accent);
  font-weight: 800;
}}
/* Cards grid */
.cards {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 6px;
}}
@media (max-width: 768px) {{
  .cards {{ grid-template-columns: 1fr; }}
}}
/* Card */
.card {{
  border-radius: 16px;
  padding: 18px 16px;
  border: 2px solid var(--accent);
  background: #fff;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  color: var(--text);
  min-height: 150px;
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 6px;
}}
.card .icon {{
  font-size: 34px;
  line-height: 1;
  color: var(--accent);
}}
.card .title {{
  font-size: clamp(1.4rem, 4.5vw, 1.9rem);
  font-weight: 900;
  letter-spacing: 0.2px;
  color: var(--text);
}}
.card .hint {{
  font-size: 0.95rem;
  color: var(--accent);
  font-weight: 700;
}}
/* Generate button */
.stButton > button {{
  width: 100%;
  padding: 14px 16px;
  border-radius: 12px;
  border: 2px solid var(--accent);
  background: var(--accent);
  color: #fff;
  font-weight: 800;
  font-size: 1rem;
}}
.stButton > button:hover {{ filter: brightness(0.95); }}
/* Footer tip */
.footer {{
  text-align: center;
  color: var(--text);
  font-size: 0.95rem;
  margin-top: 0.9rem;
}}
</style>
"""
st.markdown(CARD_CSS, unsafe_allow_html=True)

# ---------- State & helpers ----------
if "ai_pick" not in st.session_state:
    st.session_state.ai_pick = random.choice(AI_CARDS)
if "data_pick" not in st.session_state:
    st.session_state.data_pick = random.choice(DATA_CARDS)

def deal_pair():
    st.session_state.ai_pick = random.choice(AI_CARDS)
    st.session_state.data_pick = random.choice(DATA_CARDS)

# ---------- Header ----------
st.markdown(
    f"""
<div class="header">
    <img src="{LOGO_PATH}" alt="DLC logo">
    <div class="header-content">
        <h1>Data & AI Literacy - Card Game</h1>
        <p><span class="accent">Deal a pair:</span> one <b>AI</b> card (question) + one <b>DATA</b> card (domain).</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Cards ----------
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
  <div class="title">{st.session_state.data_pick}</div>
  <div class="hint">DATA card</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Button ----------
st.button("🎲 Generate card pair", on_click=deal_pair, use_container_width=True)

# ---------- Footer ----------
st.markdown(
    """
<div class="footer">Tip: Use each pair to spark a short discussion Data & AI Literacy.</div>
""",
    unsafe_allow_html=True,
)
