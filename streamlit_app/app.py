"""Streamlit UI for HR Attrition Predictor — Modern Redesign."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="HR Attrition Predictor",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f0f13 !important;
    border-right: 1px solid #1e1e28;
}
section[data-testid="stSidebar"] * { color: #c8c8d4 !important; }
section[data-testid="stSidebar"] .stRadio label {
    background: #1a1a24 !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    margin: 3px 0 !important;
    border: 1px solid #2a2a38 !important;
    transition: all 0.2s !important;
    font-size: 14px !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: #22222e !important;
    border-color: #6c63ff !important;
}
section[data-testid="stSidebar"] .stRadio [data-checked="true"] + label,
section[data-testid="stSidebar"] .stRadio input:checked + div {
    background: #1e1b4b !important;
    border-color: #6c63ff !important;
    color: #a5b4fc !important;
}

/* Page title */
.page-title {
    font-size: 28px;
    font-weight: 600;
    color: #0f0f13;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}
.page-subtitle {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 2rem;
}

/* Metric cards */
.metric-row {
    display: flex;
    gap: 16px;
    margin-bottom: 2rem;
}
.metric-card {
    flex: 1;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.metric-card.purple::before { background: linear-gradient(90deg, #6c63ff, #a78bfa); }
.metric-card.green::before  { background: linear-gradient(90deg, #10b981, #34d399); }
.metric-card.amber::before  { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.metric-card.red::before    { background: linear-gradient(90deg, #ef4444, #f87171); }
.metric-label {
    font-size: 12px;
    font-weight: 500;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 32px;
    font-weight: 600;
    color: #111827;
    line-height: 1;
}

/* Section headers */
.section-header {
    font-size: 13px;
    font-weight: 600;
    color: #6c63ff;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 1.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #e5e7eb;
}

/* Risk badge */
.risk-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
}
.risk-low    { background: #d1fae5; color: #065f46; }
.risk-medium { background: #fef3c7; color: #92400e; }
.risk-high   { background: #fee2e2; color: #991b1b; }

/* Result panel */
.result-panel {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 28px;
    margin-top: 1.5rem;
    animation: slideUp 0.4s ease;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Recommendation box */
.rec-box {
    background: #f5f3ff;
    border: 1px solid #ddd6fe;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 14px;
    color: #4c1d95;
    line-height: 1.7;
    margin-top: 1rem;
}

/* Status dot */
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #10b981;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* Slider styling */
input[type="range"] { accent-color: #6c63ff; }

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(108, 99, 255, 0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(108, 99, 255, 0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Form inputs */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 1px solid #e5e7eb !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.15) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: 1px solid #e5e7eb;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 14px;
}

/* Divider */
hr { border-color: #f3f4f6 !important; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0 0 1.5rem'>
        <div style='display:flex;align-items:center;gap:12px;margin-bottom:8px'>
            <div style='width:40px;height:40px;background:linear-gradient(135deg,#6c63ff,#8b5cf6);
                        border-radius:12px;display:flex;align-items:center;justify-content:center;
                        font-size:20px'>👥</div>
            <div>
                <div style='font-size:16px;font-weight:600;color:#fff'>HR Attrition</div>
                <div style='font-size:12px;color:#6b7280'>Predictor v1.0</div>
            </div>
        </div>
        <div style='background:#1a1a24;border:1px solid #2a2a38;border-radius:10px;
                    padding:10px 14px;font-size:12px;color:#6b7280;margin-top:8px'>
            <span class='status-dot'></span>
            <span style='color:#10b981;font-weight:500'>API Online</span>
            &nbsp;· Model loaded
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigasi",
        ["🔮  Prediksi", "📊  Dashboard", "ℹ️  Tentang"],
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#1a1a24;border:1px solid #2a2a38;border-radius:10px;padding:14px;font-size:12px;color:#6b7280'>
        <div style='font-weight:500;color:#a5b4fc;margin-bottom:6px'>Dataset</div>
        IBM HR Analytics<br>1,470 karyawan · 35 fitur
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PREDIKSI
# ══════════════════════════════════════════════════════════════════════════════
if "Prediksi" in page:
    st.markdown('<div class="page-title">Prediksi Risiko Karyawan</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Isi data karyawan untuk mengetahui probabilitas attrition secara real-time</div>', unsafe_allow_html=True)

    with st.form("predict_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="section-header">👤 Data Pribadi</div>', unsafe_allow_html=True)
            Age = st.slider("Usia", 18, 65, 35)
            Gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
            MaritalStatus = st.selectbox("Status Pernikahan", ["Single", "Married", "Divorced"])
            Education = st.selectbox(
                "Tingkat Pendidikan",
                [1, 2, 3, 4, 5],
                index=2,
                format_func=lambda x: {1:"1 – Di bawah D3",2:"2 – D3",3:"3 – S1",4:"4 – S2",5:"5 – S3"}[x],
            )
            EducationField = st.selectbox(
                "Bidang Pendidikan",
                ["Life Sciences","Medical","Marketing","Technical Degree","Human Resources","Other"],
            )
            DistanceFromHome = st.slider("Jarak dari Rumah (km)", 1, 30, 5)

        with col2:
            st.markdown('<div class="section-header">💼 Informasi Pekerjaan</div>', unsafe_allow_html=True)
            Department = st.selectbox("Departemen", ["Sales","Research & Development","Human Resources"])
            JobRole = st.selectbox(
                "Posisi",
                ["Sales Executive","Research Scientist","Laboratory Technician",
                 "Manufacturing Director","Healthcare Representative","Manager",
                 "Sales Representative","Research Director","Human Resources"],
            )
            JobLevel = st.selectbox("Level Jabatan", [1,2,3,4,5], index=1)
            BusinessTravel = st.selectbox(
                "Perjalanan Dinas",
                ["Non-Travel","Travel_Rarely","Travel_Frequently"], index=1,
            )
            OverTime = st.selectbox("Lembur", ["No","Yes"])
            NumCompaniesWorked = st.slider("Jumlah Perusahaan Sebelumnya", 0, 10, 2)
            TotalWorkingYears = st.slider("Total Tahun Pengalaman", 0, 40, 10)

        with col3:
            st.markdown('<div class="section-header">💰 Kompensasi & Tenure</div>', unsafe_allow_html=True)
            MonthlyIncome = st.number_input("Gaji Bulanan ($)", 1000, 20000, 5000, step=100)
            DailyRate = st.number_input("Daily Rate", 100, 2000, 800)
            HourlyRate = st.number_input("Hourly Rate", 30, 100, 65)
            MonthlyRate = st.number_input("Monthly Rate", 2000, 27000, 14000)
            PercentSalaryHike = st.slider("Kenaikan Gaji Terakhir (%)", 10, 25, 15)
            StockOptionLevel = st.selectbox("Level Opsi Saham", [0,1,2,3])
            YearsAtCompany = st.slider("Lama di Perusahaan (thn)", 0, 40, 5)
            YearsInCurrentRole = st.slider("Lama di Posisi Saat Ini (thn)", 0, 20, 3)
            YearsSinceLastPromotion = st.slider("Tahun Sejak Promosi Terakhir", 0, 15, 1)
            YearsWithCurrManager = st.slider("Lama dengan Manajer Ini (thn)", 0, 20, 3)

        st.markdown('<div class="section-header">😊 Kepuasan & Kinerja (1=Rendah, 4=Tinggi)</div>', unsafe_allow_html=True)
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1: JobSatisfaction = st.selectbox("Kepuasan Kerja", [1,2,3,4], index=2)
        with c2: EnvironmentSatisfaction = st.selectbox("Lingkungan", [1,2,3,4], index=2)
        with c3: RelationshipSatisfaction = st.selectbox("Hubungan", [1,2,3,4], index=2)
        with c4: JobInvolvement = st.selectbox("Keterlibatan", [1,2,3,4], index=2)
        with c5: WorkLifeBalance = st.selectbox("Work-Life Balance", [1,2,3,4], index=2)
        with c6: PerformanceRating = st.selectbox("Performa", [1,2,3,4], index=2)

        TrainingTimesLastYear = st.slider("Sesi Pelatihan Tahun Lalu", 0, 6, 2)

        submitted = st.form_submit_button("🔮 Prediksi Sekarang", use_container_width=True)

    # ── Result ────────────────────────────────────────────────────────────────
    if submitted:
        payload = {
            "Age": Age, "BusinessTravel": BusinessTravel, "DailyRate": DailyRate,
            "Department": Department, "DistanceFromHome": DistanceFromHome,
            "Education": Education, "EducationField": EducationField,
            "EnvironmentSatisfaction": EnvironmentSatisfaction, "Gender": Gender,
            "HourlyRate": HourlyRate, "JobInvolvement": JobInvolvement,
            "JobLevel": JobLevel, "JobRole": JobRole, "JobSatisfaction": JobSatisfaction,
            "MaritalStatus": MaritalStatus, "MonthlyIncome": MonthlyIncome,
            "MonthlyRate": MonthlyRate, "NumCompaniesWorked": NumCompaniesWorked,
            "OverTime": OverTime, "PercentSalaryHike": PercentSalaryHike,
            "PerformanceRating": PerformanceRating,
            "RelationshipSatisfaction": RelationshipSatisfaction,
            "StockOptionLevel": StockOptionLevel, "TotalWorkingYears": TotalWorkingYears,
            "TrainingTimesLastYear": TrainingTimesLastYear, "WorkLifeBalance": WorkLifeBalance,
            "YearsAtCompany": YearsAtCompany, "YearsInCurrentRole": YearsInCurrentRole,
            "YearsSinceLastPromotion": YearsSinceLastPromotion,
            "YearsWithCurrManager": YearsWithCurrManager,
        }

        try:
            with st.spinner("Menganalisis data karyawan..."):
                r = requests.post(f"{API_URL}/predict", json=payload, timeout=30)
            r.raise_for_status()
            result = r.json()

            prob_pct = result["probability"] * 100
            risk = result["risk_level"]
            risk_class = {"Low": "risk-low", "Medium": "risk-medium", "High": "risk-high"}[risk]
            risk_label = {"Low": "🟢 Risiko Rendah", "Medium": "🟡 Risiko Sedang", "High": "🔴 Risiko Tinggi"}[risk]

            st.markdown('<div class="result-panel">', unsafe_allow_html=True)

            colA, colB, colC = st.columns(3)
            colA.metric("Probabilitas Attrition", f"{prob_pct:.1f}%")
            colB.metric("Prediksi", "Akan Keluar" if result["prediction"] == "Will Leave" else "Akan Bertahan")
            colC.metric("Level Risiko", risk_label)

            # Gauge chart
            gauge_color = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444"}[risk]
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=prob_pct,
                number={"suffix": "%", "font": {"size": 36, "family": "DM Sans"}},
                delta={"reference": 50, "decreasing": {"color": "#10b981"}, "increasing": {"color": "#ef4444"}},
                title={"text": "Skor Risiko", "font": {"size": 14, "family": "DM Sans", "color": "#6b7280"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#e5e7eb"},
                    "bar": {"color": gauge_color, "thickness": 0.25},
                    "bgcolor": "white",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 30],  "color": "#d1fae5"},
                        {"range": [30, 60], "color": "#fef3c7"},
                        {"range": [60, 100],"color": "#fee2e2"},
                    ],
                    "threshold": {
                        "line": {"color": gauge_color, "width": 3},
                        "thickness": 0.8,
                        "value": prob_pct,
                    },
                },
            ))
            fig.update_layout(
                height=280,
                margin=dict(t=40, b=0, l=30, r=30),
                paper_bgcolor="white",
                font={"family": "DM Sans"},
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            <div class="rec-box">
                💡 <strong>Rekomendasi:</strong> {result['recommendation']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            st.error(f"❌ Tidak dapat terhubung ke API di {API_URL}. Pastikan FastAPI berjalan: `uvicorn api.main:app --reload`")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timeout. Model sedang memproses, coba lagi dalam beberapa detik.")
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ API error: {e.response.text}")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif "Dashboard" in page:
    st.markdown('<div class="page-title">Dashboard Prediksi</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Riwayat dan analisis prediksi attrition karyawan</div>', unsafe_allow_html=True)

    try:
        r = requests.get(f"{API_URL}/predictions?limit=100", timeout=10)
        r.raise_for_status()
        rows = r.json()

        if not rows:
            st.info("📭 Belum ada prediksi. Lakukan prediksi pertama di menu Prediksi!")
        else:
            df = pd.DataFrame(rows)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            total = len(df)
            high   = (df["risk_level"] == "High").sum()
            medium = (df["risk_level"] == "Medium").sum()
            low    = (df["risk_level"] == "Low").sum()

            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card purple">
                    <div class="metric-label">Total Prediksi</div>
                    <div class="metric-value">{total}</div>
                </div>
                <div class="metric-card red">
                    <div class="metric-label">Risiko Tinggi</div>
                    <div class="metric-value">{high}</div>
                </div>
                <div class="metric-card amber">
                    <div class="metric-label">Risiko Sedang</div>
                    <div class="metric-value">{medium}</div>
                </div>
                <div class="metric-card green">
                    <div class="metric-label">Risiko Rendah</div>
                    <div class="metric-value">{low}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                fig_pie = px.pie(
                    df, names="risk_level",
                    title="Distribusi Level Risiko",
                    color="risk_level",
                    color_discrete_map={"Low":"#10b981","Medium":"#f59e0b","High":"#ef4444"},
                    hole=0.55,
                )
                fig_pie.update_layout(
                    font_family="DM Sans", height=320,
                    margin=dict(t=40,b=0,l=0,r=0),
                    paper_bgcolor="white",
                    title_font_size=14, title_font_color="#111827",
                )
                fig_pie.update_traces(textinfo="percent+label", textfont_size=12)
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_b:
                fig_hist = px.histogram(
                    df, x="probability", nbins=20,
                    title="Distribusi Probabilitas",
                    color_discrete_sequence=["#6c63ff"],
                )
                fig_hist.update_layout(
                    font_family="DM Sans", height=320,
                    margin=dict(t=40,b=20,l=20,r=20),
                    paper_bgcolor="white", plot_bgcolor="white",
                    title_font_size=14, title_font_color="#111827",
                    xaxis=dict(gridcolor="#f3f4f6", title="Probabilitas"),
                    yaxis=dict(gridcolor="#f3f4f6", title="Jumlah"),
                )
                st.plotly_chart(fig_hist, use_container_width=True)

            st.markdown('<div class="section-header">📋 Riwayat Prediksi Terbaru</div>', unsafe_allow_html=True)
            display_df = df[["timestamp","probability","prediction","risk_level"]].copy()
            display_df.columns = ["Waktu","Probabilitas","Prediksi","Level Risiko"]
            display_df["Probabilitas"] = display_df["Probabilitas"].apply(lambda x: f"{x*100:.1f}%")
            display_df["Prediksi"] = display_df["Prediksi"].map({"Will Leave":"Akan Keluar","Will Stay":"Akan Bertahan"})
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            if st.button("🗑️ Hapus Semua Riwayat"):
                requests.delete(f"{API_URL}/predictions")
                st.success("Riwayat berhasil dihapus!")
                st.rerun()

    except requests.exceptions.ConnectionError:
        st.error(f"❌ Tidak dapat terhubung ke API di {API_URL}.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TENTANG
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown('<div class="page-title">Tentang Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">HR Attrition Predictor — sistem deep learning untuk retensi karyawan</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='background:white;border:1px solid #e5e7eb;border-radius:16px;padding:28px;margin-bottom:16px'>
            <div style='font-size:15px;font-weight:600;color:#111827;margin-bottom:12px'>🎯 Masalah Bisnis</div>
            <p style='font-size:14px;color:#6b7280;line-height:1.7'>
                Turnover karyawan menghabiskan biaya <strong style='color:#6c63ff'>50–200% dari gaji tahunan</strong>
                per karyawan untuk rekrutmen, pelatihan, dan hilangnya produktivitas. Tim HR biasanya
                baru bertindak <em>setelah</em> surat pengunduran diri diterima.
            </p>
        </div>
        <div style='background:white;border:1px solid #e5e7eb;border-radius:16px;padding:28px'>
            <div style='font-size:15px;font-weight:600;color:#111827;margin-bottom:12px'>💡 Solusi</div>
            <p style='font-size:14px;color:#6b7280;line-height:1.7'>
                Model Deep Learning yang memprediksi risiko attrition berdasarkan <strong style='color:#6c63ff'>30+ fitur karyawan</strong>,
                memungkinkan HR bertindak proaktif melalui:
            </p>
            <ul style='font-size:14px;color:#6b7280;line-height:2;padding-left:20px;margin-top:8px'>
                <li>Penyesuaian kompensasi</li>
                <li>Perubahan peran / rotasi</li>
                <li>Percakapan retensi langsung</li>
                <li>Perencanaan pengembangan karir</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:white;border:1px solid #e5e7eb;border-radius:16px;padding:28px;margin-bottom:16px'>
            <div style='font-size:15px;font-weight:600;color:#111827;margin-bottom:16px'>🏗️ Tech Stack</div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px'>
                <div style='background:#f5f3ff;border-radius:10px;padding:14px;text-align:center'>
                    <div style='font-size:11px;font-weight:600;color:#6c63ff;text-transform:uppercase;letter-spacing:0.05em'>ML</div>
                    <div style='font-size:13px;color:#374151;margin-top:4px'>TensorFlow/Keras<br>Keras Tuner · SMOTE</div>
                </div>
                <div style='background:#f0fdf4;border-radius:10px;padding:14px;text-align:center'>
                    <div style='font-size:11px;font-weight:600;color:#10b981;text-transform:uppercase;letter-spacing:0.05em'>API</div>
                    <div style='font-size:13px;color:#374151;margin-top:4px'>FastAPI<br>SQLAlchemy · SQLite</div>
                </div>
                <div style='background:#fff7ed;border-radius:10px;padding:14px;text-align:center'>
                    <div style='font-size:11px;font-weight:600;color:#f59e0b;text-transform:uppercase;letter-spacing:0.05em'>UI</div>
                    <div style='font-size:13px;color:#374151;margin-top:4px'>Streamlit<br>Plotly</div>
                </div>
                <div style='background:#fef2f2;border-radius:10px;padding:14px;text-align:center'>
                    <div style='font-size:11px;font-weight:600;color:#ef4444;text-transform:uppercase;letter-spacing:0.05em'>DevOps</div>
                    <div style='font-size:13px;color:#374151;margin-top:4px'>Docker<br>GitHub Actions</div>
                </div>
            </div>
        </div>
        <div style='background:white;border:1px solid #e5e7eb;border-radius:16px;padding:28px'>
            <div style='font-size:15px;font-weight:600;color:#111827;margin-bottom:12px'>📊 Dataset</div>
            <p style='font-size:14px;color:#6b7280;line-height:1.7'>
                <strong>IBM HR Analytics Employee Attrition & Performance</strong><br>
                dari Kaggle — 1.470 karyawan, 35 fitur, ~16% tingkat attrition
                (ditangani dengan teknik SMOTE untuk mengatasi ketidakseimbangan kelas).
            </p>
        </div>
        """, unsafe_allow_html=True)