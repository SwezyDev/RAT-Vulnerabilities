from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import hashlib
import base64
import System
import time
import json
import clr
import sys

clr.AddReference("System") # Add reference to System assembly
clr.AddReference("mscorlib") # Add reference to mscorlib assembly

class DecryptPayloadUtils:
    def decrypt_aes_ecb(b64: str, key: bytes) -> str: # Decrypt AES ECB encrypted base64 string
        try:
            cipher = AES.new(key, AES.MODE_ECB) # Create AES cipher in ECB mode
            encrypted_data = base64.b64decode(b64) # Decode base64 input
            decrypted_data = cipher.decrypt(encrypted_data) # Decrypt the data
            unpadded_data = unpad(decrypted_data, AES.block_size, style='pkcs7') # Unpad the decrypted data
            return unpadded_data.decode('utf-8', errors='replace') # Return as UTF-8 string
        except Exception as e:
            print(f"Decryption failed: {e}") # Print error message
            sys.exit(0) # Exit on failure

    def derive_key(mutex: str) -> bytes: # Derive AES key from mutex using MD5
        md5_hash = hashlib.md5(mutex.encode('utf-8')).digest()  # MD5 hash of the mutex
        key_array = bytearray(32) # Initialize 32-byte array
        key_array[0:16] = md5_hash # First 16 bytes
        key_array[15:31] = md5_hash # Last 16 bytes overlap by one byte
        return bytes(key_array) # Return as bytes

    def extract(exe_path: str): # Extract settings from the executable
        try:
            assembly = System.Reflection.Assembly.LoadFrom(exe_path) # Load the assembly
        except Exception as e:
            print(f"Failed to load assembly: {e}") # Print error message
            sys.exit(0) # Exit on failure

        type_names = ["Settings", "Stub.Settings"] # Possible settings class names
        settings_type = None # Initialize settings type
        for name in type_names: # Find the settings type
            settings_type = assembly.GetType(name) # Get the type by name
            if settings_type is not None: # If found, break
                break

        if settings_type is None: # If not found, exit
            print("Settings type not found.") # Print error message
            sys.exit(0) # Exit on failure

        binding_flags = System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static # Public static fields
        fields = settings_type.GetFields(binding_flags) # Get all public static fields
        if fields is None or len(fields) == 0: # If no fields found, exit
            print("No public static fields found in the Settings Class.") # Print error message
            sys.exit(0) # Exit on failure


        encrypted_settings = {} # Dictionary to hold encrypted settings
        mutex_value = None # Variable to hold mutex value used for key derivation
        for field in fields: # Iterate over fields
            value = field.GetValue(None) # Get the field value
            encrypted_settings[field.Name] = value # Store in dictionary
            if field.Name == "Mutex": # If field is Mutex, store its value
                mutex_value = value # Store mutex value

        if mutex_value is None: # If mutex not found
            print("Mutex field not found in Settings.") # Print error message
            sys.exit(0) # Exit on failure

        results = {} # Dictionary to hold decrypted results

        key_bytes = DecryptPayloadUtils.derive_key(mutex_value) # Derive decryption key
        key_hex = key_bytes.hex() # Convert key to hex for printing

        results["Decryption Key"] = key_hex # Store decryption key in results

        for setting_name, encrypted_value in encrypted_settings.items(): # Decrypt each setting
            try:
                if isinstance(encrypted_value, str): # If the value is a string
                    try:
                        decoded_value = base64.b64decode(encrypted_value) # Decode from base64
                        if len(decoded_value) % 16 == 0 and setting_name != "Mutex": # If length is multiple of 16 and not Mutex
                            decrypted_value = DecryptPayloadUtils.decrypt_aes_ecb(encrypted_value, key_bytes) # Decrypt the value
                        else:
                            decrypted_value = encrypted_value # Use the original value

                        if setting_name == "Hosts":
                            results[setting_name] = decrypted_value.split(',') # Split hosts by comma
                        else:
                            results[setting_name] = decrypted_value # Store decrypted value
                    except Exception:
                        if setting_name == "Hosts": # If decryption fails and setting is Hosts
                            results[setting_name] = encrypted_value.split(',') # Split by comma
                        else:
                            results[setting_name] = encrypted_value # Store original value
                else:
                    if setting_name == "Hosts": 
                        results[setting_name] = encrypted_value.split(',') # Split by comma
                    else:
                        results[setting_name] = encrypted_value # Store original value
            except Exception:
                results[setting_name] = "Decryption failed" # On error, note decryption failure

        return results # Return the decrypted results



class DecryptPayload:
    SPL_XCLIENT = "<Xwormmm>"

    @staticmethod
    def main():
        exe_path = sys.argv[1] if len(sys.argv) > 1 else None # Get path from command line argument
        if exe_path is None: # No path provided
            print("Usage: python decrypt_payload.py <xworm_client_path>")
            return
        
        print("Loading Assembly...\n") 
        results = DecryptPayloadUtils.extract(exe_path) # Decrypt the payload
        print(json.dumps(results, indent=4)) # Print results as JSON

        with open(f"decrypted_payload_{int(time.time())}.json", "w") as f: # Save results to file
            json.dump(results, f, indent=4)
        

if __name__ == "__main__":
    DecryptPayload.main() # Run the main function