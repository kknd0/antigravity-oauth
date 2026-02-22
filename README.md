# Antigravity OAuth Token Fetcher

[English](#english) | [中文](#中文)

---

## English

One-click tool to get your Google OAuth refresh token for [Antigravity](https://labs.google/antigravity). No Python required.

### Download

| Platform | Download |
|----------|----------|
| Windows | [Antigravity-OAuth-Windows.exe](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-Windows.exe) |
| macOS | [Antigravity-OAuth-macOS.dmg](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-macOS.dmg) |
| Linux | [Antigravity-OAuth-Linux](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-Linux) |

### Usage

1. Download for your platform
2. **Windows**: Double-click the `.exe`
3. **macOS**: Open the `.dmg`, drag app out. If it shows "damaged", run in Terminal:
   ```bash
   xattr -cr /path/to/Antigravity-OAuth.app
   ```
   Then right-click → Open.
4. **Linux**: `chmod +x Antigravity-OAuth-Linux && ./Antigravity-OAuth-Linux`
3. Browser opens — sign in with Google
4. Refresh token is saved to `antigravity_tokens.json` in the same directory

Supports multiple accounts — each login appends to the file:

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

### Build from source

```bash
pip install pyinstaller
python build.py
```

---

## 中文

一键获取 [Antigravity（反重力）](https://labs.google/antigravity) 的 Google OAuth refresh token，无需安装 Python。

### 下载

| 平台 | 下载链接 |
|------|---------|
| Windows | [Antigravity-OAuth-Windows.exe](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-Windows.exe) |
| macOS | [Antigravity-OAuth-macOS.dmg](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-macOS.dmg) |
| Linux | [Antigravity-OAuth-Linux](https://github.com/kknd0/antigravity-oauth/releases/latest/download/Antigravity-OAuth-Linux) |

### 使用方法

1. 下载对应平台的文件
2. **Windows**：双击 `.exe` 运行
3. **macOS**：打开 `.dmg`，将 app 拖出。如果提示"已损坏"，在终端执行：
   ```bash
   xattr -cr /path/to/Antigravity-OAuth.app
   ```
   然后右键点击 → 打开。
4. **Linux**：`chmod +x Antigravity-OAuth-Linux && ./Antigravity-OAuth-Linux`
3. 浏览器自动打开 — 登录 Google 账号
4. refresh token 自动保存到同目录下的 `antigravity_tokens.json`

支持多账号 — 每次登录会追加到文件中：

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

### 从源码构建

```bash
pip install pyinstaller
python build.py
```

## License

MIT
