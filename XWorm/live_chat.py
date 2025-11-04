
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import argparse
import hashlib
import socket
import os

class LiveChatUtils:
    def aes_encryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode
        padded = pad(input_bytes, AES.block_size) # Pad input to block size
        return cipher.encrypt(padded) # Return encrypted bytes

    def send_encrypted(sock, text: str, key: str): 
        encrypted = LiveChatUtils.aes_encryptor(text.encode(), key) # Encrypt the text
        header = (str(len(encrypted)) + "\0").encode() # Create header with length
        sock.sendall(header + encrypted) # Send header and encrypted data

class LiveChat:
    SPL_XCLIENT = "<Xwormmm>" # Separator constant, used in all XWorm Versions as far as i know

    @staticmethod
    def main():
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--h", "--host", dest="host", nargs="?", help="Target host") # Target host
        parser.add_argument("--p", "--port", dest="port", nargs="?", help="Target port") # Target port
        parser.add_argument("--k", "--key", dest="key", nargs="?", help="Encryption key") # Encryption key
        parser.add_argument("--u", "--username", dest="username", nargs="?", help="Username") # Username
        parser.add_argument("--help", action="store_true", dest="help_flag", help="Show this help message and exit") # Help flag

        args, unknown = parser.parse_known_args() # Parse known args only
 
        if args.help_flag:
            parser.print_help() # Show help message
            return # Exit after showing help

        host = args.host if args.host else input("Host > ") # Get target host
        port = args.port if args.port else input("Port > ") # Get target port
        key = args.key if args.key else input("Key > ") # Get encryption key

        port = int(port) if str(port).isdigit() else input("Port > ") # Ensure port is an integer

        sock = LiveChat.connection(host, port) # Connect to target

        username = args.username if args.username else input("Username > ") # Get fake error message
        LiveChat.trigger(username, sock, key) # Trigger the fake error


    def connection(host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
            sock.connect((host, int(port))) # Connect to target
            print("Connected.") 
            return sock # Return the socket
        except Exception as e:
            print(f"Connection failed: {e}")
            os._exit(0) # Exit on failure

    def trigger(user, sock, key):
        try:
            payload = f"Xchat{LiveChat.SPL_XCLIENT}ClientID" # Start Chat Payload
            LiveChatUtils.send_encrypted(sock, payload, key) # Send encrypted message
            

            while True: 
                message = input("Message > ") # Get fake chat message
                chat_payload = f"Wchat{LiveChat.SPL_XCLIENT}ClientID{LiveChat.SPL_XCLIENT}{user}: {message}\r\n"
                LiveChatUtils.send_encrypted(sock, chat_payload, key)
        except Exception as e:
            print(f"Failed to send message: {e}")

if __name__ == "__main__":
    LiveChat.main() # Run the main function