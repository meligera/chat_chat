import threading
import socket

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
    client.send(message.encode('utf-8'))


def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('utf-8').startswith('TELL'):
                name_to_whisper = msg.decode('utf-8')
                words = name_to_whisper.split(' ', 3)
                print(words)
                name = words[2]
                mes = words[3]
                full_mes = words[1] + " whispers: " + mes
                whisper(full_mes, name)
            elif msg.decode('utf-8').startswith('LIST'):
                client.send(f'Users in chatroom: {nicknames}'.encode('utf-8'))
            elif msg.decode('utf-8').startswith('HELP'):
                client.send('''
/tell       Send a private message to somebody (/tell user message)
/list       Display users in chat
                '''.encode('utf-8'))
            else:
                broadcast(message)

        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(f'{nickname} has left the Chat!'.encode('utf-8'))
                nicknames.remove(nickname)
                break


def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} has joined the Chat'.encode('utf-8'))
        client.send('Connected to the Server!'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def whisper(message, name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_whisper = clients[name_index]
        send(message, client_to_whisper)
        print(message)
    else:
        pass


print('Server is Listening ...')
recieve()
