# gpt-auto-email-reply/main.py

import imaplib
import smtplib
import email
import openai
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def fetch_unread_emails():
    emails = []
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')

        result, data = mail.search(None, 'UNSEEN')
        if result != 'OK':
            return emails

        for num in data[0].split():
            result, msg_data = mail.fetch(num, "(RFC822)")
            if result != 'OK':
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors='ignore')

            emails.append({
                'from': msg['From'],
                'subject': msg['Subject'],
                'body': body
            })

        mail.logout()
    except Exception as e:
        print(f"Error fetching emails: {e}")
    return emails

def detect_style(email_body):
    prompt = (
        "Analyze the tone of this email and suggest the most suitable reply style: formal, casual, or friendly.\n"
        f"Email: {email_body}\nStyle:"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that selects the appropriate reply style."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0
        )
        style = response.choices[0].message['content'].strip().lower()
        if style in ["formal", "casual", "friendly"]:
            return style
        return "formal"
    except Exception as e:
        print(f"Error detecting style: {e}")
        return "formal"

def generate_reply(email_body, style):
    style_instructions = {
        "formal": "Write a professional and formal reply.",
        "casual": "Write a friendly and casual reply.",
        "friendly": "Write a warm and engaging reply."
    }
    instruction = style_instructions.get(style, style_instructions["formal"])
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": email_body}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating reply: {e}")
        return ""

def send_email_reply(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to_email
        msg['Subject'] = f"Re: {subject}"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✅ Sent reply to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def process_emails():
    emails = fetch_unread_emails()
    if not emails:
        print("No unread emails.")
        return
    for mail in emails:
        print(f"Processing email from {mail['from']}")
        style = detect_style(mail['body'])
        print(f"Detected style: {style}")
        reply = generate_reply(mail['body'], style)
        if reply:
            send_email_reply(mail['from'], mail['subject'], reply)

def main():
    while True:
        print("\n🔄 Checking for new emails...")
        process_emails()
        print("Waiting 5 minutes for next check...")
        time.sleep(300)

if __name__ == "__main__":
    main()
