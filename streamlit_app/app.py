"""Sentinel — HR Attrition Intelligence. Ultra-premium dark UI + SHAP explainability."""
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Sentinel · HR Attrition Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design system (ultra-premium · glass · teal/emerald) ─────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg:#06080c; --glass:rgba(20,28,40,0.55); --glass-2:rgba(26,36,50,0.45);
    --border:rgba(255,255,255,0.08); --hair:rgba(255,255,255,0.06);
    --text:#eaf1f7; --muted:#8a97a8; --faint:#56616f;
    --accent:#2dd4bf; --accent-2:#10b981; --accent-dim:rgba(45,212,191,0.12);
    --low:#2dd4bf; --medium:#f59e0b; --high:#f43f5e;
}
.stApp {
    background:
        radial-gradient(1100px 600px at 8% -10%, rgba(45,212,191,0.13), transparent 55%),
        radial-gradient(900px 600px at 100% 0%, rgba(16,185,129,0.09), transparent 50%),
        radial-gradient(700px 700px at 85% 110%, rgba(56,189,248,0.06), transparent 55%),
        var(--bg);
    color:var(--text); font-family:'DM Sans',sans-serif;
}
.stApp::before {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:9999; opacity:.035; mix-blend-mode:overlay;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding:1.4rem 2.6rem 3rem !important; max-width:1320px; }
h1,h2,h3,h4 { font-family:'Sora',sans-serif; color:var(--text); letter-spacing:-0.6px; }
p, span, label, div { color:var(--text); }

section[data-testid="stSidebar"] {
    background:linear-gradient(180deg, rgba(11,16,24,0.85), rgba(6,9,13,0.95));
    backdrop-filter:blur(18px); -webkit-backdrop-filter:blur(18px); border-right:1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top:1.4rem; }
.brand { display:flex; align-items:center; gap:13px; padding:2px 4px 18px; border-bottom:1px solid var(--hair); margin-bottom:18px; }
.brand svg { filter:drop-shadow(0 4px 14px rgba(45,212,191,0.45)); animation:glow 3.5s ease-in-out infinite; }
@keyframes glow { 0%,100%{filter:drop-shadow(0 4px 14px rgba(45,212,191,0.35))} 50%{filter:drop-shadow(0 4px 22px rgba(45,212,191,0.65))} }
.brand-name { font-family:'Sora',sans-serif; font-size:19px; font-weight:700; color:#fff; line-height:1; }
.brand-sub { font-size:10.5px; color:var(--faint); letter-spacing:1.6px; text-transform:uppercase; margin-top:5px; }
section[data-testid="stSidebar"] .stRadio > label { display:none; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] { gap:6px; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    background:transparent !important; border:1px solid transparent !important; border-radius:12px !important;
    padding:12px 14px !important; font-family:'DM Sans',sans-serif !important; font-size:14px !important;
    font-weight:500 !important; color:var(--muted) !important; transition:all .2s ease !important;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover { background:rgba(255,255,255,0.04) !important; color:var(--text) !important; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label div:first-child { display:none; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:has(input:checked) {
    background:linear-gradient(135deg,rgba(45,212,191,0.16),rgba(16,185,129,0.06)) !important;
    border-color:rgba(45,212,191,0.4) !important; color:#7ff0e1 !important; font-weight:600 !important;
    box-shadow:inset 3px 0 0 var(--accent), 0 4px 18px rgba(45,212,191,0.12);
}
.side-card { background:var(--glass); backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px);
    border:1px solid var(--border); border-radius:15px; padding:15px 16px; margin-top:14px;
    box-shadow:inset 0 1px 0 rgba(255,255,255,0.05); }
.side-label { font-size:10px; letter-spacing:1.4px; text-transform:uppercase; color:var(--faint); margin-bottom:9px; }
.side-row { display:flex; align-items:center; justify-content:space-between; font-size:12.5px; color:var(--muted); margin:6px 0; }
.dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--accent);
    box-shadow:0 0 0 4px rgba(45,212,191,0.15); animation:pulse 2.2s infinite; margin-right:7px; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }

.topbar { display:flex; align-items:flex-end; justify-content:space-between; padding-bottom:18px; margin-bottom:24px;
    border-bottom:1px solid var(--hair); animation:fadeup .6s ease both; }
.eyebrow { font-size:11px; letter-spacing:2.5px; text-transform:uppercase; color:var(--accent); font-weight:600; }
.h-title { font-size:30px; font-weight:800; margin-top:8px;
    background:linear-gradient(120deg,#ffffff 30%,#5eead4); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }
.h-sub { font-size:13.5px; color:var(--muted); margin-top:5px; }
.env-pill { display:inline-flex; align-items:center; gap:8px; font-size:12px; font-weight:500; color:#7ff0e1;
    background:var(--accent-dim); border:1px solid rgba(45,212,191,0.3); border-radius:100px; padding:8px 15px;
    white-space:nowrap; box-shadow:0 4px 18px rgba(45,212,191,0.1); }
@keyframes fadeup { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }

.kpi-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:15px; margin-bottom:8px; animation:fadeup .7s ease both; animation-delay:.05s; }
.kpi { background:var(--glass); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
    border:1px solid var(--border); border-radius:18px; padding:19px 21px; position:relative; overflow:hidden;
    box-shadow:inset 0 1px 0 rgba(255,255,255,0.06), 0 10px 30px rgba(0,0,0,0.3); transition:all .25s ease; }
.kpi:hover { transform:translateY(-3px); border-color:rgba(45,212,191,0.35); box-shadow:inset 0 1px 0 rgba(255,255,255,0.08), 0 16px 40px rgba(45,212,191,0.12); }
.kpi::after { content:''; position:absolute; inset:0 0 auto 0; height:2px; background:linear-gradient(90deg,var(--accent),transparent); opacity:.7; }
.kpi-label { font-size:11px; letter-spacing:1px; text-transform:uppercase; color:var(--faint); }
.kpi-value { font-family:'JetBrains Mono',monospace; font-size:31px; font-weight:600; color:#fff; margin-top:10px; line-height:1; }
.kpi-foot { font-size:12px; color:var(--muted); margin-top:8px; }

.panel { background:var(--glass-2); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
    border:1px solid var(--border); border-radius:20px; padding:22px 24px; margin-bottom:16px;
    box-shadow:inset 0 1px 0 rgba(255,255,255,0.05), 0 12px 36px rgba(0,0,0,0.28); animation:fadeup .7s ease both; }
.section-h { font-size:12px; font-weight:600; color:var(--accent); text-transform:uppercase; letter-spacing:1.6px;
    margin:6px 0 14px; display:flex; align-items:center; gap:11px; }
.section-h::after { content:''; flex:1; height:1px; background:var(--hair); }

.stSelectbox div[data-baseweb="select"] > div, .stNumberInput div[data-baseweb="input"], .stNumberInput input {
    background:rgba(14,20,29,0.95) !important; border:1px solid var(--border) !important; border-radius:11px !important;
    color:var(--text) !important; font-family:'DM Sans',sans-serif !important; }
.stSelectbox div[data-baseweb="select"] > div:focus-within, .stNumberInput div[data-baseweb="input"]:focus-within {
    border-color:var(--accent) !important; box-shadow:0 0 0 3px rgba(45,212,191,0.15) !important; }
div[data-testid="stNumberInput"] input, div[data-testid="stNumberInput"] input:focus {
    -webkit-box-shadow:0 0 0 1000px rgba(14,20,29,0.98) inset !important;
    -webkit-text-fill-color:#eaf1f7 !important; background-color:rgba(14,20,29,0.98) !important;
    color:#eaf1f7 !important; caret-color:var(--accent) !important; border:none !important; }
[data-baseweb="popover"] > div, ul[role="listbox"], div[role="listbox"],
div[data-baseweb="select-dropdown"], div[data-baseweb="menu"] {
    background:rgba(11,16,24,0.98) !important; border:1px solid rgba(255,255,255,0.14) !important;
    border-radius:13px !important; backdrop-filter:blur(20px) !important;
    -webkit-backdrop-filter:blur(20px) !important;
    box-shadow:0 20px 50px rgba(0,0,0,0.7) !important; }
[role="option"], li[data-baseweb="menu-item"] {
    background:rgba(11,16,24,0.98) !important; color:var(--muted) !important;
    font-family:'DM Sans',sans-serif !important; font-size:14px !important; }
[role="option"]:hover, li[data-baseweb="menu-item"]:hover {
    background:rgba(45,212,191,0.16) !important; color:#7ff0e1 !important; }
/* Force selects in popover juga */
[data-baseweb="popover"] *, [data-baseweb="menu"] * {
    background-color:transparent; color:var(--muted); }
.stSlider [data-baseweb="slider"] [role="slider"] { background:var(--accent) !important; box-shadow:0 0 0 4px rgba(45,212,191,0.2) !important; }
div[data-testid="stSliderTickBarMin"], div[data-testid="stSliderTickBarMax"] { color:var(--faint) !important; }
.stSlider [data-baseweb="slider"] > div > div { background:var(--accent) !important; }
label, .stSelectbox label, .stNumberInput label, .stSlider label { color:var(--muted) !important; font-size:13px !important; }

.stButton > button, .stFormSubmitButton > button {
    background:linear-gradient(135deg,var(--accent-2),var(--accent)) !important; color:#042620 !important;
    border:none !important; border-radius:13px !important; padding:15px 30px !important; font-family:'Sora',sans-serif !important;
    font-size:15px !important; font-weight:700 !important; letter-spacing:.3px !important; transition:all .25s !important;
    box-shadow:0 10px 30px rgba(45,212,191,0.32) !important; }
.stButton > button:hover, .stFormSubmitButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 16px 40px rgba(45,212,191,0.5) !important; }

.verdict { display:flex; align-items:center; gap:20px; padding:24px 26px; border-radius:18px; border:1px solid var(--border);
    margin-bottom:16px; animation:fadeup .5s ease both; background:var(--glass); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
    box-shadow:inset 0 1px 0 rgba(255,255,255,0.06), 0 16px 44px rgba(0,0,0,0.32); }
.verdict.low{box-shadow:inset 0 1px 0 rgba(255,255,255,0.06),0 16px 44px rgba(45,212,191,0.14)}
.verdict.medium{box-shadow:inset 0 1px 0 rgba(255,255,255,0.06),0 16px 44px rgba(245,158,11,0.14)}
.verdict.high{box-shadow:inset 0 1px 0 rgba(255,255,255,0.06),0 16px 44px rgba(244,63,94,0.16)}
.verdict-lab { font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:1.4px; }
.verdict-pred { font-family:'Sora',sans-serif; font-size:24px; font-weight:700; margin-top:5px; }
.badge { display:inline-flex; align-items:center; gap:7px; padding:7px 16px; border-radius:100px; font-size:13px; font-weight:600; margin-left:auto; }
.badge.low{background:rgba(45,212,191,0.18);color:#5eead4} .badge.medium{background:rgba(245,158,11,0.18);color:#fbbf24} .badge.high{background:rgba(244,63,94,0.18);color:#fb7185}

.ring-wrap { position:relative; width:230px; height:230px; margin:6px auto; }
.ring-center { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.ring-num { font-family:'JetBrains Mono',monospace; font-size:46px; font-weight:600; color:#fff; line-height:1; }
.ring-lab { font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:1.4px; margin-top:7px; }

.rec-box { background:rgba(255,255,255,0.03); border:1px solid var(--border); border-left:3px solid var(--accent);
    border-radius:13px; padding:17px 20px; font-size:14px; color:#cbd5e1; line-height:1.75; margin-top:14px; }
.legend { display:flex; gap:18px; font-size:12px; color:var(--muted); margin:2px 0 6px; }
.legend b { font-weight:600; }
.lg-dot { display:inline-block; width:9px; height:9px; border-radius:3px; margin-right:6px; vertical-align:middle; }

div[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:13px; overflow:hidden; }
hr { border-color:var(--hair) !important; }
.stAlert { background:var(--glass) !important; border:1px solid var(--border) !important; border-radius:13px !important; backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); }
.tech-chip { background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:13px; padding:15px; transition:all .22s ease; }
.tech-chip:hover { border-color:rgba(45,212,191,0.3); transform:translateY(-2px); }
.tech-k { font-size:10px; letter-spacing:1px; text-transform:uppercase; font-weight:600; }
.tech-v { font-size:13px; color:#cbd5e1; margin-top:5px; }
</style>
""", unsafe_allow_html=True)


def render_ring(pct, c1, c2):
    circ = 578
    offset = circ * (1 - pct / 100)
    return f"""
    <div class="ring-wrap">
      <svg viewBox="0 0 220 220" width="230" height="230">
        <defs>
          <linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>
          </linearGradient>
          <filter id="rglow" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="4" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>
        <circle cx="110" cy="110" r="92" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="15"/>
        <circle cx="110" cy="110" r="92" fill="none" stroke="url(#rg)" stroke-width="15"
                stroke-linecap="round" stroke-dasharray="{circ}" stroke-dashoffset="{offset:.1f}"
                transform="rotate(-90 110 110)" filter="url(#rglow)"
                style="animation:sweep 1.1s cubic-bezier(.2,.8,.2,1) both"/>
      </svg>
      <div class="ring-center"><div class="ring-num">{pct:.0f}%</div><div class="ring-lab">Probabilitas</div></div>
    </div>
    <style>@keyframes sweep{{from{{stroke-dashoffset:{circ}}}to{{stroke-dashoffset:{offset:.1f}}}}}</style>
    """


def plotly_dark(fig, height=320):
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "DM Sans", "color": "#8a97a8"}, margin=dict(t=46, b=12, l=10, r=10),
        title_font={"family": "Sora", "size": 14, "color": "#eaf1f7"},
        legend={"font": {"color": "#8a97a8"}},
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    return fig


def why_chart(contribs):
    c = contribs[::-1]
    labels = [x["label"] for x in c]
    vals = [x["value"] for x in c]
    inputs = [str(x["input"]) for x in c]
    colors = ["#f43f5e" if v > 0 else "#2dd4bf" for v in vals]
    fig = go.Figure(go.Bar(
        y=labels, x=vals, orientation="h", marker=dict(color=colors),
        text=inputs, textposition="outside", textfont=dict(color="#8a97a8", size=11),
        hovertemplate="%{y}<br>kontribusi: %{x:+.3f}<extra></extra>",
        cliponaxis=False,
    ))
    fig.add_vline(x=0, line_color="rgba(255,255,255,0.18)")
    fig.update_layout(xaxis_title="← menahan (bertahan)        mendorong keluar →")
    return plotly_dark(fig, height=380)


def employee_summary(payload, res):
    """Ringkasan profil karyawan + narasi faktor risiko dari SHAP."""
    gender_id = "Pria" if payload["Gender"] == "Male" else "Wanita"
    ot = "bekerja lembur" if payload["OverTime"] == "Yes" else "tidak lembur"
    travel_map = {
        "Non-Travel": "tidak pernah bepergian dinas",
        "Travel_Rarely": "jarang bepergian dinas",
        "Travel_Frequently": "sering bepergian dinas",
    }
    travel = travel_map.get(payload["BusinessTravel"], "")
    edu_map = {1: "Di bawah D3", 2: "D3", 3: "S1", 4: "S2", 5: "S3"}
    edu = edu_map.get(payload["Education"], str(payload["Education"]))

    profil = (
        f"{gender_id}, {payload['Age']} tahun, status {payload['MaritalStatus']} — "
        f"berperan sebagai <b>{payload['JobRole']}</b> di departemen <b>{payload['Department']}</b>. "
        f"Pendidikan {edu}, bidang {payload['EducationField']}. "
        f"Gaji <b>${payload['MonthlyIncome']:,}/bulan</b>, sudah <b>{payload['YearsAtCompany']} tahun</b> "
        f"di perusahaan (posisi saat ini {payload['YearsInCurrentRole']} thn), "
        f"saat ini <b>{ot}</b> dan {travel}."
    )
    contribs = res.get("contributions", [])
    drivers = [c for c in contribs if c["direction"] == "naik"][:3]
    anchors = [c for c in contribs if c["direction"] == "turun"][:3]
    prob_pct = res["probability"] * 100
    risk_id = {"Low": "RENDAH", "Medium": "SEDANG", "High": "TINGGI"}[res["risk_level"]]
    driver_parts = [f"{c['label']} ({c['input']})" for c in drivers]
    anchor_parts = [f"{c['label']} ({c['input']})" for c in anchors]
    driver_text = ", ".join(driver_parts) if driver_parts else "tidak ada faktor dominan"
    anchor_text = ", ".join(anchor_parts) if anchor_parts else "tidak ada faktor penahan dominan"
    analisis = (
        f"Model mendeteksi risiko <b>{risk_id}</b> dengan probabilitas <b>{prob_pct:.0f}%</b>. "
        f"Faktor yang <span style='color:#fb7185;font-weight:600'>mendorong risiko keluar</span>: {driver_text}. "
        f"Faktor yang <span style='color:#5eead4;font-weight:600'>menahan karyawan ini</span>: {anchor_text}."
    )
    return profil, analisis


def header(eyebrow, title, sub):
    st.markdown(f"""
    <div class="topbar">
      <div><div class="eyebrow">{eyebrow}</div><div class="h-title">{title}</div><div class="h-sub">{sub}</div></div>
      <div class="env-pill"><span class="dot"></span> Production · Live</div>
    </div>
    """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div class="brand">
      <svg width="42" height="42" viewBox="0 0 40 40" fill="none">
        <rect width="40" height="40" rx="11" fill="url(#g)"/>
        <path d="M11 25 L17 18 L22 23 L29 13" stroke="#042620" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="29" cy="13" r="2.6" fill="#042620"/>
        <defs><linearGradient id="g" x1="0" y1="0" x2="40" y2="40"><stop stop-color="#2dd4bf"/><stop offset="1" stop-color="#10b981"/></linearGradient></defs>
      </svg>
      <div><div class="brand-name">Sentinel</div><div class="brand-sub">Attrition Intel</div></div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("nav", ["Prediksi Risiko", "Analitik", "Tentang"], label_visibility="collapsed")

    online = model_loaded = False
    try:
        h = requests.get(f"{API_URL}/health", timeout=3).json()
        online = True
        model_loaded = bool(h.get("model_loaded"))
    except Exception:
        pass
    sc = "var(--accent)" if (online and model_loaded) else "var(--high)"
    stt = "Operational" if (online and model_loaded) else ("API down" if not online else "No model")
    st.markdown(f"""
    <div class="side-card">
      <div class="side-label">System Status</div>
      <div class="side-row"><span><span class="dot" style="background:{sc};box-shadow:0 0 0 4px rgba(45,212,191,.12)"></span>Inference API</span>
        <span style="color:{sc};font-weight:600">{stt}</span></div>
      <div class="side-row"><span>Model</span><span style="font-family:'JetBrains Mono'">Random Forest</span></div>
      <div class="side-row"><span>Explainer</span><span style="font-family:'JetBrains Mono';color:#5eead4">SHAP</span></div>
    </div>
    <div class="side-card">
      <div class="side-label">Dataset</div>
      <div class="side-row"><span>IBM HR Analytics</span></div>
      <div class="side-row"><span>1.470 records · 44 features</span></div>
    </div>
    """, unsafe_allow_html=True)


# ══ PAGE: PREDIKSI ════════════════════════════════════════════════════════════
if "Prediksi" in page:
    header("Risk Engine", "Prediksi Risiko Karyawan",
           "Skor attrition real-time + penjelasan faktor pendorong (SHAP)")

    with st.form("predict_form"):
        c1, c2, c3 = st.columns(3, gap="large")
        with c1:
            st.markdown('<div class="section-h">Profil</div>', unsafe_allow_html=True)
            Age = st.slider("Usia", 18, 65, 35)
            Gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
            MaritalStatus = st.selectbox("Status Pernikahan", ["Single", "Married", "Divorced"])
            Education = st.selectbox("Pendidikan", [1, 2, 3, 4, 5], index=2,
                                     format_func=lambda x: {1: "Di bawah D3", 2: "D3", 3: "S1", 4: "S2", 5: "S3"}[x])
            EducationField = st.selectbox("Bidang Studi",
                                          ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"])
            DistanceFromHome = st.slider("Jarak dari Rumah (km)", 1, 30, 5)
        with c2:
            st.markdown('<div class="section-h">Pekerjaan</div>', unsafe_allow_html=True)
            Department = st.selectbox("Departemen", ["Sales", "Research & Development", "Human Resources"])
            JobRole = st.selectbox("Posisi",
                                   ["Sales Executive", "Research Scientist", "Laboratory Technician",
                                    "Manufacturing Director", "Healthcare Representative", "Manager",
                                    "Sales Representative", "Research Director", "Human Resources"])
            JobLevel = st.selectbox("Level Jabatan", [1, 2, 3, 4, 5], index=1)
            BusinessTravel = st.selectbox("Perjalanan Dinas", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"], index=1)
            OverTime = st.selectbox("Lembur", ["No", "Yes"])
            NumCompaniesWorked = st.slider("Jumlah Perusahaan Sebelumnya", 0, 10, 2)
            TotalWorkingYears = st.slider("Total Tahun Pengalaman", 0, 40, 10)
        with c3:
            st.markdown('<div class="section-h">Kompensasi & Tenure</div>', unsafe_allow_html=True)
            MonthlyIncome = st.number_input("Gaji Bulanan ($)", 1000, 20000, 5000, step=100)
            DailyRate = st.number_input("Daily Rate", 100, 2000, 800)
            HourlyRate = st.number_input("Hourly Rate", 30, 100, 65)
            MonthlyRate = st.number_input("Monthly Rate", 2000, 27000, 14000)
            PercentSalaryHike = st.slider("Kenaikan Gaji Terakhir (%)", 10, 25, 15)
            StockOptionLevel = st.selectbox("Level Opsi Saham", [0, 1, 2, 3])
            YearsAtCompany = st.slider("Lama di Perusahaan (thn)", 0, 40, 5)
            YearsInCurrentRole = st.slider("Lama di Posisi Ini (thn)", 0, 20, 3)
            YearsSinceLastPromotion = st.slider("Tahun Sejak Promosi", 0, 15, 1)
            YearsWithCurrManager = st.slider("Lama dengan Manajer Ini (thn)", 0, 20, 3)

        st.markdown('<div class="section-h">Kepuasan & Kinerja · 1 rendah → 4 tinggi</div>', unsafe_allow_html=True)
        s1, s2, s3, s4, s5, s6 = st.columns(6)
        with s1: JobSatisfaction = st.selectbox("Kepuasan Kerja", [1, 2, 3, 4], index=2)
        with s2: EnvironmentSatisfaction = st.selectbox("Lingkungan", [1, 2, 3, 4], index=2)
        with s3: RelationshipSatisfaction = st.selectbox("Hubungan", [1, 2, 3, 4], index=2)
        with s4: JobInvolvement = st.selectbox("Keterlibatan", [1, 2, 3, 4], index=2)
        with s5: WorkLifeBalance = st.selectbox("Work-Life", [1, 2, 3, 4], index=2)
        with s6: PerformanceRating = st.selectbox("Performa", [1, 2, 3, 4], index=2)
        TrainingTimesLastYear = st.slider("Sesi Pelatihan Tahun Lalu", 0, 6, 2)

        submitted = st.form_submit_button("Analisis Risiko  →", use_container_width=True)

    if submitted:
        payload = {
            "Age": Age, "BusinessTravel": BusinessTravel, "DailyRate": DailyRate,
            "Department": Department, "DistanceFromHome": DistanceFromHome, "Education": Education,
            "EducationField": EducationField, "EnvironmentSatisfaction": EnvironmentSatisfaction,
            "Gender": Gender, "HourlyRate": HourlyRate, "JobInvolvement": JobInvolvement,
            "JobLevel": JobLevel, "JobRole": JobRole, "JobSatisfaction": JobSatisfaction,
            "MaritalStatus": MaritalStatus, "MonthlyIncome": MonthlyIncome, "MonthlyRate": MonthlyRate,
            "NumCompaniesWorked": NumCompaniesWorked, "OverTime": OverTime,
            "PercentSalaryHike": PercentSalaryHike, "PerformanceRating": PerformanceRating,
            "RelationshipSatisfaction": RelationshipSatisfaction, "StockOptionLevel": StockOptionLevel,
            "TotalWorkingYears": TotalWorkingYears, "TrainingTimesLastYear": TrainingTimesLastYear,
            "WorkLifeBalance": WorkLifeBalance, "YearsAtCompany": YearsAtCompany,
            "YearsInCurrentRole": YearsInCurrentRole, "YearsSinceLastPromotion": YearsSinceLastPromotion,
            "YearsWithCurrManager": YearsWithCurrManager,
        }
        try:
            with st.spinner("Menjalankan inferensi & analisis SHAP..."):
                r = requests.post(f"{API_URL}/explain", json=payload, timeout=30)
            r.raise_for_status()
            res = r.json()
            prob_pct = res["probability"] * 100
            risk = res["risk_level"]
            rc = {"Low": "low", "Medium": "medium", "High": "high"}[risk]
            rlabel = {"Low": "Risiko Rendah", "Medium": "Risiko Sedang", "High": "Risiko Tinggi"}[risk]
            pred = "Berisiko Keluar" if res["prediction"] == "Will Leave" else "Cenderung Bertahan"
            grad = {"Low": ("#2dd4bf", "#10b981"), "Medium": ("#fbbf24", "#f59e0b"), "High": ("#fb7185", "#f43f5e")}[risk]

            st.markdown(f"""
            <div class="verdict {rc}">
              <div><div class="verdict-lab">Prediksi Model</div><div class="verdict-pred">{pred}</div></div>
              <div class="badge {rc}">● {rlabel}</div>
            </div>
            """, unsafe_allow_html=True)

            profil_txt, analisis_txt = employee_summary(payload, res)
            st.markdown(f"""
            <div class="panel" style="margin-top:0">
              <div class="section-h">Profil Karyawan</div>
              <p style="font-size:14px;color:#cbd5e1;line-height:1.75;margin:0 0 12px">{profil_txt}</p>
              <div class="rec-box" style="border-left-color:#6366f1">{analisis_txt}</div>
            </div>
            """, unsafe_allow_html=True)

            col_left, col_right = st.columns([1, 1.45], gap="large")
            with col_left:
                st.markdown(render_ring(prob_pct, grad[0], grad[1]), unsafe_allow_html=True)
                st.markdown(f"""
                <div style="padding-top:4px">
                  <div class="section-h">Rekomendasi Tindakan</div>
                  <div class="rec-box">{res['recommendation']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_right:
                st.markdown('<div class="section-h">Kenapa? · Faktor Pendorong Prediksi</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="legend">
                  <span><span class="lg-dot" style="background:#f43f5e"></span><b>Merah</b> = mendorong keluar</span>
                  <span><span class="lg-dot" style="background:#2dd4bf"></span><b>Teal</b> = menahan (bertahan)</span>
                  <span style="color:var(--faint)">angka = nilai input</span>
                </div>
                """, unsafe_allow_html=True)
                st.plotly_chart(why_chart(res["contributions"]), use_container_width=True)
                if res["contributions"]:
                    top = res["contributions"][0]
                    arah = "menaikkan" if top["direction"] == "naik" else "menurunkan"
                    st.caption(
                        f"Faktor paling berpengaruh: **{top['label']}** "
                        f"(nilai {top['input']}) {arah} risiko paling besar."
                    )
        except requests.exceptions.ConnectionError:
            st.error(f"Tidak terhubung ke inference API ({API_URL}). Jalankan: uvicorn api.main:app --reload")
        except requests.exceptions.Timeout:
            st.error("Request timeout — model sedang memproses, coba lagi.")
        except requests.exceptions.HTTPError as e:
            st.error(f"API error: {e.response.text}")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")


# ══ PAGE: ANALITIK ════════════════════════════════════════════════════════════
elif "Analitik" in page:
    header("Operations", "Analitik & Model Insight", "Riwayat keputusan, tren, dan faktor global model")

    # Global feature importance (independen dari riwayat)
    try:
        fi = requests.get(f"{API_URL}/feature-importance?top=12", timeout=8).json()
    except Exception:
        fi = []

    try:
        r = requests.get(f"{API_URL}/predictions?limit=100", timeout=10)
        r.raise_for_status()
        rows = r.json()
    except requests.exceptions.ConnectionError:
        rows = None
        st.error(f"Tidak terhubung ke inference API ({API_URL}).")

    if rows is not None:
        if not rows:
            st.info("Belum ada prediksi tercatat. Mulai dari menu Prediksi Risiko.")
            if fi:
                st.markdown('<div class="section-h">Faktor Pendorong Attrition (Global)</div>', unsafe_allow_html=True)
                dfi = pd.DataFrame(fi).sort_values("importance")
                figi = go.Figure(go.Bar(
                    x=dfi["importance"], y=dfi["label"], orientation="h",
                    marker=dict(color=dfi["importance"],
                                colorscale=[[0, "#0e7c6b"], [1, "#2dd4bf"]])))
                figi.update_layout(xaxis_title="Importance")
                st.plotly_chart(plotly_dark(figi, 420), use_container_width=True)
        else:
            df = pd.DataFrame(rows)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            total = len(df)
            high = int((df["risk_level"] == "High").sum())
            med = int((df["risk_level"] == "Medium").sum())
            avg = df["probability"].mean() * 100

            st.markdown(f"""
            <div class="kpi-grid">
              <div class="kpi"><div class="kpi-label">Total Prediksi</div><div class="kpi-value">{total}</div><div class="kpi-foot">sesi tercatat</div></div>
              <div class="kpi"><div class="kpi-label">Risiko Tinggi</div><div class="kpi-value" style="color:#fb7185">{high}</div><div class="kpi-foot">perlu intervensi</div></div>
              <div class="kpi"><div class="kpi-label">Risiko Sedang</div><div class="kpi-value" style="color:#fbbf24">{med}</div><div class="kpi-foot">pantau berkala</div></div>
              <div class="kpi"><div class="kpi-label">Rata-rata Skor</div><div class="kpi-value" style="color:#5eead4">{avg:.0f}%</div><div class="kpi-foot">probabilitas</div></div>
            </div>
            """, unsafe_allow_html=True)

            a, b = st.columns([1.3, 1], gap="large")
            with a:
                st.markdown('<div class="section-h">Faktor Pendorong Attrition (Global)</div>', unsafe_allow_html=True)
                if fi:
                    dfi = pd.DataFrame(fi).sort_values("importance")
                    figi = go.Figure(go.Bar(
                        x=dfi["importance"], y=dfi["label"], orientation="h",
                        marker=dict(color=dfi["importance"],
                                    colorscale=[[0, "#0e7c6b"], [1, "#2dd4bf"]])))
                    figi.update_layout(xaxis_title="Importance")
                    st.plotly_chart(plotly_dark(figi, 400), use_container_width=True)
                else:
                    st.info("Feature importance tidak tersedia.")
            with b:
                st.markdown('<div class="section-h">Distribusi Risiko</div>', unsafe_allow_html=True)
                figp = px.pie(df, names="risk_level", hole=0.64,
                              color="risk_level",
                              color_discrete_map={"Low": "#2dd4bf", "Medium": "#f59e0b", "High": "#f43f5e"})
                figp.update_traces(textinfo="percent", textfont_color="#fff",
                                   marker=dict(line=dict(color="#06080c", width=3)))
                st.plotly_chart(plotly_dark(figp, 300), use_container_width=True)
                split = df["prediction"].map({"Will Leave": "Berisiko Keluar", "Will Stay": "Bertahan"}).value_counts()
                figs = go.Figure(go.Bar(x=split.values, y=split.index, orientation="h",
                                        marker_color=["#f43f5e", "#2dd4bf"][:len(split)]))
                st.plotly_chart(plotly_dark(figs, 150), use_container_width=True)

            c, d = st.columns(2, gap="large")
            with c:
                st.markdown('<div class="section-h">Tren Skor Risiko</div>', unsafe_allow_html=True)
                dft = df.sort_values("timestamp")
                figt = go.Figure(go.Scatter(x=dft["timestamp"], y=dft["probability"] * 100,
                                            mode="lines+markers", line=dict(color="#2dd4bf", width=2),
                                            fill="tozeroy", fillcolor="rgba(45,212,191,0.12)", marker=dict(size=5)))
                figt.update_layout(yaxis_title="Probabilitas (%)")
                st.plotly_chart(plotly_dark(figt, 300), use_container_width=True)
            with d:
                st.markdown('<div class="section-h">Distribusi Probabilitas</div>', unsafe_allow_html=True)
                figh = px.histogram(df, x="probability", nbins=20, color_discrete_sequence=["#2dd4bf"])
                figh.update_layout(xaxis_title="Probabilitas", yaxis_title="Jumlah", bargap=0.08)
                st.plotly_chart(plotly_dark(figh, 300), use_container_width=True)

            wl = df[df["risk_level"] == "High"].sort_values("probability", ascending=False)
            if not wl.empty:
                st.markdown('<div class="section-h">Watchlist Risiko Tinggi</div>', unsafe_allow_html=True)
                wt = wl[["timestamp", "probability"]].head(10).copy()
                wt.columns = ["Waktu", "Probabilitas"]
                wt["Probabilitas"] = wt["Probabilitas"].apply(lambda x: f"{x * 100:.1f}%")
                st.dataframe(wt, use_container_width=True, hide_index=True)

            st.markdown('<div class="section-h">Riwayat Terbaru</div>', unsafe_allow_html=True)
            t = df[["timestamp", "probability", "prediction", "risk_level"]].copy()
            t.columns = ["Waktu", "Probabilitas", "Prediksi", "Risiko"]
            t["Probabilitas"] = t["Probabilitas"].apply(lambda x: f"{x * 100:.1f}%")
            t["Prediksi"] = t["Prediksi"].map({"Will Leave": "Berisiko Keluar", "Will Stay": "Bertahan"})
            st.dataframe(t, use_container_width=True, hide_index=True)
            if st.button("Hapus Semua Riwayat"):
                requests.delete(f"{API_URL}/predictions")
                st.success("Riwayat dihapus.")
                st.rerun()


# ══ PAGE: TENTANG ═════════════════════════════════════════════════════════════
else:
    header("Overview", "Tentang Sentinel", "Sistem machine learning untuk retensi karyawan proaktif")
    a, b = st.columns(2, gap="large")
    with a:
        st.markdown("""
        <div class="panel">
          <div class="section-h">Masalah Bisnis</div>
          <p style="font-size:14px;color:#cbd5e1;line-height:1.75">
            Turnover karyawan menelan biaya <b style="color:#5eead4">50–200% gaji tahunan</b> per orang
            untuk rekrutmen, pelatihan, dan hilangnya produktivitas. Tim HR umumnya baru bertindak
            <i>setelah</i> surat resign masuk — sudah terlambat.</p>
        </div>
        <div class="panel">
          <div class="section-h">Solusi</div>
          <p style="font-size:14px;color:#cbd5e1;line-height:1.75">
            Model <b style="color:#5eead4">Random Forest</b> memprediksi risiko attrition dari 44 fitur,
            dan <b style="color:#5eead4">SHAP</b> menjelaskan <i>kenapa</i> tiap keputusan diambil — sehingga
            HR bisa bertindak tepat sasaran, bukan menebak.</p>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.markdown("""
        <div class="panel">
          <div class="section-h">Tech Stack</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
            <div class="tech-chip"><div class="tech-k" style="color:#2dd4bf">MODEL</div><div class="tech-v">scikit-learn · RF<br>SMOTE · SHAP</div></div>
            <div class="tech-chip"><div class="tech-k" style="color:#10b981">API</div><div class="tech-v">FastAPI<br>SQLAlchemy · SQLite</div></div>
            <div class="tech-chip"><div class="tech-k" style="color:#f59e0b">UI</div><div class="tech-v">Streamlit<br>Plotly</div></div>
            <div class="tech-chip"><div class="tech-k" style="color:#f43f5e">DEVOPS</div><div class="tech-v">Docker<br>GitHub Actions</div></div>
          </div>
        </div>
        <div class="panel">
          <div class="section-h">Performa Model</div>
          <div class="kpi-grid" style="grid-template-columns:repeat(3,1fr)">
            <div class="kpi"><div class="kpi-label">ROC-AUC</div><div class="kpi-value" style="font-size:24px">0.78</div></div>
            <div class="kpi"><div class="kpi-label">Recall</div><div class="kpi-value" style="font-size:24px;color:#5eead4">0.70</div></div>
            <div class="kpi"><div class="kpi-label">F1</div><div class="kpi-value" style="font-size:24px">0.49</div></div>
          </div>
          <p style="font-size:12.5px;color:#8a97a8;margin-top:14px;line-height:1.6">
            IBM HR Analytics · 1.470 karyawan · ~16% attrition. Threshold dituning ke ~0.28
            untuk memaksimalkan recall (menangkap karyawan berisiko).</p>
        </div>
        """, unsafe_allow_html=True)