import argparse
from .analysis import analyze_churn
from .charts import generate_charts
from .pdf_report import build_pdf

def main():
    parser = argparse.ArgumentParser(
        description="Revenue Leak Finder – identify churn risk and MRR at risk"
    )
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--out", default="reports", help="Output directory")

    args = parser.parse_args()

    df, summary = analyze_churn(args.input)

    print("\n--- Revenue Leak Finder Summary ---")
    print(f"Users analyzed: {summary['users_count']}")
    print(f"Total MRR: ${summary['total_mrr']:,.0f}")
    print(f"Estimated MRR at risk: ${summary['mrr_at_risk']:,.0f}")
    print(f"High-risk users: {summary['high_risk_users']}")

    charts = generate_charts(df, output_dir=f"{args.out}/assets")

    top10 = (
        df.sort_values("risk_score", ascending=False)
          .head(10)[
              ["user_id", "plan_price", "days_inactive", "risk_score", "estimated_mrr_at_risk"]
          ]
    )

    pdf_path = f"{args.out}/revenue_report.pdf"
    build_pdf(pdf_path, summary, top10, chart_paths=charts)

    print(f"\nPDF generated: {pdf_path}")

if __name__ == "__main__":
    main()