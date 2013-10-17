import socket

# Create a Server Socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8089))
serversocket.listen(5)	# Open socket for listening, max of 5 connections

while True:
	connection, address = serversocket.accept()
	buf = connection.recv(64)

	if len(buf) > 0:
		print buf
		break

