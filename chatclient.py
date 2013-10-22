import select
import socket
import sys

HOST="localhost"
PORT=5000


# Create a connection to the chat server, return the socket
def open_connection(host, port):
	print "Connecting to %s:%s" % (host, port)
	new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	new_socket.connect((host, port))

	print "Connected"

	return new_socket


# Format a message received from the server
def format_message(msg):
	msg = msg.rstrip()
	fmsg = ""

	if "::" in msg:
		user, data = msg.split('::', 1)
		fmsg = "[%s] %s" % (user, data)
	else:
		fmsg = msg

	return fmsg


def main():
	msg_prefix = ''

	# Connect to chat server
	connection = open_connection(HOST, PORT)

	# Inputs that we'll receive data from
	inputs = [sys.stdin, connection]

	running = True
	while running:
		# Check our inputs for any data received
		inputready, outputready, exceptready = select.select(inputs, [], [])

		for s in inputready:
			if s == connection:
				# Get the message from the socket
				msg = s.recv(1024)

				if msg:
					print format_message(msg.decode())
				else:
					# We've been disconnected
					print "Disconnected"
					running = False

			else:
				# Get input from the command line
				msg = sys.stdin.readline().rstrip()

				if msg == "/quit":
					# Disconnect client
					connection.close()
					running = False
				elif msg != "":
					connection.sendall(msg.encode() + "\n")


if __name__ == "__main__":
	main()
