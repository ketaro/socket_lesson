#Socket To Me
You've been working with network applications for a little while now.  You've written a couple Flask applications and have noticed that they don't run like the previous things we've written.  Instead of running some code and exiting, when we run the Flask app, it sits there...listening...waiting for something (a web browser) to connect to it.

Flask has taken care of all the details of how that works -- all you've had to do was invoke it.  In this exercise, we're going to dive a little bit into how to make a network application and how to get two python programs to talk to each other over a network.

#May I be of Service?
The word "server" is often overloaded to mean many different things, but for our purposes, a server is something that listens for a request and returns ("serves") a result.  We refer to the side making the request as the "client" and the side serving the request as the "server".   When accessing a web page, your web browser is the "client" and your flask application has been acting as the web "server".

#Exchanging Data
So what does it mean to write a "network" application.  We've said we want our application to "talk" to another over a network, but when we say "talk", we really just mean exchanging data.

You've already written some programs that can receive data from outside the program you've written.  You've written programs that use the open() command to exchange data between a file on your local file system.  open() returns what's called a "File Object", or what other languages might call a "handle" or "pointer" to the file.  You've then used the read() or readline() functions to get data from the file, write() to send data to the file.

You've also written programs that get data from the keyboard.  Unlike reading from a file, your program had to wait for the user to enter data on the keyboard (using readline()) before taking that input and doing something with it.

When working with network connections, we can draw some parallels to what you've already worked with.  Instead of opening a local file, we'll want to create a connection to another machine.  

