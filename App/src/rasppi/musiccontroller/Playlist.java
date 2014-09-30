/******************************************************************************
 * This file is for the Playlist class. This class inherits AudioLibrary.
 * It is a collection of audio files. It is separated from AudioLibrary
 * beacause AudioLibrary only contains the audio files, but does not
 * manipulate them. The playlist can be manipulated, and songs can be used.
 * 
 * Date: 	Summer 2014
 * Class:	CSC464 
 * Author   Thomas Bare
 * 
******************************************************************************/

package rasppi.musiccontroller;

public class Playlist extends AudioLibrary {

	int currentTitleIndex;
	private boolean paused = true;
	private boolean indexSet = false;

	public Playlist() {
		currentTitleIndex = 0;
	}
	
	
	/////////////////////////////////////////////////////////////////////////////
	//Sets
	
	//Sets the current song to pause
	public void pause() {
		paused = true;
	}
	
	//Unpauses the current song
	public void unpause() {
		paused = false;
	}
	
	public void setIndex(int index) {
		currentTitleIndex = index;
		indexSet = true;
	}
	
	// Sets End
	/////////////////////////////////////////////////////////////////////////////
	
	
	/////////////////////////////////////////////////////////////////////////////
	//Gets At Index
	
	//Get the current title
	public String getTitleAtIndex(int index) {
		
		return audioFiles.get(index).getTitle();
	}
	
	//Get the current artist
	public String getArtistAtIndex(int index) {

		return audioFiles.get(index).getArtist();
	}
	
	//Get the current album
	public String getAlbumAtIndex(int index) {

		return audioFiles.get(index).getAlbum();
	}
	
	public int getIndex() {
		return currentTitleIndex;
	}
	
	// Gets At Index End
	/////////////////////////////////////////////////////////////////////////////
	
	
	
	/////////////////////////////////////////////////////////////////////////////
	//Gets Current Audio File
	
	//Get the current title
	public int getCurrentLength() {
		
		return audioFiles.get(currentTitleIndex).getLength();
	}
	
	//Get the current title
	public String getCurrentTitle() {
		
		return audioFiles.get(currentTitleIndex).getTitle();
	}
	
	//Get the current artist
	public String getCurrentArtist() {

		return audioFiles.get(currentTitleIndex).getArtist();
	}
	
	//Get the current album
	public String getCurrentAlbum() {

		return audioFiles.get(currentTitleIndex).getAlbum();
	}
	
	//Returns true if the current audio file is paused
	public boolean audioPaused() {
		return paused;
	}
	
	// Gets Current Audio File End
	/////////////////////////////////////////////////////////////////////////////

	
	

	/////////////////////////////////////////////////////////////////////////////
	//Gets Other
	
	//Get the current title
	public int getSize() {
		
		return audioFiles.size();
	}
	
	//Get the current title
	public boolean indexIsSet() {
		
		return indexSet;
	}

	//Gets Other End
	/////////////////////////////////////////////////////////////////////////////
	
	
}
