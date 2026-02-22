# Antigravity OAuth Token Fetcher

One-click tool to get your Google OAuth refresh token for [Antigravity](https://labs.google/antigravity).

Download the latest build from [Releases](../../releases/latest) — no Python required.

## Usage

1. Download the executable for your platform from Releases
2. Double-click to run
3. Browser opens → Sign in with Google
4. Refresh token is saved to `antigravity_tokens.json` in the same directory

You can add multiple accounts — each login appends to the file:

```json
{
  "accounts": [
    {
      "email": "user@gmail.com",
      "refresh_token": "1//0fXXXXXXXXXX",
      "extracted_at": "2026-02-22T01:19:00Z"
    }
  ],
  "active": "user@gmail.com"
}
```

## Build from source

```bash
pip install pyinstaller
python build.py
```

Output in `dist/`.

## License

MIT
