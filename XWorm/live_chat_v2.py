
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import threading
import hashlib
import socket
import sys
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

    def aes_decryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode 
        decrypted = cipher.decrypt(input_bytes) # Decrypt input bytes
        try:
            return unpad(decrypted, AES.block_size) # Unpad decrypted bytes
        except:
            return decrypted # Return decrypted bytes even if unpadding fails

print_lock = threading.Lock()  # Global lock for clean console output

class LiveChat:
    SPL_XCLIENT = "<Xwormmm>" # Separator constant, used in all XWorm Versions as far as i know

    @staticmethod
    def main():
        host = input("Host > ") # Get target host
        port = input("Port > ") # Get target port
        key = input("Key > ") # Get encryption key
        sock = LiveChat.connection(host, port) # Connect to target
        while True:
            username = input("Username > ") # Get fake error message
            LiveChat.trigger(username, sock, key) # Trigger the fake error


    def connection(host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
            sock.connect((host, int(port))) # Connect to target
            with print_lock: # Ensure thread-safe print
                print("Connected.") 
            return sock # Return the socket
        except Exception as e:
            with print_lock: # Ensure thread-safe print
                print(f"Connection failed: {e}")
            os._exit(0) # Exit on failure

    def receive(sock, key):
        buffer = b"" # Initialize empty buffer
        while True:
            try:
                while b"\0" not in buffer: # Read until null byte
                    buffer += sock.recv(1) # Receive one byte at a time
                header, buffer = buffer.split(b"\0", 1) # Split at null byte
                length = int(header.decode()) # Get length of incoming data

                while len(buffer) < length: # Read until full payload is received
                    buffer += sock.recv(length - len(buffer)) # Receive remaining bytes
                encrypted_payload = buffer[:length] # Extract the payload
                buffer = buffer[length:] # Update buffer

                decrypted = LiveChatUtils.aes_decryptor(encrypted_payload, key).decode(errors="ignore") # Decrypt the payload

                if decrypted.startswith(f"plugin{LiveChat.SPL_XCLIENT}"): # Handle plugin data
                    plugin_data = decrypted.split(LiveChat.SPL_XCLIENT, 1)[-1] # Extract plugin data
                    LiveChatUtils.send_encrypted(sock, f"sendPlugin{LiveChat.SPL_XCLIENT}{plugin_data}", key) # Acknowledge plugin receipt
                    continue # Dont print 
                
                if decrypted.startswith(f"savePlugin{LiveChat.SPL_XCLIENT}"): # Handle plugin data
                    plugin_data = decrypted.split(LiveChat.SPL_XCLIENT, 1)[-1] # Extract plugin data
                    LiveChatUtils.send_encrypted(sock, f"LLCHAT{LiveChat.SPL_XCLIENT}{plugin_data}", key) # Acknowledge plugin saved
                    LiveChatUtils.send_encrypted(sock, f"ENCHAT{LiveChat.SPL_XCLIENT}ClientID", key)  # Trigger chat connection
                    continue # Dont print
                
                if decrypted.startswith(f"GETChat{LiveChat.SPL_XCLIENT}"): # Handle message
                    message_data = decrypted.split(LiveChat.SPL_XCLIENT, 1)[-1] # Extract message data
                    user_name = message_data.split(":", 1)[0] # Extract username
                    real_message = message_data.split(": ", 1)[-1] # Extract message content

                    with print_lock:
                        sys.stdout.write(f"\r{user_name} > {real_message}\nMessage > ") # Print message
                        sys.stdout.flush() # Flush output
                    continue 

            except Exception as e:
                with print_lock: # Ensure thread-safe print
                    print(f"Error receiving data: {e}")
                break

    def trigger(user, sock, key):
        try:
            payload = f"Xchat{LiveChat.SPL_XCLIENT}ClientID" # Start Chat Payload
            LiveChatUtils.send_encrypted(sock, payload, key) # Send encrypted message
            
            threading.Thread(target=LiveChat.receive, args=(sock, key), daemon=True).start() # Start receiving thread

            while True: 
                message = input("Message > ") # Get fake chat message
                chat_payload = f"Wchat{LiveChat.SPL_XCLIENT}ClientID{LiveChat.SPL_XCLIENT}{user}: {message}\r\n" # Create chat message payload
                LiveChatUtils.send_encrypted(sock, chat_payload, key) # Send chat message
        except Exception as e:
            with print_lock: # Ensure thread-safe print
                print(f"Failed to send message: {e}")

if __name__ == "__main__":
    LiveChat.main() # Run the main function