import os
import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_email(to_emails, subject, body, attachments=[]):
    # Set up the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = ", ".join(to_emails)  # Join the list of emails for the header
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    for attachment in attachments:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.getvalue())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment.name}')
        msg.attach(part)

    # Send the email
    server.send_message(msg)
    server.quit()

# Streamlit UI
st.title("Email Automation with Gmail")

# User input
to_emails_input = st.text_input("Recipient Emails (comma-separated)")
subject = st.text_input("Email Subject")
body = st.text_area("Email Body")
attachments = st.file_uploader("Choose attachments", type=["pdf", "jpg", "png"], accept_multiple_files=True)

if st.button("Send Email"):
    if not to_emails_input:
        st.error("Please enter at least one recipient email.")
    else:
        # Split the input string into a list of emails and strip any whitespace
        to_emails = [email.strip() for email in to_emails_input.split(',')]
        
        if not attachments:
            st.error("Please upload at least one attachment.")
        else:
            attach_files = [attachment for attachment in attachments]  # Collect uploaded files
            try:
                send_email(to_emails, subject, body, attach_files)
                st.success("Email sent successfully!")
            except Exception as e:
                st.error(f"Error sending email: {e}")
