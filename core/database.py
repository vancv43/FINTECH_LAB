"""
Semantic Knowledge Base — Layer 1 of AI Agent Pipeline
TF-IDF + cosine similarity (FAISS-compatible architecture)
Slide 5, 12, 13 — MIT PE × Quanskill Bootcamp
"""
import os, numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "enterprise_knowledge.csv")

class EnterpriseKnowledgeBase:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="english", max_features=5000)
        self.index_matrix = self.vectorizer.fit_transform(self.df["issue_pattern"].tolist())
        print(f"[KB] Loaded {len(self.df)} patterns")

    def search(self, query: str, top_k: int = 1) -> list[dict]:
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.index_matrix)[0]
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [{
            "issue_pattern": self.df.iloc[i]["issue_pattern"],
            "solution": self.df.iloc[i]["solution"],
            "department": self.df.iloc[i]["department"],
            "urgency_level": self.df.iloc[i]["urgency_level"],
            "recommended_action": self.df.iloc[i]["recommended_action"],
            "confidence_score": float(scores[i]),
        } for i in top_indices]

    def get_stats(self) -> dict:
        return {
            "total_patterns": len(self.df),
            "departments": self.df["department"].nunique(),
            "urgency_distribution": self.df["urgency_level"].value_counts().to_dict(),
        }

if __name__ == "__main__":
    kb = EnterpriseKnowledgeBase()
    r = kb.search("KPI performance delays for employees")[0]
    print(f"Dept: {r['department']} | Confidence: {r['confidence_score']:.1%}")
    print(f"Action: {r['recommended_action']}")
