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

## 🚀 Current Status: Phase 3 Completed

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

### 🔜 Phase 4: Data Transmission (NEXT)
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

## 📚 Educational Value

This project demonstrates:
- **Event-driven programming** with keyboard listeners
- **File I/O operations** with logging and rotation
- **System-level programming** with Windows API
- **Data analysis** with text reconstruction and pattern detection
- **Stealth techniques** used in real malware
- **Security awareness** of keyboard logging threats
