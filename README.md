# 🏦 AI Finance Lab — Thực Nghiệm Agentic AI trong Tài Chính

> **MIT PE × Quanskill Bootcamp** — *AI in Digital Finance & Fintech*  
> Môi trường thực nghiệm dành cho sinh viên/học viên: khám phá, thao tác và phân tích hệ thống AI Agent trong ngành tài chính số.

---

## 📋 Tổng Quan Dự Án

**FINTECH_LAB** là ứng dụng thực nghiệm giáo dục minh hoạ một **Agentic AI Pipeline** hoàn chỉnh — từ tiếp nhận yêu cầu nghiệp vụ đến sinh báo cáo tài chính — ứng dụng trực tiếp các công nghệ được triển khai tại các ngân hàng và fintech hàng đầu: bunq (Finn), DBS (ADA/ALAN), Techcombank AI.

### Mục Tiêu Học Tập

| Module | Nội dung | Slide |
|--------|----------|-------|
| Lab A  | ML Budget Prediction với RandomForest + 95% CI | 11, 13 |
| Lab B  | Prompt Engineering: Zero-Shot → Role → Structured Output | 7, 9, 12 |
| Lab C  | API Integration: FastAPI ↔ Gradio real-time | 5, 14 |
| Capstone | End-to-End AI Finance Agent với FAISS + LangChain + SHAP | 15–16 |

### Công Nghệ Áp Dụng Thực Tế

```
bunq Finn        → Role Prompting + Constrained Rewrite (lab_b_prompt_experiment.py)
DBS ALAN         → RandomForest Budget Engine (core/predictor.py)
DBS ADA          → Structured JSON Output for workflow automation
Techcombank AI   → TF-IDF Semantic Knowledge Base (core/database.py)
```

---

## 🗂️ Cấu Trúc Dự Án

```
fintech_lab/
│
├── 📄 app_frontend.py          # Giao diện Gradio — UI chính (5 bước thao tác)
├── 📄 app_backend.py           # Orchestrator — kết nối toàn bộ pipeline
├── 📄 app_api.py               # FastAPI REST API — port 8000
├── 📄 lab_b_prompt_experiment.py   # Lab B: 3 kỹ thuật Prompt Engineering
│
├── 📁 core/                    # Các module AI cốt lõi
│   ├── database.py             # Layer 1: TF-IDF Semantic Knowledge Base
│   ├── predictor.py            # Layer 2–3: RandomForest ML Budget Engine
│   └── explainer.py            # Layer 5: FLAN-T5 LLM Executive Explainer
│
├── 📁 data/                    # Dữ liệu huấn luyện và tri thức
│   ├── enterprise_knowledge.csv    # 4 loại sự cố fintech + giải pháp
│   └── project_cost_data.csv       # 10 mẫu chi phí dự án thực tế
│
├── 📁 docs/                    # Tài liệu học tập
│   ├── AI_Finance_Lab_Guide.html   # Hướng dẫn Lab đầy đủ (HTML)
│   └── Capstone_Module8.html       # Đề cương Capstone Mini-Project
│
├── 📁 Google_Colab/
│   └── Fintech_Lab.ipynb       # Notebook độc lập cho Google Colab / VS Code
│
└── 📄 requirements.txt         # Dependencies Python
```

---

## ⚡ Cài Đặt & Khởi Động Nhanh

### Yêu Cầu Hệ Thống

- Python 3.10 hoặc 3.11
- macOS / Linux / Windows (WSL2)
- RAM tối thiểu: 4 GB (8 GB nếu bật FLAN-T5)
- Ổ đĩa: ~2 GB (bao gồm model FLAN-T5 khi tải lần đầu)

### Cài Đặt Môi Trường

```bash
# 1. Clone dự án (hoặc giải nén zip từ giảng viên)
cd fintech_lab

# 2. Tạo virtual environment
python3.11 -m venv .venv

# 3. Kích hoạt môi trường
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows

# 4. Cài đặt thư viện
pip install -r requirements.txt
```

### Kiểm Tra Pipeline Trước Khi Chạy

```bash
# Kiểm tra Knowledge Base (Layer 1)
python core/database.py
# ✅ Expected: [KB] Loaded 4 patterns — Dept: HR Bot | Confidence: 84.2%

# Kiểm tra ML Engine (Layer 2-3)
python core/predictor.py
# ✅ Expected: [ML] RandomForest ready — R²=0.998
#              Cost: $37,xxx | 95% CI: $35,xxx – $39,xxx
```

### Khởi Động Ứng Dụng

**Terminal 1 — FastAPI Backend:**
```bash
python app_api.py
# → API: http://127.0.0.1:8000
# → Swagger docs: http://127.0.0.1:8000/docs
```

**Terminal 2 — Gradio Frontend:**
```bash
python app_frontend.py
# → UI: http://127.0.0.1:7860
```

> **Lưu ý:** Nếu port bị chiếm, giải phóng bằng:
> ```bash
> kill -9 $(lsof -t -i:7860)    # Gradio
> kill -9 $(lsof -t -i:8000)    # FastAPI
> ```

### Chạy Trên Google Colab

```python
# Mở file: Google_Colab/Fintech_Lab.ipynb
# Chọn: Runtime → Run All
# Gradio sẽ tự tạo public link (share=True trên Colab)
```

---

## 🔀 Kiến Trúc Agentic Pipeline

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐    ┌─────────────┐    ┌───────────────┐
│  Step 1     │    │  Step 2      │    │  Step 3      │    │  Step 4  │    │  Step 5     │    │  Output       │
│  User Input │───▶│  KB Retrieval│───▶│  ML Predict  │───▶│  Memory  │───▶│ LLM Explainer│───▶│ Dashboard     │
│             │    │  TF-IDF      │    │ RandomForest  │    │  Log     │    │  FLAN-T5    │    │  Charts+Report│
└─────────────┘    └──────────────┘    └──────────────┘    └──────────┘    └─────────────┘    └───────────────┘
                                                                                                        │
                                                                                                        ▼
                                                                                              ┌─────────────────┐
                                                                                              │  🏆 Capstone    │
                                                                                              │  Mini-Project   │
                                                                                              │  Module 8       │
                                                                                              └─────────────────┘
```

### Chi Tiết Từng Layer

| Layer | File | Thuật Toán | Output |
|-------|------|------------|--------|
| 1 — Semantic Search | `core/database.py` | TF-IDF + Cosine Similarity | Agent, Urgency, Solution, Action |
| 2–3 — ML Prediction | `core/predictor.py` | RandomForest (200 trees) | Cost, 95% CI, R², Sensitivity |
| 4 — Memory | `app_backend.py` | In-memory session log | Query history, Audit trail |
| 5 — LLM Explainer | `core/explainer.py` | FLAN-T5-Large (lazy load) | Executive Brief (human-readable) |
| UI — Dashboard | `app_frontend.py` | Gradio 4.44 + Plotly | 6 loại biểu đồ, báo cáo, API log |

---

## 🖥️ Hướng Dẫn Sử Dụng Giao Diện (5 Bước)

### Bước 01 — Nhập Thông Tin Doanh Nghiệp

| Trường | Mô tả | Ví dụ |
|--------|-------|-------|
| Business Name | Chọn từ 12 công ty Fintech Việt Nam hoặc nhập tên mới | `Techcombank` |
| Admin Email | Email người phụ trách phân tích | `admin@techcombank.vn` |
| Issue Description | Mô tả vấn đề nghiệp vụ bằng tiếng Anh | `delays in calculating KPIs` |

### Bước 02 — Cấu Hình Tham Số Dự Án

| Tham số | Phạm vi | Ý nghĩa & Công thức |
|---------|---------|---------------------|
| Team Size | 2–50 người | `Labor = Team × Duration × $800/tuần` |
| Duration | 1–52 tuần | Short ≤8w → Mid 9–20w → Long >20w |
| Risk Level | Low / Medium / High | Buffer: Low=5%, Medium=15%, High=30% |
| Region | SW / NW / SE / NE | Multiplier: SW=×1.0 → NE=×1.15 |

### Bước 03 — Chạy Phân Tích

Nhấn **"🚀 Run Analysis"** để kích hoạt toàn bộ pipeline.  
Kết quả KPI xuất hiện ngay lập tức:

- 💰 **Estimated Cost** — Chi phí dự án (USD)
- 📊 **Confidence** — Độ tin cậy KB match (%)
- 🎯 **Model R²** — Độ chính xác mô hình ML (%)
- ⚡ **Agent Type** — Department AI agent được kích hoạt

### Bước 04 — Xem Kết Quả Chi Tiết (4 Tab)

| Tab | Nội dung |
|-----|----------|
| 📋 Executive Brief | Báo cáo phân tích định dạng executive, tùy chọn FLAN-T5 rewrite |
| 🤖 ML Engine | Input features, Budget breakdown, 95% Confidence Interval |
| 🔌 API Log | Raw JSON output từ Agent pipeline (format tích hợp hệ thống) |
| 📚 Knowledge Base | Thống kê KB, pattern matched, solution recommendation |

### Bước 05 — Trực Quan Hóa Dashboard (6 Loại Biểu Đồ)

| Biểu Đồ | Mô tả | Kỹ Thuật |
|---------|-------|----------|
| Cost Breakdown Pie | Phân bổ chi phí: Labor / Infra / Risk / Overhead | Plotly Pie |
| Sensitivity Bar | Ảnh hưởng Team Size / Duration / Risk đến Budget | Plotly Bar |
| 95% CI Range | Khoảng tin cậy RandomForest (lower – mean – upper) | Plotly Scatter |
| Feature Importance | Trọng số feature trong ML model | Plotly Bar |
| Risk Comparison | So sánh chi phí 3 mức rủi ro | Plotly Bar |
| Region Heatmap | Phân bố chi phí theo vùng địa lý | Plotly Bar |

---

## 🔬 Lab A — ML Budget Prediction

**Mục tiêu:** Hiểu cơ chế RandomForest và 95% Confidence Interval (Slide 11, 13)

```bash
python core/predictor.py
```

**Thực nghiệm được thiết kế sẵn:**

```python
# Base profile (Team=12, Duration=8w, Risk=Medium, Region=Southwest)
base = pred.predict(12, 8, "medium", "southwest")

# Sensitivity: tăng Team +4 người → Budget thay đổi bao nhiêu?
more_team = pred.predict(16, 8, "medium", "southwest")
delta = more_team["estimated_cost"] - base["estimated_cost"]

# Sensitivity: tăng Risk từ Medium → High
high_risk = pred.predict(12, 8, "high", "southwest")
```

**Câu hỏi thảo luận Lab A:**
1. Tại sao 95% CI rộng khi risk=high và team_size nhỏ?
2. Feature nào quan trọng nhất với mô hình? Tại sao?
3. R² = 0.998 có phải là overfitting không?

---

## 💬 Lab B — Prompt Engineering

**Mục tiêu:** So sánh 3 kỹ thuật prompting (Slide 7, 9, 12 — bunq Finn Pattern)

```bash
python lab_b_prompt_experiment.py
```

**3 bước thực nghiệm:**

| Bước | Kỹ Thuật | Pattern | Output |
|------|----------|---------|--------|
| Step 1 | Zero-Shot | `"Summarize this: {data}"` | Generic, kỹ thuật |
| Step 2 | Role + Constrained | `"You are a senior compliance officer..."` | Human-friendly, 3 câu |
| Step 3 | Structured JSON | `"Respond ONLY in valid JSON: {schema}"` | API-ready, machine-parseable |

**Câu hỏi thảo luận Lab B:**
1. Tại sao Step 2 tốt hơn Step 1 cho retail banking communication?
2. Step 3 có thể auto-feed vào JIRA/ServiceNow không?
3. GDPR Article 22 — right to explanation — ảnh hưởng thế nào đến AI design?

---

## 🌐 REST API Endpoints

Sau khi khởi động `app_api.py`, truy cập Swagger UI tại `http://127.0.0.1:8000/docs`

### `GET /api/v1/health`
```json
{
  "status": "online",
  "agents": ["SemanticSearch", "ML_RandomForest", "FLAN_T5_Explainer"]
}
```

### `POST /api/v1/analyze`
```bash
curl -X POST http://127.0.0.1:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Techcombank",
    "admin_email": "admin@techcombank.vn",
    "team_size": 12,
    "duration_weeks": 8,
    "risk_level": "medium",
    "region": "southwest",
    "issue_description": "delays in calculating employees KPIs and bonuses",
    "use_llm": false
  }'
```

### `GET /api/v1/kb-stats`
```json
{
  "total_patterns": 4,
  "departments": 4,
  "urgency_distribution": {"high": 2, "medium": 2}
}
```

---

## 📊 Dữ Liệu Thực Nghiệm

### enterprise_knowledge.csv — Knowledge Base

| Department | Urgency | Issue Pattern |
|------------|---------|---------------|
| Finance Advisor | 🔴 High | Unauthorized financial variance in general ledger |
| IT Copilot | 🔴 High | Latency spike & data desync on cloud ERP |
| HR Bot | 🟡 Medium | Delays in calculating KPIs and bonuses |
| Product Management | 🟡 Medium | Shortage of senior QA software engineers |

### project_cost_data.csv — Training Data ML

```
team_size | duration_weeks | risk_level | region    | estimated_cost
    5     |       4        |     1      | northwest |    $12,500
   12     |       8        |     3      | southeast |    $45,800
  ...     |      ...       |    ...     |    ...    |      ...
```

> **Mở rộng dữ liệu:** Thêm hàng mới vào `project_cost_data.csv` và khởi động lại app để retrain RandomForest tự động.

---

## 🏆 Capstone Mini-Project — Module 8

Xem đề cương đầy đủ tại: `docs/Capstone_Module8.html` (hoặc click box **Capstone** trên pipeline UI)

### Phạm Vi Công Việc (3 Module)

**Module 1 — Data & ML Enhancement**
- Mở rộng KB từ 4 → 20+ patterns với FAISS vector search
- Tích hợp GPT-4o API thay thế FLAN-T5
- SHAP explainability: giải thích từng dự đoán ML

**Module 2 — Advanced AI Agent**
- LangChain multi-step agent với memory persistence
- SQLite audit trail thay thế in-memory log
- Streaming output real-time

**Module 3 — Production UI**
- Dark/light theme toggle
- Export PDF báo cáo
- Multi-session comparison dashboard

### Rubric Chấm Điểm (100 điểm)

| Hạng mục | Điểm |
|----------|------|
| Technical Implementation | 40 |
| Business Analysis & Insights | 25 |
| UI/UX Design | 20 |
| Documentation & Presentation | 15 |
| Bonus: Innovation | +15 |

---

## 📦 Dependencies

```
scikit-learn==1.4.2     # RandomForest, TF-IDF, Cosine Similarity
pandas==2.2.2           # Data manipulation
numpy==1.26.4           # Numerical computation
gradio==4.44.0          # Web UI framework
plotly==5.22.0          # Interactive charts
fastapi==0.111.0        # REST API backend
uvicorn==0.30.1         # ASGI server
transformers==4.42.4    # FLAN-T5-Large LLM
sentencepiece==0.2.0    # Tokenizer
faiss-cpu==1.8.0        # Vector similarity (Capstone)
httpx==0.27.0           # Async HTTP client
```

---

## 🛠️ Khắc Phục Sự Cố Thường Gặp

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `Port 7860 already in use` | Tiến trình cũ chưa tắt | `kill -9 $(lsof -t -i:7860)` |
| `ModuleNotFoundError: sklearn` | Chưa cài requirements | `pip install -r requirements.txt` |
| `FLAN-T5 load failed` | Thiếu RAM / transformers | Tắt LLM: bỏ check "Use FLAN-T5" trên UI |
| `KB returns 0.0% confidence` | Issue text quá ngắn hoặc không liên quan | Mô tả chi tiết hơn bằng tiếng Anh |
| `Gradio không load được chart` | Plotly version mismatch | `pip install plotly==5.22.0 --upgrade` |
| `Capstone link không mở` | Path tương đối trong Gradio | Đảm bảo `docs/` folder tồn tại, restart app |

---

## 📁 Môi Trường Thực Nghiệm

Dự án hỗ trợ **2 môi trường**:

### VS Code + Local Python
```bash
# Cài đặt theo hướng dẫn trên và chạy:
python app_frontend.py
```

### Google Colab
```
Mở file: Google_Colab/Fintech_Lab.ipynb
→ Runtime → Run All
→ Gradio public link sẽ xuất hiện tự động
```

Notebook Colab có:
- ✅ Tất cả dữ liệu embedded (không cần upload file)
- ✅ Auto-detect Colab vs local environment
- ✅ `share=True` tự động trên Colab
- ✅ 39 cells: Setup → Labs → Discussion → UI

---

## 📚 Tài Liệu Tham Khảo

| Tài liệu | Mô tả |
|----------|-------|
| `docs/AI_Finance_Lab_Guide.html` | Hướng dẫn Lab hoàn chỉnh — mở bằng trình duyệt |
| `docs/Capstone_Module8.html` | Đề cương và rubric Capstone |
| `http://127.0.0.1:8000/docs` | Swagger API documentation (khi app đang chạy) |

### Slide Reference

| Slide | Chủ đề |
|-------|--------|
| 5 | Chatbot vs AI Agent — Agentic Pipeline Architecture |
| 7 | Prompt Engineering: Zero-Shot / Role / Structured |
| 9 | bunq Finn Pattern — Role Prompting trong Banking |
| 11 | Lab A — RandomForest Budget Prediction |
| 12 | DBS ADA — Structured Output cho Workflow Automation |
| 13 | DBS ALAN — ML-powered Financial Decision Support |
| 14 | API Integration — FastAPI ↔ Gradio |
| 15–16 | Capstone Mini-Project Specification |

---

## 👨‍💻 Thông Tin Khoá Học

**MIT Professional Education × Quanskill Bootcamp**  
*AI in Digital Finance & Fintech*

- **Đối tượng:** Sinh viên, học viên, chuyên gia tài chính muốn ứng dụng AI
- **Môi trường:** VS Code / Google Colab / Jupyter Notebook
- **Ngôn ngữ:** Python 3.10+, tiếng Anh (technical), tiếng Việt (hướng dẫn)

---

*Cập nhật lần cuối: Tháng 6, 2026 · FINTECH_LAB v2.0*
