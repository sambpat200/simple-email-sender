# Simple Email Sender

A small local Streamlit application that sends one separate email per recipient through Gmail SMTP.

## Setup

1. Install Python 3.10 or newer.
2. Extract this folder.
3. Open a terminal in this folder and run:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   python -m streamlit run app.py
   ```

5. Your browser should open the app. If not, open the local URL shown in the terminal (usually http://localhost:8501).

## Gmail requirements

- Use a Gmail account with 2-Step Verification enabled.
- Generate a Google App Password at https://myaccount.google.com/apppasswords, if available for your account.
- Enter the App Password into the password field in the app.
- Never use your normal Google password.
- Do not commit passwords, recipient lists, or other private data to GitHub.

## Features

- Source email and password fields
- Multiple destination addresses (one per line, comma-separated, or semicolon-separated)
- Subject and message body fields
- Basic recipient validation and duplicate removal
- Confirmation checkbox before sending
- Sends separate messages, not one shared To/BCC email
- Progress and per-recipient status

## Important

Run this locally on a trusted computer. Sending limits and account security rules are controlled by Google. Successful SMTP submission does not guarantee inbox delivery. Review all recipients and content before sending.
