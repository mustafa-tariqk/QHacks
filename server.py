import socket
import text_analysis
# Gets the IP
HOST = socket.gethostname()
PORT = 55555
# Creates a socket object
server=socket.socket()
# Binds the host and port number tupple to socket
server.bind((HOST, PORT))
# Server waits for a connection (1 person)
server.listen(1)
# Accepts a connection with a host and port number
conn,addr=server.accept()
print(addr, "Server has now connected")
print("")
while True:
    # Waits for a message to be inputed
    message=input(str(": "))
    # Encodes message to UTF-8 to send
    message=message.encode("utf-8")
    # Sends message over connection
    conn.send(message)
    print("")
    # Receives a message up to 1024 bytes and assigns to a variable
    incoming_message=conn.recv(1024)
    # Decodes the incoming message from bytes to text
    incoming_message=incoming_message.decode("utf-8")
    # Prints the incoming message
    print("Person 1: ",incoming_message)
    # Runs the code through the text analysis AI to print mood
    print(text_analysis.get_emotion(incoming_message))
    print("")