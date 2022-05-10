import socket
import threading

nickname = input("Choose Your Nickname:\n")
if nickname == 'admin':
    password = input("Enter Password for Admin:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

stop_thread = False


def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection is Refused !! Wrong Password")
                        stop_thread = True

                elif next_message == 'BAN':
                    print('Connection Refused due to Ban')
                    client.close()
                    stop_thread = True
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
        if message[len(nickname) + 2:].startswith('/whisper'):
            client.send(f'WHISPER {message[len(nickname) + 2 + 9:]}'.encode('ascii'))
        else:
            pass
        if message[len(nickname) + 2:].startswith('#'):
            if nickname == 'admin':
                if message[len(nickname) + 2:].startswith('#kick'):

                    client.send(f'KICK {message[len(nickname) + 2 + 6:]}'.encode('ascii'))
                elif message[len(nickname) + 2:].startswith('#ban'):

                    client.send(f'BAN {message[len(nickname) + 2 + 5:]}'.encode('ascii'))
            else:
                print("Commands can be executed by Admins only !!")
        else:
            client.send(message.encode('ascii'))

# ПОЧЕМУ Я ИГРАЮ В РУЛЕТКУ?!
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()