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
####################################################################


#Creating a list of Songs to pretend to be playing
songLibrary = ['Kyoto', 'Ice Ice Baby', 'Untouched', 'Whip It', 'Material Girl', 'Zoot Suit Riot']

#Can implement namedtuples when the clients require data to be kept about them
ServerInfo = namedtuple('ServerInfo', 'NumOfClients', 'CurrentSong', 'Running')
ServerInfo.NumOfClients = 0
#Select a random song to be the current song
ServerInfo.CurrentSong = random.choice(songLibrary)
#Let all the threads know that the server is running
ServerInfo.Running = True

#Queue for communication between threads and main
###commQueue = Queue.Queue()

#Queue for output to server's command line
printQueue = Queue.Queue()

#Print the current song
printThis = "Current Song: " + (ServerInfo.CurrentSong)
printQueue.put(printThis)



def AddClient(serversRecvSocket, serversSendSocket, clientNum, ServerInfo):
	#####Send the client it's client number#####
	
	#Tell the client the current song
	serversSendSocket.send('CS' + ServerInfo.CurrentSong + '\n')
	
	clientCurrentSong = ServerInfo.CurrentSong
	
	numOfTimeouts = 0

	while ServerInfo.Running:
		try:
			#Check if the current song changed
			if(clientCurrentSong <> ServerInfo.CurrentSong):
				serversSendSocket.send('CS' + ServerInfo.CurrentSong + '\n')
				clientCurrentSong = ServerInfo.CurrentSong
				
			
			#Get input from Client
			data = serversRecvSocket.recv(size)
				
			if data and data <> 'EXIT':
				printQueue.put("Msg from Client " + (str)(clientNum) + ": " + (str)(data))
			
			if data == 'EXIT':
				break
				
				
			if data.upper() == "NS":
				ServerInfo.CurrentSong = random.choice(songLibrary)
				printQueue.put(ServerInfo.CurrentSong)
				

		except socket.timeout:
			numOfTimeouts += 1
			if numOfTimeouts > 6000:##############################Lower this if we want to disconnect silent connections
				printQueue.put("No response from Client " + (str)(clientNum) + " for 60 seconds.")
				break
			pass
			
		except socketError as error:
			if error.errno == errno.ECONNABORTED:
				break
				pass
			else:
				raise
			
	#Happens at the end of the thread
	printQueue.put("Connection with Client " + (str)(clientNum) + " Ended")
	ServerInfo.NumOfClients -= 1
	serversSendSocket.close()
	serversRecvSocket.close()

	
def serverCmdOutputHandler():
	#Keep checking if there is stuff to be printed to the Queue
	while ((not printQueue.empty()) or (ServerInfo.Running)):
		if (not printQueue.empty()):
			print printQueue.get()
			
def tellThreadsToClose():
	x = 0 #Place holder. Delete this
	
	
#Make a thread, and give the new client to the thread
printingThread = thread.start_new_thread(serverCmdOutputHandler, ( ));
			
#Listener loop
while 1:
	#try statement skips socket timeouts
	try:
	########################################RACE CONDITION:
	#####################################Two clients could possibly have the wrong sockets if they try to connect at the same time
		#When a client connects, accept the connection
		receivingSocket, address = serverReceivingSocket.accept()
		sendingSocket, address = serverSendingSocket.accept()
	
	
		ServerInfo.NumOfClients += 1
		
		#Putting this in the Queue to be printed:
		printThis = "Client " + (str)(ServerInfo.NumOfClients) + " Connected"
		printQueue.put(printThis)
		
		#Set the socket to not block indefinitely
		receivingSocket.setblocking(0)
		receivingSocket.settimeout(1)
		
		#Make a thread, and give the new client to the thread
		clientThreads = thread.start_new_thread(AddClient, 
											(receivingSocket, 
											sendingSocket, 
											ServerInfo.NumOfClients, 
											ServerInfo, ));
	
	except KeyboardInterrupt:
		ServerInfo.Running = False		
	
	except socket.timeout:
		pass
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	