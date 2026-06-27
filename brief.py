import anthropic
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

PROMPT = """Produce a daily brief on AI monetization, value chain, and pricing news, covering a mix of business and technical topics. Research using your knowledge and reasoning for current trends.

Structure the brief with these sections:
1. Headline roundup (3-5 items): latest news on AI pricing models, monetization announcements, earnings/margin commentary from major AI labs and infra providers.
2. Value chain spotlight: rotate through layers (compute/infra, model providers, platform/tooling, application layer, end-user/consumer), tracking where value and margin are concentrating.
3. Pricing model watch: usage-based vs. subscription vs. outcome-based vs. hybrid pricing trends; notable pricing changes from vendors (OpenAI, Anthropic, Google, Microsoft, etc.).
4. Business deep dive: one focused topic per day (e.g. unit economics of inference, enterprise AI ROI data, agentic pricing, API cost trends).
5. Technical deep dive: one focused topic per day (e.g. inference cost optimization, GPU/compute economics, model efficiency vs. pricing tradeoffs).
6. Quick links: 2-3 additional topics worth a skim.

Each section should include a 1-2 sentence summary. Keep the tone concise and direct, minimal fluff. Format in Markdown."""

def generate_brief():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2048,
        messages=[{"role": "user", "content": PROMPT}]
    )
    return message.content[0].text

def send_email(body):
    sender = os.environ["GMAIL_USER"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["GMAIL_USER"]
    today = date.today().strftime("%B %d, %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"AI Monetization Brief — {today}"
    msg["From"] = sender
    msg["To"] = recipient

    # Plain text fallback
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
    print("Email sent successfully.")

if __name__ == "__main__":
    print("Generating brief...")
    brief = generate_brief()
    print("Sending email...")
    send_email(brief)
