import os
import matplotlib
matplotlib.use("Agg")  # required for headless environments
import matplotlib.pyplot as plt

def generate_charts(df, output_dir="reports/assets"):
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------
    # Chart 1: Risk Score Histogram
    # -------------------------
    risk_hist_path = os.path.join(output_dir, "risk_score_distribution.png")

    plt.figure()
    plt.hist(df["risk_score"], bins=20)
    plt.title("Churn Risk Score Distribution")
    plt.xlabel("Risk Score (0–100)")
    plt.ylabel("Number of Users")
    plt.tight_layout()
    plt.savefig(risk_hist_path, dpi=150)
    plt.close()

    # -------------------------
    # Chart 2: MRR at Risk by Band
    # -------------------------
    mrr_band_path = os.path.join(output_dir, "mrr_at_risk_by_band.png")

    grouped = (
        df.groupby("risk_band")["estimated_mrr_at_risk"]
        .sum()
        .reindex(["Low", "Medium", "High"])
    )

    plt.figure()
    plt.bar(grouped.index, grouped.values)
    plt.title("Estimated MRR at Risk by Risk Band")
    plt.xlabel("Risk Band")
    plt.ylabel("Estimated MRR at Risk ($)")
    plt.tight_layout()
    plt.savefig(mrr_band_path, dpi=150)
    plt.close()

    return {
        "risk_histogram": risk_hist_path,
        "mrr_by_band": mrr_band_path
    }