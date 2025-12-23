import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def _money(x):
    return f"${x:,.0f}"

def build_pdf(output_path, summary, top_risks_df, chart_paths=None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # -------------------------
    # Page 1: Executive Summary
    # -------------------------
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, height - 1 * inch, "Revenue Leak Finder Report")

    c.setFont("Helvetica", 10)
    c.drawString(
        1 * inch,
        height - 1.25 * inch,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    y = height - 1.75 * inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1 * inch, y, "Executive Summary")
    y -= 0.30 * inch

    c.setFont("Helvetica", 11)
    lines = [
        f"Users analyzed: {summary['users_count']}",
        f"Total MRR: {_money(summary['total_mrr'])}",
        f"Estimated MRR at risk: {_money(summary['mrr_at_risk'])}",
        f"High-risk users: {summary['high_risk_users']}",
    ]
    for line in lines:
        c.drawString(1 * inch, y, line)
        y -= 0.23 * inch

    c.setFont("Helvetica-Oblique", 10)
    y -= 0.10 * inch
    c.drawString(
        1 * inch,
        y,
        "Note: Risk scores are rule-based and intended to prioritize outreach, retention, and pricing review."
    )

    # -------------------------
    # Page 2: Top Risks Table
    # -------------------------
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, height - 1 * inch, "Top Churn Risks (Top 10)")

    y = height - 1.5 * inch
    c.setFont("Helvetica-Bold", 10)
    headers = ["user_id", "plan_price", "days_inactive", "risk_score", "est_mrr_at_risk"]
    x_positions = [1.0, 2.0, 3.2, 4.6, 5.6]  # inches

    for h, x in zip(headers, x_positions):
        c.drawString(x * inch, y, h)
    y -= 0.18 * inch

    c.setFont("Helvetica", 10)
    for _, row in top_risks_df.iterrows():
        c.drawString(x_positions[0] * inch, y, str(int(row["user_id"])))
        c.drawString(x_positions[1] * inch, y, _money(row["plan_price"]))
        c.drawString(x_positions[2] * inch, y, str(int(row["days_inactive"])))
        c.drawString(x_positions[3] * inch, y, str(int(row["risk_score"])))
        c.drawString(x_positions[4] * inch, y, _money(row["estimated_mrr_at_risk"]))
        y -= 0.20 * inch

        if y < 1.0 * inch:
            c.showPage()
            y = height - 1.0 * inch

    # -------------------------
    # Page 3: Charts
    # -------------------------
    if chart_paths:
        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1 * inch, height - 1 * inch, "Charts")

        y_top = height - 1.4 * inch

        # Chart 1
        if chart_paths.get("risk_histogram"):
            c.setFont("Helvetica-Bold", 11)
            c.drawString(1 * inch, y_top, "Churn Risk Score Distribution")
            c.drawImage(
                chart_paths["risk_histogram"],
                1 * inch,
                y_top - 3.2 * inch,
                width=6.5 * inch,
                height=3.0 * inch,
                preserveAspectRatio=True
            )

        # Chart 2
        if chart_paths.get("mrr_by_band"):
            c.setFont("Helvetica-Bold", 11)
            c.drawString(1 * inch, y_top - 3.6 * inch, "Estimated MRR at Risk by Risk Band")
            c.drawImage(
                chart_paths["mrr_by_band"],
                1 * inch,
                y_top - 6.8 * inch,
                width=6.5 * inch,
                height=3.0 * inch,
                preserveAspectRatio=True
            )

    c.save()
    return output_path