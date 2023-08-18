import socket
import sys

# function to get input from user
def user_input():
    while True:
        data = input("Please enter the message to the server: ")

        if len(data) > 0:
            return data

# function to chech if user wants to continue or not
def cont_program():
    while True:
        answer = input("Do you wish to continue? (Y/N): ")
        if answer.lower() == "y":
            return True
        elif answer.lower() == "n":
            return False

# check if args are correct or not
if len(sys.argv) != 3:
    print("Usage: python client.py <server_ip> <port_number>")
    sys.exit()

# input of port and host from user cmd
PORT = int(sys.argv[2])
HOST = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = user_input()
        s.sendall(data.encode())
        result = s.recv(1024).decode().strip()
        print(f"Server replied: {result}")
        if not cont_program():
            break
    quit()        



