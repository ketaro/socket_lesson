import select
import socket
import sys


def main():
	msg_prefix = ''

	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	connection.connect(('localhost', 5000))

	print "Connected to server"

	inputs = [sys.stdin, connection]

	running = True
	while running:
		inputready, outputready, exceptready = select.select(inputs, [], [])

		for s in inputready:
			if s == connection:
				msg = s.recv(1024)

				if not msg:
					print "Disconnected"
					running = False
				else:
					msg = msg.decode().rstrip()

					if "::" in msg:
						user, data = msg.split('::', 1)
						print "[%s] %s" % (user, data)

					else:
						print "%s" % msg

			else:
				msg = sys.stdin.readline().rstrip()

				if msg == "/quit":
					# Disconnect client
					connection.close()
					running = False
				elif msg != "":
					connection.sendall(msg.encode() + "\n")




if __name__ == "__main__":
	main()
