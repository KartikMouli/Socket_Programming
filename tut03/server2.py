import socket
import threading
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
    print("Usage: python server2.py <server_ip> <port_number>")
    sys.exit()


# configure the logger
logging.basicConfig(filename='server2.log', level=logging.DEBUG)


# input of port and host from user cmd
PORT = int(sys.argv[2])
HOST = sys.argv[1]


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    logging.info("Connected by %s",addr)
    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            print(f"Client using port {addr[1]} sent message: {data}")
            logging.info("Client using port %s sent message: %s",addr[1],data)
            result = evaluate_expression(data)
            print(f"Sending reply: {result}")
            logging.info("Sending reply: %s",result)
            conn.sendall(result.encode())
        except:
            conn.sendall(
                "Error occurred while processing your request".encode())
    conn.close()
    print(f"Connection closed by {addr}")
    logging.info("Connection closed by %s",addr)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server started on {HOST}:{PORT}")
    logging.info("Server started on %s:%s",HOST,PORT)
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
