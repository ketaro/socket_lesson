#Socket To Me[*](http://www.youtube.com/watch?v=w0gYhuUzx8Q)
You've been working with network applications for a little while now.  You've written a couple Flask applications and have noticed that they don't run like the previous things we've written.  Instead of running some code and exiting, when we run the Flask app, it sits there...listening...waiting for something (a web browser) to connect to it.

Flask has taken care of all the details of how that works -- all you've had to do was invoke it.  In this exercise, we're going to dive a little bit into how to make a network application and how to get two python programs to talk to each other over a network.

##May I be of Service?
The word "server" is often overloaded to mean many different things, but for our purposes, a server is something that listens for a request and returns ("serves") a result.  We refer to the side making the request as the "client" and the side serving the request as the "server".   When accessing a web page, your web browser is the "client" and your flask application has been acting as the web "server".


##Exchanging Data
So what does it mean to write a "network" application.  We've said we want our application to "talk" to another over a network, but when we say "talk", we really just mean exchanging data.

You've already written some programs that can receive data from outside the program you've written.  You've written programs that use the open() command to exchange data with a file on your local file system.  The open() function returns what's called a "File Object", or what other languages might call a "handle" to the file.  You've then used the read() or readline() functions with that file object to get data from the file and write() to send data to the file.

You've also written programs that get data from the keyboard.  Unlike reading from a file, your program had to wait for the user to enter data on the keyboard (using readline()) before taking that input and doing something with it.

When working with network connections, we can draw some parallels to what you've already worked with.  Instead of opening a local file, we'll want to create a connection to another machine.   The server end listens for an incoming connection on a "socket".  We can call the connection from our client to the server the "socket connection".  Python (and the operation system) will handle all the hard work of making the connections happen, we'll just get a Socket Object back that we can use to do the data exchanging.  We'll be using the [socket](http://docs.python.org/2/library/socket.html) library.

##Writing a Client

Previously, to read from a file, we might have written something like this:

	# Open a File
	f = open('myfile.txt', 'r')
	# Read in first line
	line = f.readline()
  
In our file example, we needed to know the name of the file we wanted to open (which we passed to the open() function).  With our socket we need to know two pieces of information:

* Where the server we want to connect to lives (it's "address")
* Which port on the server we want to connect to (which outlet we want to plug our socket connection into)

To read from a socket connection, we'll first have to import the socket module (import socket), then we can open a connection like below.  Port numbers can be between 0 and 65535 (2^16).  We've picked the port 5555 for our chat application.  The number isn't necessarily important, what's important is that both the client and server speak on the same port number.  Servers listening on ports less than 1024 need to have root (super user) permissions.

	import socket
	
	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	my_socket.connect(("localhost", 5555))
	
Create a new file and run the code above.  However, when we run, we'll get an error:

	socket.error: [Errno 111] Connection refused

That's because we've told our application to connect to a server listening on port 5555 on the local machine ("localhost" always points to the machine you're on) and there's nothing currently listening on the port.  We need to run a server!

Clone this repository and in another terminal window run the chatserver.py application.

	$ python chatserver.py

You should see the following message:

	Listening on :5555

Leave that running and now run the connection code again from another terminal window.  This time the program should just exit without an error.  On the server window you should see that the server detected an incomming connection and then immediatly disconnected:

	Incoming Connection
	client disconnecting

Just like with our file handle, it's good practice to call .close() on our socket when we're done with it.  Add this to the end of your program:

	my_socket.close()


### Receive Some Data

Making a connection is fine and all, but not very interesting by itself.  The server might be trying to tell us something!  Let's try and receive what it's sending us.  With our file, we could use readline() to get a line of text.  For our Socket, we need to specify how much data we'd like receive at a time.  Networks usually break up data before sending it over the wire.  The Socket library will handle all of that for us, but chances our we haven't received all the data yet, so we usually write our network application to take this into account and read the chunks of data as they come in.

For now, just add the following before your .close() command:

	data = my_socket.recv(1024)
	
	print "received:\n%s" %  data

Run your client application again and you should now see a message welcoming you to the Hackbright Chat Server:

	received: 
	-------------------------------------
	Welcome to the Hackbright Chat Server
	-------------------------------------
	Please enter your screen name:


### Bi-Directional Sockets: They Go Both Ways

If we notice the last line of the output we received from the server, it was asking us to enter a screen name.  Just as we received data from the server socket, the server was also expecting our client to send the server some data.  Our socket connection can be bi-directional -- meaning we can both send and receive data over the same connection.

To send data to the server, there are two methods of the socket class we could use: .send() and .sendall().  See the [docs](http://docs.python.org/2/library/socket.html#socket.socket.send) for more details on the differences, but for this exercise we'll want to use .sendall() which will send all the data we give it.

Now alter your program so it does the following:

* Receive 1024 bytes from the socket and displays them
* Get a line of input from the user (keyboard) using sys.stdin
* Send that input to the server socket
* Receive another 1024 bytes from the socket and display

If everything worked, you should see the server asking for a name.  After you enter a name you should see a message saying you logged in.

On the server window you have open, you should see 

	Incoming Connection
	None -> FoofusTheCat logged in
	client disconnecting


### Let's Chat

What we've written so far works...kinda...  It at least sends some data back and forth.  We could maybe put the code we've written in a loop to keep exchanging data back and forth, but that still wouldn't be ideal... we'd only see new messages from the server after we send a message (and we wouldn't be able to send a message until we receive a message).  Not ideal.

So we know how to wait for data from one input source (we've already done that), but how do we wait for data that could come from two different places (our server socket and the keyboard)?  How do we know which one is ready and needs to be handled?

Python gives us another module that makes that easy, it's called "[select](http://docs.python.org/2/library/select.html#select.select)".  If we give it a list of sources (our socket and our keyboard (aka sys.stdin)), it will tell us if any of those sources have data ready to be read.

So before we call my_socket.recv() or sys.stdin.readline(), we can call select.select() which will wait until data is ready to be read.  When data is available, the connection that's ready will be returned.

So now we could write something along the lines of:

	running = True
	while running:
		inputready, outputready, exceptready = select.select([my_socket], [], [])
		
		for s in inputready:
			msg = s.recv(1024)
			
			if msg:
				print msg
			else:
				print "Disconnected from server!"
				running = False

So when the server has something new to send us, we can display it on the screen.  The select.select() function takes three lists of arguments for input:

* A list to check if they're available for reading
* A list to check if they're available for writing
* A list to check if they have an exception

For our exercise, we only care about reading, so we'll just send empty lists for the other arguments.

You may have noticed another thing that was added in that example -- If select says our socket is ready to receive data but recv() doesn't return any data, it probably means our socket has been disconnected.

Another great thing about select.select() -- we can treat our keyboard input (sys.stdin) like we do a socket and it will let us know when a user has enter new data on the keyboard.

Update the code you've written to also listen for input from sys.stdin, only when we get data from that input source, we want to send it to our server socket.

* Add sys.stdin to the list of sockets to listen if they're available for reading
* Make sure you're checking for what connection type was returned (for inputready)
* If inputready is stdin, read a line of text from the input and send it to the server socket
* If inputready is our server socket (my_socket), receive the data and display it on the screen
* Open a 3rd terminal window and run another copy of your chat client.  Can you send a message and see it in the other client window?

## Extra Credit

If you get everything above working, you should have a basic chat server running.  If you notice, our chat server will display any messages coming from other users by prefixing the message with the user name and "::" as a seperator.

* Clean up the code to break out sections into functions
** a main() function for our main program
** open_connection(host, port) that returns a new socket connection
** format_message(message) - Format any messages returned from our server.  If the message has a username, format the output so it looks like:  [username] Message
** If the user enters '/quit' it should exit the program
