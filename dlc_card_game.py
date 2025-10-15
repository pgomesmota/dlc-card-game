# streamlit_app.py
import os, base64, random
from PIL import Image
import streamlit as st

# ---------- Locate logo ----------
CANDIDATES = [
    "dlc-logo.png", "./dlc-logo.png", "assets/dlc-logo.png",
    "/mnt/data/de31a37a-11e6-4fc0-a566-b321e6971d63.png"  # fallback
]
LOGO_PATH = next((p for p in CANDIDATES if os.path.exists(p)), None)

def image_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(path)[1].lower().replace(".", "") or "png"
    return f"data:image/{'png' if ext not in ['png','jpg','jpeg','gif','webp','svg'] else ext};base64,{b64}"

# ---------- App config (must be first Streamlit call) ----------
if LOGO_PATH:
    try:
        st.set_page_config(page_title="Data & AI Literacy - Card Game",
                           page_icon=Image.open(LOGO_PATH),
                           layout="centered")
    except Exception:
        st.set_page_config(page_title="Data & AI Literacy - Card Game",
                           page_icon="🧠", layout="centered")
else:
    st.set_page_config(page_title="Data & AI Literacy - Card Game",
                       page_icon="🧠", layout="centered")

# ---------- Brand / theme ----------
BRAND_RED = "#E9462E"
BLACK = "#111111"
LOGO_DATA_URI = image_to_data_uri(LOGO_PATH) if LOGO_PATH else ""

# ---------- Data: the two mini-decks ----------
AI_CARDS = ["WHY?", "HOW?", "WHO?", "WHEN?", "WHAT?", "WHERE?", "WHAT FOR?", "WHAT IF?", "WHICH?"]
DATA_CARDS = ["Marketing", "Communications", "Training", "Change Management", "Leadership",
              "Tools", "Governance", "Mindset", "Culture"]

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
  margin: 0 !important; padding: 0 !important;
}}
[data-testid="stElementContainer"] {{ padding: 0 !important; margin: 0 !important; }}
.header {{
  display: flex; align-items: center; gap: 16px; margin-bottom: 0.6rem; flex-wrap: wrap;
}}
.header img {{
  width: 80px; height: auto; border-radius: 6px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}}
.header-content h1 {{
  margin: 0; font-size: clamp(1.6rem, 4.6vw, 2.4rem); line-height: 1.15; color: var(--text); font-weight: 800;
}}
.header-content p {{
  margin: 6px 0 0 0; font-size: clamp(0.95rem, 3.2vw, 1.05rem); color: var(--text);
}}
.header-content b, .header-content .accent {{ color: var(--accent); font-weight: 800; }}
.cards {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 6px; }}
@media (max-width: 768px) {{ .cards {{ grid-template-columns: 1fr; }} }}
.card {{
  border-radius: 16px; padding: 18px 16px; border: 2px solid var(--accent); background: #fff;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06); color: var(--text); min-height: 150px;
  display: grid; grid-template-rows: auto 1fr auto; gap: 6px;
}}
.card .icon {{ font-size: 34px; line-height: 1; color: var(--accent); }}
.card .title {{ font-size: clamp(1.4rem, 4.5vw, 1.9rem); font-weight: 900; letter-spacing: 0.2px; color: var(--text); }}
.card .hint {{ font-size: 0.95rem; color: var(--accent); font-weight: 700; }}
.stButton > button {{
  width: 100%; padding: 14px 16px; border-radius: 12px; border: 2px solid var(--accent);
  background: var(--accent); color: #fff; font-weight: 800; font-size: 1rem;
}}
.stButton > button:hover {{ filter: brightness(0.95); }}
.footer {{ text-align: center; color: var(--text); font-size: 0.95rem; margin-top: 0.9rem; }}
</style>
"""
st.markdown(CARD_CSS, unsafe_allow_html=True)

# ---------- State ----------
if "ai_pick" not in st.session_state:
    st.session_state.ai_pick = random.choice(AI_CARDS)
if "data_pick" not in st.session_state:
    st.session_state.data_pick = random.choice(DATA_CARDS)

def deal_pair():
    st.session_state.ai_pick = random.choice(AI_CARDS)
    st.session_state.data_pick = random.choice(DATA_CARDS)

# ---------- Header (logo left, title right) ----------
st.markdown(
    f"""
<div class="header">
    {'<img src="'+LOGO_DATA_URI+'" alt="DLC logo">' if LOGO_DATA_URI else ''}
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
""", unsafe_allow_html=True,
)
st.markdown(
    f"""
<div class="card">
  <div class="icon">📊</div>
  <div class="title">{st.session_state.data_pick}</div>
  <div class="hint">DATA card</div>
</div>
""", unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Button & Footer ----------
st.button("🎲 Generate card pair", on_click=deal_pair, use_container_width=True)
st.markdown('<div class="footer">Tip: Use each pair to spark a short discussion Data & AI Literacy.</div>',
            unsafe_allow_html=True)
