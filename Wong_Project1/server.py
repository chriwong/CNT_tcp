import socket
import sys
import pickle

def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverSocket.bind('', 0)
        serverSocket.listen(1)
        print(serverSocket.getsockname()[1])

        while True:
            connectionSocket, addr = serverSocket.accept()	# serverSocket keeps listening; connectionSocket can now communicate 
            serverWelcome = 'Welcome to the Networking project'
            connectionSocket.send(serverWelcome.encode())
                            
            clientWelcome = connectionSocket.recv(1024)
            print('The client said: ', clientWelcome.decode())
                            
            connectionSocket.close()
            print('Client left...')
            
    except Exception as e:
        print('Error: unable to create server', file=sys.stderr)
        sys.exit(-1)


if __name__ == '__main__':
	main()
