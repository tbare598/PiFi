import socket
import errno
import os
import sys
from mutagen import mp3
from socket import error as socketError


def sendMsg():

	####################################################################
	#Server connection settings

	# use '' for localhost
	host = ''
	backlog = 23423423

	#Sending Socket
	sendPort = 5678
	serverSendingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSendingSocket.bind((host, sendPort))
	serverSendingSocket.listen(backlog)
	####################################################################

	
	
	file = mp3.MP3('a.mp3')
	a = file.tags['APIC:'].data
	b = list(a)
	
	
	try:
	
		sendingSocket, address = serverSendingSocket.accept()
		sendingSocket.send(a)
		
		
		print "Image Sent"
				
				
				
	except KeyboardInterrupt:
		ServerInfo.Running = False		
	
	except socket.timeout:
		pass