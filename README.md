# Antigravity OAuth Token Fetcher

[English](#english) | [中文](#中文)

---

## English

Get your Google OAuth refresh token for [Antigravity](https://labs.google/antigravity) with one command.

### Quick Start (Recommended)

```bash
npx antigravity-oauth
```

That's it. Browser opens, sign in with Google, token saved to `antigravity_tokens.json`.

> Requires [Node.js](https://nodejs.org/) installed.

### Download Executables

No Node.js? Download a standalone executable:

| Platform | Download |
|----------|----------|
| Windows | [Antigravity-OAuth-Windows.exe](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-Windows.exe) |
| macOS | [Antigravity-OAuth-macOS.dmg](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-macOS.dmg) |
| Linux | [Antigravity-OAuth-Linux](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-Linux) |

> macOS: If it shows "damaged", run `xattr -cr Antigravity-OAuth.app` then right-click → Open.

### Output

Tokens are saved to `antigravity_tokens.json` in the current directory:

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

Supports multiple accounts — run again to add more.

---

## 中文

一条命令获取 [Antigravity（反重力）](https://labs.google/antigravity) 的 Google OAuth refresh token。

### 快速开始（推荐）

```bash
npx antigravity-oauth
```

浏览器自动打开，登录 Google，token 自动保存到当前目录的 `antigravity_tokens.json`。

> 需要安装 [Node.js](https://nodejs.org/)。

### 下载可执行文件

没有 Node.js？下载独立可执行文件：

| 平台 | 下载链接 |
|------|---------|
| Windows | [Antigravity-OAuth-Windows.exe](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-Windows.exe) |
| macOS | [Antigravity-OAuth-macOS.dmg](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-macOS.dmg) |
| Linux | [Antigravity-OAuth-Linux](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-Linux) |

> macOS：如果提示"已损坏"，在终端执行 `xattr -cr Antigravity-OAuth.app`，然后右键 → 打开。

### 输出格式

Token 保存到当前目录的 `antigravity_tokens.json`：

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

支持多账号，再次运行可添加更多账号。

## License

MIT
