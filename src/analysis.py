import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------
# DATA GENERATION (already used)
# -----------------------------
def generate_sample_data(n_users=400, output_path="data/sample_data.csv"):
    random.seed(42)

    today = datetime.today()
    rows = []

    for i in range(n_users):
        user_id = i + 1

        signup_days_ago = random.randint(30, 900)
        signup_date = today - timedelta(days=signup_days_ago)

        last_active_days_ago = random.randint(0, signup_days_ago)
        last_active_date = today - timedelta(days=last_active_days_ago)

        plan_price = random.choice([9, 19, 29, 49, 99])
        monthly_usage = max(0, int(random.gauss(30, 15)))

        discount_applied = 1 if random.random() < 0.25 else 0

        rows.append({
            "user_id": user_id,
            "plan_price": plan_price,
            "signup_date": signup_date.date(),
            "last_active_date": last_active_date.date(),
            "monthly_usage": monthly_usage,
            "discount_applied": discount_applied
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} users → {output_path}")

# -----------------------------
# ANALYSIS
# -----------------------------
def analyze_churn(input_path="data/sample_data.csv"):
    df = pd.read_csv(input_path, parse_dates=["signup_date", "last_active_date"])
    today = pd.Timestamp.today()

    # days inactive
    df["days_inactive"] = (today - df["last_active_date"]).dt.days

    # churn risk score (simple, explainable)
    def risk_score(row):
        score = 0
        if row["days_inactive"] > 60:
            score += 50
        elif row["days_inactive"] > 30:
            score += 30

        if row["discount_applied"] == 1:
            score += 10

        if row["monthly_usage"] < 10:
            score += 10

        return min(score, 100)

    df["risk_score"] = df.apply(risk_score, axis=1)

    # estimated monthly revenue at risk
    df["estimated_mrr_at_risk"] = df["plan_price"] * (df["risk_score"] / 100)

    # risk bands (used later for charts)
    def band(score):
        if score <= 33:
            return "Low"
        elif score <= 66:
            return "Medium"
        return "High"

    df["risk_band"] = df["risk_score"].apply(band)

    summary = {
        "users_count": len(df),
        "total_mrr": df["plan_price"].sum(),
        "mrr_at_risk": round(df["estimated_mrr_at_risk"].sum(), 2),
        "high_risk_users": int((df["risk_band"] == "High").sum())
    }

    return df, summary