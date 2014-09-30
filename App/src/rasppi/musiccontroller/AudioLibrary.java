/******************************************************************************
 * 
 * This file is for the AudioLibrary class. It is used for a collection
 * of audio files. 
 * 
 * Date: 	Summer 2014
 * Class:	CSC464 
 * Author   Thomas Bare
 * 
******************************************************************************/

package rasppi.musiccontroller;

import java.util.ArrayList;

public class AudioLibrary {

	ArrayList<AudioFile> audioFiles = new ArrayList<AudioFile>();
	
	public void add(AudioFile newAudioFile) {
		audioFiles.add(newAudioFile);
	}
	

	/**
	 * Function:   addAudio
	 * Parameters: audioString - String of information about audio files.
	 * Return:     None.
	 * Purpose:    This goes through the String for spots separated by ';;;'
	 * 					Between those characters, there should be song 
	 * 					information corresponding to its relative position
	**/
	public void addAudio(String audioString) {
		String title;
		String artist;
		String album;
		int tracknumber;
		String genre;
		//int length;

		
		//indexPrev is going to be the index to start from
		//indexNext is going to be the index of the next ;;; or the end
		//of the string
		int indexPrev = 0;
		int indexNext = audioString.indexOf(";;;");
		
		//Loop that will continue through the string until all the audio
		//information is extracted from the string
		while(audioString.indexOf(";;;", indexPrev) != -1) {
		
			//This looks gross, but it is an effiecient way of going through
			//the string withougt having the overhead of string manipulation
			title = audioString.substring(indexPrev, indexNext);
			indexPrev = indexNext + 3;
			indexNext = audioString.indexOf(";;;", indexPrev);
			
			artist = audioString.substring(indexPrev, indexNext);
			indexPrev = indexNext + 3;
			indexNext = audioString.indexOf(";;;", indexPrev);
			
			album = audioString.substring(indexPrev, indexNext);
			indexPrev = indexNext + 3;
			indexNext = audioString.indexOf(";;;", indexPrev);
			
			tracknumber = Integer.parseInt(audioString.substring(indexPrev, indexNext));
			indexPrev = indexNext + 3;
			indexNext = audioString.indexOf(";;;", indexPrev);
			
			genre = audioString.substring(indexPrev, indexNext);
			indexPrev = indexNext + 3;
			indexNext = audioString.indexOf(";;;", indexPrev);
			/************************************************************************************************
			length = Integer.parseInt(audioString.substring(indexPrev, indexNext));
			indexPrev = indexNext + 3;
			indexNext = audioString.indexOf(";;;", indexPrev);
			************************************************************************************************/
			AudioFile audio = new AudioFile(title, artist, album, tracknumber, genre);/////////////, length);
			
			this.audioFiles.add(audio);
		}
	}
	
	

	/**
	 * Function:   
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    
	**/
	public ArrayList<AudioFile> getAudioFiles() {
		return audioFiles;
	}
	
	
	
}
