# streamlit_app.py
import os, base64, random
from PIL import Image
import streamlit as st

# ---------- Helpers ----------
def image_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(path)[1].lower().replace(".", "") or "png"
    if ext not in ["png","jpg","jpeg","gif","webp","svg"]:
        ext = "png"
    return f"data:image/{ext};base64,{b64}"

def find_image(cands):
    for p in cands:
        if os.path.exists(p):
            return p
    return None

# ---------- Assets ----------
LOGO_PATH = find_image(["dlc-logo.png","./dlc-logo.png","/mnt/data/de31a37a-11e6-4fc0-a566-b321e6971d63.png"])
AI_ICON_PATH = find_image(["ai-icon.png","./ai-icon.png"])
DATA_ICON_PATH = find_image(["data-icon.png","./data-icon.png"])

LOGO_URI  = image_to_data_uri(LOGO_PATH)   if LOGO_PATH  else ""
AI_ICON_URI   = image_to_data_uri(AI_ICON_PATH)   if AI_ICON_PATH   else ""
DATA_ICON_URI = image_to_data_uri(DATA_ICON_PATH) if DATA_ICON_PATH else ""

# ---------- App config ----------
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

# ---------- Theme ----------
BRAND_RED = "#E9462E"
BLACK = "#111111"

# ---------- Decks ----------
AI_CARDS   = ["WHY?","HOW?","WHO?","WHEN?","WHAT?","WHERE?","WHAT FOR?","WHAT IF?","WHICH?"]
DATA_CARDS = ["Marketing","Communications","Training","Change Management","Leadership",
              "Tools","Governance","Mindset","Culture"]

# ---------- Styles ----------
CARD_CSS = f"""
<style>
:root {{
  --accent: {BRAND_RED};
  --text: {BLACK};
  --bg: #ffffff;
}}
html, body, [data-testid="stAppViewContainer"] {{
  background: var(--bg) !important; color: var(--text); margin: 0 !important; padding: 0 !important;
}}
[data-testid="stElementContainer"] {{ padding: 0 !important; margin: 0 !important; }}

/* Header */
.header {{
  display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: center; margin: 0 0 0.6rem 0;
}}
.header .logo img {{ width: 80px; height: auto; border-radius: 6px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }}
.header .textblock {{ display: flex; flex-direction: column; justify-content: center; }}
.header .textblock h1 {{ margin: 0; font-size: clamp(1.7rem, 4.8vw, 2.6rem); line-height: 1.12; color: var(--text); font-weight: 900; }}
.header .textblock p {{ margin: 6px 0 0 0; font-size: clamp(0.98rem, 3.1vw, 1.08rem); color: var(--text); }}
.header .textblock .accent, .header .textblock b {{ color: var(--accent); font-weight: 800; }}

/* Cards grid */
.cards {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 6px; }}
@media (max-width: 768px) {{ .cards {{ grid-template-columns: 1fr; }} }}

/* Card base */
.card {{
  border-radius: 16px; padding: 18px 16px;
  border: 2px solid var(--accent); background: #fff; box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  min-height: 150px; display: grid; grid-template-rows: auto 1fr auto; gap: 8px; align-items: start; color: var(--text);
}}
.card .icon {{ display: flex; justify-content: center; align-items: center; }}
.card .icon img {{ width: 56px; height: 56px; object-fit: contain; }}
.card .title {{ font-size: clamp(1.4rem, 4.5vw, 1.9rem); font-weight: 900; letter-spacing: 0.2px; text-align: center; }}
.card .hint  {{ font-size: 0.95rem; color: var(--accent); font-weight: 700; text-align: center; }}

/* Face-down tweaks */
.card.face-down {{ border-style: dashed; }}
.card.face-down .title {{ color: var(--accent); letter-spacing: 1px; }}

/* Button */
.stButton > button {{
  width: 100%; padding: 14px 16px; border-radius: 12px;
  border: 2px solid var(--accent); background: var(--accent); color: #fff; font-weight: 800; font-size: 1rem;
}}
.stButton > button:hover {{ filter: brightness(0.95); }}

/* Footer */
.footer {{ text-align: center; color: var(--text); font-size: 0.95rem; margin-top: 0.9rem; }}
</style>
"""
st.markdown(CARD_CSS, unsafe_allow_html=True)

# ---------- State (start face-down) ----------
if "revealed" not in st.session_state:
    st.session_state.revealed = False
if "ai_pick" not in st.session_state:
    st.session_state.ai_pick = random.choice(AI_CARDS)
if "data_pick" not in st.session_state:
    st.session_state.data_pick = random.choice(DATA_CARDS)

def deal_pair():
    st.session_state.ai_pick = random.choice(AI_CARDS)
    st.session_state.data_pick = random.choice(DATA_CARDS)
    st.session_state.revealed = True

# ---------- Header ----------
st.markdown(
    f"""
<div class="header">
  <div class="logo">{'<img src="'+LOGO_URI+'" alt="DLC logo">' if LOGO_URI else ''}</div>
  <div class="textblock">
    <h1>Data & AI Literacy - Card Game</h1>
    <p><span class="accent">Deal a pair:</span> one <b>AI</b> card (question) + one <b>DATA</b> card (domain).</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- Cards ----------
st.markdown('<div class="cards">', unsafe_allow_html=True)

if st.session_state.revealed:
    # AI card (face-up)
    st.markdown(
        f"""
<div class="card">
  <div class="icon">{'<img src="'+AI_ICON_URI+'" alt="AI icon">' if AI_ICON_URI else ''}</div>
  <div class="title">{st.session_state.ai_pick}</div>
  <div class="hint">AI card</div>
</div>
""", unsafe_allow_html=True)

    # DATA card (face-up) — DOMAIN ALWAYS UPPERCASE
    st.markdown(
        f"""
<div class="card">
  <div class="icon">{'<img src="'+DATA_ICON_URI+'" alt="DATA icon">' if DATA_ICON_URI else ''}</div>
  <div class="title">{st.session_state.data_pick.upper()}</div>
  <div class="hint">DATA card</div>
</div>
""", unsafe_allow_html=True)

else:
    # Face-down cards: DLC logo + '?' + dashed border
    st.markdown(
        f"""
<div class="card face-down">
  <div class="icon">{'<img src="'+LOGO_URI+'" alt="DLC logo">' if LOGO_URI else ''}</div>
  <div class="title">?</div>
  <div class="hint">AI card</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(
        f"""
<div class="card face-down">
  <div class="icon">{'<img src="'+LOGO_URI+'" alt="DLC logo">' if LOGO_URI else ''}</div>
  <div class="title">?</div>
  <div class="hint">DATA card</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Button & Footer ----------
st.button("🎲 Generate card pair", on_click=deal_pair, use_container_width=True)
st.markdown('<div class="footer">Tip: Use each pair to spark a short discussion Data & AI Literacy.</div>', unsafe_allow_html=True)
