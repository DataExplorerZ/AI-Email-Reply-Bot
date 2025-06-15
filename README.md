# AI Email Reply Bot 🤖📧

An automated email responder that reads unread emails from your Gmail inbox, analyzes the tone of each message, and generates professional, context-aware replies using OpenAI's GPT-4 API. Supports scheduled inbox checks and automatic email sending.

---

## Features

- Connects securely to Gmail via IMAP to fetch unread emails
- Auto-detects the tone of incoming emails (formal, casual, friendly)
- Generates relevant and professional replies using GPT-4
- Automatically sends replies to the original sender
- Scheduled inbox checking (every 5 minutes by default)
- Easy setup using environment variables (.env file)
- Logs activity for monitoring sent replies and errors

---

## Requirements

- Python 3.8+
- Gmail account (with App Password if 2FA enabled)
- OpenAI API key with GPT-4 access
- Internet connection

---

## Installation & Setup

1. **Clone the repository:**

Create and activate a virtual environment:

On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

On Windows:
python -m venv venv
venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt

Configure environment variables:
Create a .env file in the root directory with the following:

EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
OPENAI_API_KEY=your_openai_api_key
For Gmail accounts with two-factor authentication, create an App Password.

Get your OpenAI API key from OpenAI Dashboard.
Run the bot:
python main.py
