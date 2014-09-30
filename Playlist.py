'''
Author:       Thomas Bare                                      	
Date:         Summer 2014                                       	
Class:        CSC464                                        	
Filename:     Playlist.py                                 	
Description:  This file is for the Playlist.PlaylistLibrary class and variables that
			  pertain to this class.
'''


import AudioFile
import AudioLibrary
import os
from os.path import basename
from os.path import splitext


#######################################################################################
##Playlist Functions and variables

PAUSED = 'paused'
INDEX = 'index'


'''                                                      	
Function:   Playlist.compare                                      	
Parameters: oldInfo - old information to be compared.
			newInfo - new information to be compared.
Return:     same - true if both lists are the same.
			differences - dictionary of all the differences
Purpose:    Find differences between one song's information and another's
'''
def compare(oldInfo, newInfo):
	same = True
	differences = {}
	
	keys = oldInfo.keys()
	
	for keyIndex in range(0, len(keys)):
		if( oldInfo[keys[keyIndex]] <> newInfo[keys[keyIndex]]):
			same = False
			differences[keys[keyIndex]] = newInfo[keys[keyIndex]]
			
	return same, differences
	
##End Playlist Functions
#######################################################################################	





	
class PlaylistLibrary(AudioLibrary.Library):
	
	###################################################################################
	##Playlist.Playlist Variables
	
	playlist = [] #This is the list of currently playing titles
	currentTitleIndex = 0
	paused = True
	started = False
	
	##Playlist.Playlist Variables End
	###################################################################################
	

	
	
	###################################################################################
	##File Loading Functions
	
	'''                                                      	
	Function:   loadPlaylistFromAudioLibrary                                      	
	Parameters: audioLib - library to load from
	Return:     None.
	Purpose:    Loads the library given, into this playlist
	'''
	def loadPlaylistFromAudioLibrary(self, audioLib):
		self.playlist = audioLib.getAudioLibrary()
	
	
	##End File Loading Functions
	###################################################################################
	
		
	
	
	
	###################################################################################
	##Playlist info manipulation
		
	'''                                                      	
	Function:   shufflePlaylist                                      	
	Parameters: None.
	Return:     None.
	Purpose:    Changes the order of the audio files in the playlist
	'''	
	def shufflePlaylist(self):
		random.shuffle(self.playlist)
		self.currentTitleIndex = 0
	
	##End Playlist info manipulation
	###################################################################################
	
	
	
	
	
	
	###################################################################################
	##Playlist controls
		
	'''                                                      	
	Function:   prevTitle                                      	
	Parameters: None.
	Return:     None.
	Purpose:    Makes the playlist's current index, the next audio file in the playlist.
				If the playlist is  at the beginning, it will point back to the end.
	'''
	def prevTitle(self):
		if(not self.paused or
			self.playlist[self.currentTitleIndex].ispaused()):
			self.playlist[self.currentTitleIndex].stop()
			
		self.currentTitleIndex -= 1
		
		if(self.currentTitleIndex == -1):
			self.currentTitleIndex = len(self.playlist) - 1
		#If the audio is not paused play the new audio clip
		if(not self.paused):
			self.play()
		
	'''                                                      	
	Function:   nextTitle                                      	
	Parameters: None.
	Return:     None.
	Purpose:    Makes the playlist's current index, the previous audio file in 
				the playlist. If the playlist is  at the end, it will point back 
				to the beginning.
	'''		
	def nextTitle(self):
		if((not self.paused) or
			self.playlist[self.currentTitleIndex].ispaused()):
			self.playlist[self.currentTitleIndex].stop()
			
		self.currentTitleIndex += 1
		
		if(self.currentTitleIndex == len(self.playlist)):
			self.currentTitleIndex = 0
		#If the audio is not paused play the new audio clip
		if(not self.paused):
			self.play()
		
		
	'''                                                      	
	Function:   play                                      	
	Parameters: None.
	Return:     None.
	Purpose:    Makes the audio file that is at the current index play.
	'''		
	def play(self):
		#The song was paused, unpause it, otherwise start from the beginning
		if(self.playlist[self.currentTitleIndex].ispaused()):
			self.playlist[self.currentTitleIndex].unpause()
		elif not self.playlist[self.currentTitleIndex].isplaying():
			self.playlist[self.currentTitleIndex].play()
		
		self.started = True
		self.paused = False
		
		
	'''                                                      	
	Function:   playSongAt                                      	
	Parameters: index - This is the index in the playlist that will be played
	Return:     None.
	Purpose:    Makes the audio file at that index play, and then changes the
				current index to that audio file.
	'''		
	def playSongAt(self, index):
		#This makes sure not to play the song again if it is already playing
		if(self.currentTitleIndex <> index):
			if((not self.paused) or
				self.playlist[self.currentTitleIndex].ispaused()):
				self.playlist[self.currentTitleIndex].stop()
				
			self.currentTitleIndex = index
			self.play()
		else:
			#if (self.playlist[self.currentTitleIndex].ispaused():
			#	self.playlist[self.currentTitleIndex].stop()
				
			if not self.playlist[self.currentTitleIndex].isplaying():
				self.play()
	
		
	'''                                                      	
	Function:   pause                                      	
	Parameters: None.
	Return:     None.
	Purpose:    Pauses the audio file at the current index.
	'''
	def pause(self):
		self.playlist[self.currentTitleIndex].pause()
		self.paused = True
	
	##End Playlist controls
	###################################################################################
	
	
	
	
	
	###################################################################################
	##Gets
	def isPaused(self):
		return self.paused
		
	def hasStarted(self):
		return self.started
		
	def isPlaying(self):
		return self.playlist[self.currentTitleIndex].isplaying()
		
	def getCurrentIndex(self):
		return self.currentTitleIndex
		
	def getCurrentTitle(self):
		return self.playlist[self.currentTitleIndex].title()
		
	def getCurrentArtist(self):
		return self.playlist[self.currentTitleIndex].artist()
		
	def getCurrentAlbum(self):
		return self.playlist[self.currentTitleIndex].album()
		
	def getCurrentTrackNum(self):
		return self.playlist[self.currentTitleIndex].tracknumber()
		
	def getCurrentGenre(self):
		return self.playlist[self.currentTitleIndex].genre()
		
	def getCurrentAlbumArt(self):
		return self.playlist[self.currentTitleIndex].albumart()
		
	def getPlaylist(self):
		return self.playlist
		
	def getCurrentSongInfo(self):
		playlistInfo = {}
		
		playlistInfo[PAUSED] = self.isPaused()
		playlistInfo[INDEX] = self.currentTitleIndex
		
		return playlistInfo
		
	def getCurrentSongInfoDetailed(self):
		playlistInfo = {}
		
		playlistInfo[AudioLibrary.TITLE] = self.getCurrentTitle()
		playlistInfo[AudioLibrary.ARTIST] = self.getCurrentArtist()
		playlistInfo[AudioLibrary.ALBUM] = self.getCurrentAlbum()
		playlistInfo[AudioLibrary.TRACKNUMBER] = self.getCurrentTrackNum()
		playlistInfo[AudioLibrary.GENRE] = self.getCurrentGenre()
		playlistInfo[PAUSED] = self.isPaused()
		playlistInfo[INDEX] = self.currentTitleIndex
		
		return playlistInfo
	
	##End Gets
	###################################################################################
	
	


	
	
	
	
	
	
	
	
		