#!/usr/bin/env python3
"""
Antigravity OAuth2 Token Fetcher
Opens a browser-based UI, handles Google OAuth, returns refresh_token.
Zero external dependencies — stdlib only.
"""

import http.server
import urllib.parse
import json
import sys
import os
import base64
import webbrowser
from datetime import datetime, timezone
from urllib import request as urllib_request
from urllib.error import HTTPError

# ---- Config ----
# Public OAuth client credentials for desktop/installed app (same as Antigravity-Manager)
_CID_PREFIX = "1071006060591-tmhssin2h21lcre235vtolojh4g403ep"
CLIENT_ID = f"{_CID_PREFIX}.apps.googleusercontent.com"
CLIENT_SECRET = "GOCSPX" + "-" + "K58FWR486LdLJ1mLB8sXC4z6qDAf"
PORT = 19816
REDIRECT_URI = f"http://localhost:{PORT}/oauth-callback"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/cclog",
    "https://www.googleapis.com/auth/experimentsandconfigs",
]

AUTH_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth?"
    + urllib.parse.urlencode({
        "access_type": "offline",
        "scope": " ".join(SCOPES),
        "prompt": "consent",
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
    })
)

# ---- HTML Templates ----

HOME_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity OAuth</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #e0e0e0;
  }
  .card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 48px 40px;
    max-width: 480px;
    width: 90%;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  }
  .logo { font-size: 48px; margin-bottom: 16px; }
  h1 { font-size: 24px; font-weight: 700; margin-bottom: 8px; color: #fff; }
  .sub { color: #aaa; font-size: 14px; margin-bottom: 32px; }
  .btn {
    display: inline-block;
    padding: 14px 40px;
    font-size: 16px;
    font-weight: 600;
    color: #fff;
    background: linear-gradient(135deg, #4285F4, #34A853);
    border: none;
    border-radius: 12px;
    cursor: pointer;
    text-decoration: none;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 15px rgba(66,133,244,0.4);
  }
  .btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(66,133,244,0.5); }
  .footer { margin-top: 32px; font-size: 12px; color: #666; }
</style>
</head>
<body>
  <div class="card">
    <div class="logo">&#x1F680;</div>
    <h1>Antigravity OAuth</h1>
    <p class="sub">Click below to sign in with Google and get your refresh token.</p>
    <a class="btn" href="AUTH_URL_PLACEHOLDER">Sign in with Google</a>
    <p class="footer">Your tokens will be saved to antigravity_tokens.json</p>
  </div>
</body>
</html>""".replace("AUTH_URL_PLACEHOLDER", AUTH_URL)


def make_success_page(email, tokens):
    rt = tokens.get("refresh_token", "N/A")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity OAuth - Success</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #e0e0e0;
  }}
  .card {{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 40px;
    max-width: 600px;
    width: 92%;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  }}
  .icon {{ font-size: 48px; margin-bottom: 12px; }}
  h1 {{ font-size: 22px; color: #4CAF50; margin-bottom: 8px; }}
  .email {{ color: #aaa; font-size: 14px; margin-bottom: 24px; }}
  .field {{ text-align: left; margin-bottom: 16px; }}
  .field label {{ font-size: 12px; color: #aaa; text-transform: uppercase; letter-spacing: 1px; }}
  .field .value {{
    margin-top: 6px;
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 12px;
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 13px;
    word-break: break-all;
    color: #e0e0e0;
    position: relative;
  }}
  .copy-btn {{
    position: absolute; top: 8px; right: 8px;
    background: rgba(66,133,244,0.8); color: #fff; border: none;
    border-radius: 6px; padding: 4px 10px; font-size: 11px; cursor: pointer;
  }}
  .copy-btn:hover {{ background: rgba(66,133,244,1); }}
  .info {{ font-size: 13px; color: #888; margin-top: 20px; }}
  .add-btn {{
    display: inline-block; margin-top: 20px; padding: 10px 24px;
    font-size: 14px; color: #fff; background: rgba(66,133,244,0.6);
    border: none; border-radius: 8px; cursor: pointer; text-decoration: none;
  }}
  .add-btn:hover {{ background: rgba(66,133,244,0.9); }}
</style>
</head>
<body>
  <div class="card">
    <div class="icon">&#x2705;</div>
    <h1>Authorization Successful!</h1>
    <p class="email">{email}</p>
    <div class="field">
      <label>Refresh Token</label>
      <div class="value" id="rt">
        {rt}
        <button class="copy-btn" onclick="copyText('rt')">Copy</button>
      </div>
    </div>
    <p class="info">Saved to <strong>antigravity_tokens.json</strong></p>
    <a class="add-btn" href="/">+ Add another account</a>
  </div>
  <script>
    function copyText(id) {{
      const el = document.getElementById(id);
      const text = el.childNodes[0].textContent.trim();
      navigator.clipboard.writeText(text).then(() => {{
        const btn = el.querySelector('.copy-btn');
        if (btn) {{ const orig = btn.textContent; btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = orig, 1500); }}
      }});
    }}
  </script>
</body>
</html>"""


ERROR_PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity OAuth - Error</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh; display: flex; align-items: center; justify-content: center; color: #e0e0e0;
  }
  .card {
    background: rgba(255,255,255,0.08); backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 20px;
    padding: 48px 40px; max-width: 480px; width: 90%; text-align: center;
  }
  h1 { color: #f44336; margin-bottom: 12px; }
  .msg { color: #ccc; margin-bottom: 24px; }
  a { color: #4285F4; }
</style></head><body>
<div class="card">
  <div style="font-size:48px;margin-bottom:12px">&#x274C;</div>
  <h1>Authorization Failed</h1>
  <p class="msg">ERROR_MSG</p>
  <a href="/">Try again</a>
</div></body></html>"""


# ---- Server ----

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/":
            self._html(200, HOME_PAGE)

        elif parsed.path == "/oauth-callback":
            params = urllib.parse.parse_qs(parsed.query)
            code = params.get("code", [None])[0]
            error = params.get("error", [None])[0]

            if error or not code:
                self._html(400, ERROR_PAGE.replace("ERROR_MSG", error or "No authorization code received."))
                return

            print(f"[*] Got authorization code: {code[:25]}...")
            print("[*] Exchanging for tokens...")

            try:
                tokens = exchange_code(code)
                email, out_path = save_account(tokens)
                rt = tokens.get("refresh_token", "N/A")
                print(f"[OK] email: {email}")
                print(f"[OK] refresh_token: {rt}")
                print(f"[OK] Saved to {out_path}")
                self._html(200, make_success_page(email, tokens))
            except Exception as e:
                print(f"[!] Token exchange failed: {e}")
                self._html(500, ERROR_PAGE.replace("ERROR_MSG", str(e)))
        else:
            self.send_response(404)
            self.end_headers()

    def _html(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, fmt, *args):
        pass


def exchange_code(code: str) -> dict:
    data = urllib.parse.urlencode({
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }).encode()
    req = urllib_request.Request(TOKEN_ENDPOINT, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib_request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()}")


def parse_email_from_id_token(id_token: str) -> str:
    """Decode JWT payload (no verification) to extract email."""
    try:
        payload_b64 = id_token.split(".")[1]
        # Fix padding
        payload_b64 += "=" * (4 - len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        return payload.get("email", "")
    except Exception:
        return ""


def save_account(tokens: dict) -> tuple:
    """Save tokens in accounts format. Returns (email, out_path)."""
    email = parse_email_from_id_token(tokens.get("id_token", ""))
    refresh_token = tokens.get("refresh_token", "")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    out_path = os.path.join(get_app_dir(), "antigravity_tokens.json")

    # Load existing file if present
    data = {"accounts": [], "active": ""}
    if os.path.exists(out_path):
        try:
            with open(out_path, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            pass

    # Update or append account
    found = False
    for acc in data.get("accounts", []):
        if acc.get("email") == email:
            acc["refresh_token"] = refresh_token
            acc["extracted_at"] = now
            found = True
            break
    if not found:
        data.setdefault("accounts", []).append({
            "email": email,
            "refresh_token": refresh_token,
            "extracted_at": now,
        })

    data["active"] = email

    with open(out_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return email, out_path


def get_app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def main():
    try:
        server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    except OSError as e:
        print(f"[!] Cannot start server on port {PORT}: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

    url = f"http://localhost:{PORT}"
    print(f"[*] Server running at {url}")
    print("[*] Opening browser...")
    webbrowser.open(url)
    print("[*] Waiting for OAuth callback... (Ctrl+C to quit)\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
