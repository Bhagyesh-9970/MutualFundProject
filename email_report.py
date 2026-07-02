import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent


def build_weekly_report_html() -> str:
    summary_path = ROOT / 'reports' / 'summary.txt'
    summary_text = summary_path.read_text(encoding='utf-8') if summary_path.exists() else 'No weekly summary available yet.'

    scheme_path = ROOT / 'data' / 'processed' / '07_scheme_performance_cleaned.csv'
    top_performers = ''
    if scheme_path.exists():
        schemes = pd.read_csv(scheme_path)
        top_rows = schemes.nlargest(3, 'return_3yr_pct')[['scheme_name', 'return_3yr_pct', 'risk_grade']]
        top_performers = ''.join(
            f"<tr><td>{row.scheme_name}</td><td>{row.return_3yr_pct:.2f}%</td><td>{row.risk_grade}</td></tr>"
            for _, row in top_rows.iterrows()
        )

    return f"""<!DOCTYPE html>
<html>
  <head><meta charset='utf-8'><title>Weekly Mutual Fund Summary</title></head>
  <body>
    <h2>Weekly Mutual Fund Performance Summary</h2>
    <p>{summary_text}</p>
    <h3>Top 3 performers</h3>
    <table border='1' cellpadding='6' cellspacing='0'>
      <tr><th>Scheme</th><th>3Y Return</th><th>Risk</th></tr>
      {top_performers}
    </table>
  </body>
</html>"""


def send_weekly_report(recipient: str, subject: str = 'Weekly Mutual Fund Performance Summary', smtp_server: str | None = None) -> Path:
    output_path = ROOT / 'reports' / 'weekly_report.html'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    html_content = build_weekly_report_html()
    output_path.write_text(html_content, encoding='utf-8')

    smtp_server = smtp_server or os.getenv('SMTP_SERVER')
    if not recipient or not smtp_server:
        return output_path

    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = os.getenv('SMTP_FROM', 'mutualfund@example.com')
    message['To'] = recipient
    message.set_content('Weekly mutual fund performance summary attached.')
    message.add_alternative(html_content, subtype='html')
    message.add_attachment(output_path.read_bytes(), maintype='text', subtype='html', filename='weekly_report.html')

    with smtplib.SMTP(smtp_server) as smtp:
        smtp.send_message(message)

    return output_path


if __name__ == '__main__':
    send_weekly_report('recipient@example.com')
