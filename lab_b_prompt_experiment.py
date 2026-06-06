"""
Lab B — Prompt Engineering Experiment (Slides 7 & 12)
Thực hành 3 kỹ thuật: Zero-Shot, Role Prompting, Structured Output
Liên kết: bunq Finn pattern + DBS ADA pipeline
"""
from app_backend import run_analysis

r = run_analysis("VinFintech","demo@lab.vn",12,8,"medium","southwest",
    "delays in calculating employees end-of-year performance KPIs and bonuses",False)
kb, br = r["kb_result"], r["budget_result"]
raw_data = f"""
Department: {kb['department']} | Urgency: {kb['urgency_level']}
Issue: delays in calculating KPIs and bonuses
Solution: {kb['solution']}
Action: {kb['recommended_action']}
Budget: ${br['estimated_cost']:,.0f} USD | Confidence: {kb['confidence_score']*100:.0f}%
"""

print("="*60)
print("RAW DATA FROM AI AGENT PIPELINE:"); print(raw_data)

print("="*60); print("STEP 1 — ZERO-SHOT PROMPT (Slide 7)")
print("="*60)
step1 = f"Summarize this operational data: {raw_data}"
print(f"PROMPT:\n{step1}")
print("→ Expected: Generic, technical — what a basic chatbot produces\n")

print("="*60); print("STEP 2 — ROLE + CONSTRAINED REWRITE (bunq Finn pattern — Slide 7, 9)")
print("="*60)
step2 = f"""You are a senior compliance officer at a global bank.
Translate operational system alerts into clear, customer-friendly communications.

Rules:
- No technical jargon
- Maximum 3 sentences
- Include ONE specific next action
- Tone: professional but empathetic
- End with: "Contact support@bank.com if you have questions."

Operational Alert: {raw_data}
Write the customer advisory:"""
print(f"PROMPT:\n{step2}")
print("→ This is the bunq Finn approach: LLM rewriting raw ML output\n")

print("="*60); print("STEP 3 — STRUCTURED OUTPUT for API integration (Slide 7, DBS ADA pattern)")
print("="*60)
step3 = f"""Analyze this alert and respond ONLY in valid JSON.
Alert: {raw_data}
Required structure:
{{"risk_score":"LOW|MEDIUM|HIGH","rationale":"one sentence","recommended_action":"specific step","estimated_resolution_days":integer,"escalation_required":boolean}}"""
print(f"PROMPT:\n{step3}")
print("→ Enables feeding AI output back into workflow automation systems\n")

print("="*60); print("DISCUSSION QUESTIONS:")
print("1. Tại sao Step 2 tốt hơn Step 1 cho retail banking communication?")
print("2. Step 3 có thể auto-feed vào JIRA/ServiceNow workflow không?")
print("3. GDPR Article 22: right to explanation — ảnh hưởng gì đến design?")
print("4. Tại sao bunq Finn cần Role Prompting thay vì Zero-Shot?")
