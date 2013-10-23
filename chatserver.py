import socket
import select
import sys

class Server:
    def __init__(self):
        self.host    = ''
        self.port    = 5555
        self.server  = None
        self.inputs  = []
        self.running = True

    # Open the Main Server Socket
    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            self.server.setblocking(0)

            print "Listening on %s:%s" % (self.host, self.port)

        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    # Handle a new incomming client connection
    def process_new_client(self):
        print "Incoming Connection"
        c = Client(self.server.accept())
        self.inputs.append(c)
        c.send("-------------------------------------\n")
        c.send("Welcome to the Hackbright Chat Server\n")
        c.send("-------------------------------------\n")
        c.send("Please enter your screen name:\n")


    # Process a command received on the local console
    def process_console_command(self, cmd):
        print "console: %s" % cmd

        if (cmd == "quit"):
            self.shutdown()

    # Process a message from a connected client
    def process_client_message(self, client):
        # Message from a client
        data = client.socket.recv(1024)
        if data:
            msg = data.rstrip()     # Remove any line returns
            
            if client.screenname:   
                # This client session has set a screen name
                self.sendall(msg, client.screenname)            # Send message to all the connected clients
            else:
                # The client session has not set a screenname
                # The first message we receive from them should contain the screen name
                #   (limit 12 characters)
                client.screenname = msg[:12]
                self.sendall("%s logged in" % client.screenname)

        else:
            # Close the connection with this client
            client.socket.close()
            self.inputs.remove(client)
            print "client disconnecting"

            if client.screenname:
                self.sendall("%s disconnected" % client.screenname)


    # Send a message to all connected clients
    def sendall(self, data, fromuser=None):
        for c in self.inputs:
            if isinstance(c, Client):
                # Only send a message if the user has "logged in" (we have a username)
                if c.screenname:
                    if fromuser:
                        c.send("::".join([fromuser, data]) + "\n")
                    else:
                        c.send(data + "\n")
            elif c == sys.stdin:
                # Print to the local console
                print "%s -> %s" % (fromuser, data)
    

    # Shutdown the server
    def shutdown(self):
        # Close all the connected clients
        for c in self.inputs:
            if isinstance(c, Client):
                self.inputs.remove(c)
                c.send("Server Shutting Down!\n")
                c.socket.close()

        # Now close the server socket
        if self.server:
            self.server.close()

        # And stop running
        self.running = False


    # Main Server Loop
    def run(self):
        # Input Sources
        self.inputs = [self.server, sys.stdin]

        self.running = True
        while self.running:

            # Check if any of our input sources have data ready for us
            inputready, outputready, exceptready = select.select(self.inputs, [], [])

            for s in inputready:
                if s == self.server:
                    self.process_new_client()

                elif s == sys.stdin:
                    # Handle standard input
                    inp = sys.stdin.readline().rstrip()
                    self.process_console_command(inp)

                elif isinstance(s, Client):
                    # Process a message from a connected client
                    self.process_client_message(s)


        # Shutdown the Server
        self.shutdown()


# Class to keep track of a connected client
class Client:
    def __init__(self, (socket, address)):
        self.socket     = socket
        self.address    = address
        self.size       = 1024

        self.screenname = None

        self.socket.setblocking(0)

    # Pass along the server's fileno() refernce.
    # This lets the Client class pretend to be a socket
    def fileno(self):
        return self.socket.fileno()

     # Send message to Client
    def send(self, data):
        self.socket.send(data)




if __name__ == "__main__":
    # Create our server instance
    s = Server()
    # Start Listening for incomming connections
    s.open_socket()
    # Main loop of our server
    s.run()
