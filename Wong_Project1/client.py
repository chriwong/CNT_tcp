import pickle
import socket
import sys

class QuestionEntry:
    """Questions have a tag, text, two or more choices, and an answer"""
    def __init__(self):
        self.tag = ''
        self.text = ''
        self.choices = {}   # {letter:choiceText} that way the answer is an index
        self.answer = ''

def getValidInput():
    while True:
        try:
            s = str(input("> "))
            # Error checking for c <n> <a> is just too much...
            if s=='p' or s=='r' or s=='k' or s=='q' or s=='h' or s[0]=='c':
                return s
            else:
                try:
                    if ( (s[0]=='d' or s[0]=='g') and isinstance(int(s[2:]), int) ):
                        return s
                    else:
                        print('Error: incorrect input. Choose pdgrckqh')
                except IndexError as e:
                    print('Error: missing arguments')
                except ValueError as e:
                    print('Error: numeric arguments expected')
        except Exception as e:
            print('Error:', str(e))
            s = None

def main():

    # Need command-line args to connect
    if len(sys.argv) < 2:
        print('Error: missing command-line arguments', file=sys.stderr)
        sys.exit(-1)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to address specified in command-line args
        clientSocket.connect((sys.argv[1], int(sys.argv[2])))
        print('Connected!')


        while True:
            # Get menu choice and send to server
            menuOption = getValidInput()
            clientSocket.send(menuOption.encode())

            if menuOption == 'p':
                # Tag
                tag = input()
                clientSocket.send(tag.encode())

                # Text
                text = ''
                buf = input()
                while buf != '.':
                    text += buf
                    buf = input()
                clientSocket.send(text.encode())

                # Choices
                # Send each choice, including letter, to server
                # When choices are finished, send a period to indicate as such
                choice = input()
                while True:
                    buf = input()
                    while buf != '.':
                        choice += '\n'  # Keep multi-line choices multi-line
                        choice += buf
                        buf = input()
                    clientSocket.send(choice.encode())
                    terminator = input()
                    if terminator == '.':
                        clientSocket.send(terminator.encode())
                        break
                    else:
                        choice = terminator

                # Answer
                a = input()
                clientSocket.send(a.encode())

            elif menuOption[0] == 'd':
                pass
                # Delete

            elif menuOption[0] == 'g':
                pass
                # Get

            elif menuOption == 'r':
                pass
                # Random

            elif menuOption[0] == 'c':
                pass
                # Answer

            elif menuOption == 'k':
                pass
                # Kill server

            elif menuOption == 'q':
                # Kill client only
                clientSocket.close()
                sys.exit(1)

            elif menuOption == 'h':
                pass

            else:
                # This shouldn't be reachable
                print('Error: unhandled input')

    except ConnectionRefusedError as e:
        print('Error: unable to connect', file=sys.stderr)
        sys.exit(-1)
    except Exception as e:
        print('Error:', str(e), file=sys.stderr)
        sys.exit(-1)
        

if __name__ == '__main__':
	main()
