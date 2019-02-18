import socket
import sys
import pickle

def main():

    if len(sys.argv) < 2:
        print('Error: missing command-line arguments', file=sys.stderr)
        sys.exit(-1)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        clientSocket.connect((sys.argv[1], sys.argv[2]))
        print('Connected!')
                        
        serverWelcome = clientSocket.recv(1024)
        print('The server said: ', serverWelcome.decode())
                        
        clientWelcome = input('Say hello back: ')
        clientSocket.send(clientWelcome.encode())
                        
        print('Closing connection...')
        clientSocket.close()
        
    except ConnectionRefusedError e:
        print('Error: unable to connect', file=sys.stderr)
        sys.exit(-1)
    except Exception as e:
        print('Error:', str(e), file=sys.stderr)
        sys.exit(-1)
        
        

    
print('goodbye')

if __name__ == '__main__':
	main()
