"""
Gradio Frontend v2 — Port 7860
Left: inputs | Right: Executive Text + ML Engine + API Logs
Below: 6 Plotly charts with dropdown selector
Themes: 5 color palettes
"""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__))
import gradio as gr
import plotly.graph_objects as go
import pandas as pd, numpy as np
from app_backend import run_analysis, get_kb_stats

PALETTES = {
    "🟠 Fintech Orange": ["#E85D04","#F59E0B","#DC2626","#7C3AED","#059669"],
    "🌊 Ocean Blue":     ["#0EA5E9","#06B6D4","#3B82F6","#6366F1","#8B5CF6"],
    "🌿 Forest Green":   ["#10B981","#34D399","#059669","#6EE7B7","#047857"],
    "🌙 Midnight":       ["#94A3B8","#64748B","#475569","#334155","#CBD5E1"],
    "🪻 Lavender":       ["#7C3AED","#A78BFA","#8B5CF6","#C4B5FD","#6D28D9"],
}
CHART_LIST = [
    "📊 Cost Sensitivity — Bar Chart",
    "🥧 Cost Breakdown — Pie Chart",
    "🧠 Feature Importance — Horizontal Bar",
    "📈 Budget Confidence — Area Chart",
    "🍩 Urgency Distribution — Donut",
    "🔵 Cost vs Team Size — Scatter Bubble",
]
session_history = []

def _empty_chart(msg="Click Analyze to generate charts"):
    fig=go.Figure(); fig.add_annotation(text=msg,xref="paper",yref="paper",x=0.5,y=0.5,showarrow=False,font=dict(size=14,color="#888"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",height=350); return fig

def chart_sensitivity(sen, p):
    cats={"team_size":"Team Size","duration":"Duration","risk":"Risk Level"}
    fig=go.Figure()
    for i,(key,label) in enumerate(cats.items()):
        pts=[s for s in sen if s["category"]==key]
        if pts: fig.add_trace(go.Bar(name=label,x=[s["variable"] for s in pts],y=[s["cost"] for s in pts],marker_color=p[i%5]))
    fig.update_layout(title="Cost Sensitivity Analysis",barmode="group",yaxis_tickprefix="$",yaxis_tickformat=",.0f",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",height=380,legend=dict(orientation="h",y=-0.22)); return fig

def chart_pie(bd, p):
    fig=go.Figure(go.Pie(labels=["Labor","Infrastructure","Risk Buffer","Overhead"],values=[bd.get("labor",0),bd.get("infrastructure",0),bd.get("risk_buffer",0),bd.get("overhead",0)],marker_colors=p[:4],hole=0.42,textinfo="label+percent"))
    fig.update_layout(title="Cost Breakdown by Category",height=360,annotations=[dict(text=f"${bd.get('total',0):,.0f}",x=0.5,y=0.5,font_size=14,showarrow=False)],paper_bgcolor="rgba(0,0,0,0)"); return fig

def chart_feature_importance(fi, p):
    items=sorted(fi.items(),key=lambda x:x[1]); labels=[k.replace("_"," ").title() for k,_ in items]; values=[v for _,v in items]
    fig=go.Figure(go.Bar(x=values,y=labels,orientation="h",marker_color=p[:4],text=[f"{v:.3f}" for v in values],textposition="outside"))
    fig.update_layout(title="RandomForest Feature Importance",height=300,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)"); return fig

def chart_confidence(br, p):
    cost=br.get("estimated_cost",0); ci_l=br.get("confidence_low",0); ci_h=br.get("confidence_high",cost*2); std=max(br.get("std_dev",1),1)
    xs=np.linspace(max(0,ci_l*0.8),ci_h*1.2,200); ys=np.exp(-0.5*((xs-cost)/std)**2)
    fig=go.Figure(); fig.add_trace(go.Scatter(x=xs,y=ys,fill="tozeroy",fillcolor=p[0]+"30",line=dict(color=p[0],width=2)))
    fig.add_vline(x=cost,line=dict(color=p[1],width=2.5),annotation_text=f"${cost:,.0f}",annotation_position="top right")
    for vx,lbl in [(ci_l,"CI Low"),(ci_h,"CI High")]: fig.add_vline(x=vx,line=dict(color=p[2],dash="dash"),annotation_text=lbl)
    fig.update_layout(title="Budget Prediction — 95% Confidence Interval",height=340,xaxis_tickprefix="$",xaxis_tickformat=",.0f",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)"); return fig

def chart_donut(ks, urgency, p):
    dist=ks.get("urgency_distribution",{})
    fig=go.Figure(go.Pie(labels=[k.upper() for k in dist],values=list(dist.values()),marker_colors=p,hole=0.58,textinfo="label+value"))
    fig.update_layout(title="KB Urgency Distribution",height=320,annotations=[dict(text=urgency.upper(),x=0.5,y=0.5,font_size=13,showarrow=False)],paper_bgcolor="rgba(0,0,0,0)"); return fig

def chart_scatter(p):
    df=pd.read_csv(os.path.join(os.path.dirname(__file__),"data","project_cost_data.csv"))
    df["risk_label"]=df["risk_level"].map({1:"Low",2:"Medium",3:"High"})
    fig=go.Figure()
    for i,(rl,grp) in enumerate(df.groupby("risk_label")):
        fig.add_trace(go.Scatter(x=grp["team_size"],y=grp["estimated_cost"],mode="markers+text",name=f"Risk: {rl}",text=grp["region"],textposition="top center",marker=dict(size=grp["duration_weeks"]*2.5,color=p[i%5],opacity=0.8)))
    fig.update_layout(title="Cost vs Team Size (bubble = duration weeks)",height=360,yaxis_tickprefix="$",yaxis_tickformat=",.0f",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)"); return fig

def render_chart(name, rj, theme):
    p=PALETTES.get(theme,list(PALETTES.values())[0])
    if not rj or rj=="{}": return _empty_chart()
    try: r=json.loads(rj)
    except: return _empty_chart("JSON parse error")
    bd=r.get("cost_breakdown",{}); sen=r.get("sensitivity",[]); fi=r.get("feature_importances",{})
    br=r.get("budget_result",{}); ks=r.get("kb_stats",{}); urg=r.get("kb_result",{}).get("urgency_level","medium")
    if "Sensitivity" in name: return chart_sensitivity(sen,p)
    if "Pie"         in name: return chart_pie(bd,p)
    if "Feature"     in name: return chart_feature_importance(fi,p)
    if "Confidence"  in name: return chart_confidence(br,p)
    if "Donut"       in name: return chart_donut(ks,urg,p)
    if "Scatter"     in name: return chart_scatter(p)
    return _empty_chart()

def analyze_all(bname,email,ts,dur,risk,region,issue,flan,chart,theme):
    if not bname.strip() or not issue.strip():
        return "⚠️ Fill Business Name and Issue Description.","N/A","",_empty_chart(),"{}","_No queries_","—"
    r=run_analysis(bname,email,int(ts),int(dur),risk,region,issue,flan)
    br=r["budget_result"]
    ml=(f"${br['estimated_cost']:,.2f} USD\n\n95% CI: ${br['confidence_low']:,.0f} – ${br['confidence_high']:,.0f}\n"
        f"R²: {br['model_accuracy']:.1f}%  |  Std Dev: ${br['std_dev']:,.0f}")
    session_history.append({"Business":bname,"Dept":r["kb_result"]["department"],"Urgency":r["kb_result"]["urgency_level"].upper(),
                            "Budget":f"${br['estimated_cost']:,.0f}","Conf":f"{r['kb_result']['confidence_score']*100:.1f}%"})
    rj=json.dumps(r,default=str)
    return (r["executive_brief"],ml,r["api_log"],render_chart(chart,rj,theme),rj,
            pd.DataFrame(session_history).to_markdown(index=False),r["flan_status"])

def build_app():
    with gr.Blocks(theme=gr.themes.Default(primary_hue=gr.themes.colors.orange,secondary_hue=gr.themes.colors.blue),title="Enterprise AI Agent") as demo:
        state=gr.State("{}")
        gr.HTML('<h2 style="margin:0 0 4px">🏢 Digital Business Operations Management</h2><p style="color:#666;margin:0">Gradio Frontend → FastAPI Backend | MIT Professional Education × Quanskill</p>')
        with gr.Row():
            theme_dd=gr.Dropdown(choices=list(PALETTES.keys()),value="🟠 Fintech Orange",label="🎨 Color Theme")
        gr.Markdown("---")
        with gr.Row(equal_height=False):
            with gr.Column(scale=1):
                bname=gr.Textbox(label="Business Name",value="VinFintech Corp")
                email=gr.Textbox(label="Administrator Email",value="admin@vinfintech.vn")
                with gr.Row():
                    ts=gr.Number(label="Project Team Size",value=12,minimum=1)
                    dur=gr.Number(label="Duration (Weeks)",value=8,minimum=1)
                risk=gr.Dropdown(["low","medium","high"],value="medium",label="Risk")
                region=gr.Dropdown(["northeast","northwest","southeast","southwest"],value="southwest",label="Deployment Scope")
                issue=gr.Textbox(label="Issue Description",lines=3,value="delays in calculating employees end-of-year performance KPIs and bonuses")
                flan=gr.Checkbox(label="Activate FLAN-T5 (LLM English tone fine-tuning)")
                flan_status=gr.Textbox(label="FLAN-T5 Status",interactive=False,lines=1)
                btn=gr.Button("🚀 Analyze",variant="primary",size="lg")
            with gr.Column(scale=1):
                gr.HTML("<b>📊 Experimental Results from the Expert System</b>")
                with gr.Row():
                    with gr.Column(scale=3):
                        brief_out=gr.Textbox(label="📄 Executive Platform Text",lines=16,interactive=False)
                    with gr.Column(scale=2):
                        ml_out=gr.Textbox(label="💵 ML Predictive Engine",lines=5,interactive=False)
                        log_out=gr.Textbox(label="ℹ️ Information & API Logs",lines=8,interactive=False)
        gr.Markdown("---\n### 📈 Analytics & Visualization")
        chart_dd=gr.Dropdown(choices=CHART_LIST,value=CHART_LIST[0],label="Select Chart Type")
        chart_out=gr.Plot(show_label=False)
        gr.Markdown("---")
        with gr.Accordion("🕒 Session Query History",open=False):
            hist_md=gr.Markdown("_No queries yet._")
        inputs=[bname,email,ts,dur,risk,region,issue,flan,chart_dd,theme_dd]
        outputs=[brief_out,ml_out,log_out,chart_out,state,hist_md,flan_status]
        btn.click(fn=analyze_all,inputs=inputs,outputs=outputs)
        chart_dd.change(fn=render_chart,inputs=[chart_dd,state,theme_dd],outputs=[chart_out])
        theme_dd.change(fn=render_chart,inputs=[chart_dd,state,theme_dd],outputs=[chart_out])
    return demo

if __name__=="__main__":
    build_app().launch(server_name="0.0.0.0",server_port=7860,share=False)
    # http://127.0.0.1:7860
