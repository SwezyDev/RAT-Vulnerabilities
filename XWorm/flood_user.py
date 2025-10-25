
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import hashlib
import socket
import os

class FloodUserUtils:
    def aes_encryptor(input_bytes, key):
        key_hash_UWU = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash_UWU, AES.MODE_ECB) # AES cipher in ECB mode
        padded = pad(input_bytes, AES.block_size) # Pad input to block size
        return cipher.encrypt(padded) # Return encrypted bytes

    def send_encrypted(sock, text: str, key: str): 
        encrypted = FloodUserUtils.aes_encryptor(text.encode(), key) # Encrypt the text
        header = (str(len(encrypted)) + "\0").encode() # Create header with length
        sock.sendall(header + encrypted) # Send header and encrypted data

class FloodUser:
    SPL_XCLIENT = "<Xwormmm>"

    @staticmethod
    def main():
        host = input("Host > ") # Get target host
        port = input("Port > ") # Get target port
        key = input("Key > ") # Get encryption key
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
    FloodUser.main()