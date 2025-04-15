[img]https://github.com/Lovsan/CrackSmith/blob/main/crack_smith.png[/img]

# 🔐 CrackSmith

A full-featured terminal-based hash cracking tool written in Python. Supports `bcrypt`, `md5`, `sha1`, and `sha256`. Includes threading, live system stats, resume mode, notifications via webhook/Discord/Telegram, and support for cracking multiple hashes.

---

## 🛠️ Features

- Multi-hash cracking from file
- Live stats: attempts, speed, ETA, resource usage
- Resume support
- Webhook + Discord + Telegram notifications
- HTML report generation
- Benchmark mode
- Test mode with known bcrypt hash
- Graceful interrupt support (Ctrl+C to stop)

---

## 🚀 Usage

Run the script:
```bash
python cracker.py
```
If no arguments are provided, you'll be prompted with a menu.

---

## ⚙️ Command-Line Options

| Option           | Description                                      |
|------------------|--------------------------------------------------|
| `--hash`         | Crack a single hash                              |
| `--hashfile`     | Path to a file with multiple hashes (one per line) |
| `--wordlist`     | Path to a wordlist file (default: rockyou.txt)   |
| `--resume`       | Resume from the last cracking session            |
| `--settings`     | Path to `settings.json` for config values        |
| `--test`         | Run test mode with a known bcrypt hash           |
| `--benchmark`    | Run bcrypt benchmark (10k hashes)                |

---

## 🔧 settings.json Format

```json
{
  "webhook": "https://your-custom-webhook.url",
  "discord_webhook": "https://discord.com/api/webhooks/...",
  "telegram_token": "123456:ABCDEF-ghIklmnopQrstuv123",
  "telegram_chat_id": "123456789",
  "threads": 4
}
```

Place this file in the working directory or pass via `--settings path/to/file.json`.

---

## 📄 HTML Report

After a password is found, an HTML report is saved as `crack_report.html` with details like:
- Found password
- Time taken
- Attempts
- Hash type

---

## 🧪 Example Commands

```bash
# Crack a bcrypt hash
python cracker.py --hash "$2y$10$...."

# Crack multiple hashes
python cracker.py --hashfile hashes.txt

# Resume a previous session
python cracker.py --hash "$2b$..." --resume

# Run in test mode
python cracker.py --test

# Run benchmark
python cracker.py --benchmark
```

---

## 🧯 Exiting

Press `Ctrl+C` anytime. The tool will safely stop, show progress, and save resume info.

---

## 💬 Notifications

Enable notifications via:
- Discord webhook
- Telegram bot
- Generic webhook

All managed via `settings.json`.

---

## 📬 Contributions

PRs welcome! Suggest improvements, add hash algorithms, or integrate GPU backends (like Hashcat) in the future!

---

## License

MIT License

