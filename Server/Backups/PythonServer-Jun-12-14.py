import socket
import random
import thread
import Queue
import errno
import time
from collections import namedtuple
from socket import error as socketError

####################################################################
#Server connection settings

# use '' for localhost
host = ''
backlog = 5
size = 1024

#Receiving Socket
receivePort = 5000
serverReceivingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverReceivingSocket.bind((host, receivePort))
serverReceivingSocket.listen(backlog)
serverReceivingSocket.setblocking(0)
serverReceivingSocket.settimeout(1)

#Sending Socket
sendPort = 5001
serverSendingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSendingSocket.bind((host, sendPort))
serverSendingSocket.listen(backlog)


#Can implement namedtuples when the clients require data to be kept about them
ServerInfo = namedtuple('ServerInfo', 'NumOfClients', 'CurrentSong', 'Running')

####################################################################



####################################################################
#Client Info
ClientInfo = namedtuple('IP', 'IDNum', 'Connected')

Clients = []

####################################################################


#Creating a list of Songs to pretend to be playing
songLibrary = ['Kyoto', 'Ice Ice Baby', 'Untouched', 'Whip It', 'Material Girl', 'Zoot Suit Riot']

#Current Client Number
ServerInfo.NumOfClients = 0
#Select a random song to be the current song
ServerInfo.CurrentSong = random.choice(songLibrary)
#Let all the threads know that the server is running
ServerInfo.Running = True

#Queue for output to server's command line
printQueue = Queue.Queue()

#Print the current song
printThis = "Current Song: " + (ServerInfo.CurrentSong)
printQueue.put(printThis)



def AddClient(ClientInfo, RecvSock, SendSock, ServerInfo):
	#Tell the client the current song
	SendSock.send('CS' + ServerInfo.CurrentSong + '\n')
	
	clientCurrentSong = ServerInfo.CurrentSong
	
	numOfTimeouts = 0

	while ServerInfo.Running:
		try:
			#Check if the current song changed, by another thread/client
			if(clientCurrentSong <> ServerInfo.CurrentSong):
				SendSock.send('CS' + ServerInfo.CurrentSong + '\n')
				clientCurrentSong = ServerInfo.CurrentSong
				
			
			#Get input from Client
			data = RecvSock.recv(size)
				
			if data and data <> 'EXIT':
				printQueue.put("Msg from Client " + (str)(ClientInfo.IDNum) + ": " + (str)(data))
			
			if data == 'EXIT':
				break
				
				
			if data.upper() == "NS":
				ServerInfo.CurrentSong = random.choice(songLibrary)
				printQueue.put(ServerInfo.CurrentSong)
				

		except socket.timeout:
			numOfTimeouts += 1
			if numOfTimeouts > 6000:##############################Lower this if we want to disconnect silent connections
				printQueue.put("No response from Client " + (str)(ClientInfo.IDNum) + " for 6000 seconds.")
				break
			pass
			
		except socketError as error:
			if error.errno == errno.ECONNABORTED:
				break
				pass
			else:
				raise
			
	#Happens at the end of the thread
	printQueue.put("Connection with Client " + (str)(ClientInfo.IDNum) + " Ended")
	ServerInfo.NumOfClients -= 1
	SendSock.close()
	RecvSock.close()
			
			
def tellThreadsToClose():
	ServerInfo.Running = False
	
	
def serverCmdOutputHandler():
	#Keep checking if there is stuff to be printed to the Queue
	while ((not printQueue.empty()) or (ServerInfo.Running)):
		if (not printQueue.empty()):
			print printQueue.get()

	
#Make a thread, and give the new client to the thread
printingThread = thread.start_new_thread(serverCmdOutputHandler, ( ));



############################################################This will be a check to see if there is another client that is still connected with the same ip as the 
############################################################client that just connected. If so, get rid of that client 
def checkClientDuplicateConnection(ipAddress):
	x = 0 #Place holder
	return True
	
	
			
#Listener loop
while 1:
	#try statement skips socket timeouts
	try:
	########################################RACE CONDITION:
	#####################################Two clients could possibly have the wrong sockets if they try to connect at the same time
		#When a client connects, accept the connection
		RecvSock, ClientInfo.IP = serverReceivingSocket.accept()
		SendSock, ClientInfo.IP = serverSendingSocket.accept()
		
		
	
		ServerInfo.NumOfClients += 1
		
		#Checks if the client that just connected is a duplicate connection, if so drop the connection
		if checkClientDuplicateConnection(ClientInfo.IP):  ####################This function still has to be implemented
			ClientInfo.IDNum = ServerInfo.NumOfClients
		
			#Putting this in the Queue to be printed:
			printThis = "IP " + (str)(ClientInfo.IP) + ": Client " + (str)(ServerInfo.NumOfClients) + " Connected"
			printQueue.put(printThis)
			
			#Set the socket to not block indefinitely
			RecvSock.setblocking(0)
			RecvSock.settimeout(1)
			
			Clients.append(ClientInfo)
			
			#Make a thread, and give the new client to the thread
			clientThreads = thread.start_new_thread(AddClient, 
												#Cannot pass ClientInfo for this next one, 
												#because it would pass by reference, and
												#the next time someone connects, it will reset
												#the client and connection info
												(Clients[ServerInfo.NumOfClients - 1], 
												RecvSock,
												SendSock,
												ServerInfo, ));
	
	except KeyboardInterrupt:
		ServerInfo.Running = False		
	
	except socket.timeout:
		pass
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	