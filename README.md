# Daily Exchange Rate Emailer

Sends you an email every morning at 8:00 AM Nigeria time with the current
NGN exchange rates for USD, GBP, EUR, CNY, CAD, and ZAR. Runs automatically
via GitHub Actions — no server or laptop needs to be on.

## Setup (takes about 5 minutes)

### 1. Create a Gmail App Password
Regular Gmail passwords won't work for sending automated mail. You need an
"App Password":
1. Go to https://myaccount.google.com/security
2. Turn on **2-Step Verification** if it isn't already on.
3. Go to https://myaccount.google.com/apppasswords
4. Create a new app password (name it e.g. "exchange-rate-bot").
5. Copy the 16-character password shown — you'll need it in step 3.

### 2. Create a GitHub repository
1. Go to https://github.com/new
2. Create a new **private** repository (e.g. `exchange-rate-bot`).
3. Upload these three files, keeping the folder structure:
   - `send_exchange_rate.py`
   - `.github/workflows/daily-exchange-rate.yml`
   - `README.md`
   (Easiest way: on the repo page, click "Add file" → "Upload files" and
   drag all three in — GitHub will preserve the `.github/workflows/` path
   if you drag the whole folder, or you can create the file manually and
   paste the content.)

### 3. Add your secrets
In your new repo: **Settings → Secrets and variables → Actions → New repository secret**.
Add three secrets:
| Name | Value |
|---|---|
| `GMAIL_ADDRESS` | your Gmail address |
| `GMAIL_APP_PASSWORD` | the 16-character app password from step 1 |
| `RECIPIENT_EMAIL` | the email address you want the update sent to |

### 4. Test it
Go to the **Actions** tab in your repo → select "Daily Exchange Rate Email"
→ click **Run workflow** to send a test email immediately, without waiting
for 8 AM.

### 5. Done
From now on, GitHub will automatically run the script every day at
7:00 AM UTC (8:00 AM Nigeria/WAT time) and email you the rates. No further
action needed.

## Customizing
- To change which currencies are tracked, edit the `CURRENCIES` list near
  the top of `send_exchange_rate.py`.
- To change the delivery time, edit the cron line in
  `.github/workflows/daily-exchange-rate.yml` (format: minute hour * * *,
  all in UTC).
