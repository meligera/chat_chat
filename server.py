import threading
import socket


# broadcast to all users in chat
def broadcast(message):
    for client in clients:
        client.send(message)


# send a private message
def send(message, client):
    client.send(message.encode('utf-8'))


# function that will work with client`s requests or broadcast a message
def handle(client):
    while True:
        try:
            # Two variables are used to make it easier for threading to divide them
            msg = message = client.recv(1024)
            # Checking if a message was a command
            if msg.decode('utf-8').startswith('TELL'):  # Receive a private message
                name_to_whisper = msg.decode('utf-8')
                words = name_to_whisper.split(' ', 3)
                # There are strings that user doesn't see, so we split
                # them: [0] is a command, [1] nickname of sender,
                # [2] is a receiver client, [3] is the rest of the message
                # we don't split it
                print(words)  # Debugging purposes
                name = words[2]
                mes = words[3]
                full_mes = words[1] + " whispers: " + mes  # Creating a full structured message to send
                whisper(full_mes, name)
            elif msg.decode('utf-8').startswith('LIST'):  # Message with a list of nicknames
                client.send(f'Users in chatroom: {nicknames}'.encode('utf-8'))
            elif msg.decode('utf-8').startswith('HELP'):  # Message with a list of available commands
                client.send('''
A list of available commands:
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


#  Function that accept clients and create a separate Thread for each of them
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send('NICK'.encode('utf-8'))  # Auth message
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)  # Adding a nickname to nickname list
        clients.append(client)  # Adding a tech info to client list

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} has joined the Chat'.encode('utf-8'))  # Telling everyone about a new user
        client.send('Connected to the Server!'.encode('utf-8'))  # Confirming message to client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


#  Private message function
def whisper(message, name):
    if name in nicknames:  # Searching a user in nicknames
        name_index = nicknames.index(name)  # Making a link with nickname index
        client_to_whisper = clients[name_index]  # Order of lists are identical, take client's info
        send(message, client_to_whisper)  # Call up a send function
        print(message)  # Debugging purpose


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1995))
    server.listen()
    clients = []  # List for technical information about users
    nicknames = []  # List for nicknames
    try:
        print('Server is listening...')
        recieve()
    except KeyboardInterrupt:
        print('How rude of you\n')
        server.close()
        quit()
