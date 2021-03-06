import mp3play
from mutagen import mp3
#import ID3
from os.path import basename
	
	
#AudioFile Constants that map to mutagen
TITLE = 'TIT2'
ARTIST = 'TPE1'
ALBUM = 'TALB'
TRACKNUMBER = 'TRCK'
GENRE = 'TCON'
ALBUMART = 'APIC:'




#AudioFile inherits AudioClip from mp3play
class AudioFile(mp3play.AudioClip):
	#This is the name of the file
	fileLocation = ""
	#This is the current title time in milliseconds
	timeElapsed = 0
	#Used to get the titles meta data from the file
	titleMeta = mp3.MP3#ID3.ID3
	
	
	
	def __init__(self, filename):
		super(AudioFile, self).__init__(filename)
		self.fileLocation = filename
		self.titleMeta = mp3.MP3(filename)
		
	def getFileLocation(self):
		return self.fileLocation
		
	def timeElapsed(self):
		return self.timeElapsed
		
	def title(self):
		return self.titleMeta.tags[TITLE].text[0]
		
	def artist(self):
		return self.titleMeta.tags[ARTIST].text[0]
		
	def album(self):
		return self.titleMeta.tags[ALBUM].text[0]
		
	def tracknumber(self):
		return self.titleMeta.tags[TRACKNUMBER].text[0]
		
	def genre(self):
		return self.titleMeta.tags[GENRE].text[0]
		
	def albumart(self):
		return self.titleMeta.tags[ALBUMART].data
		
	def toString(self):
		string = (self.titleMeta.tags[TITLE].text[0] + ';;;'
					+ self.titleMeta.tags[ARTIST].text[0] + ';;;'
					+ self.titleMeta.tags[ALBUM].text[0] + ';;;'
					+ self.titleMeta.tags[TRACKNUMBER].text[0] + ';;;'
					+ self.titleMeta.tags[GENRE].text[0] + ';;;')
		return string

