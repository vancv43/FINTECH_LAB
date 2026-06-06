"""
Predictive Budget Engine — Layer 2-3 of AI Agent Pipeline
RandomForestRegressor: 200 trees, 95% CI via tree variance
Slide 11 (Lab A), 13 — DBS ALAN pattern
"""
import os, numpy as np, pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "project_cost_data.csv")
RISK_MAP  = {"low": 1, "medium": 2, "high": 3}
REGIONS   = ["northeast", "northwest", "southeast", "southwest"]

class BudgetPredictor:
    def __init__(self):
        df = pd.read_csv(DATA_PATH)
        self.le = LabelEncoder()
        self.le.fit(REGIONS)
        X = np.column_stack([df["team_size"].values, df["duration_weeks"].values,
                             df["risk_level"].values, self.le.transform(df["region"])])
        y = df["estimated_cost"].values
        self.rf = RandomForestRegressor(n_estimators=200, max_depth=8, random_state=42)
        self.rf.fit(X, y)
        names = ["team_size", "duration_weeks", "risk_level", "region"]
        self.feature_importances = dict(zip(names, self.rf.feature_importances_.tolist()))
        self.train_r2 = r2_score(y, self.rf.predict(X))
        print(f"[ML] RandomForest ready — R²={self.train_r2:.3f}")

    def _encode(self, team_size, duration_weeks, risk_level, region):
        r = RISK_MAP.get(risk_level.lower(), 2)
        reg = region.lower() if region.lower() in REGIONS else "southeast"
        return np.array([[team_size, duration_weeks, r, self.le.transform([reg])[0]]])

    def predict(self, team_size, duration_weeks, risk_level, region) -> dict:
        X = self._encode(team_size, duration_weeks, risk_level, region)
        tree_preds = np.array([t.predict(X)[0] for t in self.rf.estimators_])
        mean, std = float(np.mean(tree_preds)), float(np.std(tree_preds))
        return {
            "estimated_cost":  round(mean, 2),
            "confidence_low":  round(max(0, mean - 1.96*std), 2),
            "confidence_high": round(mean + 1.96*std, 2),
            "std_dev":         round(std, 2),
            "model_accuracy":  round(self.train_r2 * 100, 2),
        }

    def get_cost_breakdown(self, team_size, duration_weeks, risk_level, region) -> dict:
        total = self.predict(team_size, duration_weeks, risk_level, region)["estimated_cost"]
        rn = RISK_MAP.get(risk_level.lower(), 2)
        rp = 0.08 * rn / 3
        return {"total": total, "labor": round(total*0.55, 2),
                "infrastructure": round(total*0.20, 2), "risk_buffer": round(total*rp, 2),
                "overhead": round(total*(1-0.55-0.20-rp), 2)}

    def sensitivity_analysis(self, base_team, base_weeks, base_risk, base_region) -> list[dict]:
        results = []
        for ts in [max(1,base_team-4), base_team, base_team+4, base_team+8]:
            results.append({"variable": f"Team {ts}", "cost": self.predict(ts, base_weeks, base_risk, base_region)["estimated_cost"], "category": "team_size"})
        for wk in [max(1,base_weeks-2), base_weeks, base_weeks+2, base_weeks+4]:
            results.append({"variable": f"{wk}w", "cost": self.predict(base_team, wk, base_risk, base_region)["estimated_cost"], "category": "duration"})
        for rl in ["low", "medium", "high"]:
            results.append({"variable": rl.capitalize(), "cost": self.predict(base_team, base_weeks, rl, base_region)["estimated_cost"], "category": "risk"})
        return results

if __name__ == "__main__":
    pred = BudgetPredictor()
    base = pred.predict(12, 8, "medium", "southwest")
    print(f"\n--- Base Profile (team=12, weeks=8, risk=medium) ---")
    print(f"Cost: ${base['estimated_cost']:,.2f}  |  R²: {base['model_accuracy']}%")
    print(f"95% CI: ${base['confidence_low']:,.0f} – ${base['confidence_high']:,.0f}")
    more_team = pred.predict(16, 8, "medium", "southwest")["estimated_cost"]
    high_risk  = pred.predict(12, 8, "high",   "southwest")["estimated_cost"]
    print(f"\n--- Lab A Sensitivity ---")
    print(f"Team +4:   ${more_team:,.0f}  (Δ ${more_team-base['estimated_cost']:+,.0f})")
    print(f"Risk high: ${high_risk:,.0f}  (Δ ${high_risk-base['estimated_cost']:+,.0f})")
    print(f"\nFeature importances: {pred.feature_importances}")
