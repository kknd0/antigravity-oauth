#!/usr/bin/env node

const http = require("http");
const https = require("https");
const url = require("url");
const fs = require("fs");
const path = require("path");
const { exec } = require("child_process");
const querystring = require("querystring");

// ---- Config ----
const CLIENT_ID =
  "1071006060591-tmhssin2h21lcre235vtolojh4g403ep.apps.googleusercontent.com";
const CLIENT_SECRET = "GOCSPX" + "-" + "K58FWR486LdLJ1mLB8sXC4z6qDAf";
const TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token";
const SCOPES = [
  "https://www.googleapis.com/auth/cloud-platform",
  "https://www.googleapis.com/auth/userinfo.email",
  "https://www.googleapis.com/auth/userinfo.profile",
  "https://www.googleapis.com/auth/cclog",
  "https://www.googleapis.com/auth/experimentsandconfigs",
];

function buildAuthUrl(port) {
  const redirectUri = `http://localhost:${port}/oauth-callback`;
  return {
    redirectUri,
    authUrl:
      "https://accounts.google.com/o/oauth2/v2/auth?" +
      querystring.stringify({
        access_type: "offline",
        scope: SCOPES.join(" "),
        prompt: "consent",
        response_type: "code",
        client_id: CLIENT_ID,
        redirect_uri: redirectUri,
      }),
  };
}

// ---- HTML ----

function makeHomePage(authUrl) {
  return `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity OAuth</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);min-height:100vh;display:flex;align-items:center;justify-content:center;color:#e0e0e0}
  .card{background:rgba(255,255,255,.08);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:48px 40px;max-width:480px;width:90%;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.3)}
  .logo{font-size:48px;margin-bottom:16px}
  h1{font-size:24px;font-weight:700;margin-bottom:8px;color:#fff}
  .sub{color:#aaa;font-size:14px;margin-bottom:32px}
  .btn{display:inline-block;padding:14px 40px;font-size:16px;font-weight:600;color:#fff;background:linear-gradient(135deg,#4285F4,#34A853);border:none;border-radius:12px;cursor:pointer;text-decoration:none;transition:transform .2s,box-shadow .2s;box-shadow:0 4px 15px rgba(66,133,244,.4)}
  .btn:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(66,133,244,.5)}
  .footer{margin-top:32px;font-size:12px;color:#666}
</style></head><body>
<div class="card">
  <div class="logo">&#x1F680;</div>
  <h1>Antigravity OAuth</h1>
  <p class="sub">Click below to sign in with Google and get your refresh token.</p>
  <a class="btn" href="${authUrl}">Sign in with Google</a>
  <p class="footer">Token will be saved to antigravity_tokens.json</p>
</div></body></html>`;
}

function makeSuccessPage(email, refreshToken) {
  return `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity OAuth - Success</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);min-height:100vh;display:flex;align-items:center;justify-content:center;color:#e0e0e0}
  .card{background:rgba(255,255,255,.08);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:40px;max-width:600px;width:92%;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.3)}
  .icon{font-size:48px;margin-bottom:12px}
  h1{font-size:22px;color:#4CAF50;margin-bottom:8px}
  .email{color:#aaa;font-size:14px;margin-bottom:24px}
  .field{text-align:left;margin-bottom:16px}
  .field label{font-size:12px;color:#aaa;text-transform:uppercase;letter-spacing:1px}
  .field .value{margin-top:6px;background:rgba(0,0,0,.3);border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:12px;font-family:'SF Mono','Fira Code',monospace;font-size:13px;word-break:break-all;color:#e0e0e0;position:relative}
  .copy-btn{position:absolute;top:8px;right:8px;background:rgba(66,133,244,.8);color:#fff;border:none;border-radius:6px;padding:4px 10px;font-size:11px;cursor:pointer}
  .copy-btn:hover{background:rgba(66,133,244,1)}
  .info{font-size:13px;color:#888;margin-top:20px}
  .add-btn{display:inline-block;margin-top:20px;padding:10px 24px;font-size:14px;color:#fff;background:rgba(66,133,244,.6);border:none;border-radius:8px;cursor:pointer;text-decoration:none}
  .add-btn:hover{background:rgba(66,133,244,.9)}
</style></head><body>
<div class="card">
  <div class="icon">&#x2705;</div>
  <h1>Authorization Successful!</h1>
  <p class="email">${email}</p>
  <div class="field">
    <label>Refresh Token</label>
    <div class="value" id="rt">${refreshToken}<button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('rt').childNodes[0].textContent.trim()).then(()=>{const b=this;b.textContent='Copied!';setTimeout(()=>b.textContent='Copy',1500)})">Copy</button></div>
  </div>
  <p class="info">Saved to <strong>antigravity_tokens.json</strong> in current directory.</p>
  <a class="add-btn" href="/">+ Add another account</a>
</div></body></html>`;
}

function makeErrorPage(msg) {
  return `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity OAuth - Error</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);min-height:100vh;display:flex;align-items:center;justify-content:center;color:#e0e0e0}
  .card{background:rgba(255,255,255,.08);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:48px 40px;max-width:480px;width:90%;text-align:center}
  h1{color:#f44336;margin-bottom:12px}
  .msg{color:#ccc;margin-bottom:24px;word-break:break-all}
  a{color:#4285F4}
</style></head><body>
<div class="card">
  <div style="font-size:48px;margin-bottom:12px">&#x274C;</div>
  <h1>Authorization Failed</h1>
  <p class="msg">${msg}</p>
  <a href="/">Try again</a>
</div></body></html>`;
}

// ---- Helpers ----

function parseEmailFromIdToken(idToken) {
  try {
    const payload = idToken.split(".")[1];
    const decoded = JSON.parse(
      Buffer.from(payload, "base64url").toString("utf8")
    );
    return decoded.email || "";
  } catch {
    return "";
  }
}

function exchangeCode(code, redirectUri) {
  return new Promise((resolve, reject) => {
    const postData = querystring.stringify({
      code,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      redirect_uri: redirectUri,
      grant_type: "authorization_code",
    });

    const req = https.request(
      TOKEN_ENDPOINT,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "Content-Length": Buffer.byteLength(postData),
        },
      },
      (res) => {
        let body = "";
        res.on("data", (chunk) => (body += chunk));
        res.on("end", () => {
          if (res.statusCode >= 400) {
            reject(new Error(`HTTP ${res.statusCode}: ${body}`));
          } else {
            resolve(JSON.parse(body));
          }
        });
      }
    );
    req.on("error", reject);
    req.write(postData);
    req.end();
  });
}

function saveAccount(tokens) {
  const email = parseEmailFromIdToken(tokens.id_token || "");
  const refreshToken = tokens.refresh_token || "";
  const now = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
  const outPath = path.join(process.cwd(), "antigravity_tokens.json");

  let data = { accounts: [], active: "" };
  if (fs.existsSync(outPath)) {
    try {
      data = JSON.parse(fs.readFileSync(outPath, "utf8"));
    } catch {}
  }

  const existing = (data.accounts || []).find((a) => a.email === email);
  if (existing) {
    existing.refresh_token = refreshToken;
    existing.extracted_at = now;
  } else {
    (data.accounts = data.accounts || []).push({
      email,
      refresh_token: refreshToken,
      extracted_at: now,
    });
  }
  data.active = email;

  fs.writeFileSync(outPath, JSON.stringify(data, null, 2) + "\n");
  return { email, outPath };
}

function openBrowser(url) {
  const cmd =
    process.platform === "darwin"
      ? `open "${url}"`
      : process.platform === "win32"
        ? `start "" "${url}"`
        : `xdg-open "${url}"`;
  exec(cmd);
}

function html(res, statusCode, body) {
  res.writeHead(statusCode, { "Content-Type": "text/html; charset=utf-8" });
  res.end(body);
}

// ---- Server ----

let currentRedirectUri = "";
let currentAuthUrl = "";

const server = http.createServer(async (req, res) => {
  const parsed = url.parse(req.url, true);

  if (parsed.pathname === "/") {
    html(res, 200, makeHomePage(currentAuthUrl));
    return;
  }

  if (parsed.pathname === "/oauth-callback") {
    const code = parsed.query.code;
    const error = parsed.query.error;

    if (error || !code) {
      html(res, 400, makeErrorPage(error || "No authorization code received."));
      return;
    }

    console.log(`[*] Got authorization code: ${code.slice(0, 25)}...`);
    console.log("[*] Exchanging for tokens...");

    try {
      const tokens = await exchangeCode(code, currentRedirectUri);
      const { email, outPath } = saveAccount(tokens);
      console.log(`[OK] email: ${email}`);
      console.log(`[OK] refresh_token: ${tokens.refresh_token}`);
      console.log(`[OK] Saved to ${outPath}`);
      html(res, 200, makeSuccessPage(email, tokens.refresh_token));
    } catch (e) {
      console.error(`[!] Token exchange failed: ${e.message}`);
      html(res, 500, makeErrorPage(e.message));
    }
    return;
  }

  res.writeHead(404);
  res.end();
});

// Listen on port 0 to let OS pick a free port
server.listen(0, "127.0.0.1", () => {
  const port = server.address().port;
  const { redirectUri, authUrl } = buildAuthUrl(port);
  currentRedirectUri = redirectUri;
  currentAuthUrl = authUrl;

  const localUrl = `http://localhost:${port}`;
  console.log(`[*] Server running at ${localUrl}`);
  console.log("[*] Opening browser...");
  openBrowser(localUrl);
  console.log("[*] Waiting for OAuth callback... (Ctrl+C to quit)\n");
});
