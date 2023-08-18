import socket
import sys
import logging
import threading 

# function to evaluate expression 
def evaluate_expression(expr):
    try:
        return str(eval(expr))
    except:
        return "Invalid input"
    

# configure the logger
logging.basicConfig(filename='server1.log', level=logging.DEBUG)

# check if args are correct
if len(sys.argv) != 3:
    print("Usage: python server1.py <server_ip> <port_number>")
    sys.exit()

# input of port and host from user cmd
PORT = int(sys.argv[2])
HOST = sys.argv[1]


def handle_client(connection, address):
    print('New client connected:', address)
    logging.info('New client connected: %s', address[1])
    with connection:
            while True:
                data = connection.recv(1024).decode().strip()
                if not data:
                    print('Client disconnected:%s', address)
                    logging.info('Client disconnected:', address[1])
                    break
                result=evaluate_expression(data)
                connection.sendall(result.encode())
    print('Client connection closed:', address)
    logging.info('Client connection closed:', address[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print('Server started on', HOST, PORT)
    logging.info('Server started on %s: %s', HOST, PORT)
    while True:
        try:
            connection, address = s.accept()
            # If there is already a connected client, reject this connection with an error message.
            if threading.active_count() > 1:
                print('Server is busy with another client. Rejecting new connection:', address)
                logging.info('Server is busy with another client. Rejecting new connection:%s', address[1])
                connection.sendall(b"Server is busy with another client. Rejecting new connection")
                logging.info("Server is busy with another client. Rejecting new connection")
                connection.close()
                continue
        
            t = threading.Thread(target=handle_client, args=(connection, address))
            t.start()            
        except socket.error as e:
            print('Error accepting connection:', e)
            logging.info('Error accepting connection:%s', e)
            continue
        

