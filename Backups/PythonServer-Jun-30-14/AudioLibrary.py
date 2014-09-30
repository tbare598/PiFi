import AudioFile
import os
from os.path import basename
from os.path import splitext


#######################################################################################
#AudioLibrary Functions and Variables
	
#Constants
TITLE = 'title'
ARTIST = 'artist'
ALBUM = 'album'
TRACKNUMBER = 'tracknumber'
GENRE = 'genre'
ALBUMART = 'albumart'
	
#End AudioLibrary Functions and Variables
#######################################################################################	





	
class Library(object):
	
	###################################################################################
	#AudioLibrary.Library Variables
	
	audioLib = []
	
	#AudioLibrary.Library Variables End
	###################################################################################
	
	
	
	
	###################################################################################
	#File Loading Functions
	
	#The variable path is used for the location of the audio files to be loaded. 
	#The default for path is the Library folder inside the current working directory
	def loadAudioFromDir(self, path = ""):
		if(path == ""):
			path = os.getcwd() + '\\Library'
		
		#This loop gets the absolute location of all the files in the library folder
		for root, dirs, files in os.walk(path):
			for f in files:
				filename = os.path.join(root, f)
				if filename.endswith('.mp3'):
					#Creates an audio file for the file
					self.audioLib.append(AudioFile.AudioFile(filename))
	

	#This function is used if you want to add more titles to the library from another directory
	def loadMoreAudioFiles(self, path):
		#This loop gets the absolute location of all the files in the library folder
		for root, dirs, files in os.walk(path):
			for f in files:
				filename = os.path.join(root, f)
				if filename.endswith('.mp3'):
					#Creates an audio file for the file
					self.audioLib.append(AudioFile.AudioFile(filename))
					
	
	#The variable path is used for the location of the audio files to be loaded. 
	#The default for path is the Library folder inside the current working directory
	def loadAudioFilesByFileLocation(self, paths):
		self.audioLib = []
		
		#Loop through paths list
		for path in paths:
			#Creates an audio file for the file
			self.audioLib.append(AudioFile.AudioFile(path))
	
	
	def clear(self):
		self.audioLib = []
	
	#File Loading Functions End
	###################################################################################

	
	
	###################################################################################
	#Gets
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
	
	#End Gets
	###################################################################################
	
	


	
	
	
	
	
	
	
	
		