"""
Daily Exchange Rate Emailer
----------------------------
Fetches major currency rates against the Nigerian Naira (NGN) and emails
a clean summary. Designed to be run once a day by GitHub Actions.

Required environment variables (set as GitHub Secrets):
    GMAIL_ADDRESS       - the Gmail address sending the email
    GMAIL_APP_PASSWORD  - a Gmail App Password (NOT your normal password)
    RECIPIENT_EMAIL     - where the daily rate should be sent
"""

import os
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests

# Currencies to report, shown as "1 UNIT = X NGN"
CURRENCIES = ["USD", "GBP", "EUR", "CNY", "CAD", "ZAR"]

API_URL = "https://open.er-api.com/v6/latest/USD"


def fetch_rates():
    """Fetch live rates (base USD) and convert everything to 'per 1 NGN' view."""
    resp = requests.get(API_URL, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if data.get("result") != "success":
        raise RuntimeError(f"API did not return success: {data}")

    rates = data["rates"]  # amount of X per 1 USD
    ngn_per_usd = rates["NGN"]

    results = {}
    for code in CURRENCIES:
        if code == "USD":
            ngn_per_unit = ngn_per_usd
        else:
            units_per_usd = rates.get(code)
            if not units_per_usd:
                continue
            # NGN per 1 unit of currency = (NGN per USD) / (units of currency per USD)
            ngn_per_unit = ngn_per_usd / units_per_usd
        results[code] = round(ngn_per_unit, 2)

    return results, data.get("time_last_update_utc", "")


def build_email_body(rates, last_update):
    today = datetime.now().strftime("%A, %d %B %Y")

    lines = [
        f"Exchange Rate Update — {today}",
        "",
        "Today's rates (to Nigerian Naira):",
        "",
    ]
    for code, value in rates.items():
        lines.append(f"  1 {code}  =  ₦{value:,.2f}")

    lines.append("")
    lines.append(f"Source: open.er-api.com (last updated: {last_update})")
    lines.append("This is an automated daily update.")

    return "\n".join(lines)


def send_email(subject, body):
    gmail_address = os.environ["GMAIL_ADDRESS"]
    gmail_app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    msg = MIMEMultipart()
    msg["From"] = gmail_address
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=context)
        server.login(gmail_address, gmail_app_password)
        server.sendmail(gmail_address, recipient, msg.as_string())


def main():
    rates, last_update = fetch_rates()
    body = build_email_body(rates, last_update)
    subject = f"💱 Exchange Rate Update — {datetime.now().strftime('%d %b %Y')}"
    send_email(subject, body)
    print("Email sent successfully.")
    print(body)


if __name__ == "__main__":
    main()
