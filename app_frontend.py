"""
AI Finance Lab Frontend — Step-by-Step Student UI
Port: 7861
URL : http://127.0.0.1:7861
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

import gradio as gr
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app_backend import run_analysis, get_kb_stats


# =========================
# COLOR PALETTES
# =========================
PALETTES = {
    "Lab Guide": ["#00B4D8", "#1565C0", "#8B5CF6", "#10B981", "#F59E0B"],
    "Risk Review": ["#EF4444", "#F59E0B", "#1565C0", "#64748B", "#10B981"],
    "Operations": ["#10B981", "#00B4D8", "#1565C0", "#F59E0B", "#8B5CF6"],
}

BUSINESS_OPTIONS = [
    "VinFintech Corp",
    "Techcombank Digital",
    "VPBank AI Division",
    "MBBank Analytics",
    "Sacombank Operations",
    "ACB Risk Management",
    "HDBank Finance Dept",
    "TPBank Innovation Lab",
    "VietCredit Group",
    "FE Credit Analytics",
    "Agribank Digital Unit",
    "BIDV Smart Banking",
]

ISSUE_OPTIONS = [
    "delays in calculating employees end-of-year performance KPIs and bonuses",
    "slow monthly financial reporting consolidation",
    "manual invoice reconciliation causing errors",
    "customer churn prediction failure",
    "loan approval processing bottleneck",
]

CHART_LIST = [
    "Cost Sensitivity",
    "Cost Breakdown",
    "Feature Importance",
    "Budget Confidence",
    "Urgency Distribution",
    "Cost vs Team Size",
]

session_history = []


# =========================
# CSS — Lab Guide Visual System
# =========================
LAB_CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=DM+Sans:wght@300;400;600;700&family=Playfair+Display:wght@700;900&display=swap');

:root {
  --navy:   #0A1628;
  --blue:   #1565C0;
  --cyan:   #00B4D8;
  --gold:   #F59E0B;
  --green:  #10B981;
  --red:    #EF4444;
  --purple: #8B5CF6;
  --gray:   #64748B;
  --light:  #F0F4FF;
  --border: #E2E8F0;
  --code-bg:#0D1B2A;
}

/* ── Global ── */
body, .gradio-container {
  background: #F8FAFF !important;
  color: var(--navy);
  font-family: 'DM Sans', ui-sans-serif, system-ui, sans-serif !important;
}
.gradio-container { max-width: 1120px !important; }

/* ── HERO ── */
.lab-hero {
  background: var(--navy);
  border-radius: 0 0 16px 16px;
  margin: -16px -8px 32px;
  padding: 44px 40px 0;
  overflow: hidden;
  position: relative;
}
.lab-hero::before {
  content: "";
  position: absolute;
  top: -70px; right: -90px;
  width: 440px; height: 440px;
  background: radial-gradient(circle, rgba(0,180,216,0.18) 0%, transparent 70%);
  pointer-events: none;
}
.lab-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(0,180,216,0.15);
  border: 1px solid rgba(0,180,216,0.42);
  border-radius: 20px; padding: 5px 16px;
  color: var(--cyan); font-size: 11px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
}
.lab-hero h1 {
  color: white;
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(1.9rem, 4vw, 3.1rem);
  line-height: 1.12; margin: 18px 0 10px;
}
.lab-hero h1 span { color: var(--cyan); }
.lab-hero > p { color: #A8C4E8; max-width: 700px; font-size: 0.97rem; margin: 0 0 28px; }
.lab-meta {
  display: flex; flex-wrap: wrap; gap: 28px;
  border-top: 1px solid rgba(255,255,255,0.08);
  padding: 16px 0;
}
.lab-meta-item .lbl {
  display: block; color: #64748B;
  font-size: 10px; font-weight: 700;
  letter-spacing: 1px; text-transform: uppercase;
}
.lab-meta-item .val { display: block; color: #FFFFFF; font-size: 14px; font-weight: 700; }
.hero-progress { height: 4px; margin: 0 -40px; background: rgba(255,255,255,0.06); }
.hero-progress div { height: 4px; background: linear-gradient(90deg, var(--cyan), var(--purple)); }

/* ── PIPELINE BAR ── */
.pipeline-wrap {
  background: #FFFFFF; border: 1px solid var(--border);
  border-radius: 12px; padding: 20px 24px; margin-bottom: 28px;
  overflow-x: auto;
}
.pipeline-title {
  font-size: 10px; font-weight: 700; letter-spacing: 2px;
  color: var(--gray); text-transform: uppercase; margin-bottom: 14px;
}
.pipeline { display: flex; align-items: center; gap: 0; }
.pipe-box {
  background: #F8FAFF; border: 1.5px solid var(--border);
  border-radius: 10px; padding: 10px 16px;
  text-align: center; min-width: 120px; flex-shrink: 0;
  transition: all 0.2s;
}
.pipe-box .picon { font-size: 20px; margin-bottom: 4px; display: block; }
.pipe-box .plabel { font-size: 11px; font-weight: 700; color: var(--navy); line-height: 1.3; }
.pipe-box .psub { font-size: 10px; color: var(--gray); margin-top: 2px; display: block; }
.pipe-box.active { border-color: var(--cyan); background: rgba(0,180,216,0.07); }
.pipe-box.active .plabel { color: var(--blue); }
.pipe-arrow { color: var(--cyan); font-size: 18px; padding: 0 8px; flex-shrink: 0; font-weight: 700; }

/* ── CAPSTONE BOX ── */
.pipe-box.capstone {
  border: 2px solid var(--gold);
  background: linear-gradient(135deg, #FEF9EC 0%, #FFF7ED 100%);
  cursor: pointer;
  text-decoration: none;
  display: block;
  transition: all 0.2s;
  min-width: 130px;
}
.pipe-box.capstone:hover {
  border-color: #D97706;
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(245,158,11,0.25);
}
.pipe-box.capstone .plabel { color: #92400E; font-weight: 800; }
.pipe-box.capstone .psub { color: #B45309; }
.capstone-arrow { color: var(--gold); font-size: 18px; padding: 0 8px; flex-shrink: 0; font-weight: 700; }
.capstone-sep {
  width: 1px; height: 48px; background: var(--border);
  margin: 0 6px; flex-shrink: 0; align-self: center;
}

/* ── STEP SECTION ── */
.step-section {
  background: #FFFFFF; border: 1px solid var(--border);
  border-radius: 14px; margin-bottom: 20px;
  overflow: hidden;
}
.step-header {
  display: flex; align-items: center; gap: 14px;
  padding: 18px 22px;
  border-bottom: 1px solid var(--border);
}
.step-num {
  width: 38px; height: 38px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; font-family: 'IBM Plex Mono', monospace;
  font-size: 14px; font-weight: 700;
}
.step-num.s1 { background: #EEF2FF; color: var(--purple); }
.step-num.s2 { background: #ECFDF5; color: var(--green); }
.step-num.s3 { background: rgba(0,180,216,0.12); color: var(--cyan); }
.step-num.s4 { background: #FFF7ED; color: #EA580C; }
.step-num.s5 { background: #F5F3FF; color: var(--purple); }
.step-header h2 { color: var(--navy); font-size: 1.05rem; font-weight: 700; margin: 0; }
.step-header p { color: var(--gray); font-size: 11.5px; margin: 2px 0 0; }
.step-badge {
  margin-left: auto; font-size: 10px; font-weight: 700;
  padding: 3px 12px; border-radius: 20px; letter-spacing: .5px; text-transform: uppercase;
}
.step-badge.theory { background: #EEF2FF; color: var(--purple); }
.step-badge.run    { background: #FFF7ED; color: #EA580C; }
.step-badge.result { background: rgba(0,180,216,0.12); color: var(--cyan); }
.step-badge.chart  { background: #F5F3FF; color: var(--purple); }
.step-body { padding: 22px 24px; }

/* ── CALLOUT ── */
.callout {
  border-radius: 10px; padding: 12px 16px;
  margin: 0 0 20px; display: flex; gap: 12px; align-items: flex-start;
  font-size: 12.5px; line-height: 1.5;
}
.callout-icon { font-size: 16px; flex-shrink: 0; margin-top: 1px; }
.callout.info   { background: #EFF6FF; border-left: 3px solid var(--blue); }
.callout.theory { background: #F5F3FF; border-left: 3px solid var(--purple); }
.callout.tip    { background: #ECFDF5; border-left: 3px solid var(--green); }
.callout.warn   { background: #FFFBEB; border-left: 3px solid var(--gold); }

/* ── INPUT GRID ── */
.input-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0 16px; }
.input-grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0 16px; }
.field-label {
  font-size: 10px; font-weight: 700; letter-spacing: 1px;
  color: var(--gray); text-transform: uppercase; margin-bottom: 4px; display: block;
}
.field-hint { font-size: 11px; color: var(--gray); margin-top: 4px; }

/* ── RUN BUTTON ── */
.run-btn-wrap {
  display: flex; gap: 12px; align-items: center;
  margin: 8px 0 0;
}

/* ── KPI CARDS ROW ── */
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.kpi-card {
  background: #FFFFFF; border: 1px solid var(--border);
  border-radius: 12px; padding: 16px 20px;
  transition: all 0.2s;
}
.kpi-card.ready { border-color: var(--cyan); }
.kpi-card-label {
  font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
  color: var(--gray); text-transform: uppercase; margin-bottom: 6px;
}
.kpi-card-value {
  font-size: 1.55rem; font-weight: 700; color: var(--navy);
  font-family: 'IBM Plex Mono', monospace;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.kpi-card-value.await { color: #CBD5E1; font-size: 0.85rem; font-family: 'DM Sans', sans-serif; }

/* ── STEP STEPPER ── */
.stepper {
  display: flex; align-items: center; gap: 4px;
  margin-bottom: 20px;
}
.stepper-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--border); flex-shrink: 0;
}
.stepper-dot.done { background: var(--cyan); }
.stepper-line { flex: 1; height: 2px; background: var(--border); }
.stepper-line.done { background: var(--cyan); }

/* ── MONO OUTPUT — light theme (dễ đọc) ── */
.mono-out textarea {
  background: #F8FAFF !important;
  color: #1E293B !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 12.5px !important;
  line-height: 1.72 !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
}
/* API log — dùng màu navy nhẹ để phân biệt với ML */
.api-log-out textarea {
  background: #F0F4FF !important;
  color: #0A1628 !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 12px !important;
  line-height: 1.72 !important;
  border: 1px solid #C7D5F0 !important;
  border-radius: 8px !important;
}

/* ── CHART CARD ── */
.chart-card {
  background: #FFFFFF; border: 1px solid var(--border);
  border-radius: 12px; overflow: hidden;
}
.chart-controls {
  display: flex; gap: 14px; align-items: flex-end;
  padding: 16px 20px; border-bottom: 1px solid var(--border);
  flex-wrap: wrap;
}

/* ── SESSION HISTORY ── */
.history-section {
  background: #FFFFFF; border: 1px solid var(--border);
  border-radius: 12px; padding: 18px 22px;
  margin-bottom: 28px;
}

/* ── GRADIO OVERRIDES ── */
.gradio-container label, .gradio-container .block-title {
  color: var(--navy) !important; font-weight: 600 !important;
  font-size: 13px !important;
}
.gradio-container textarea, .gradio-container input, .gradio-container select {
  font-family: 'DM Sans', ui-sans-serif !important;
  border-radius: 8px !important;
  border-color: var(--border) !important;
}
.gradio-container textarea:focus, .gradio-container input:focus {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 3px rgba(0,180,216,0.12) !important;
}
.gradio-container button.primary, .gradio-container button[variant="primary"] {
  background: var(--navy) !important;
  border: none !important; border-radius: 10px !important;
  color: white !important; font-weight: 700 !important;
  font-size: 15px !important; padding: 12px 32px !important;
  letter-spacing: 0.3px !important;
  transition: all 0.2s !important;
}
.gradio-container button.primary:hover, .gradio-container button[variant="primary"]:hover {
  background: var(--blue) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 18px rgba(21,101,192,0.28) !important;
}
.gradio-container .tabs { border-radius: 10px !important; }
.gradio-container .tabitem {
  background: #FFFFFF !important; border-color: var(--border) !important;
}
.gradio-container .tab-nav button {
  font-weight: 600 !important; font-size: 13px !important;
}
.gradio-container .tab-nav button.selected {
  color: var(--blue) !important; border-bottom-color: var(--blue) !important;
}
.gradio-container .accordion {
  border-radius: 10px !important; border-color: var(--border) !important;
}
.gradio-container .svelte-1gfkn6j {
  border-radius: 8px !important;
}

/* ── SLIDER CUSTOM ── */
.gradio-container input[type=range] { accent-color: var(--cyan); }

/* ── SECTION DIVIDER ── */
.sdivider {
  height: 1px; background: var(--border); margin: 28px 0;
}

/* ── INSTRUCTION TAG ── */
.ins-tag {
  display: inline-block; font-size: 10px; font-weight: 700;
  letter-spacing: 1px; text-transform: uppercase;
  background: var(--light); color: var(--blue);
  border-radius: 4px; padding: 2px 8px; margin-bottom: 10px;
  border: 1px solid var(--border);
}

@media (max-width: 768px) {
  .lab-hero { margin: -16px -16px 24px; padding: 32px 20px 0; }
  .kpi-row { grid-template-columns: 1fr 1fr; }
  .input-grid-2, .input-grid-3 { grid-template-columns: 1fr; }
  .pipeline { flex-direction: column; gap: 6px; }
}
"""


# =========================
# CHART HELPERS
# =========================
def empty_chart(msg="⬆ Nhấn Analyze để xem biểu đồ"):
    fig = go.Figure()
    fig.add_annotation(
        text=msg, x=0.5, y=0.5,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(color="#94A3B8", size=14, family="DM Sans")
    )
    fig.update_layout(
        height=380, paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        font=dict(color="#64748B", family="DM Sans"),
        margin=dict(l=24, r=24, t=34, b=24),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
    )
    return fig


def chart_pie(cost, p):
    fig = go.Figure(go.Pie(
        labels=["Labor", "Infrastructure", "Risk Buffer", "Overhead"],
        values=[cost.get("labor", 0), cost.get("infrastructure", 0),
                cost.get("risk_buffer", 0), cost.get("overhead", 0)],
        hole=.45, marker_colors=p[:4],
        textfont_size=12,
    ))
    fig.update_layout(title="Cost Breakdown", height=380,
                      font=dict(family="DM Sans"),
                      margin=dict(l=24, r=24, t=52, b=24),
                      paper_bgcolor="#FFFFFF")
    return fig


def chart_feature(fi, p):
    items = sorted(fi.items(), key=lambda x: x[1])
    fig = go.Figure(go.Bar(
        x=[v for _, v in items], y=[k for k, _ in items],
        orientation="h", marker_color=p[0],
        marker_line_color="#FFFFFF", marker_line_width=1,
    ))
    fig.update_layout(
        title="Feature Importance", height=380,
        font=dict(family="DM Sans"),
        margin=dict(l=140, r=24, t=52, b=28),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        xaxis=dict(gridcolor="#E2E8F0"),
    )
    return fig


def chart_confidence(br, p):
    cost, low, high = br["estimated_cost"], br["confidence_low"], br["confidence_high"]
    x = np.linspace(low, high, 120)
    y = np.exp(-(x - cost) ** 2 / (2 * 5000 ** 2))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, fill="tozeroy",
        line=dict(color=p[0], width=2.5),
        fillcolor="rgba(0,180,216,0.14)"
    ))
    fig.add_vline(x=cost, line_color=p[4], line_width=2,
                  annotation_text=f"${cost:,.0f}", annotation_position="top")
    fig.update_layout(
        title="Budget Confidence Interval", height=380,
        font=dict(family="DM Sans"),
        margin=dict(l=48, r=24, t=52, b=38),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        xaxis=dict(gridcolor="#E2E8F0"),
        yaxis=dict(visible=False),
    )
    return fig


def chart_donut(ks, p):
    d = ks["urgency_distribution"]
    fig = go.Figure(go.Pie(
        labels=list(d.keys()), values=list(d.values()),
        hole=.60, marker_colors=p,
        textfont_size=12,
    ))
    fig.update_layout(
        title="Urgency Distribution (KB)", height=380,
        font=dict(family="DM Sans"),
        margin=dict(l=24, r=24, t=52, b=24),
        paper_bgcolor="#FFFFFF"
    )
    return fig


def chart_scatter(p):
    try:
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), "data", "project_cost_data.csv"))
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["team_size"], y=df["estimated_cost"],
            mode="markers",
            marker=dict(color=p[0], size=9, opacity=0.75,
                        line=dict(color="#FFFFFF", width=1))
        ))
        fig.update_layout(
            title="Cost Sensitivity vs Team Size", height=380,
            font=dict(family="DM Sans"),
            margin=dict(l=54, r=24, t=52, b=42),
            plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
            xaxis=dict(title="Team Size", gridcolor="#E2E8F0"),
            yaxis=dict(title="Estimated Cost ($)", gridcolor="#E2E8F0"),
        )
        return fig
    except Exception:
        return empty_chart("Không tìm thấy dữ liệu CSV")


def render_chart(name, result_json, theme):
    p = PALETTES[theme]
    if not result_json or result_json == "{}":
        return empty_chart()
    try:
        r = json.loads(result_json)
    except Exception:
        return empty_chart("Lỗi parse JSON")
    if "Sensitivity" in name:    return chart_scatter(p)
    if "Breakdown" in name:      return chart_pie(r["cost_breakdown"], p)
    if "Feature" in name:        return chart_feature(r["feature_importances"], p)
    if "Confidence" in name:     return chart_confidence(r["budget_result"], p)
    if "Urgency" in name:        return chart_donut(r["kb_stats"], p)
    return chart_scatter(p)


# =========================
# MAIN ANALYSIS FUNCTION
# =========================
def analyze_all(business, email, issue, team, dur, risk, region, use_llm, chart, theme):
    r = run_analysis(business, email, int(team), int(dur), risk, region, issue, use_llm)
    br = r["budget_result"]
    kpi_budget = f"${br['estimated_cost']:,.0f}"
    kpi_conf   = f"{r['kb_result']['confidence_score'] * 100:.1f}%"
    kpi_dept   = r["kb_result"]["department"]
    kpi_urg    = r["kb_result"]["urgency_level"].upper()

    session_history.append({
        "Business": business,
        "Issue": issue[:35] + "..." if len(issue) > 35 else issue,
        "Budget": kpi_budget,
        "Urgency": kpi_urg,
    })

    rj = json.dumps(r, default=str)
    ml_summary = (
        f"Estimated Cost : {kpi_budget}\n"
        f"95% CI         : ${br['confidence_low']:,.0f} – ${br['confidence_high']:,.0f}\n"
        f"Model Accuracy : {br['model_accuracy']}%\n"
        f"Department     : {kpi_dept}\n"
        f"Urgency        : {kpi_urg}\n"
        f"Confidence     : {kpi_conf}"
    )

    hist_df = pd.DataFrame(session_history)
    hist_md = hist_df.to_markdown(index=False) if not hist_df.empty else "_Chưa có phân tích._"

    return (
        kpi_budget, kpi_conf, kpi_dept, kpi_urg,
        r["executive_brief"],
        ml_summary,
        r["api_log"],
        render_chart(chart, rj, theme),
        rj,
        hist_md,
        r["flan_status"],
    )


# =========================
# HTML HELPERS
# =========================
def hero_html():
    return """
<div class="lab-hero">
  <div class="lab-badge">🎓 MIT PE × Quanskill Bootcamp · Lab Runtime</div>
  <h1>AI in <span>Digital Finance</span><br>&amp; Fintech — Lab</h1>
  <p>Giao diện thực nghiệm bám theo AI Finance Lab Guide: từ user input, retrieval, ML budget engine, memory đến executive explainer. Làm theo từng bước để hiểu toàn bộ Agentic Pipeline.</p>
  <div class="lab-meta">
    <div class="lab-meta-item"><span class="lbl">Kịch bản</span><span class="val">Lab B · AI Agent Pipeline</span></div>
    <div class="lab-meta-item"><span class="lbl">Backend</span><span class="val">FastAPI-ready</span></div>
    <div class="lab-meta-item"><span class="lbl">ML Model</span><span class="val">TF-IDF · RandomForest</span></div>
    <div class="lab-meta-item"><span class="lbl">Explainer</span><span class="val">FLAN-T5 (optional)</span></div>
  </div>
  <div class="hero-progress"><div style="width:100%"></div></div>
</div>
"""


def pipeline_html():
    # Build absolute URL cho Gradio file serving
    _abs = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "docs", "Capstone_Module8.html")
    )
    _url = f"/file={_abs}"

    return f"""
<div class="pipeline-wrap">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px">
    <div class="pipeline-title" style="margin-bottom:0">🔀 Agentic Pipeline — Slide 5 · Chatbot vs AI Agent</div>
    < "
       style="display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:700;
              letter-spacing:1px;text-transform:uppercase;cursor:pointer;border:none;
              background:rgba(245,158,11,0.12);color:#92400E;
              border:1px solid rgba(245,158,11,0.4);border-radius:6px;padding:5px 13px">
      📋 Xem Đề cương Capstone ↗
    </button>
  </div>
  <div class="pipeline">
    <div class="pipe-box active">
      <span class="picon">📝</span>
      <div class="plabel">Step 1<br>User Input</div>
      <span class="psub">Issue description</span>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-box">
      <span class="picon">🔍</span>
      <div class="plabel">Step 2<br>Retrieval</div>
      <span class="psub">TF-IDF / KB</span>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-box">
      <span class="picon">🤖</span>
      <div class="plabel">Step 3<br>ML Predict</div>
      <span class="psub">RandomForest</span>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-box">
      <span class="picon">💾</span>
      <div class="plabel">Step 4<br>Memory</div>
      <span class="psub">Session log</span>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-box">
      <span class="picon">✍️</span>
      <div class="plabel">Step 5<br>LLM Explainer</div>
      <span class="psub">FLAN-T5</span>
    </div>
    <div class="pipe-arrow">→</div>
    <div class="pipe-box active">
      <span class="picon">📊</span>
      <div class="plabel">Output<br>Dashboard</div>
      <span class="psub">Charts + Report</span>
    </div>

    <!-- SEPARATOR + CAPSTONE -->
    <div class="capstone-sep"></div>
    <div class="capstone-arrow">→</div>

    <div class="pipe-box capstone"
         onclick="window.open('{_url}','_blank')"
         title="Mở Capstone Module 8 trong tab mới">
      <span class="picon">🏆</span>
      <div class="plabel">Capstone<br>Mini-Project</div>
      <span class="psub">Module 8 · Slide 15–16</span>
      <span style="display:block;font-size:9px;color:#B45309;margin-top:4px;font-weight:700">↗ Mở Tab Mới</span>
    </div>
  </div>
</div>
"""


def step_header_html(num, num_class, title, subtitle, badge, badge_class):
    return f"""
<div class="step-header">
  <div class="step-num {num_class}">{num}</div>
  <div>
    <h2>{title}</h2>
    <p>{subtitle}</p>
  </div>
  <span class="step-badge {badge_class}">{badge}</span>
</div>
"""


def callout_html(kind, icon, text):
    return f"""
<div class="callout {kind}">
  <div class="callout-icon">{icon}</div>
  <div style="font-size:12.5px;line-height:1.55">{text}</div>
</div>
"""


def kpi_block_html(label, value_id, value="—", is_await=True):
    cls = "await" if is_await else ""
    return f"""
<div class="kpi-card">
  <div class="kpi-card-label">{label}</div>
  <div class="kpi-card-value {cls}" id="{value_id}">{value}</div>
</div>
"""


# =========================
# BUILD APP
# =========================
def build_app():
    base_theme = gr.themes.Base(
        primary_hue="blue",
        secondary_hue="cyan",
        neutral_hue="slate",
        font=["DM Sans", "ui-sans-serif", "system-ui"],
        font_mono=["IBM Plex Mono", "ui-monospace"],
    )

    with gr.Blocks(theme=base_theme, title="AI Finance Lab — Lab B", css=LAB_CSS) as demo:

        result_state = gr.State("{}")

        # ── HERO ──
        gr.HTML(hero_html())

        # ── PIPELINE OVERVIEW ──
        gr.HTML(pipeline_html())

        # ════════════════════════════════════════
        # STEP 1 — INPUT DỮ LIỆU
        # ════════════════════════════════════════
        with gr.Group(elem_classes="step-section"):
            gr.HTML(step_header_html(
                "01", "s1",
                "Nhập Dữ Liệu Input",
                "Business context đưa vào agent pipeline · Slides 11–13",
                "Setup", "theory"
            ))
            with gr.Column(elem_classes="step-body"):
                gr.HTML(callout_html(
                    "theory", "🧠",
                    "<strong>Lý thuyết (Slide 11):</strong> AI Agent cần business context để routing đúng. "
                    "Các trường bên dưới tương ứng với <em>User Input layer</em> của Agentic Pipeline. "
                    "Thay đổi Issue để xem Knowledge Base retrieval trả về kết quả khác nhau."
                ))

                # Row 1: Business (dropdown) + Email
                with gr.Row():
                    bname = gr.Dropdown(
                        choices=BUSINESS_OPTIONS,
                        value="VinFintech Corp",
                        allow_custom_value=True,
                        label="🏢  Business Name / Phòng ban",
                        info="Chọn từ danh sách hoặc gõ tên mới — dùng để cá nhân hoá Executive Brief"
                    )
                    email = gr.Textbox(
                        label="📧  Administrator Email",
                        value="admin@vinfintech.vn",
                        placeholder="admin@company.com",
                        info="Ghi vào session log (Memory layer)"
                    )

                # Row 2: Issue (full width)
                issue = gr.Dropdown(
                    ISSUE_OPTIONS,
                    value=ISSUE_OPTIONS[0],
                    label="🔍  Issue Description — chọn vấn đề cần AI Agent xử lý",
                    info="Đây là query input cho TF-IDF Retrieval. Thay đổi để thấy Department & Urgency thay đổi."
                )

                # Row 3: Team + Duration
                with gr.Row():
                    team = gr.Slider(
                        1, 100, value=12, step=1,
                        label="👥  Team Size (số người)",
                        info="Feature quan trọng nhất của RandomForest budget model"
                    )
                    dur = gr.Slider(
                        1, 52, value=8, step=1,
                        label="📅  Duration (tuần)",
                        info="Kết hợp với Team Size → ước tính labor cost"
                    )

                # Row 4: Risk + Region
                with gr.Row():
                    risk = gr.Radio(
                        ["low", "medium", "high"],
                        value="medium",
                        label="⚠️  Risk Level",
                        info="Tác động đến risk_buffer trong cost breakdown"
                    )
                    region = gr.Dropdown(
                        ["northeast", "northwest", "southeast", "southwest"],
                        value="southwest",
                        label="🗺️  Region",
                        info="Overhead cost thay đổi theo vùng địa lý"
                    )

                # ── RULE DESCRIPTION PANEL ──
                gr.HTML("""
<div style="margin:18px 0 6px">
  <div style="font-size:10px;font-weight:700;letter-spacing:2px;color:#64748B;text-transform:uppercase;margin-bottom:10px">
    📐 Quy tắc & Công thức tính — Hướng dẫn chọn giá trị hợp lý
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">

    <!-- Team Size -->
    <div style="background:#F8FAFF;border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px">
      <div style="font-size:12px;font-weight:700;color:#0A1628;margin-bottom:6px">👥 Team Size (số người)</div>
      <div style="font-size:11.5px;color:#334155;line-height:1.6">
        <b>Công thức:</b> <code style="background:#EEF2FF;color:#1565C0;padding:1px 5px;border-radius:3px;font-family:monospace">Labor Cost = Team × Duration × $800/tuần</code><br>
        <div style="margin-top:6px;display:flex;flex-direction:column;gap:3px">
          <span>🟢 <b>1–10 người</b> → Small team, chi phí thấp, phù hợp PoC</span>
          <span>🟡 <b>11–30 người</b> → Mid-scale, phù hợp production build</span>
          <span>🔴 <b>31–100 người</b> → Enterprise, cần quản trị chặt</span>
        </div>
        <div style="margin-top:7px;font-size:11px;color:#64748B;font-style:italic">
          ✏️ RandomForest coi Team Size là feature quan trọng nhất trong 4 features.
        </div>
      </div>
    </div>

    <!-- Duration -->
    <div style="background:#F8FAFF;border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px">
      <div style="font-size:12px;font-weight:700;color:#0A1628;margin-bottom:6px">📅 Duration (tuần)</div>
      <div style="font-size:11.5px;color:#334155;line-height:1.6">
        <b>Công thức:</b> <code style="background:#EEF2FF;color:#1565C0;padding:1px 5px;border-radius:3px;font-family:monospace">Total Labor = Team × Duration × Rate</code><br>
        <div style="margin-top:6px;display:flex;flex-direction:column;gap:3px">
          <span>🟢 <b>1–4 tuần</b> → Quick fix / Hotfix sprint</span>
          <span>🟡 <b>5–12 tuần</b> → Full project cycle (phổ biến nhất)</span>
          <span>🔴 <b>13–52 tuần</b> → Long-term programme, cần milestone rõ</span>
        </div>
        <div style="margin-top:7px;font-size:11px;color:#64748B;font-style:italic">
          ✏️ Duration × Team Size tạo ra labor_hours — input chính của ML model.
        </div>
      </div>
    </div>

    <!-- Risk Level -->
    <div style="background:#F8FAFF;border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px">
      <div style="font-size:12px;font-weight:700;color:#0A1628;margin-bottom:6px">⚠️ Risk Level</div>
      <div style="font-size:11.5px;color:#334155;line-height:1.6">
        <b>Công thức:</b> <code style="background:#EEF2FF;color:#1565C0;padding:1px 5px;border-radius:3px;font-family:monospace">risk_buffer = base_cost × risk_rate</code><br>
        <div style="margin-top:6px;display:flex;flex-direction:column;gap:3px">
          <span>🟢 <b>Low</b> → risk_rate = <b>5%</b> · Dự án nội bộ, ít phụ thuộc bên ngoài</span>
          <span>🟡 <b>Medium</b> → risk_rate = <b>15%</b> · Tích hợp API, 2–3 hệ thống</span>
          <span>🔴 <b>High</b> → risk_rate = <b>30%</b> · Regulatory, real-time trading, security-critical</span>
        </div>
        <div style="margin-top:7px;font-size:11px;color:#64748B;font-style:italic">
          ✏️ Risk buffer được cộng vào Total Cost trong Cost Breakdown chart.
        </div>
      </div>
    </div>

    <!-- Region -->
    <div style="background:#F8FAFF;border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px">
      <div style="font-size:12px;font-weight:700;color:#0A1628;margin-bottom:6px">🗺️ Region (vùng địa lý)</div>
      <div style="font-size:11.5px;color:#334155;line-height:1.6">
        <b>Công thức:</b> <code style="background:#EEF2FF;color:#1565C0;padding:1px 5px;border-radius:3px;font-family:monospace">overhead = base_cost × region_multiplier</code><br>
        <div style="margin-top:6px;display:flex;flex-direction:column;gap:3px">
          <span>🟢 <b>Southwest</b> → multiplier <b>×1.00</b> · HCM, chi phí baseline</span>
          <span>🟡 <b>Southeast</b> → multiplier <b>×1.05</b> · Khu vực Đông Nam</span>
          <span>🟡 <b>Northwest</b> → multiplier <b>×1.10</b> · Khu vực Tây Bắc</span>
          <span>🔴 <b>Northeast</b> → multiplier <b>×1.15</b> · Hà Nội, chi phí cao nhất</span>
        </div>
        <div style="margin-top:7px;font-size:11px;color:#64748B;font-style:italic">
          ✏️ Region ảnh hưởng Overhead trong Cost Breakdown — thấy rõ trên biểu đồ Pie.
        </div>
      </div>
    </div>

  </div>
</div>
""")

                # Row 5: FLAN option
                gr.HTML(callout_html(
                    "tip", "💡",
                    "<strong>FLAN-T5 Explainer (optional):</strong> Khi bật, pipeline gọi thêm một Small Language Model "
                    "để viết executive brief ngôn ngữ tự nhiên thay vì template. Tắt để chạy nhanh hơn khi không có GPU."
                ))
                with gr.Row():
                    flan = gr.Checkbox(
                        label="✨ Bật FLAN-T5 Language Model Explainer",
                        value=False,
                    )
                    flan_status = gr.Textbox(
                        label="FLAN Status",
                        interactive=False,
                        scale=3,
                        placeholder="Trạng thái FLAN-T5 hiện thị ở đây sau khi chạy..."
                    )

        # ════════════════════════════════════════
        # STEP 2 — RUN ANALYSIS
        # ════════════════════════════════════════
        with gr.Group(elem_classes="step-section"):
            gr.HTML(step_header_html(
                "02", "s2",
                "Chạy Phân Tích",
                "Kích hoạt toàn bộ Agentic Pipeline · Retrieval → ML → Memory → LLM",
                "Run", "run"
            ))
            with gr.Column(elem_classes="step-body"):
                gr.HTML(callout_html(
                    "info", "🚀",
                    "Nhấn <strong>▶ Analyze</strong> để chạy toàn bộ pipeline: "
                    "(1) TF-IDF search knowledge base → "
                    "(2) RandomForest predict budget → "
                    "(3) Ghi session memory → "
                    "(4) Build executive brief. "
                    "Kết quả hiện ở Steps 3, 4, 5 bên dưới."
                ))
                btn = gr.Button("▶  Analyze — Chạy AI Agent Pipeline", variant="primary", size="lg")

        # ════════════════════════════════════════
        # STEP 3 — KPI KẾT QUẢ
        # ════════════════════════════════════════
        with gr.Group(elem_classes="step-section"):
            gr.HTML(step_header_html(
                "03", "s3",
                "KPI Kết Quả",
                "Các chỉ số chính từ Retrieval + ML layers",
                "Result", "result"
            ))
            with gr.Column(elem_classes="step-body"):
                gr.HTML(callout_html(
                    "info", "📊",
                    "<strong>Budget</strong> = RandomForest prediction · "
                    "<strong>Confidence</strong> = TF-IDF similarity score · "
                    "<strong>Department</strong> + <strong>Urgency</strong> = Knowledge Base routing output"
                ))
                with gr.Row(equal_height=True):
                    k_budget = gr.Textbox(
                        label="💰 Estimated Budget",
                        value="Awaiting analysis...",
                        interactive=False,
                        info="RandomForest ML prediction ($USD)"
                    )
                    k_conf = gr.Textbox(
                        label="🎯 KB Confidence",
                        value="Awaiting analysis...",
                        interactive=False,
                        info="TF-IDF similarity score (%)"
                    )
                    k_dept = gr.Textbox(
                        label="🏛 Department",
                        value="Awaiting analysis...",
                        interactive=False,
                        info="Routing từ Knowledge Base"
                    )
                    k_urg = gr.Textbox(
                        label="🚨 Urgency Level",
                        value="Awaiting analysis...",
                        interactive=False,
                        info="Priority classification"
                    )

        # ════════════════════════════════════════
        # STEP 4 — PHÂN TÍCH CHI TIẾT
        # ════════════════════════════════════════
        with gr.Group(elem_classes="step-section"):
            gr.HTML(step_header_html(
                "04", "s4",
                "Phân Tích Chi Tiết",
                "Executive Brief · ML Engine output · API Pipeline Log",
                "Output", "run"
            ))
            with gr.Column(elem_classes="step-body"):
                with gr.Tabs():
                    with gr.Tab("📋  Executive Summary"):
                        gr.HTML(callout_html(
                            "tip", "✍️",
                            "<strong>LLM Explainer output (Slide 13):</strong> "
                            "Khi FLAN-T5 tắt, output là template-based. "
                            "Khi bật, FLAN-T5 generate ngôn ngữ tự nhiên từ context."
                        ))
                        brief_out = gr.Textbox(
                            label="Executive Brief",
                            lines=14, interactive=False,
                            placeholder="Executive brief sẽ hiện ở đây sau khi Analyze...",
                        )

                    with gr.Tab("🤖  ML Predictive Engine"):
                        gr.HTML(callout_html(
                            "theory", "🔬",
                            "<strong>RandomForest Budget Model (Slide 12):</strong> "
                            "Estimated cost + 95% Confidence Interval. "
                            "Model accuracy thể hiện R² score trên test set. "
                            "<br><b>Công thức:</b> <code style='background:#EEF2FF;color:#1565C0;padding:1px 5px;border-radius:3px'>Total = Labor + Infrastructure + Risk Buffer + Overhead</code>"
                        ))
                        ml_out = gr.Textbox(
                            label="Budget Model Output",
                            lines=12, interactive=False,
                            elem_classes="mono-out",
                            placeholder="Estimated Cost, CI, Model Accuracy... hiện ở đây sau khi Analyze."
                        )

                    with gr.Tab("🔌  API Pipeline Log"):
                        gr.HTML(callout_html(
                            "info", "🔗",
                            "<strong>Pipeline Log (Slide 14 — FastAPI):</strong> "
                            "Log đầy đủ từng layer: "
                            "<b>KB retrieval</b> (TF-IDF score + matched pattern) → "
                            "<b>ML prediction</b> (feature values + predicted cost) → "
                            "<b>Memory write</b> (session append) → "
                            "<b>LLM call</b> (FLAN-T5 status). "
                            "Dùng log này để debug và hiểu flow từng bước."
                        ))
                        gr.HTML("""
<div style="display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap">
  <span style="background:#EFF6FF;color:#1565C0;border:1px solid #BFDBFE;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:700">[Agent] Department routing</span>
  <span style="background:#F5F3FF;color:#7C3AED;border:1px solid #DDD6FE;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:700">[Pattern] KB match</span>
  <span style="background:#ECFDF5;color:#059669;border:1px solid #A7F3D0;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:700">[Confidence] Score %</span>
  <span style="background:#FFF7ED;color:#EA580C;border:1px solid #FED7AA;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:700">[Action] Recommendation</span>
  <span style="background:#F0FDF4;color:#166534;border:1px solid #BBF7D0;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:700">[Budget] Estimated $</span>
</div>
""")
                        log_out = gr.Textbox(
                            label="Pipeline Log — Full Output",
                            lines=16, interactive=False,
                            elem_classes="api-log-out",
                            placeholder="[Agent]: ...\n[Pattern]: ...\n[Confidence]: ...\n[Action]: ...\n[Budget]: ...\n\nLog đầy đủ hiện ở đây sau khi Analyze."
                        )

        # ════════════════════════════════════════
        # STEP 5 — ANALYTICS DASHBOARD
        # ════════════════════════════════════════
        with gr.Group(elem_classes="step-section"):
            gr.HTML(step_header_html(
                "05", "s5",
                "Analytics Dashboard",
                "Biểu đồ cost breakdown, confidence, feature importance và knowledge base",
                "Charts", "chart"
            ))
            with gr.Column(elem_classes="step-body"):
                gr.HTML(callout_html(
                    "theory", "📈",
                    "<strong>Hướng dẫn khám phá:</strong> "
                    "① <em>Cost Breakdown</em> → xem phân bổ chi phí · "
                    "② <em>Feature Importance</em> → feature nào ảnh hưởng budget nhất · "
                    "③ <em>Budget Confidence</em> → khoảng tin cậy 95% · "
                    "④ <em>Urgency Distribution</em> → toàn bộ Knowledge Base phân bổ theo urgency"
                ))
                with gr.Row():
                    chart_dd = gr.Dropdown(
                        CHART_LIST, value=CHART_LIST[1],
                        label="📊  Chọn biểu đồ",
                        scale=3
                    )
                    theme_dd = gr.Dropdown(
                        list(PALETTES.keys()), value="Lab Guide",
                        label="🎨  Color Palette",
                        scale=1
                    )
                chart_out = gr.Plot(value=empty_chart(), label="")

        # ════════════════════════════════════════
        # SESSION HISTORY
        # ════════════════════════════════════════
        with gr.Accordion("📂  Session History — Lịch sử phân tích", open=False):
            gr.HTML(callout_html(
                "info", "💾",
                "<strong>Memory Layer (Slide 13):</strong> "
                "Mỗi lần Analyze, kết quả được append vào session log. "
                "Đây là cách AI Agent duy trì context qua nhiều lần tương tác."
            ))
            hist_md = gr.Markdown("_Chưa có phân tích nào._")

        # ════════════════════════════════════════
        # WIRING
        # ════════════════════════════════════════
        inputs = [bname, email, issue, team, dur, risk, region, flan, chart_dd, theme_dd]
        outputs = [
            k_budget, k_conf, k_dept, k_urg,
            brief_out, ml_out, log_out,
            chart_out, result_state, hist_md, flan_status
        ]

        btn.click(fn=analyze_all, inputs=inputs, outputs=outputs)

        chart_dd.change(fn=render_chart, inputs=[chart_dd, result_state, theme_dd], outputs=chart_out)
        theme_dd.change(fn=render_chart, inputs=[chart_dd, result_state, theme_dd], outputs=chart_out)

    return demo


# =========================
if __name__ == "__main__":
    # allowed_paths cho phép Gradio serve file tĩnh trong thư mục docs/
    # → /file=docs/Capstone_Module8.html và /file=docs/AI_Finance_Lab_Guide.html
    _docs = os.path.join(os.path.dirname(__file__), "docs")
    build_app().launch(
        server_name="127.0.0.1",
        server_port=7861,
        share=False,
        allowed_paths=[_docs],
    )
