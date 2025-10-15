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
  background: var(--bg) !important; color: var(--text);
  margin: 0 !important; padding: 0 !important;
}}
[data-testid="stElementContainer"] {{ padding: 0 !important; margin: 0 !important; }}

/* Header */
.header {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.0rem;
  text-align: center;
}}
.header .top {{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}}
.header .top img {{
  width: 72px;
  height: auto;
  border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}}
.header .top h1 {{
  margin: 0;
  font-size: clamp(1.6rem, 4.6vw, 2.4rem);
  line-height: 1.12;
  color: var(--text);
  font-weight: 900;
}}
.header .subtitle {{
  margin-top: 0.4rem;
  font-size: clamp(0.96rem, 3vw, 1.06rem);
  color: var(--text);
}}
.header .subtitle .accent,
.header .subtitle b {{
  color: var(--accent);
  font-weight: 800;
}}

/* Cards grid: two columns, even on mobile */
.cards {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  justify-items: center;
  align-items: start;
  gap: 12px;
  margin-top: 6px;
}}

/* Card base: portrait, phone-friendly sizing */
.card {{
  width: clamp(140px, 42vw, 300px);   /* fits two across on phones */
  aspect-ratio: 2 / 3;                /* portrait */
  border-radius: 14px;
  padding: 14px 12px;
  border: 2px solid var(--accent);
  background: #fff;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  color: var(--text);
}}
.card .icon {{
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2px;
}}
.card .icon img {{
  width: 44px;
  height: 44px;
  object-fit: contain;
}}
.card .title {{
  font-size: clamp(1.1rem, 3.8vw, 1.6rem);
  font-weight: 900;
  text-align: center;
  line-height: 1.2;
}}
.card .hint {{
  font-size: clamp(0.8rem, 2.8vw, 0.95rem);
  color: var(--accent);
  font-weight: 700;
  text-align: center;
  margin-bottom: 2px;
}}
.card.face-down {{
  border-style: dashed;
}}
.card.face-down .title {{
  color: var(--accent);
  letter-spacing: 1px;
}}

/* Button */
.stButton > button {{
  width: 100%;
  padding: 12px 14px;
  border-radius: 12px;
  border: 2px solid var(--accent);
  background: var(--accent);
  color: #fff;
  font-weight: 800;
  font-size: 1rem;
}}
.stButton > button:hover {{ filter: brightness(0.95); }}

/* Footer */
.footer {{
  text-align: center;
  color: var(--text);
  font-size: 0.92rem;
  margin-top: 0.8rem;
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
""",
        unsafe_allow_html=True,
    )
    # DATA card (face-up)
    st.markdown(
        f"""
<div class="card">
  <div class="icon">{'<img src="'+DATA_ICON_URI+'" alt="DATA icon">' if DATA_ICON_URI else ''}</div>
  <div class="title">{st.session_state.data_pick.upper()}</div>
  <div class="hint">DATA card</div>
</div>
""",
        unsafe_allow_html=True,
    )
else:
    # Face-down cards
    st.markdown(
        f"""
<div class="card face-down">
  <div class="icon">{'<img src="'+LOGO_URI+'" alt="DLC logo">' if LOGO_URI else ''}</div>
  <div class="title">?</div>
  <div class="hint">AI card</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<div class="card face-down">
  <div class="icon">{'<img src="'+LOGO_URI+'" alt="DLC logo">' if LOGO_URI else ''}</div>
  <div class="title">?</div>
  <div class="hint">DATA card</div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Button & Footer ----------
st.button("🎲 Generate card pair", on_click=deal_pair, use_container_width=True)
st.markdown('<div class="footer">Tip: Use each pair to spark a short discussion Data & AI Literacy.</div>',
            unsafe_allow_html=True)
