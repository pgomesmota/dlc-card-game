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
LOGO_PATH = find_image(["dlc-logo.png","./dlc-logo.png"])
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
  background: var(--bg) !important; color: var(--text);
  margin: 0 !important; padding: 0 !important;
}}
[data-testid="stElementContainer"] {{ padding: 0 !important; margin: 0 !important; }}

/* Header */
.header {{
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  margin-bottom: 1rem; text-align: center;
}}
.header .top {{ display: flex; align-items: center; justify-content: center; gap: 12px; }}
.header .top img {{
  width: 72px; height: auto; border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}}
.header .top h1 {{
  margin: 0;
  font-size: clamp(1.2rem, 3.8vw, 2.3rem);
  color: var(--text);
  font-weight: 900;
  white-space: nowrap;      /* prevent line breaks */
  overflow: hidden;
  text-overflow: ellipsis;  /* ensure no wrapping on mobile */
  max-width: 100%;
}}
@media (max-width: 430px) {{
  .header .top h1 {{
    font-size: 1.15rem;      /* slightly smaller for iPhone */
  }}
}}

.header .subtitle {{
  margin-top: .4rem;
  font-size: clamp(.9rem, 2.5vw, 1.05rem);
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
.header .subtitle .accent, .header .subtitle b {{
  color: var(--accent);
  font-weight: 800;
}}

/* Cards Row */
.cards-row {{
  display: flex; flex-direction: row; justify-content: center; align-items: stretch;
  gap: 14px; flex-wrap: nowrap; margin-top: 10px; margin-bottom: 24px;
}}
@media (max-width: 430px) {{
  .cards-row {{ gap: 10px; }}
}}

/* Card base */
.card {{
  width: clamp(130px, 44vw, 210px);
  aspect-ratio: 2 / 3;
  border-radius: 14px;
  padding: 12px 10px;
  border: 2px solid var(--accent);
  background: #fff;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
  display: flex; flex-direction: column; align-items: center; justify-content: space-between;
  gap: 8px; color: var(--text);
}}
.card .icon {{ display: flex; justify-content: center; align-items: center; margin-top: 4px; }}
.card .icon img {{ width: 64px; height: 64px; object-fit: contain; }}
.card .title {{
  font-size: clamp(1rem, 3.4vw, 1.35rem);
  font-weight: 900;
  text-align: center;
  line-height: 1.2;
}}
.card .hint {{
  font-size: clamp(.75rem, 2.6vw, .9rem);
  color: var(--accent);
  font-weight: 800;
  text-transform: uppercase;
  text-align: center;
  margin-bottom: 4px;
}}
.card.face-down {{ border-style: dashed; }}
.card.face-down .title {{ color: var(--accent); letter-spacing: 1px; }}

/* Button: always red with press feel */
.stButton > button {{
  width: 100%;
  padding: 12px 14px;
  border-radius: 12px;
  border: 2px solid var(--accent);
  background: var(--accent) !important;
  color: #fff !important;
  font-weight: 800;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 6px 0 rgba(181, 52, 32, 0.9);
  transition: transform 80ms ease, box-shadow 80ms ease;
  outline: none !important;
}}
.stButton > button:hover {{ filter: brightness(0.98); }}
.stButton > button:active {{
  background: var(--accent) !important;
  color: #fff !important;
  transform: translateY(2px);
  box-shadow: 0 3px 0 rgba(181, 52, 32, 0.9);
}}
.stButton > button:focus {{
  box-shadow: 0 6px 0 rgba(181, 52, 32, 0.9) !important;
}}

/* Footer Tip: one line */
.footer {{
  text-align: center;
  color: var(--text);
  font-size: .9rem;
  margin-top: .8rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
</style>
"""
st.markdown(CARD_CSS, unsafe_allow_html=True)

# ---------- State ----------
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
  <div class="top">
    {'<img src="'+LOGO_URI+'" alt="DLC logo">' if LOGO_URI else ''}
    <h1>Data & AI Literacy - Card Game</h1>
  </div>
  <div class="subtitle">
    <span class="accent">Deal a pair:</span> one <b>AI</b> card (question) + one <b>DATA</b> card (domain).
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Cards ----------
if st.session_state.revealed:
    cards_html = f"""
<div class="cards-row">
  <div class="card">
    <div class="icon">{'<img src="'+AI_ICON_URI+'" alt="AI icon">' if AI_ICON_URI else ''}</div>
    <div class="title">{st.session_state.ai_pick}</div>
    <div class="hint">AI CARD</div>
  </div>
  <div class="card">
    <div class="icon">{'<img src="'+DATA_ICON_URI+'" alt="DATA icon">' if DATA_ICON_URI else ''}</div>
    <div class="title">{st.session_state.data_pick.upper()}</div>
    <div class="hint">DATA CARD</div>
  </div>
</div>
"""
else:
    cards_html = f"""
<div class="cards-row">
  <div class="card face-down">
    <div class="icon">{'<img src="'+LOGO_URI+'" alt="DLC logo">' if LOGO_URI else ''}</div>
    <div class="title">?</div>
    <div class="hint">AI CARD</div>
  </div>
  <div class="card face-down">
    <div class="icon">{'<img src="'+LOGO_URI+'" alt="DLC logo">' if LOGO_URI else ''}</div>
    <div class="title">?</div>
    <div class="hint">DATA CARD</div>
  </div>
</div>
"""
st.markdown(cards_html, unsafe_allow_html=True)

# ---------- Button & Footer ----------
st.button("🃏 Deal card pair", on_click=deal_pair, use_container_width=True)
st.markdown('<div class="footer">Tip: Use each pair to spark a discussion about Literacy.</div>',
            unsafe_allow_html=True)
