"""Orchestrator — connects all pipeline layers"""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from core.database import EnterpriseKnowledgeBase
from core.predictor import BudgetPredictor
from core.explainer import EnterpriseExplainer

_kb=_pred=_exp=None
def _init():
    global _kb,_pred,_exp
    if _kb is None: _kb=EnterpriseKnowledgeBase(); _pred=BudgetPredictor(); _exp=EnterpriseExplainer()
    return _kb,_pred,_exp

def run_analysis(business_name,admin_email,team_size,duration_weeks,risk_level,region,issue_description,use_llm=False):
    kb,pred,exp=_init()
    kb_results=kb.search(issue_description,top_k=1)
    kb_result=kb_results[0] if kb_results else {"issue_pattern":issue_description,"solution":"Manual review.","department":"Operations","urgency_level":"medium","recommended_action":"Escalate.","confidence_score":0.0}
    budget_result=pred.predict(team_size,duration_weeks,risk_level,region)
    cost_breakdown=pred.get_cost_breakdown(team_size,duration_weeks,risk_level,region)
    sensitivity=pred.sensitivity_analysis(team_size,duration_weeks,risk_level,region)
    executive_brief,flan_status=exp.build_executive_brief(business_name,issue_description,kb_result,budget_result,use_llm)
    api_log=exp.format_api_log(kb_result,budget_result)
    return {"executive_brief":executive_brief,"flan_status":flan_status,"api_log":api_log,
            "kb_result":kb_result,"budget_result":budget_result,"cost_breakdown":cost_breakdown,
            "sensitivity":sensitivity,"feature_importances":pred.feature_importances,"kb_stats":kb.get_stats()}

def get_kb_stats(): kb,_,_=_init(); return kb.get_stats()
