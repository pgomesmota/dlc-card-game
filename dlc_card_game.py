# streamlit_app.py
import random
import base64
from pathlib import Path
import streamlit as st

# -------------------- Setup --------------------
st.set_page_config(
    page_title="Data & AI Literacy - Card Game",
    page_icon="🧠",
    layout="wide",
)

# DLC brand colors (tweak if you want an exact HEX)
DLC_ORANGE = "#EF4D37"  # primary
DLC_ORANGE_DARK = "#D43E2C"

def load_logo_b64():
    """Loads assets/dlc-logo.png if present and returns base64 string."""
    p = Path("dlc-logo.png")
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode("utf-8")
    return None

logo_b64 = load_logo_b64()

# -------------------- Mini-decks --------------------
AI_CARDS = [
    "WHY?", "HOW?", "WHO?", "WHEN?", "WHAT?", "WHERE?",
    "WHAT FOR?", "WHAT IF?", "WHICH?"
]
DATA_CARDS = [
    "Marketing", "Communications", "Training", "Change Management",
    "Leadership", "Tools", "Governance", "Mindset", "Culture"
]

# -------------------- Styles (mobile-first) --------------------
CSS = f"""
<style>
:root {{
  --dlc: {DLC_ORANGE};
  --dlc-dark: {DLC_ORANGE_DARK};
}}

[data-testid="stAppViewContainer"] {{
  background: #ffffff !important;
}}

.header-bar {{
  width: 100%;
  background: var(--dlc);
  padding: 14px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-sizing: border-box;
}}
.header-logo {{
  height: 32px;
  width: 32px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}}
.header-texts {{
  display: grid;
  line-height: 1.15;
}}
.app-title {{
  color: #fff;
  font-weight: 800;
  letter-spacing: .02em;
  font-size: clamp(1.0rem, 2.6vw, 1.25rem);
  margin: 0;
}}
.subtitle {{
  color: #ffece8;
  font-size: clamp(.82rem, 2.2vw, .95rem);
  margin: 0;
}}

.wrap {{
  max-width: 1080px;
  margin: 0 auto;
  padding: 10px 12px 14px;
}}

.button-wrap {{
  position: sticky;          /* makes the button easy to reach on mobile */
  top: 0;
  z-index: 5;
  background: #fff;
  padding: 8px 0 10px;
  border-bottom: 1px solid rgba(0,0,0,0.06);
  margin-bottom: 10px;
}}

div.stButton > button[kind="secondary"],
div.stButton > button[kind="primary"],
div.stButton > button {{
  background: var(--dlc) !important;
  color: #fff !important;
  border: 0 !important;
  border-radius: 10px !important;
  font-weight: 800 !important;
  letter-spacing: .02em !important;
  padding: 10px 14px !important;
  box-shadow: 0 4px 16px rgba(239,77,55,.28) !important;
}}
div.stButton > button:hover {{
  background: var(--dlc-dark) !important;
}}

.card-grid {{
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}}
@media (min-width: 720px) {{
  .card-grid {{
    grid-template-columns: 1fr 1fr; /* two columns on tablets/desktop */
    gap: clamp(12px, 3vw, 28px);
  }}
}}

.card {{
  aspect-ratio: 3 / 5;
  background: #fff;
  border: 6px solid var(--dlc);
  border-radius: 20px;
  position: relative;
  box-shadow: 0 10px 26px rgba(0,0,0,0.08);
  display: grid;
  place-items: center;
  overflow: hidden;
}}

.card-inner {{
  width: 85%;
  height: 85%;
  display: grid;
  place-items: center;
  position: relative;
}}

.card-title {{
  color: var(--dlc);
  font-weight: 900;
  letter-spacing: 0.06em;
  font-size: clamp(1.25rem, 8vw, 3.2rem); /* scales up on bigger screens */
  transform: rotate(-90deg);
  white-space: nowrap;
  text-align: center;
}}

.corner {{
  position: absolute;
  width: clamp(26px, 7vw, 40px);
  height: clamp(26px, 7vw, 40px);
}}
.corner.tl {{ top: 12px; left: 12px; }}
.corner.br {{ bottom: 12px; right: 12px; }}
.corner svg {{
  width: 100%;
  height: 100%;
  stroke: var(--dlc);
  fill: none;
  stroke-width: 2.2px;
}}

.badge {{
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--dlc);
  color: #fff;
  font-weight: 800;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  padding: 4px 8px;
  border-radius: 999px;
  opacity: 0.95;
}}

.footer-note {{
  text-align: center;
  color: #6b7280;
  font-size: 0.92rem;
  margin-top: 12px;
}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -------------------- SVG icons --------------------
BRAIN_SVG = """
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M22 24c-2.5-4-9-3-9 3 0 5 4 7 4 7-3 8 8 11 10 6m5-21c-1-4 4-7 7-4 2-2 6-1 7 2 4-1 7 2 6 6 4 2 4 8-1 10 1 5-4 9-8 6-2 4-8 4-10-1-3 2-8 0-8-4"/>
</svg>
"""
DASHBOARD_SVG = """
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect x="8" y="12" width="48" height="36" rx="4"/>
  <line x1="14" y1="22" x2="30" y2="22"/>
  <line x1="14" y1="30" x2="26" y2="30"/>
  <rect x="34" y="20" width="18" height="14" rx="2"/>
  <line x1="12" y1="50" x2="52" y2="50"/>
</svg>
"""

# -------------------- State --------------------
if "ai" not in st.session_state:
    st.session_state.ai = random.choice(AI_CARDS)
if "data" not in st.session_state:
    st.session_state.data = random.choice(DATA_CARDS)

def deal_pair():
    st.session_state.ai = random.choice(AI_CARDS)
    st.session_state.data = random.choice(DATA_CARDS)

# -------------------- Header --------------------
st.markdown('<div class="header-bar">', unsafe_allow_html=True)
if logo_b64:
    st.markdown(f'<img class="header-logo" alt="DLC" src="data:image/png;base64,{logo_b64}"/>', unsafe_allow_html=True)
st.markdown(
    '<div class="header-texts">'
    '<div class="app-title">Data & AI Literacy - Card Game</div>'
    '<div class="subtitle">Deal a pair: one AI card (question) + one DATA card (domain).</div>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Controls --------------------
st.markdown('<div class="wrap">', unsafe_allow_html=True)
st.markdown('<div class="button-wrap">', unsafe_allow_html=True)
st.button("🎲 Generate card pair", use_container_width=True, on_click=deal_pair)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Cards --------------------
st.markdown('<div class="card-grid">', unsafe_allow_html=True)

ai_html = f"""
<div class="card">
  <div class="card-inner">
    <div class="badge">AI</div>
    <div class="corner tl">{BRAIN_SVG}</div>
    <div class="corner br">{BRAIN_SVG}</div>
    <div class="card-title">{st.session_state.ai}</div>
  </div>
</div>
"""
data_html = f"""
<div class="card">
  <div class="card-inner">
    <div class="badge">DATA</div>
    <div class="corner tl">{DASHBOARD_SVG}</div>
    <div class="corner br">{DASHBOARD_SVG}</div>
    <div class="card-title">{st.session_state.data.upper()}</div>
  </div>
</div>
"""
st.markdown(ai_html + data_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Footer tip --------------------
st.markdown('<div class="footer-note">Tip: Use each pair to spark a short discussion Data & AI Literacy.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # wrap end
