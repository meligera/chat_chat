import threading
import socket
import time

PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', PORT))
server.listen()
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def send(message, client):
    client.send(message.encode('ascii'))


def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('command was refused!'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned by the Admin!')
                else:
                    client.send('Command Refused!'.encode('ascii'))

            elif msg.decode('ascii').startswith('WHISPER'):
                client.send(f'Users in chatroom: {nicknames}\n'.encode('ascii'))
                name_to_whisper = msg.decode('ascii')
                words = name_to_whisper.split(' ', 2)
                client.send(f'List of words you entered: {words}'.encode('ascii'))
                name = words[1]
                mes = words[2]
                whisper(mes, name)
            else:
                broadcast(message)

        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(f'{nickname} has left the Chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break


def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        with open('bans.txt', 'r') as f:
            bans = f.readlines()

        if nickname + '\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the Chat'.encode('ascii'))
        client.send('Connected to the Server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You Were Kicked from Chat !'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked from the server!'.encode('ascii'))


def whisper(message, name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_whisper = clients[name_index]
        client_to_whisper.send('Somebody whispers you\n'.encode('ascii'))
        time.sleep(0.1)
        send(message, client_to_whisper)
        print(client_to_whisper)
        print(message)


print('Server is Listening ...')
recieve()
