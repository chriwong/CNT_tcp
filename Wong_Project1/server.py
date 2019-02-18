import os
import random
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

QuestionBank = {}
QuestionNumber = 0

try:
    if os.stat('questionbank.pickle').st_size != 0:
        with open('questionbank.pickle', 'rb') as file:
            QuestionBank = pickle.load(file)
            file.close()
    else:
        pass

except FileNotFoundError as e:
    print('Creating new question bank in questionbank.pickle')
    a = open('questionbank.pickle', 'wb+')
    a.close()



def main():
    global QuestionBank, QuestionNumber
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Get local address, begin listening, and report port obtained
        serverSocket.bind(('', 0))
        serverSocket.listen(1)
        print(serverSocket.getsockname()[1])

        # Loop to continue accepting connections
        while True:
            connectionSocket, addr = serverSocket.accept()
            print(' ~Got a new connection')

            while True:
                menuOption = connectionSocket.recv(1024).decode()
                print('Menu option:', menuOption)

                if menuOption == 'p':
                    newEntry = QuestionEntry()
                    newEntry.tag = connectionSocket.recv(1024).decode()
                    newEntry.text = connectionSocket.recv(1024).decode()
                    choice = connectionSocket.recv(1024).decode()
                    while choice != '.':
                        newEntry.choices[choice[1]] = choice[4:]
                        choice = connectionSocket.recv(1024).decode()
                    newEntry.answer = connectionSocket.recv(1024).decode()
                    QuestionBank[QuestionNumber] = newEntry
                    QuestionNumber += 1

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
                    # I'm too lazy to send message for confirmation
                    print('Terminating...')
                    sys.exit(1)

                elif menuOption == 'q':
                    print('Client initiated closing connection')
                    break

                elif menuOption == 'h':
                    pass
                    # Help
                    # Server does nothing

                else:
                    # This shouldn't be reachable
                    print('Error: unhandled input')

                printQuestionBank()
                with open('questionbank.pickle', 'wb+') as file:
                    pickle.dump(QuestionBank, file)
                            
            connectionSocket.close()
            print(' ~Closed connection')
            
    except Exception as e:
        print('Error:', str(e), file=sys.stderr)
        sys.exit(-1)

def printQuestionBank():
    global QuestionBank
    for n, q in QuestionBank.items():
        print('~Question ', n, '~', sep='')
        print('Tag: ', q.tag, sep='')
        print('Text: ', q.text, sep='')
        print('Choices:')
        for c, a in q.choices.items():
            print('\t(', c, '): ', a, sep='')
        print('Answer: ', q.answer)


if __name__ == '__main__':
	main()
