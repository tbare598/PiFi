'''	
Author:       Thomas Bare                                      	
Date:         Summer 2014                                       	
Class:        CSC464                                        	
Filename:     PythonServer.py                                 	
Description:  This file works as the code for a audio server. It listens
              to the port specified in receivePort and communicates with 
				 the client connected there. 

'''


import socket
import random
import thread
import Queue
import errno
import time
import sys
import AudioLibrary
import Playlist
from collections import namedtuple
from socket import error as socketError


####################################################################
##Server connection settings

#Using '' for localhost
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

#Lower this if we want to disconnect silent connections
timeoutsTolerated = 6000

#Start dictionary for the ServerInfo
#ServerInfo = {'NumOfClients', 'CurrentTitleIndex', 'Running'}
ServerInfo = {}

##Server connection settings End
####################################################################





#The information for each individual client is kept here
Clients = []

#This is where the music and music info is stored
audioLib = AudioLibrary.Library()
#This is where the playlist info is stored
playlist = Playlist.PlaylistLibrary()

#Current Client Number
ServerInfo['NumOfClients'] = 0
#Let all the threads know that the server is running
ServerInfo['Running'] = True
#Sets the index that the current title is at
ServerInfo['CurrentTitleIndex'] = 0

#Queue for output to server's command line
printQueue = Queue.Queue()

#This thread is used by the threads to control the music
musicControlQueue = Queue.Queue()


'''
                                                           	
Function:    AddClient                                      	
Parameters:  Client     - Includes the a dictionary with information	
							 particular to that client, including:
								Client['IDNum']
								Client['Cont']
								Client['IP']
				RecvSock   - This is the receiving socket for the client
				SendSock   - This is the sending socket for the client
				ServerInfo - This is a pointer to the server information
				audioLib   - This is a pointer to the global audio library.
							 This has not been implemented yet.
				playlist   - This is a pointer to the global playlist
Return:      None.                                           	
Purpose:     Handling the messages sent and received from the clients

'''
def AddClient(Client, RecvSock, SendSock, ServerInfo, audioLib, playlist):
	
	#Get the current playlist information
	currSongInfo = playlist.getCurrentSongInfo()
	
	#Sends all the songs in the playlist to the client
	sendPlaylist(SendSock, playlist)
	
	#Tell the client the current information
	sendUpdates(SendSock, currSongInfo)
	
	numOfTimeouts = 0

	while ServerInfo['Running'] and Client['Cont']:
		try:
			newSongInfo = playlist.getCurrentSongInfo()
			
			same, changes = Playlist.compare(currSongInfo, newSongInfo)
			
			if(not same):
				sendUpdates(SendSock, changes)
				currSongInfo = newSongInfo
			
			#Blocks on client input until 'timeout', so that we can send info to
			#client if anything has changed
			data = RecvSock.recv(size)
				
			if data and data <> 'EXIT':
				printQueue.put("Msg from Client " + (str)(Client['IDNum']) + ": " + (str)(data))
			
			if data == 'EXIT':
				break
			
			#Put the message in the queue for the server to handle it
			musicControlQueue.put(data)
			

		except socket.timeout:
			numOfTimeouts += 1
			if numOfTimeouts > timeoutsTolerated:
				printQueue.put("No response from Client " \
								+ (str)(Client['IDNum']) \
								+ " for " \
								+ (str)(timeoutsTolerated) \
								+ " seconds.")
				break
			pass
			
		except socketError as error:
			if error.errno == errno.ECONNABORTED:
				break
				pass
			else:
				raise
			
	#Happens at the end of the thread
	printQueue.put("Connection with Client " + (str)(Client['IDNum']) + " Ended")
	SendSock.close()
	RecvSock.close()

	
	
	
	
'''                                                         	
Function:    sendPlaylist                                      	
Parameters:  sender   - the sending socket, for sending to the client
				playlist - pointer to the global playlist variable
Return:      None.                                           	
Purpose:     Sends all the information for all the audio files in the 
				playlist to the client.
'''
def sendPlaylist(sender, playlist):
	playlistList = playlist.getPlaylist()
	msg = ""
	
	for audioFile in playlistList:
		msg += audioFile.toString()
	
	sender.send("PL" + msg + '\n')
	
	
	
'''                                                          	
Function:    sendIndex                                      	
Parameters:  sender - the sending socket, for sending to the client
				index  - the index of the current audio file
Return:      None.                                           	
Purpose:     To format the message that will be sent to the client to 
				tell it the index of the current audio file.
'''
def sendIndex(sender, index):
	sender.send("IX" + index + '\n')
	
	
	
	
'''                                                           	
Function:    sendUpdates                                      	
Parameters:  sender  - the sending socket, for sending to the client
				changes - these are all the updates that should be sent
						  to the client
Return:      None.                                           	
Purpose:     Send changes that have happened to the server to the client.
'''
def sendUpdates(sender, changes):
	keys = changes.keys()
	
	for keyIndex in range(0, len(keys)):
		msg = createMsg(keys[keyIndex], changes[keys[keyIndex]])
		sender.send(msg)
		
		#If I am going to send album art, I will need to give the receiver
		#notice, so that they can prepare for the image
		if msg == 'AA':
			sender.send('AA' + '\n')
			sender.send(changes[keys[keyIndex]])

			
	
	
'''                                                           	
Function:    createMsg
Parameters:  playlistInfoType - This is the type of information in
								   playlistInfo.
				playlistInfo	 - This is the information that will sent.
Return:      The message that is formatted to be sent to the client.
Purpose:     Used to formatted a message so that the client can understand
'''		
def createMsg(playlistInfoType, playlistInfo):
	#These if statements are ordered for by the chance they they will return
	#'true' for performance reasons 
	
	if playlistInfoType == Playlist.INDEX:
		msg = 'IX'
	elif playlistInfoType == AudioLibrary.TITLE:
		msg = 'CT'
	elif  playlistInfoType == AudioLibrary.TRACKNUMBER:
		msg = 'TN'
	#If this is true, that means it is paused, if not it is playing
	elif  playlistInfoType == Playlist.PAUSED:
		if(playlistInfo):
			return 'PU' + '\n'
		else:
			return 'PY' + '\n'
	elif  playlistInfoType == AudioLibrary.ARTIST:
		msg = 'AR'
	elif  playlistInfoType == AudioLibrary.ALBUM:
		msg = 'AL'
	elif  playlistInfoType == AudioLibrary.GENRE:
		msg = 'GN'
	
	if  playlistInfoType == AudioLibrary.ALBUMART:
		msg = 'AA'
		return msg
		
	return msg + (str)(playlistInfo) + '\n'


		
		
	
	
	
'''                                                           	
Function:    threadToControllerMsgHandler
Parameters:  None.
Return:      None.                                           	
Purpose:     This is the function that will be in it's own thread, and 
				will control the messages sent from a client to the server
				to affect the playlist.
'''
def threadToControllerMsgHandler():
	#Loads the library from the default folder
	audioLib.loadAudioFromDir()
	#Loads all the titles from the Library into the playlist
	playlist.loadPlaylistFromAudioLibrary(audioLib)

	#Print the current title
	printThis = "Current Title: " + (playlist.getCurrentTitle())
	printQueue.put(printThis)
	
	#Keep checking if there is stuff to be printed to the Queue
	while ((not musicControlQueue.empty()) or (ServerInfo['Running'])):
		if (not musicControlQueue.empty()):
			threadMsgDecipher(musicControlQueue.get())
			
		if (not playlist.isPaused() 
			and not playlist.isPlaying()
			and playlist.hasStarted()):
			playlist.nextTitle()
			

	
#Make a thread, and give the new client to the thread
thread.start_new_thread(threadToControllerMsgHandler, ( ));



	
'''                                                           	
Function:    threadMsgDecipher
Parameters:  msg - This is the message received from the client
Return:      None.                                           	
Purpose:     Takes the message from the client, and figures out what
				to do with it.
'''
def threadMsgDecipher(msg):			
	if msg.upper() == "NX":
		playlist.nextTitle()
		printQueue.put("Current Title: " + playlist.getCurrentTitle())
	
	elif msg.upper() == "PV":
		playlist.prevTitle()
		printQueue.put("Current Title: " + playlist.getCurrentTitle())
	
	elif msg.upper() == "PY":
		playlist.play()
	
	elif msg.upper() == "PU":
		playlist.pause()  
	
	elif msg.upper().startswith("IX"):
		#Gets the substring after IX then uses that for playSongAt()
		playlist.playSongAt((int)(msg[2:]))  
	
	elif len(msg) > 0: 
		printQueue.put("UNKOWN MSG: " + msg) 
	




	
	
'''                                                           	
Function:    tellThreadsToClose
Parameters:  None.
Return:      None.                                           	
Purpose:     Lets all the threads know that they should close.
'''		
def tellThreadsToClose():
	ServerInfo['Running'] = False



	
'''                                                           	
Function:    getClientsIndex
Parameters:  ipAddress - This is the IP address to check against
Return:      Returns the index in Clients that has the same IP address
				as ipAddress, or the length of Clients, because that is
				the index of where ipAddress should go in Clients.
Purpose:     Finds where to put the client with IP address of ipAddress
'''
def getClientsIndex(ipAddress):
	for i in range(0, len(Clients)):
		if(ipAddress == Clients[i]['IP']):
			return i

	return len(Clients)
	
	

	
'''                                                           	
Function:    handleDuplicateConnnection
Parameters:  clientsIndex - index in clients to put the client info
				RecvSock     - receiving socket for the client
				SendSock     - sending socket for the client
				ServerInfo   - pointer to the global variable for ServerInfo
Return:      None.                                           	
Purpose:     Handles the connection of a client has is reconnecting.
'''	
def handleDuplicateConnnection(clientsIndex, RecvSock, SendSock, ServerInfo):
	#This stops the previous thread
	Clients[clientsIndex]['Cont'] = False
	
	#This create a new thread with the previous one's info
	Clients[clientsIndex] = {'IP':Clients[clientsIndex]['IP'],
							 'IDNum':Clients[clientsIndex]['IDNum'],
							 'Cont':True
							}
	
	#Putting this in the Queue to be printed:
	printThis = "IP " \
				+ (str)(Clients[clientsIndex]['IP']) \
				+ ": Client " \
				+ (str)(Clients[clientsIndex]['IDNum']) \
				+ " Reconnected" 
	printQueue.put(printThis)
	
	#Set the socket to not block indefinitely
	RecvSock.setblocking(0)
	RecvSock.settimeout(.25)
	
	#Make a thread, and give the new client to the thread
	thread.start_new_thread(AddClient, 
									(Clients[clientsIndex], 
									RecvSock,
									SendSock,
									ServerInfo, 
									audioLib,
									playlist,
									)
							  )

										

	
'''                                                           	
Function:    handleNewConnection
Parameters:  RecvSock     - receiving socket for the client
				SendSock     - sending socket for the client
				ServerInfo   - pointer to the global variable for ServerInfo
				ip           - the ip address of the new client
Return:      None.                                           	
Purpose:     Handles the connection of a client that has connected for
				the first time.
'''				
def handleNewConnection(RecvSock, SendSock, ServerInfo, ip):
	#temp is created for the sole reason of adding another 
	#dictionary to the end of Clients
	temp = {}
	Clients.append(temp)
	
	#Set up client's info
	Clients[len(Clients) - 1]['IDNum'] = ServerInfo['NumOfClients']
	Clients[len(Clients) - 1]['IP'] = ip
	Clients[len(Clients) - 1]['Cont'] = True

	#Putting this in the Queue to be printed:
	printThis = "IP " \
				+ (str)(ip) \
				+ ": Client " \
				+ (str)(ServerInfo['NumOfClients']) \
				+ " Connected"
	printQueue.put(printThis)
	
	#Set the socket to not block indefinitely
	RecvSock.setblocking(0)
	RecvSock.settimeout(.25)
	
	#Make a thread, and give the new client to the thread
	thread.start_new_thread(AddClient, 
								(Clients[len(Clients) - 1], 
								RecvSock,
								SendSock,
								ServerInfo,
								audioLib,
								playlist, )
							)
	
	
	
	
	

	
'''                                                           	
Function:    serverCmdOutputHandler
Parameters:  None.
Return:      None.                                           	
Purpose:     Handles the output from all of the threads to the 
				command line
'''				
def serverCmdOutputHandler():
	#Keep checking if there is stuff to be printed to the Queue
	while ((not printQueue.empty()) or (ServerInfo['Running'])):
		if (not printQueue.empty()):
			print printQueue.get()

	
#Make a thread, and give the new client to the thread
thread.start_new_thread(serverCmdOutputHandler, ( ));






	
#Loops around, waiting for a client to connect
while 1:
	#try statement skips socket timeouts
	try:
		########################################RACE CONDITION:
		#####################################Two clients could possibly have the wrong sockets if they try to connect at the same time
		#When a client connects, accept the connection
		RecvSock, tempIP = serverReceivingSocket.accept()
		SendSock, tempIP = serverSendingSocket.accept()
		tempIP = tempIP[0]
		
		
		clientsIndex = getClientsIndex(tempIP)
		
		#Checks if the client that just connected is a duplicate 
		#connection, by seeing if the index of the client being 
		#checked is less than the number of clients currently connected
		if clientsIndex == len(Clients): 
			ServerInfo['NumOfClients'] += 1
			handleNewConnection(RecvSock,
								SendSock,
								ServerInfo, 
								tempIP);
		else:
			handleDuplicateConnnection(clientsIndex,
										RecvSock,
										SendSock,
										ServerInfo);
	
	except KeyboardInterrupt:
		ServerInfo['Running'] = False		
	
	except socket.timeout:
		pass
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	