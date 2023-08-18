import select
import socket
import sys
import logging

# Set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# check if args are correct
if len(sys.argv) != 3:
    print("Usage: python server1.py <server_ip> <port_number>")
    sys.exit()


# configure the logger
logging.basicConfig(filename='server4.log', level=logging.DEBUG)

# input of port and host from user cmd
PORT = int(sys.argv[2])
HOST = sys.argv[1]



server_address = (HOST, PORT)
server.bind(server_address)
server.listen()

# List to keep track of clients
clients = [server]


print(f"Server started on {HOST}:{PORT}")
logging.info('Server started on %s: %s', HOST, PORT)

while True:
    # Use select to handle multiple clients
    read_sockets, write_sockets, error_sockets = select.select(clients, [], [])

    for sock in read_sockets:
        # New connection
        if sock == server:
            client_socket, client_address = server.accept()
            clients.append(client_socket)
            print(f"New client connected with port number: {client_address[1]}")
            logging.info("New client connected with port nunmber: %s",client_address[1])
        # Incoming data from client
        else:
            data = sock.recv(1024)
            if data:
                # Echo the data back to the client
                sock.send(data)
                logging.info("data sent:%s",data)
            else:
                # Remove the client socket from the list
                clients.remove(sock)
                logging.info("%s client disconnected",sock)
                sock.close()
