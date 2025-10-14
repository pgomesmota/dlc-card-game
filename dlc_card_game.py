# streamlit_app.py
import random
import base64
from pathlib import Path
import streamlit as st

# -------------------- Setup --------------------
st.set_page_config(page_title="Data & AI Literacy - Card Game", page_icon="🧠", layout="wide")

# Brand color (DLC orange)
DLC_ORANGE = "#EF4D37"

def load_logo_b64():
    p = Path("dlc-logo.png")
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode("utf-8")
    return None

logo_b64 = load_logo_b64()

# -------------------- Mini-decks --------------------
AI_CARDS = [
    "WHY?", "HOW?", "WHO?", "WHEN?", "WHAT?", "WHERE?", "WHAT FOR?", "WHAT IF?", "WHICH?"
]

DATA_CARDS = [
    "Marketing", "Communications", "Training", "Change Management",
    "Leadership", "Tools", "Governance", "Mindset", "Culture"
]

# -------------------- Styles --------------------
CSS = f"""
<style>
:root {{
  --dlc: {DLC_ORANGE};
}}

[data-testid="stAppViewContainer"] {{
  background: #ffffff !important;
}}

.header-wrap {{
  width: 100%;
  background: var(--dlc);
  padding: 28px 20px 22px 20px;
  border-bottom: 3px solid rgba(0,0,0,0.06);
  margin-bottom: 18px;
}}
.header-inner {{
  max-width: 1080px;
  margin: 0 auto;
  display: grid;
  place-items: center;
  row-gap: 8px;
}}
.header-inner img {{ height: 60px; }}
.app-title {{
  color: #fff;
  font-weight: 800;
  letter-spacing: 0.04em;
  font-size: clamp(1.1rem, 3vw, 1.6rem);
}}
.subtitle {{
  color: #ffece8;
  font-size: 0.98rem;
}}

.controls, .footer-note {{
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 10px;
  text-align: center;
}}

.card-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: clamp(12px, 3vw, 28px);
  align-items: start;
  max-width: 1080px;
  margin: 12px auto 20px auto;
  padding: 0 10px;
}}

.card {{
  aspect-ratio: 3 / 5;
  background: #fff;
  border: 6px solid var(--dlc);
  border-radius: 20px;
  position: relative;
  box-shadow: 0 10px 26px rgba(0,0,0,0.10);
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
  font-weight: 800;
  letter-spacing: 0.06em;
  font-size: clamp(1.2rem, 5.4vw, 3.2rem);
  transform: rotate(-90deg);
  white-space: nowrap;
}}

.corner {{
  position: absolute;
  width: clamp(26px, 5.2vw, 40px);
  height: clamp(26px, 5.2vw, 40px);
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
  font-weight: 700;
  font-size: 0.70rem;
  letter-spacing: 0.08em;
  padding: 4px 8px;
  border-radius: 999px;
  opacity: .95;
}}
.footer-note {{
  color: #6b7280;
  font-size: 0.9rem;
  margin-top: 6px;
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
st.markdown('<div class="header-wrap"><div class="header-inner">', unsafe_allow_html=True)
if logo_b64:
    st.markdown(f'<img alt="DLC" src="data:image/png;base64,{logo_b64}"/>', unsafe_allow_html=True)
st.markdown('<div class="app-title">Data & AI Literacy - Card Game</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Deal a pair: one AI card (question) + one DATA card (domain).</div></div></div>', unsafe_allow_html=True)

# -------------------- Controls --------------------
_, c, _ = st.columns([1,1,1])
with c:
    st.button("🎲 Generate card pair", use_container_width=True, on_click=deal_pair)

# -------------------- Cards --------------------
st.markdown('<div class="card-grid">', unsafe_allow_html=True)

# AI card (Brain icon)
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

# DATA card (Dashboard icon)
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
