# streamlit_app.py
import random
import streamlit as st

st.set_page_config(page_title="AI Literacy Card Pair", page_icon="🧠", layout="centered")

# ---------- Data: the two mini-decks ----------
BRAIN_CARDS = [
    "WHY?", "HOW?", "WHO?", "WHEN?", "WHAT?", "WHERE?",
    "WHAT FOR?", "WHAT IF?", "WHICH?"
]

DASHBOARD_CARDS = [
    "Marketing", "Communications", "Training", "Change Management",
    "Leadership", "Tools", "Governance", "Mindset", "Culture"
]

# ---------- Minimal style ----------
CARD_CSS = """
<style>
:root {
  --bg: #0f172a;         /* slate-900 */
  --card: #111827;       /* gray-900 */
  --card2: #0b1021;      /* darker alt */
  --ring: #6366f1;       /* indigo-500 */
  --text: #e5e7eb;       /* gray-200 */
  --muted: #93c5fd;      /* blue-300 */
}
html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(80vw 80vh at 50% -10%, #141a31 0%, var(--bg) 60%, #0b0f1f 100%) !important;
}
.header {
  text-align: center; margin: 0 0 0.6rem 0;
}
.header h1 {
  font-size: clamp(1.6rem, 2.5vw, 2.2rem);
  line-height: 1.2; color: var(--text); margin: 0;
}
.header p {
  color: #cbd5e1; margin: 0.25rem 0 0 0; font-size: 0.95rem;
}
.btn-wrap { text-align: center; margin: 0.7rem 0 1.1rem 0; }

.card {
  border-radius: 18px;
  padding: 20px 18px;
  position: relative;
  border: 1px solid rgba(99,102,241,0.25);
  background:
    radial-gradient(120% 120% at 0% 0%, rgba(99,102,241,0.10) 0%, rgba(99,102,241,0.05) 35%, transparent 60%) ,
    linear-gradient(180deg, var(--card), var(--card2));
  box-shadow:
    0 10px 30px rgba(0,0,0,0.45),
    inset 0 0 30px rgba(99,102,241,0.08);
  color: var(--text);
  min-height: 170px;
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 8px;
}
.card .icon {
  font-size: 38px; line-height: 1; filter: drop-shadow(0 2px 6px rgba(99,102,241,0.35));
}
.card .title {
  font-size: 1.6rem; font-weight: 800; letter-spacing: 0.3px;
}
.card .hint {
  font-size: 0.85rem; color: #a5b4fc; opacity: 0.95;
}
.ring {
  position: absolute;
  inset: -2px; border-radius: 20px;
  padding: 1px;
  background: linear-gradient(145deg, rgba(99,102,241,0.65), rgba(14,165,233,0.45), rgba(59,130,246,0.50));
  -webkit-mask:
    linear-gradient(#000 0 0) content-box, 
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude;
  pointer-events: none; opacity: 0.6;
}
.footer {
  text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 1.2rem;
}
.small {
  font-size: 0.8rem; color: #94a3b8; text-align: center; margin-top: 0.25rem;
}
</style>
"""

st.markdown(CARD_CSS, unsafe_allow_html=True)

# ---------- State & helpers ----------
if "brain_pick" not in st.session_state:
    st.session_state.brain_pick = random.choice(BRAIN_CARDS)
if "dash_pick" not in st.session_state:
    st.session_state.dash_pick = random.choice(DASHBOARD_CARDS)

def deal_pair():
    st.session_state.brain_pick = random.choice(BRAIN_CARDS)
    st.session_state.dash_pick = random.choice(DASHBOARD_CARDS)

# ---------- UI ----------
st.markdown(
    """
<div class="header">
  <h1>AI Literacy – Card Pair</h1>
  <p>Deal a pair: one <b>Brain</b> card (question) + one <b>Dashboard</b> card (domain).</p>
</div>
""",
    unsafe_allow_html=True,
)

colA, colB = st.columns(2, gap="large")

with colA:
    st.markdown(
        f"""
<div class="card">
  <div class="ring"></div>
  <div class="icon">🧠</div>
  <div class="title">{st.session_state.brain_pick}</div>
  <div class="hint">Brain card</div>
</div>
""",
        unsafe_allow_html=True,
    )

with colB:
    st.markdown(
        f"""
<div class="card">
  <div class="ring"></div>
  <div class="icon">📊</div>
  <div class="title">{st.session_state.dash_pick}</div>
  <div class="hint">Dashboard card</div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown('<div class="btn-wrap"></div>', unsafe_allow_html=True)
st.button("🎲 Generate card pair", on_click=deal_pair, use_container_width=True)

st.markdown(
    """
<div class="small">Inspiration: Data & AI Literacy deck vibe. Your pair is randomly generated on each click.</div>
<div class="footer">Tip: Use each pair to spark a short discussion: connect the question to the domain.</div>
""",
    unsafe_allow_html=True,
)
