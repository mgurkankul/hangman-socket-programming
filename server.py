from socket import *                                                                                                    # Mustafa Gürkan Kul
import threading                                                                                                        # 150150040
import time
import random

class ThreadedServer():

    def startGame(self, socketList, userList, userNames, wordList):                                      #Function of Hangman game 
        ran = random.randint(0, len(wordList)-1)                                                         #Choosing a random word
        chosenWord = list(map(list, wordList[ran]))
        correctLetter = 0
        gameNotOver = True
        falseGuess = 7
        wrongGuesses=[]
        sendedWord = ""
        for i in range (0,len(wordList[ran])):                                                           #Making an list of "_"
            chosenWord[i] = '_'
        for i in range (0,len(wordList[ran])):
            sendedWord += chosenWord[i] + ' '                                                            #sendedWord is "_ _ _..."
        for addr in socketList:                                                                          #Sending every player the sendedWord
            addr.send(sendedWord.encode('utf-8'))
        while gameNotOver:                                                                               #Game ends if gameNotOver is false
            sendedWord = ""
            turn = 0
            for addr in socketList:
                if not gameNotOver:
                    break
                time.sleep(1)
                message = "Your turn to play: "                                                         #Players get your turn or someone is playing message
                addr.send(message.encode('utf-8'))                                                      #according to their order.
                for port in socketList:
                    if port != addr:
                        message = "Player " + userNames[turn] + " is playing. "
                        port.send(message.encode('utf-8'))
                turn = turn + 1
                guessLetter = addr.recv(1024)
                guessLetter = guessLetter.decode('utf-8').lower()
                if len(guessLetter) > 1:                                                                #If the guess is a word
                    if guessLetter == wordList[ran]:                                                    #If it mathces the chosen word
                        correctLetter = len(wordList[ran])
                        message = guessLetter + " is gueessed and it is true! "
                        gameNotOver = False
                        for addr in socketList:                                                         #Informing players
                            addr.send(message.encode('utf-8'))
                    else:                                                                               #If the guess is wrong
                        falseGuess = falseGuess - 1                                                     
                        wrongGuesses.append(guessLetter)
                        message = guessLetter + " is gueessed but it is wrong! " + str(falseGuess) + " attemps remaining."
                        if falseGuess == 0:
                            gameNotOver = False
                        for addr in socketList:                                                         #Informing players
                            addr.send(message.encode('utf-8'))
                elif guessLetter in wordList[ran]:                                                      #If the guess is a letter and it exist in the word
                    message = guessLetter + " is guessed and it exist in the word! " + str(falseGuess) + " attemps remaining."
                    for addr in socketList:                                                             #Informing players
                        addr.send(message.encode('utf-8'))
                    for j in range (0, len(wordList[ran])):
                        if wordList[ran][j] == guessLetter:
                            chosenWord[j] = guessLetter
                            correctLetter = correctLetter + 1
                    sendedWord = ""
                    for i in range (0,len(wordList[ran])):
                        sendedWord += chosenWord[i] + ' '
                    for addr in socketList:
                        addr.send(sendedWord.encode('utf-8'))
                    if correctLetter == len(wordList[ran]):                                             #If all of the letters have been found, game is over.
                        gameNotOver = False
                else:                                                                                   #If the guess is wrong
                    falseGuess = falseGuess - 1
                    wrongGuesses.append(guessLetter)
                    message = guessLetter + " is gueessed but it is wrong! " + str(falseGuess) + " attemps remaining."
                    if falseGuess == 0:
                        gameNotOver = False
                    for addr in socketList:                                                             #Informing players
                        addr.send(message.encode('utf-8'))
        if correctLetter == len(wordList[ran]):                                                         #If the word is found, sends "You win!" to every player.
            message = "You win!"
        else:
            message = "You lose!"                                                                       
        for addr in socketList:
            addr.send(message.encode('utf-8'))
        player = 0
        toBedeleted =[]
        time.sleep(0.5)
        for addr in socketList:                                                                         #Checks the attandance to the next game.                                                                        
            time.sleep(0.5)
            message = "Want to play again :"
            addr.send(message.encode('utf-8'))
            message = addr.recv(1024)
            message = message.decode('utf-8').lower()
            if message == "yes":                                                                        #If the received message is yes, it continues.                                                                      
                addr.send(("New game is starting. Wait for others.").encode('utf-8'))
            else:
                addr.send(("Good bye!").encode('utf-8'))                                                #If it is no, the informations about the player are deleted.
                time.sleep(0.5)
                for i in range(0, len(socketList)):
                    if addr == socketList[i]:
                        toBedeleted.append(addr)
                del userList[userNames[player]]
                del userNames[player]
            player = player + 1
        while len(toBedeleted) > 0 :                                      
            for i in range(0, len(socketList)):
                if toBedeleted[0] == socketList[i]:
                    del socketList[i]
            del toBedeleted[0]
        self.startGame(socketList, userList, userNames, wordList)
    def __init__(self,serverPort, numberOfPlayer):
        counter = 0
        socketList = []
        userList = {}
        userNames = []
        wordList = ['communication', 'network', 'protocol', 'hangman', 'calculation', 'registration', 'client', 'server', 'status', 'player', 'python', 'message']
        try:
            serverSocket=socket(AF_INET,SOCK_STREAM)
        except:
            print("Socket cannot be created!!!")
            exit(1)
        print("Socket is created...")
        try:
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:
            print("Socket cannot be used!!!")
            exit(1)
        print("Socket is being used...")
        try:
            serverSocket.bind(('',serverPort))
        except:
            print("Binding cannot de done!!!")
            exit(1)
        print("Binding is done...")
        try:
            serverSocket.listen(45)
        except:
            print("Server cannot listen!!!")
            exit(1)
        print("The server is ready to receive")
        while True:
            connectionSocket,addr=serverSocket.accept()
            if numberOfPlayer > counter:                                                                #If there are empty slots, socket is connected.                        
                message = "username:"
                connectionSocket.send(message.encode('utf-8'))
                username = connectionSocket.recv(1024)
                username = username.decode('utf-8').lower()
                if username in userList:                                                                #If it is an existing user, checks password
                    message = "password:"
                    connectionSocket.send(message.encode('utf-8'))
                    password = connectionSocket.recv(1024)
                    password = password.decode('utf-8').lower()
                    if password == userList[username]:
                        counter = counter + 1
                        userNames.append(username)
                        socketList.append(connectionSocket)
                        if numberOfPlayer == counter:
                            self.startGame(self, socketList, userList, userNames, wordList)
                    else:
                        message = "Wrong Password!"
                        connectionSocket.send(message.encode('utf-8'))
                else:                                                                                  #If it does not exist, it adds new user.
                    message = "password:"
                    connectionSocket.send(message.encode('utf-8'))
                    password = connectionSocket.recv(1024)
                    password = password.decode('utf-8').lower()
                    userList[username] = password
                    counter = counter + 1
                    userNames.append(username)
                    socketList.append(connectionSocket)
                    if numberOfPlayer == counter:
                        self.startGame(socketList, userList, userNames, wordList)
            else:
                connectionSocket.close()
            

if __name__=="__main__":
    serverPort=12000
    numberOfPlayer=int(input('How many players there will be? : '), 10)
    ThreadedServer(serverPort, numberOfPlayer)
	