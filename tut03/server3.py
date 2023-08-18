import socket
import select
import sys
import logging


# function to evaluate expression 
def evaluate_expression(expr):
    try:
        return str(eval(expr))
    except:
        return "Invalid input"


# check if args are correct
if len(sys.argv) != 3:
    print("Usage: python server1.py <server_ip> <port_number>")
    sys.exit()


# input of port and host from user cmd
PORT = int(sys.argv[2])
HOST = sys.argv[1]
BUFFER_SIZE = 1024

# initialize number of users
numuser = 1

# configure the logger
logging.basicConfig(filename='server3.log', level=logging.DEBUG)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

#create list and array to store clients
sockets_list = [server_socket]
clients = {}

print(f"Server started on {HOST}:{PORT}")
logging.info('Server started on %s: %s', HOST, PORT)


#function to recieve message from client
def receive_message(client_socket):
    try:
        message = client_socket.recv(BUFFER_SIZE).decode().strip()
        return message
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            sockets_list.append(client_socket)
            
            clients[client_socket] = "User" + str(numuser)
            numuser += 1

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]}")
                logging.info("Closed connection from %s",clients[notified_socket])
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                notified_socket.close()
                continue

            user = clients[notified_socket]
            print(f"Received message from {user} : {message}")
            logging.info("Received message from %s : %s",user,message)

            result = evaluate_expression(message)
            notified_socket.sendall(result.encode())

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
