import socket
import threading

print("""
Welcome to the ChatRoom!
""")
nickname = input("Choose Your Nickname:\n")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

stop_thread = False


def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error Occurred while Connecting')
            client.close()
            break


def write():
    while True:
        if stop_thread:
            break

        message = f'{nickname}: {input("")}'
        if message[len(nickname) + 2:].startswith('/tell'):
            client.send(f'TELL {nickname} {message[len(nickname) + 2 + 6:]}'.encode('utf-8'))
        elif message[len(nickname) + 2:].startswith('/list'):
            client.send(f'LIST {message[len(nickname) + 2 + 6:]}'.encode('utf-8'))
        elif message[len(nickname) + 2:].startswith('/help'):
            client.send(f'HELP {message[len(nickname) + 2 + 6:]}'.encode('utf-8'))
        else:
            client.send(message.encode('utf-8'))


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
