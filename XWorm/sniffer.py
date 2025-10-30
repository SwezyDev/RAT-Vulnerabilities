from Crypto.Util.Padding import unpad, pad
from Crypto.Cipher import AES
from datetime import datetime
import hashlib
import pefile
import base64
import random
import string
import socket
import time
import gzip
import os
import io

class ReceiveUtils:
    def aes_decryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode 
        decrypted = cipher.decrypt(input_bytes) # Decrypt input bytes
        try:
            return unpad(decrypted, AES.block_size) # Unpad decrypted bytes
        except:
            return decrypted # Return decrypted bytes even if unpadding fails

    def aes_encryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode
        padded = pad(input_bytes, AES.block_size) # Pad input to block size
        return cipher.encrypt(padded) # Return encrypted bytes

    def send_encrypted(sock, text: str, key: str): 
        encrypted = ReceiveUtils.aes_encryptor(text.encode(), key) # Encrypt the text
        header = (str(len(encrypted)) + "\0").encode() # Create header with length
        sock.sendall(header + encrypted) # Send header and encrypted data

    def decompress(input_bytes: bytes) -> bytes:
        with io.BytesIO(input_bytes) as memory_stream: # Create memory stream
            try:
                original_len = int.from_bytes(memory_stream.read(4), "little") # Read original length
            except Exception:
                original_len = None

            with gzip.GzipFile(fileobj=memory_stream, mode="rb") as gzip_file: # Create gzip file
                if original_len:
                    decompressed_data = gzip_file.read(original_len) # Read decompressed data
                else:
                    decompressed_data = gzip_file.read()

            return decompressed_data # Return decompressed bytes

    def decode_key(key):
        return key.decode(errors="ignore") if isinstance(key, bytes) else key # Decode key if bytes

    def generate_hex_string(length=20):
        hex_chars = string.hexdigits.upper()[:16] # Hexadecimal characters
        return ''.join(random.choices(hex_chars, k=length)) # Generate random hex string

    def random_true_false():
        return random.choice(["True", "False"]) # Randomly return True or False

    def generate_windows_version():
        windows_versions = {
            "7": ["Home Premium", "Professional", "Ultimate"],
            "8": ["Core", "Pro", "Enterprise"],
            "8.1": ["Core", "Pro", "Enterprise"],
            "10": ["Home", "Pro", "Enterprise", "Education"],
            "11": ["Home", "Pro", "Enterprise", "Education"]
        }

        version = random.choice(list(windows_versions.keys())) # Random Windows version
        edition = random.choice(windows_versions[version]) # Random edition
        arch = random.choice(["32bit", "64bit"]) # Random architecture

        return f"Windows {version} {edition} {arch}" # Return full Windows version string

    def generate_gpu():
        nvidia_gpus = [
            "GeForce GTX 1050 Ti", "GeForce GTX 1060", "GeForce GTX 1650",
            "GeForce GTX 1660", "GeForce GTX 1660 Super", "GeForce GTX 1660 Ti",
            "GeForce RTX 2060", "GeForce RTX 2070", "GeForce RTX 2080 Ti",
            "GeForce RTX 3060", "GeForce RTX 3060 Ti", "GeForce RTX 3070", "GeForce RTX 3070 Ti",
            "GeForce RTX 3080", "GeForce RTX 3080 Ti", "GeForce RTX 3090",
            "GeForce RTX 4060", "GeForce RTX 4060 Ti", "GeForce RTX 4070", "GeForce RTX 4080", "GeForce RTX 4090"
        ]

        amd_gpus = [
            "Radeon RX 560", "Radeon RX 570", "Radeon RX 580", "Radeon RX 590",
            "Radeon RX 6500 XT", "Radeon RX 6600", "Radeon RX 6600 XT",
            "Radeon RX 6650 XT", "Radeon RX 6700 XT", "Radeon RX 6750 XT",
            "Radeon RX 6800", "Radeon RX 6800 XT", "Radeon RX 6900 XT",
            "Radeon RX 7600", "Radeon RX 7700 XT", "Radeon RX 7900 XT", "Radeon RX 7900 XTX"
        ]

        return random.choice(nvidia_gpus + amd_gpus) # Return random GPU
    

    def generate_cpu():
        intel_generations = {
            "10th Gen": ["i3-10100F", "i5-10400", "i5-10600K", "i7-10700K", "i9-10900K"],
            "11th Gen": ["i5-11400F", "i5-11600K", "i7-11700K", "i9-11900K"],
            "12th Gen": ["i3-12100F", "i5-12400F", "i5-12600K", "i7-12700K", "i9-12900K"],
            "13th Gen": ["i3-13100", "i5-13400F", "i5-13600K", "i7-13700K", "i9-13900K"],
            "14th Gen": ["i5-14400F", "i7-14700K", "i9-14900K"]
        }

        amd_cpus = [
            "Ryzen 3 3200G", "Ryzen 3 4100", "Ryzen 5 3500", "Ryzen 5 3600",
            "Ryzen 5 5600", "Ryzen 5 5600X", "Ryzen 5 7600", "Ryzen 5 7600X",
            "Ryzen 7 3700X", "Ryzen 7 5800X", "Ryzen 7 7700X",
            "Ryzen 9 3900X", "Ryzen 9 5900X", "Ryzen 9 7900X", "Ryzen 9 7950X"
        ]

        if random.choice([True, False]):
            gen = random.choice(list(intel_generations.keys())) # Random Intel generation
            model = random.choice(intel_generations[gen]) # Random model from generation
            return f"{gen} Intel {model}" # Return random Intel CPU
        else:
            return random.choice(amd_cpus) # Return random AMD CPU
        
    def generate_ram():
        ram_options = ["4", "6", "8", "10", "12", "16", "24", "32"]  # RAM options in GB
        return f"{random.choice(ram_options)} GB" # Return random RAM size
    
    def generate_antivirus():
        antivirus_list = [
            "Windows Defender", "Avast", "AVG", "BitDefender", "Kaspersky",
            "Norton", "McAfee", "ESET NOD32", "Malwarebytes", "Sophos",
            "Trend Micro", "Webroot", "Panda", "F-Secure", "Avira"
        ]
        return random.choice(antivirus_list) # Return random antivirus name

    def generate_window_title():
        window_titles = [
            "explorer", "discord", "Fortnite", "Steam", "Chrome", "Visual Studio Code",
            "Notepad", "Spotify", "Microsoft Word", "Photoshop", "Edge", "Minecraft", 
            "Task Manager", "Skype", "WhatsApp", "Eclipse", "Slack", "Battle.net", 
            "Microsoft Excel", "Spotify", "YouTube", "Adobe Acrobat", "Zoom", 
            "Twitch", "VLC Media Player", "Opera", "Git Bash", "Paint", "Teams", 
            "Trello", "WinRAR", "FileZilla", "Blender", "Cydia", "Spotify", "GIMP",
            "SteamVR", "Epic Games Launcher", "Autocad", "PyCharm", "VirtualBox", 
            "Node.js", "GitHub Desktop", "GitKraken", "Unity", "Windows Media Player", 
            "OneDrive", "QuickTime", "Notepad++", "MSI Afterburner", "OBS Studio", 
            "Razer Synapse", "Battlefield V", "Apex Legends", "World of Warcraft", 
            "League of Legends", "Google Drive", "Dropbox", "Reddit", "Facebook", 
            "Twitter", "Instagram", "Visual Studio Code", "Visual Studio", "Python",
            "PayPal", "US Bank", "Development Builder", "Vencord", "Swezy", "PornHub",
            "XXX", "YouPorn", "XHamster", "Watch Free Porn"
        ]
        return random.choice(window_titles) # Return random window title

    def current_time():
        return datetime.today().strftime("%d.%m.%Y")
    
    def current_datetime():
        return datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    def generate_username():
        rndm_usernames = ["Admin", "Administrator", "Joe", "Anne", "Thomas", "GamingPC",
                    "Jordan", "John", "Mike", "PC-1941", "Laptop-2140", "admin", "666",
                    "Bromes", "Amy", "Timo", "Ben", "Lucy", "Luca", "Ingo", "Ely", "Evil",
                    "mango", "Sers", "Olaf Scholz", "Doris", "xxx", "Owner", "Axel", "Putin",
                    "Kim Jong-un"]
        return random.choice(rndm_usernames) # Return random username

    def generate_group():
        rndm_groub = ["User", "XWorm", "XWorm v5.6", "Slaves", "Slave", "Ratted", "Business", "V.I.P", "XWorm v3.1", "XWorm v5", "XWorm v4.1", "XWorm v5.2", "XWorm v2"]
        return random.choice(rndm_groub) # Return random group

class Receive:
    SPL_XCLIENT = "<Xwormmm>" # Separator constant, used in all XWorm Versions as far as i know

    @staticmethod
    def main():
        host = input("Host > ") # Get target host
        port = input("Port > ") # Get target port
        key = input("Key > ") # Get encryption key
        sock = Receive.connection(host, port) # Connect to target
        dump = input("Dump Plugins - DLLs? (y/n) > ").lower() # Ask to dump existing clients
        if not dump in ["y", "n"]: # Validate input
            print("Invalid input. Please enter 'y' or 'n'.") 
            return # Exit if invalid

        payload = ("INFO" + Receive.SPL_XCLIENT +
                    ReceiveUtils.generate_hex_string() + Receive.SPL_XCLIENT +
                    ReceiveUtils.generate_username() + Receive.SPL_XCLIENT +
                    ReceiveUtils.generate_windows_version() + Receive.SPL_XCLIENT +
                    ReceiveUtils.generate_group() + Receive.SPL_XCLIENT +
                    ReceiveUtils.current_time() + Receive.SPL_XCLIENT +
                    ReceiveUtils.random_true_false() + Receive.SPL_XCLIENT +
                    ReceiveUtils.random_true_false() + Receive.SPL_XCLIENT +
                    ReceiveUtils.random_true_false() + Receive.SPL_XCLIENT +
                    ReceiveUtils.generate_cpu() + Receive.SPL_XCLIENT +
                    ReceiveUtils.generate_gpu() + Receive.SPL_XCLIENT +
                    ReceiveUtils.generate_ram() + Receive.SPL_XCLIENT +
                    ReceiveUtils.generate_antivirus()
                   ) # Create User Payload
        payload2 = ("PING!" + Receive.SPL_XCLIENT +
                ReceiveUtils.generate_window_title() + Receive.SPL_XCLIENT +
                ReceiveUtils.current_datetime()) # Second User Payload
        
        ReceiveUtils.send_encrypted(sock, payload, key) # Send encrypted message
        ReceiveUtils.send_encrypted(sock, payload2, key) # Send encrypted message

        Receive.receive(sock, key, dump) # Start receiving


    def connection(host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
            sock.connect((host, int(port))) # Connect to target
            print("Connected.") 
            return sock # Return the socket
        except Exception as e:
            print(f"Connection failed: {e}")
            os._exit(0) # Exit on failure

    def receive(sock, enc_key, dump):
        buffer = b"" # Initialize empty buffer
        while True:
            try:
                while b"\0" not in buffer: # Read until null byte
                    chunk = sock.recv(4096)
                    if not chunk:
                        raise ConnectionError("Socket closed")
                    buffer += chunk
                header, buffer = buffer.split(b"\0", 1) # Split at null byte
                length = int(header.decode()) # Get length of incoming data

                while len(buffer) < length: # Read until full payload is received
                    chunk = sock.recv(length - len(buffer))
                    if not chunk:
                        raise ConnectionError("Socket closed while reading payload") # Check for closed socket
                    buffer += chunk
                encrypted_payload = buffer[:length] # Extract the payload
                buffer = buffer[length:] # Update buffer

                try:
                    decrypted = ReceiveUtils.aes_decryptor(encrypted_payload, enc_key).decode(errors="ignore") # Decrypt the payload
                except Exception as e:
                    print(f"Decryption failed: {e}")
                    continue

                if decrypted.startswith(f"plugin{Receive.SPL_XCLIENT}"): # Handle plugin data
                    plugin_data = decrypted.split(Receive.SPL_XCLIENT, 1)[-1] # Extract plugin data
                    ReceiveUtils.send_encrypted(sock, f"sendPlugin{Receive.SPL_XCLIENT}{plugin_data}", enc_key) # Acknowledge plugin receipt
                
                print(f"Received: {decrypted}") # Print the decrypted message

                if dump == "y": # If dumping is enabled
                    if decrypted.startswith(f"savePlugin{Receive.SPL_XCLIENT}"): # Handle save plugin command
                        plugin_info = decrypted.split(Receive.SPL_XCLIENT, 2) # Split the command
                        if len(plugin_info) < 3:
                            continue # Skip if not enough parts

                        plugin_tempname = f"plugin_{random.randint(1000,9999)}.dll" # Create unique plugin name
                        b64_payload = plugin_info[2]

                        try:
                            raw = base64.b64decode(b64_payload, validate=True) # Try to decode Base64
                        except Exception as e: 
                            print(f"Base64 decode failed: {e}")
                            try:
                                raw = base64.b64decode(b64_payload + "===") # Try to fix padding and decode
                            except Exception as e:
                                print(f"Base64 decode with padding failed: {e}")
                                continue # skip this plugin, keep receiver alive
                            
                        try:
                            decompressed = ReceiveUtils.decompress(raw) # Decompress the data
                        except Exception as e:
                            decompressed = raw # Use raw data if decompression fails

                        with open(plugin_tempname, "wb") as f: # Save the plugin
                            f.write(decompressed) # Write to file

                        pe_name = None # Initialize pe name
                        try:
                            pe = pefile.PE(plugin_tempname) # Parse PE file
                            if hasattr(pe, 'FileInfo') and pe.FileInfo: # Check for FileInfo
                                stack = list(pe.FileInfo) # Initialize stack
                                while stack: # Traverse FileInfo
                                    item = stack.pop() # Pop item from stack
                                    if isinstance(item, (list, tuple)): # If item is a list or tuple
                                        stack.extend(item) # Extend stack
                                        continue # Continue to next iteration
                                    key_obj = getattr(item, 'Key', None) # Get Key attribute
                                    if key_obj and ReceiveUtils.decode_key(key_obj) == 'StringFileInfo': # Check for StringFileInfo
                                        for st in getattr(item, 'StringTable', []) or []: # Iterate over StringTable
                                            entries = getattr(st, 'entries', {}) or {} # Get entries
                                            for entry_key, entry_value in entries.items(): # Iterate over entries
                                                if ReceiveUtils.decode_key(entry_key) == 'OriginalFilename': # Check for OriginalFilename
                                                    pe_name = entry_value.decode(errors="ignore") if isinstance(entry_value, bytes) else entry_value # Decode value
                                                    break
                                            if pe_name: 
                                                break
                                    if pe_name:
                                        break
                            pe.close()
                        except Exception:
                            pass # Ignore PE parsing errors

                        if pe_name:
                            if os.path.exists(pe_name):
                                os.remove(pe_name) # Remove existing file
                            os.rename(plugin_tempname, pe_name) # Rename file to original name
                            plugin_tempname = pe_name # Update temp name
                            
                        print(f"Plugin saved: {plugin_tempname}") # Notify user

            except Exception as e:
                print(f"Error receiving data: {e}")
                break

if __name__ == "__main__":
    Receive.main() # Run the main function 
