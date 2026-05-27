from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://zafran-frontend.netlify.app"])

GMAIL_USER     = os.getenv("GMAIL_USER")    
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")  
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL") 


def send_email(name, email, phone, message):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"New Client Inquiry from {name} — Zafran Site"
    msg["From"]    = GMAIL_USER
    msg["To"]      = RECEIVER_EMAIL

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f9f9f9; padding:30px;">
      <div style="max-width:560px; margin:auto; background:#fff; border-radius:8px;
                  padding:32px; border:1px solid #e0e0e0;">
        <h2 style="color:#c9963a; margin-top:0;">New Message from Your Portfolio Site</h2>
        <table style="width:100%; border-collapse:collapse; font-size:15px;">
          <tr><td style="padding:8px 0; color:#888; width:100px;">Name</td>
              <td style="padding:8px 0; font-weight:bold;">{name}</td></tr>
          <tr><td style="padding:8px 0; color:#888;">Email</td>
              <td style="padding:8px 0;"><a href="mailto:{email}">{email}</a></td></tr>
          <tr><td style="padding:8px 0; color:#888;">Phone</td>
              <td style="padding:8px 0;">{phone}</td></tr>
          <tr><td style="padding:8px 0; color:#888; vertical-align:top;">Message</td>
              <td style="padding:8px 0;">{message}</td></tr>
        </table>
        <hr style="border:none; border-top:1px solid #eee; margin:24px 0;">
        <p style="font-size:12px; color:#aaa;">Sent via Zafran Restaurant website — Bulbul Portfolio</p>
      </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, RECEIVER_EMAIL, msg.as_string())


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()

    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    phone   = data.get("phone", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "Name, email aur message required hai"}), 400

    try:
        send_email(name, email, phone, message)
        return jsonify({"success": True, "message": "Message bhej diya gaya!"})
    except Exception as e:
        print("Email error:", e)
        return jsonify({"success": False, "error": "Email send nahi hui. Config check karo."}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Bulbul Portfolio Backend — Running ✓"})


if __name__ == "__main__":
    app.run(debug=False)
