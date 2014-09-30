/******************************************************************************
 * 
 * This file is for the AudioFile class, that keeps the information and
 * functions for all the audio files.
 * 
 * Date: 	Summer 2014
 * Class:	CSC464 
 * Author   Thomas Bare
 * 
******************************************************************************/

package rasppi.musiccontroller;

public class AudioFile {
	
	private String title;
	private String artist;
	private String album;
	private int tracknumber;
	private String genre;
	//private Image albumart;
	private int length;

	public AudioFile() {
		title = "";
		artist = "";
		album = "";
		tracknumber = -1;
		genre = "";
		//private Image albumart = null;
		length = -1;
		
	}

	public AudioFile(String initTitle,
					 String initArtist,
					 String initAlbum,
					 int initTracknumber,
					 String initGenre//////////////////////////,
					 ){/////////////////////////////int initLength) {
		title = initTitle;
		artist = initArtist;
		album = initAlbum;
		tracknumber = initTracknumber;
		genre = initGenre;
		//private Image albumart = initAlbumArt;
		////////////////////////////////////////////length = initLength;
	}

	public AudioFile(AudioFile initAudioFile) {
		title = initAudioFile.title;
		artist = initAudioFile.artist;
		album = initAudioFile.album;
		tracknumber = initAudioFile.tracknumber;
		genre = initAudioFile.genre;
		//private Image albumart = initAudioFile.albumart;
	}
	

	/////////////////////////////////////////////////////////////////////////////
	//Sets
	
	public void setLength(int newLength) {
		this.length = newLength;
	}
	
	public void setTitle(String newTitle) {
		this.title = newTitle;
	}
	
	public void setArtist(String newArtist) {
		this.artist = newArtist;
	}
	
	public void setAlbum(String newAlbum) {
		this.album = newAlbum;
	}
	
	public void setTracknumber(int newTracknumber) {
		this.tracknumber = newTracknumber;
	}
	
	public void setGenre(String newGenre) {
		this.genre = newGenre;
	}

	//End Sets
	/////////////////////////////////////////////////////////////////////////////
	
	
	/////////////////////////////////////////////////////////////////////////////
	//Gets
	
	public int getLength() {
		return length;
	}
	
	public String getTitle() {
		return title;
	}
	
	public String getArtist() {
		return artist;
	}
	
	public String getAlbum() {
		return album;
	}
	
	public int getTracknumber() {
		return tracknumber;
	}
	
	public String getGenre() {
		return genre;
	}

	//End Gets
	/////////////////////////////////////////////////////////////////////////////
}
