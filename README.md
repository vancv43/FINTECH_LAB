# AI in Digital Finance & Fintech — Lab Code
AI Engineer Professional Education × Quanskill Bootcamp

fintech_lab % tree -L 2
.
├── __pycache__
│   ├── app_backend.cpython-310.pyc
│   └── app_frontend.cpython-310.pyc
├── AI_Finance_Lab_Guide.html
├── app_api.py
├── app_backend.py
├── app_frontend_bk.py
├── app_frontend.py
├── core
│   ├── __init__.py
│   ├── __pycache__
│   ├── database.py
│   ├── explainer.py
│   └── predictor.py
├── data
│   ├── enterprise_knowledge.csv
│   └── project_cost_data.csv
├── lab_b_prompt_experiment.py
├── README.md
└── requirements.txt

## Quick Start (macBook)
```bash
# 1. Setup
cd fintech_ai_agent
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Test pipeline
python core/database.py   # Layer 1: Semantic Search
python core/predictor.py  # Layer 2-3: ML Budget Engine

# 3. Run (2 terminals)
python app_api.py          # FastAPI: http://127.0.0.1:8000/docs
python app_frontend.py     # Gradio: http://127.0.0.1:7860

# 4. Lab B experiment
python lab_b_prompt_experiment.py
```

## Architecture (Slides 5, 12, 13)
User Input → KB Search (TF-IDF) → ML Predict (RandomForest) → Explainer (FLAN-T5) → Gradio UI

# kill -9 $(lsof -t -i:7861)
python app_frontend.py
# FINTECH_LAB
# FINTECH_LAB
