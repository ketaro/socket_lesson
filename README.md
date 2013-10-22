#Socket To Me
You've been working with network applications for a little while now.  You've written a couple Flask applications and have noticed that they don't run like the previous things we've written.  Instead of running some code and exiting, when we run the Flask app, it sits there...listening...waiting for something (a web browser) to connect to it.

Flask has taken care of all the details of how that works -- all you've had to do was invoke it.  In this exercise, we're going to dive a little bit into how to make a network application and how to get two python programs to talk to each other over a network.

#May I be of Service?
The word "server" is often overloaded to mean many different things, but for our purposes, a server is something that listens for a request and returns ("serves") a result.  We refer to the side making the request as the "client" and the side serving the request as the "server".   When accessing a web page, your web browser is the "client" and your flask application has been acting as the web "server".

#Exchanging Data
So what does it mean to write a "network" application.  We've said we want our application to "talk" to another over a network, but when we say "talk", we really just mean exchanging data.

You've already written some programs that can receive data from outside the program you've written.  You've written programs that use the open() command to exchange data between a file on your local file system.  open() returns what's called a "File Object", or what other languages might call a "handle" or "pointer" to the file.  You've then used the read() or readline() functions to get data from the file, write() to send data to the file.

You've also written programs that get data from the keyboard.  Unlike reading from a file, your program had to wait for the user to enter data on the keyboard (using readline()) before taking that input and doing something with it.

When working with network connections, we can draw some parallels to what you've already worked with.  Instead of opening a local file, we'll want to create a connection to another machine.   The server end listens for an incoming connection on a "socket".  We can call the connection from our client to the server the "socket connection".  Python (and the operation system) will handle all the hard work of making the connections happen, we'll just get a Socket Object back that we can use to do the data exchanging.

#Writing a Client

Previously, to read from a file, we might have written something like this:

	# Open a File
	f = open('myfile.txt', 'r')
	# Read in first line
	line = f.readline()
  
In our file example, we needed to know the name of the file we wanted to open (which we passed to the open() function).  With our socket we need to know two pieces of information:

	* Where the server we want to connect to lives (it's "address")
	* Which port on the server we want to connect to (which outlet we want to plug our socket connection into)

To read from a socket connection, we'll first have to import the socket module (import socket), then we can open a connection like this:

	import socket
	
	new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	new_socket.connect(("localhost", 5000))
	
If we run the above code, we'll get an error:

	socket.error: [Errno 111] Connection refused

That's because we've told our application to connect to a server listening on port 5000 on the local machine ("localhost" always points to the machine you're on) and there's nothing currently listening on the port.  We need to run a server!

Clone this repository and in another terminal window run the chatserver.py application.

	$ python chatserver.py

You should see the following message:

	Listening on :5000

Leave that running and now run the connection code again.  This time the program should just exit without an error.  On the server window you should see that the server detected an incomming connection and then immediatly disconnected:

	Incoming Connection
	client disconnecting

Just like with our file handle, it's good practice to call .close() on our socket when we're done with it.  Add this to the end of your program:

	new_socket.close()


## Receive Some Data

Making a connection is fine and all, but not very interesting by itself.  The server might be trying to tell us something!  Let's try and receive what it's sending us.  With our file, we could use readline() to get an line of text.  For our Socket, we need to specify how much data we'd like receive at a time.  Networks usually break up data before sending it over the wire.  The Socket library will handle all of that for us, but chances our we haven't received all the data yet, so we usually write our network application to take this into account and read the chunks of data as they come in.

For now, just add the following before your .close() command:

	data = new_socket.recv(1024)
	
	print "received:\n%s" %  data

Run your client application again and you should now see a message welcoming you to the Hackbright Chat Server:

	received: 
	-------------------------------------
	Welcome to the Hackbright Chat Server
	-------------------------------------
	Please enter your screen name:

