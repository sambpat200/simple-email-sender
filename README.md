
# Simple Email Sender

A Python application that sends individual emails to multiple recipients using Gmail SMTP and Streamlit.

## Requirements

- Python 3.10 or newer
- Gmail account with 2-Step Verification enabled
- Gmail App Password, if available for your account

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## Features

- Source Gmail address and App Password fields
- Multiple destination email addresses
- Custom email subject and body
- Individual emails for each recipient
- Input validation and sending status

## Security

Never commit your Gmail App Password or other secrets to GitHub. Run the app on a trusted computer, and add authentication and access controls before making it available to others.

Successful submission to Gmail does not guarantee inbox delivery.
