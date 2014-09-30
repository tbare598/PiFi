'''
Author:       Thomas Bare                                      	
Date:         Summer 2014                                       	
Class:        CSC464                                        	
Filename:     AudioLibrary.py                                 	
Description:  This file is for the AudioLibrary.Library class
'''


import AudioFile
import os
from os.path import basename
from os.path import splitext


###############################################################################
##AudioLibrary Variables
	
#Constants
TITLE = 'title'
ARTIST = 'artist'
ALBUM = 'album'
TRACKNUMBER = 'tracknumber'
GENRE = 'genre'
ALBUMART = 'albumart'
	
##End AudioLibrary Variables
###############################################################################	





	
class Library(object):
	
	###########################################################################
	##AudioLibrary.Library Variables
	
	audioLib = []
	
	##AudioLibrary.Library Variables End
	###########################################################################
	
	
	
	
	###########################################################################
	##File Loading Functions
	
	'''                                                           	
	Function:   loadAudioFromDir
	Parameters: path - This is the place to load the songs from. 
						If the default is used, then it will search the
						library directory, inside the current directory.
	Return:     None.                                           	
	Purpose:    Looks inside the path given to load the songs from the
					there, into audioLib.
	'''
	def loadAudioFromDir(self, path = ""):
		if(path == ""):
			path = os.getcwd() + '\\Library'
		
		#This loop gets the absolute location of all the files in the
		#library folder
		for root, dirs, files in os.walk(path):
			for f in files:
				filename = os.path.join(root, f)
				if filename.endswith('.mp3'):
					#Creates an audio file for the file
					self.audioLib.append(AudioFile.AudioFile(filename))
	

	'''                                                           	
	Function:   loadMoreAudioFiles
	Parameters: path - This is the place to load the songs from. 
	Return:     None.                                           	
	Purpose:    Looks inside the path given to load the songs from the
					there, into audioLib. The difference between this 
	'''
	def loadMoreAudioFiles(self, path):
		#This loop gets the absolute location of all the files in the 
		#library folder
		for root, dirs, files in os.walk(path):
			for f in files:
				filename = os.path.join(root, f)
				if filename.endswith('.mp3'):
					#Creates an audio file for the file
					self.audioLib.append(AudioFile.AudioFile(filename))
					
	
	'''                                                           	
	Function:   
	Parameters: paths - this is a list of all the paths to audio files
						that should be loaded.
	Return:     None.                                           	
	Purpose:    Load the audio files that are given. 
	'''
	def loadAudioFilesByFileLocation(self, paths):
		self.audioLib = []
		
		#Loop through paths list
		for path in paths:
			#Creates an audio file for the file
			self.audioLib.append(AudioFile.AudioFile(path))
	
	
	'''                                                           	
	Function:   clear
	Parameters: None.
	Return:     None.                                           	
	Purpose:    Remove all the audio files from audioLib
	'''
	def clear(self):
		self.audioLib = []
	
	##File Loading Functions End
	###########################################################################

	
	
	###########################################################################
	##Gets
	
	def isPaused(self):
		return self.paused
		
	
	#This returns the file location for all of the audio files in the library
	def getAudioPaths(self):
		paths = []
		
		for audioFile in self.audioLib:
			paths.append(audioFile.getFileLocation())
			
		return paths
		
	
	def getAudioLibrary(self):
		return self.audioLib
		
		
	def getSongInfo(self, index):
		songInfo = {}
		
		songInfo[TITLE] = self.audioLib[index].title()
		songInfo[ARTIST] = self.audioLib[index].artist()
		songInfo[ALBUM] = self.audioLib[index].album()
		songInfo[TRACKNUMBER] = self.audioLib[index].tracknumber()
		songInfo[GENRE] = self.audioLib[index].genre()
		
		return songInfo
	
	##End Gets
	###########################################################################
	
	


	
	
	
	
	
	
	
	
		