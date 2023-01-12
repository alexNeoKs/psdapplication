# Connect client to client
import threading
import socket
import os
import sys

# Global declare
clients = []
aliases = []
test = []
# mypath = r'C:\Users\Calvert\Desktop\SIT\CSC1010 Computer Networks\Assignment_2\server\image'
# files=("cookie.jpg\neldenring.jpg\neldenring2.jpg")

# function to broadcast message to all clients
def broadcast(message, clientinfo):
    for client in clients:
        if(clientinfo == client):
            continue
        try:
            client.send(message)
        except:
            print("Cannot find user deleting user from list")
            print(client)
            deleteUser(client)

def deleteUser(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    aliases.remove(aliases[index])

# Function to handle clients'connections
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message:
                test = message.split()
                if 'DOWNLOAD' in test:
                    print("User requested download")
                    print(message)
                    print(test)
                    filepath = str(mypath) + '\\' + str(test[3])
                    print(filepath)
                    size = os.path.getsize(filepath)
                    print(size)
                    temp = "DOWNLOAD " + test[3] + " " + str(size)
                    client.sendall(temp.encode('ascii'))
                    # Download function here
                    myfile = open(filepath,'rb')
                    bytes = myfile.read()
                    size = len(bytes)
                    print(size)
                    print(bytes)
                    client.sendall(bytes)

                elif 'LIST' in test:
                    print("User requested list of images")
                    print(message)
                    print(test)
                    # Send over images name
                    client.sendall(files.encode('ascii'))
                else:
                    print(message)
                    broadcast(message.encode('ascii'), client)


        except:
            index = clients.index(client)
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('ascii'),client)
            deleteUser(client)
            break

#function to send chat message to other clients from the server
def client_send():
    while True:
        message = '{} > {}'.format(name, input(''))
        broadcast(message.encode('ascii'),None)

# Main function to receive the clients connection
def receive():
    while True:
        print("waiting for incoming connections...")
        client, address = server.accept()
        print(f'Received connection from {str(address)}')
        print(f'connection Established. Connected from: {str(address)}')
        alias = client.recv(1024).decode('ascii')
        aliases.append(alias)
        clients.append(client)
        broadcast("{} has joined the chat".format(alias).encode('ascii'),None)
        client.send('\nConnected...'.encode('ascii'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        send_thread = threading.Thread(target=client_send)
        send_thread.start()

# Main
if __name__ == "__main__":
    print('Hello, this is CSC1010 Chat Server, please enter the listening port')
    host = socket.gethostbyname(socket.gethostname())
    port = int(input("Enter your desired port number: "))
    print("Server IP and Port is : " + str(host) + " " + str(port))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen()
    name =input("Enter name: ")
    receive()

