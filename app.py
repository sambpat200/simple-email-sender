import re
import smtplib
import time
from email.message import EmailMessage

import streamlit as st

st.set_page_config(page_title="Simple Email Sender", page_icon="✉️", layout="centered")

st.title("✉️ Simple Email Sender")
st.caption("Send a separate email to each recipient from your Gmail account.")

with st.form("email_form"):
    sender = st.text_input("Source Gmail address", placeholder="yourname@gmail.com")
    app_password = st.text_input(
        "Gmail App Password",
        type="password",
        help="Use a Google App Password, not your normal Gmail password. It is used only for this run.",
    )
    st.link_button(
        "Create or manage your Google App Password",
        "https://myaccount.google.com/apppasswords",
        help="Opens Google Account's App Passwords page in a new tab.",
    )
    with st.expander("How to generate a Gmail App Password"):
        st.markdown(
            "1. Open **Manage your Google Account** and sign in.\n"
            "2. Select **Security** and make sure **2-Step Verification** is enabled.\n"
            "3. Open **App passwords**, create a new password for this app, and copy the 16-character code.\n"
            "4. Paste the code above. Spaces are removed automatically when connecting to Gmail."
        )
    destinations_text = st.text_area(
        "Destination email addresses",
        placeholder="person1@example.com\nperson2@example.com",
        help="Enter one address per line, or separate addresses with commas or semicolons.",
        height=120,
    )
    subject = st.text_input("Subject", placeholder="Did you get feedback?")
    body = st.text_area(
        "Email content",
        placeholder="Write your email here...",
        height=220,
    )
    confirm = st.checkbox(
        "I have checked the recipients and email content, and I want to send these emails."
    )
    submitted = st.form_submit_button("Send individual emails", type="primary", use_container_width=True)

def parse_addresses(raw):
    candidates = re.split(r"[\n,;]+", raw)
    addresses = []
    invalid = []
    seen = set()
    for item in candidates:
        address = item.strip()
        if not address:
            continue
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", address):
            invalid.append(address)
            continue
        key = address.lower()
        if key not in seen:
            seen.add(key)
            addresses.append(address)
    return addresses, invalid

if submitted:
    recipients, invalid = parse_addresses(destinations_text)
    errors = []
    if not sender.strip() or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", sender.strip()):
        errors.append("Enter a valid source email address.")
    if not app_password.strip():
        errors.append("Enter your Gmail App Password.")
    if not recipients:
        errors.append("Enter at least one valid destination email address.")
    if invalid:
        errors.append("These destination entries do not look like valid email addresses: " + ", ".join(invalid))
    if not subject.strip():
        errors.append("Enter an email subject.")
    if not body.strip():
        errors.append("Enter the email content.")
    if not confirm:
        errors.append("Tick the confirmation checkbox before sending.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.info(f"Ready to send {len(recipients)} separate email(s). Connecting to Gmail…")
        sent = []
        failed = []
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(sender.strip(), app_password.strip().replace(" ", ""))

                progress = st.progress(0)
                status = st.empty()
                for index, recipient in enumerate(recipients, start=1):
                    message = EmailMessage()
                    message["From"] = sender.strip()
                    message["To"] = recipient
                    message["Subject"] = subject.strip()
                    message.set_content(body)
                    try:
                        server.send_message(message)
                        sent.append(recipient)
                        status.write(f"Processed {index} of {len(recipients)}: {recipient}")
                    except Exception as exc:
                        failed.append((recipient, str(exc)))
                        status.write(f"Processed {index} of {len(recipients)}: {recipient} (failed)")
                    progress.progress(index / len(recipients))
                    if index < len(recipients):
                        time.sleep(1)

            if sent:
                st.success(f"Submitted {len(sent)} email(s) successfully to Gmail.")
                with st.expander("View successful recipients"):
                    for address in sent:
                        st.write(f"✓ {address}")
            if failed:
                st.warning(f"{len(failed)} email(s) could not be submitted.")
                with st.expander("View failed recipients"):
                    for address, reason in failed:
                        st.write(f"✗ {address}: {reason}")
            st.caption("Successful submission to Gmail does not guarantee delivery to the recipient's inbox.")
        except smtplib.SMTPAuthenticationError:
            st.error("Gmail authentication failed. Check the source address and App Password. Do not use your normal Gmail password.")
        except Exception as exc:
            st.error(f"Could not connect to Gmail or complete the send operation: {exc}")

st.divider()
st.caption("Privacy tip: use this app on your own computer. Do not publish it with your App Password or recipient lists.")
