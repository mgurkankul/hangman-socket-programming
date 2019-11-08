from socket import *                                                                                # Mustafa Gürkan Kul
serverName="localhost"                                                                              # 150150040
serverPort=12000

clientSocket=socket(AF_INET,SOCK_STREAM)

clientSocket.connect((serverName,serverPort))                                                   #Connect to the server

while True:
    modifiedMessage=clientSocket.recv(1024)                                                     #Checks the message that comes from server. 
    modifiedMessage = modifiedMessage.decode('utf-8')
    if modifiedMessage=="exit":
        clientSocket.close()
        exit(0)
    elif modifiedMessage == "username:" or modifiedMessage == "password:":                      #If the message is "username:", "password:", "Your turn to play: " or
        message=input(modifiedMessage)                                                          #"Want to play again" send response
        clientSocket.send(message.encode('utf-8'))
    elif modifiedMessage == "Your turn to play: " or modifiedMessage == "Want to play again :":
        message = input(modifiedMessage)
        clientSocket.send(message.encode('utf-8'))  
    else:
        print(modifiedMessage)