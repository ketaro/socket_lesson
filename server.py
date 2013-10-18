import socket

PORT = 8089

# Create a Server Socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', PORT))
serversocket.listen(5)	# Open socket for listening, max of 5 connections

while True:
	print "Server listening on port: ", PORT
	connection, address = serversocket.accept()
	
	running = True
	while running:
		buf = connection.recv(64)

		if len(buf) > 0:
			print buf
	#		break
		else:
			running = False



