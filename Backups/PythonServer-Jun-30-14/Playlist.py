import AudioFile
import AudioLibrary
import os
from os.path import basename
from os.path import splitext


#######################################################################################
#Playlist Functions and variables

PAUSED = 'paused'


#Gets a library with playlist info, and compares that to the playlist associated
#with 'self'. If they are different, it will return False and the differences
def compare(oldInfo, newInfo):
	same = True
	differences = {}
	
	if( oldInfo[AudioLibrary.TITLE] <> newInfo[AudioLibrary.TITLE]):
		same = False
		differences[AudioLibrary.TITLE] = newInfo[AudioLibrary.TITLE]
	
	if( oldInfo[AudioLibrary.ARTIST] <> newInfo[AudioLibrary.ARTIST]):
		same = False
		differences[AudioLibrary.ARTIST] = newInfo[AudioLibrary.ARTIST]
	
	if( oldInfo[AudioLibrary.ALBUM] <> newInfo[AudioLibrary.ALBUM]):
		same = False
		differences[AudioLibrary.ALBUM] = newInfo[AudioLibrary.ALBUM]
		#Needs the new album art as well
		#differences[ALBUMART] = newInfo[ALBUMART]
	
	if( oldInfo[AudioLibrary.TRACKNUMBER] <> newInfo[AudioLibrary.TRACKNUMBER]):
		same = False
		differences[AudioLibrary.TRACKNUMBER] = newInfo[AudioLibrary.TRACKNUMBER]
	
	if( oldInfo[AudioLibrary.GENRE] <> newInfo[AudioLibrary.GENRE]):
		same = False
		differences[AudioLibrary.GENRE] = newInfo[AudioLibrary.GENRE]
	
	if( oldInfo[PAUSED] <> newInfo[PAUSED]):
		same = False
		differences[PAUSED] = newInfo[PAUSED]
	
	return same, differences
	
#End Playlist Functions
#######################################################################################	





	
class PlaylistLibrary(AudioLibrary.Library):
	
	###################################################################################
	#Playlist.Playlist Variables
	
	playlist = [] #This is the list of currently playing titles
	currentTitleIndex = 0
	paused = True
	
	#Playlist.Playlist Variables End
	###################################################################################
	

	
	
	###################################################################################
	#File Loading Functions
	
	def loadPlaylistFromAudioLibrary(self, audioLib):
		self.playlist = audioLib.getAudioLibrary()
	
	
	#End File Loading Functions
	###################################################################################
	
		
	
	
	
	###################################################################################
	#Playlist info manipulation
		
	def shufflePlaylist(self):
		random.shuffle(self.playlist)
		self.currentTitleIndex = 0
	
	#End Playlist info manipulation
	###################################################################################
	
	
	
	
	
	
	###################################################################################
	#Playlist controls
	
	def prevTitle(self):
		if(not self.paused):
			self.playlist[self.currentTitleIndex].stop()
			
		self.currentTitleIndex -= 1
		
		if(self.currentTitleIndex == -1):
			self.currentTitleIndex = len(self.playlist) - 1
		#If the audio is not paused play the new audio clip
		if(not self.paused):
			self.play()
			
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
		
			
	def play(self):
		#The song was paused, unpause it, otherwise start from the beginning
		if(self.playlist[self.currentTitleIndex].ispaused() ):
			self.playlist[self.currentTitleIndex].unpause()
		else:
			self.playlist[self.currentTitleIndex].play()
			
		self.paused = False
			
	def pause(self):
		self.playlist[self.currentTitleIndex].pause()
		self.paused = True
	
	#End Playlist controls
	###################################################################################
	
	
	
	
	
	###################################################################################
	#Gets
	def isPaused(self):
		return self.paused
		
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
		
		playlistInfo[AudioLibrary.TITLE] = self.getCurrentTitle()
		playlistInfo[AudioLibrary.ARTIST] = self.getCurrentArtist()
		playlistInfo[AudioLibrary.ALBUM] = self.getCurrentAlbum()
		playlistInfo[AudioLibrary.TRACKNUMBER] = self.getCurrentTrackNum()
		playlistInfo[AudioLibrary.GENRE] = self.getCurrentGenre()
		playlistInfo[PAUSED] = self.isPaused()
		
		return playlistInfo
	
	#End Gets
	###################################################################################
	
	


	
	
	
	
	
	
	
	
		