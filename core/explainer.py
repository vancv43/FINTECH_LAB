"""
Executive Explainer — Layer 5 of AI Agent Pipeline
Role Prompting + Constrained Rewrite (Slide 7, 9, 12)
bunq Finn pattern: raw ML output → human-friendly narrative
FLAN-T5: lazy load, thread-safe
"""
import threading
from datetime import datetime

URGENCY_ICON = {"high":"🔴","medium":"🟡","low":"🟢"}
DEPT_ICON = {"Finance Advisor":"💰","IT Copilot":"⚙️","HR Bot":"👥","Product Management":"📦"}

_lock=threading.Lock(); _tok=_mdl=None; _loaded=False; _err=None

def _load_flan():
    global _tok,_mdl,_loaded,_err
    if _loaded: return True
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        print("[FLAN] Loading google/flan-t5-large ... (~60s first time)")
        _tok = AutoTokenizer.from_pretrained("google/flan-t5-large")
        _mdl = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
        _loaded=True; print("[FLAN] ✅ Ready"); return True
    except Exception as e:
        _err=str(e); print(f"[FLAN] ❌ {e}"); return False

def _flan_rewrite(text):
    # Slide 7: Role Prompting + Constrained Rewrite pattern
    prompt = (
        "You are a senior compliance officer at a global bank. "
        "Rewrite the following operational alert as a professional executive brief. "
        "Rules: preserve all facts, no jargon, max 8 sentences, "
        "end with: 'Please consult a licensed professional before acting.'\n\nText:\n" + text
    )
    with _lock:
        inp = _tok(prompt, return_tensors="pt", truncation=True, max_length=512)
        out = _mdl.generate(**inp, max_new_tokens=280, temperature=0.3, do_sample=True)
        r   = _tok.decode(out[0], skip_special_tokens=True).strip()
    return r if len(r)>80 else None

class EnterpriseExplainer:
    def __init__(self): self.query_log=[]

    def build_structured(self, business_name, issue_desc, kb, br) -> str:
        dept=kb.get("department","Ops"); urg=kb.get("urgency_level","medium")
        ts=datetime.now().strftime("%Y-%m-%d %H:%M")
        report = (
            f"=== EXECUTIVE OPERATIONAL ANALYSIS REPORT ===\n"
            f"Business: {business_name}\nGenerated: {ts}\n{'─'*50}\n\n"
            f"{URGENCY_ICON.get(urg,'🟡')} INCIDENT CLASSIFICATION\n"
            f"- Issue:      {issue_desc}\n"
            f"- Agent:      {DEPT_ICON.get(dept,'🏢')} {dept}\n"
            f"- Alert:      {urg.upper()}\n"
            f"- Confidence: {kb.get('confidence_score',0)*100:.1f}%\n\n"
            f"RECOMMENDED DIGITAL SOLUTION\n{kb.get('solution','N/A')}\n\n"
            f"IMMEDIATE ACTION\n{kb.get('recommended_action','N/A')}\n\n"
            f"BUDGET PROJECTION (RandomForest ML Engine)\n"
            f"- Cost:   ${br.get('estimated_cost',0):,.2f} USD\n"
            f"- 95% CI: ${br.get('confidence_low',0):,.0f} – ${br.get('confidence_high',0):,.0f}\n"
            f"- R²:     {br.get('model_accuracy',0):.1f}%\n\n"
            f"{'─'*50}\n"
            f"Note: Auto-generated per MIT PE Digital Transformation Framework."
        )
        self.query_log.append({"ts":ts,"business":business_name,"dept":dept,
                               "urg":urg,"cost":br.get("estimated_cost",0)})
        return report

    def build_executive_brief(self, business_name, issue_desc, kb, br, use_llm=False):
        base = self.build_structured(business_name, issue_desc, kb, br)
        if not use_llm:
            return base, "FLAN-T5 not activated — deterministic report"
        if not _load_flan():
            return base, f"⚠️ FLAN load failed: {_err}"
        try:
            r = _flan_rewrite(base)
            if r:
                return (f"[✅ FLAN-T5-Large Enhanced]\n{'─'*50}\n{r}\n\n{'─'*50}\n[Deterministic]\n{base}",
                        "✅ FLAN-T5-Large rewrite applied")
            return base, "⚠️ FLAN output too short — fallback"
        except Exception as e:
            return base, f"⚠️ FLAN error: {e}"

    def format_api_log(self, kb, br) -> str:
        return (f"[Agent]: {kb.get('department','N/A')}\n"
                f"[Pattern]: '{kb.get('issue_pattern','N/A')}'\n"
                f"[Confidence]: {kb.get('confidence_score',0)*100:.2f}%\n"
                f"[Action]: {kb.get('recommended_action','N/A')}\n"
                f"[Budget]: ${br.get('estimated_cost',0):,.2f} USD")
