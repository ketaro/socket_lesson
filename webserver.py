import socket
import re
import os

PORT = 8080

# Create a Server Socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', PORT))
serversocket.listen(5)	# Open socket for listening, max of 5 connections


# Take a request "string"
def process_request(reqdata):
	request_headers = {}

	# Loop through each line and record the request headers
	for line in data.split("\r\n"):
		# If the line contains a colon, it's a header
		if (line.find(':') != -1):
			(key, value) = line.split(": ", 1)
			request_headers[key] = value

		# Maybe it's a GET request...
		elif (line.find("GET") != -1):
			location = re.findall(r'^GET (.*) HTTP/.*', line)
			if len(location):
				request_headers['GET'] = location[0]

	return request_headers

# Get a response
def process_response(request):

	r = "HTTP/1.0 200 OK\n"
	r += "Content-type: text/html\n\n"

	url = request.get('GET', '/index.html')

	r += "You're running: %s<br/>\n" % request.get('User-Agent', 'unknown')
	r += "You asked for: %s<br/>\n" % url

	if os.path.isfile("." + url):
		r += "Here it is: \n"

		f = open("." + url)
		r += f.read()

	return r


while True:
	print "Server listening on port: ", PORT
	connection, address = serversocket.accept()
	
	running = True
	data = ""
	while running:
		buf = connection.recv(1024)

		requestdone = False

		if len(buf) > 0:
			data += buf

			if buf.find("\r\n\r\n") != -1:
				requestdone = True
				print "End of request found!"
			else:
				print "read: '%s'" % buf

			if requestdone:
				# Data should now contain a string of the entire request
				request = process_request(data)

				connection.send(process_response(request));

				# Disconnect our client
				connection.close()
				running = False

		else:
			running = False


