
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import argparse
import hashlib
import socket
import os

class FloodUserUtils:
    def aes_encryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode
        padded = pad(input_bytes, AES.block_size) # Pad input to block size
        return cipher.encrypt(padded) # Return encrypted bytes

    def send_encrypted(sock, text: str, key: str): 
        encrypted = FloodUserUtils.aes_encryptor(text.encode(), key) # Encrypt the text
        header = (str(len(encrypted)) + "\0").encode() # Create header with length
        sock.sendall(header + encrypted) # Send header and encrypted data

class FloodUser:
    SPL_XCLIENT = "<Xwormmm>" # Separator constant, used in all XWorm Versions as far as i know

    @staticmethod
    def main():
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--h", "--host", dest="host", nargs="?", help="Target host") # Target host
        parser.add_argument("--p", "--port", dest="port", nargs="?", help="Target port") # Target port
        parser.add_argument("--k", "--key", dest="key", nargs="?", help="Encryption key") # Encryption key
        parser.add_argument("--help", action="store_true", dest="help_flag", help="Show this help message and exit") # Help flag

        args, unknown = parser.parse_known_args() # Parse known args only
 
        if args.help_flag:
            parser.print_help() # Show help message
            return # Exit after showing help

        host = args.host if args.host else input("Host > ") # Get target host
        port = args.port if args.port else input("Port > ") # Get target port
        key = args.key if args.key else input("Key > ") # Get encryption key

        port = int(port) if str(port).isdigit() else input("Port > ") # Ensure port is an integer

        sock = FloodUser.connection(host, port) # Connect to target
        FloodUser.trigger(sock, key) # Trigger the User


    def connection(host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
            sock.connect((host, int(port))) # Connect to target
            print("Connected.") 
            return sock # Return the socket
        except Exception as e:
            print(f"Connection failed: {e}")
            os._exit(0) # Exit on failure

    def trigger(sock, key):
        try:
            payload = ("INFO" + FloodUser.SPL_XCLIENT +
                        "Client ID" + FloodUser.SPL_XCLIENT +
                        "Username" + FloodUser.SPL_XCLIENT +
                        "Operating System" + FloodUser.SPL_XCLIENT +
                        "Group" + FloodUser.SPL_XCLIENT +
                        "Date" + FloodUser.SPL_XCLIENT +
                        "USB" + FloodUser.SPL_XCLIENT +
                        "UAC" + FloodUser.SPL_XCLIENT +
                        "CAM" + FloodUser.SPL_XCLIENT +
                        "CPU" + FloodUser.SPL_XCLIENT +
                        "GPU" + FloodUser.SPL_XCLIENT +
                        "RAM" + FloodUser.SPL_XCLIENT +
                        "Anti Virus"
                       ) # Create User Payload
            payload2 = ("PING!" + FloodUser.SPL_XCLIENT +
                    "https://github.com/SwezyDev" + FloodUser.SPL_XCLIENT +
                    "13.37.1337 13:37:13") # Fake Time
            while True:
                FloodUserUtils.send_encrypted(sock, payload, key) # Send encrypted message
                FloodUserUtils.send_encrypted(sock, payload2, key) # Send encrypted message
                print("User sent.") # The connection could crash, so if you want to keep spamming just make a try - except here and reconnect if needed
        except Exception as e:
            print(f"Failed to send message: {e}")

if __name__ == "__main__":
    FloodUser.main() # Run the main function