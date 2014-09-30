/******************************************************************************
 * 
 * This file is for the MusicController class. The MusicController
 * is used for sending commands to the server, and then telling
 * the UI about any updates. This class inherits Thread
 * so that it can be run inside a thread.
 * 
 * Date: 	Summer 2014
 * Class:	CSC464 
 * Author   Thomas Bare
 * 
******************************************************************************/

package rasppi.musiccontroller;


import java.util.Timer;
import java.util.TimerTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;

public class MusicController extends Thread {

	//Server Info
	private ClientSockets clientSock;
	private String serverIP =  "localhost";

	private boolean pausePlayBtnSet = false;
	private Playlist playlist = new Playlist();
	private AudioLibrary audioLib = new AudioLibrary(); //Implement library browsing later
	
	//Handler for the UI so that we can send it messages
	private Handler uiHandler;
	

	//Makes a timer to go off every tenth of a second to refresh the screen
	private Timer updateTimer = new Timer();
	private int timerStartTime = 100;
	private int timerInterval = 100;
	private int timeElasped = 0;
	

	///////////////////////////////////////////////////////////////////////////
	//Constructors
	
	public MusicController(String initServerIP) {
		
		serverIP = initServerIP;
	}

	
	public MusicController(String initIP, Handler initUIHandler) {
		serverIP = initIP;
		uiHandler = initUIHandler;
	}
	
	//Constructors End
	///////////////////////////////////////////////////////////////////////////
	
	
	/**
	 * Function:   run
	 * Parameters: None.
	 * Return:     None
	 * Purpose:    This is what happens when this thread is started
	*/
	@Override
	public void run() {
		connectToServer();
		
		updateMusicServerInfo();
	}
	

	/**
	 * Function:   connectToServer
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    Connects the sockets to server
	**/
	private void connectToServer() {
		
        clientSock = new ClientSockets(serverIP);
        clientSock.start(); 
	}
	

	

	/**
	 * Function:   connectToServer
	 * Parameters: ip - the IP address of the server to connect to.
	 * Return:     None.
	 * Purpose:    Connects the sockets to server at specified IP address
	**/
	public void connectToServer(String ip) {

		serverIP = ip;
        clientSock = new ClientSockets(ip);
        clientSock.start(); 
	}
	
	


	/**
	 * Function:   disconnectFromServer
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    Closes the sockets that connect the controller to the 
	 * 					server, and stops updating title info
	**/
	public void disconnectFromServer() throws InterruptedException  {
		stopUpdating();
		clientSock.closeConnection();
		clientSock.join();
	}
	
	

	/**
	 * Function:   getServerInfo
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    Gets any messages in the server's message queue.
	**/
	public void getServerInfo() {
		
		String msgFromServer = clientSock.readLine();
		
		//Loop as long as there are messages left from the server
		 while(!msgFromServer.equals("")) {

			checkServerMsg(msgFromServer.trim());
			
			msgFromServer = clientSock.readLine();
		}
		
	}
	
	

	/**
	 * Function:   updateMusicServerInfo
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    This function is used to continually update the music
	 * 		 			controller's information pertaining to the music server
	**/
	public void updateMusicServerInfo() {

		//This is a timer that will keep going off until the function stopUpdating() is called.
		updateTimer.scheduleAtFixedRate(new TimerTask() {
			@Override
			public void run() {

				//Each time the timer goes off, it will get info from the server
				getServerInfo();
				
			}
		},  timerStartTime, timerInterval); 
		
	}
	

	/**
	 * Function:   stopUpdating
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    This function is used to stop the timer in the function updateMusicServerInfo
	 * 					from going off forever.
	**/
	private void stopUpdating() {
		updateTimer.cancel();
		updateTimer.purge();
	}
	
	
	

	/**
	 * Function:   checkServerMsg
	 * Parameters: serverMsg - This is a message that was received from the server
	 * Return:     None.
	 * Purpose:    Takes the message from the server and then finds its meaning of it then
	 * 					updates the MusicContoller variables to reflect any messages from the server
	**/
	public void checkServerMsg(String serverMsg) {

		//String of if statements to find the meaning of the server message
		if(serverMsg.equals("EXIT")) {
			try {
				disconnectFromServer();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		else if(serverMsg.startsWith("CT")) {
			setTitle(serverMsg.substring(2, serverMsg.length()));
		}
		else if(serverMsg.startsWith("AR")) {
			setArtist(serverMsg.substring(2, serverMsg.length()));
		}
		else if(serverMsg.startsWith("AL")) {
			setAlbum(serverMsg.substring(2, serverMsg.length()));
		}
		else if(serverMsg.startsWith("PU")) {
			setPauseState(true);
		}
		else if(serverMsg.startsWith("IX")) {
			setIndex(Integer.parseInt(serverMsg.substring(2, serverMsg.length())));
		}
		else if(serverMsg.startsWith("LN")) {
			setTime(Integer.parseInt(serverMsg.substring(2, serverMsg.length())));
		}
		else if(serverMsg.startsWith("PY")) {
			setPauseState(false);
		}
		else if(serverMsg.startsWith("PL")) {
			setPlaylist(serverMsg.substring(2, serverMsg.length()));
		}
		else {
			System.out.println("Unknown message from server: " + serverMsg);
		}
	}
	

	/**
	 * Function:   setNewInfo
	 * Parameters: oldIndex - this is the index of the AudioFile with the old information
	 * 			   newIndex - this is the index of the AudioFile with the new information
	 * Return:     None.
	 * Purpose:    This compares the information in the AudioFiles to see if the UI
	 * 					information has to be updated.
	**/
	private void setNewInfo(int oldIndex, int newIndex) {

		if( playlist.getTitleAtIndex(oldIndex) != playlist.getTitleAtIndex(newIndex)
				|| !playlist.indexIsSet())
			setTitle(playlist.getTitleAtIndex(newIndex));

		if( playlist.getArtistAtIndex(oldIndex) != playlist.getArtistAtIndex(newIndex)
				|| !playlist.indexIsSet())
			setArtist(playlist.getArtistAtIndex(newIndex));

		if( playlist.getAlbumAtIndex(oldIndex) != playlist.getAlbumAtIndex(newIndex)
				|| !playlist.indexIsSet())
			setAlbum(playlist.getAlbumAtIndex(newIndex));

		
		//if( oldInfo[AudioLibrary.TRACKNUMBER] != newInfo[AudioLibrary.TRACKNUMBER])
		//|| !indexSet)

		
		//if( oldInfo[AudioLibrary.GENRE] != newInfo[AudioLibrary.GENRE])
		//|| !indexSet)

	}
	

	/**
	 * Function:   setStart
	 * Parameters: start - This is the time to start the seek bar at
	 * Return:     None.
	 * Purpose:    Used to set the time on the seek bar.
	**/
	private void setTime(int startTime){

		Message msg = uiHandler.obtainMessage();
		Bundle b = new Bundle();

		b.putString("SeekBarStr", "NotNull");
		b.putInt("SeekBarStart", startTime);
		
		msg.setData(b);
		
		uiHandler.sendMessage(msg);
	}
	

	/**
	 * Function:   setIndex
	 * Parameters: index - This is the new current audio file index.
	 * Return:     None.
	 * Purpose:    Sets the current audio file index.
	**/
	private void setIndex(int index){
		int oldIndex;
		oldIndex = playlist.getIndex();
		
		if(!playlist.indexIsSet()){
			setUIIndex();}
		
		if(oldIndex != index || !playlist.indexIsSet()){
			setNewInfo(oldIndex, index);
			playlist.setIndex(index);
		}
	}
	

	/**
	 * Function:   setUIIndex
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    Sets the song on the GUI, to the current song index.
	**/
	private void setUIIndex(){

		Message msg = uiHandler.obtainMessage();
		Bundle b = new Bundle();

		//This line might be useful in the future
		//b.putInt("Index", index);

		b.putString("IndexStr", "NotNull");
		
		msg.setData(b);
		
		uiHandler.sendMessage(msg);
	}
	

	/**
	 * Function:   setPauseState
	 * Parameters: paused - this is the state of paused the current audio
	 * 						file has.
	 * Return:     None.
	 * Purpose:    Used to set the paused state of the GUI
	**/
	private void setPauseState(Boolean paused){
		
		//Makes sure that this is a new paused state before handling
		if(playlist.audioPaused() != paused 
			|| !pausePlayBtnSet){
			
			if(paused)
				playlist.pause();
			else
				playlist.unpause();
	
			Message msg = uiHandler.obtainMessage();
			Bundle b = new Bundle();
	
			b.putString("PausedStr", "NotNull");
			b.putBoolean("Paused", paused);
			
			msg.setData(b);
			
			uiHandler.sendMessage(msg);
		}
	}
	

	/**
	 * Function:   setTitle
	 * Parameters: title - this is the title to set the GUI to.
	 * Return:     None.
	 * Purpose:    To set the GUI to a title.
	**/
	private void setTitle(String title){

		Message msg = uiHandler.obtainMessage();
		Bundle b = new Bundle();

		b.putString("Title", title);
		
		msg.setData(b);
		
		uiHandler.sendMessage(msg);
	}
	

	/**
	 * Function:   setArtist
	 * Parameters: artist - this is the artist to set the GUI to.
	 * Return:     None.
	 * Purpose:    Set the GUI to an artist.
	**/
	private void setArtist(String artist){

		Message msg = uiHandler.obtainMessage();
		Bundle b = new Bundle();

		b.putString("Artist", artist);
		
		msg.setData(b);
		
		uiHandler.sendMessage(msg);
	}
	

	/**
	 * Function:   setAlbum
	 * Parameters: album - this is the album to set the GUI to.
	 * Return:     None.
	 * Purpose:    Set the GUI to an artist.
	**/
	private void setAlbum(String album){

		Message msg = uiHandler.obtainMessage();
		Bundle b = new Bundle();

		b.putString("Album", album);
		
		msg.setData(b);
		
		uiHandler.sendMessage(msg);
	}
	
	
	

	/**
	 * Function:   setPlaylist
	 * Parameters: songs - this is a string of information for audio files.
	 * Return:     None.
	 * Purpose:    Take a string of information for audio files, then set the
	 * 					playlist to that information.
	**/
	private void setPlaylist(String songs) {
		playlist.addAudio(songs);
		
		Message msg = uiHandler.obtainMessage();
		Bundle b = new Bundle();
		
		for(int i = 0; i < playlist.getSize(); i++)
			b.putString(("Title" + i), playlist.getTitleAtIndex(i));
		
		msg.setData(b);
		
		uiHandler.sendMessage(msg);
		
	}
	
	
	
	///////////////////////////////////////////////////////////////////////////
	//UI Functions
	
	
	//Sends a message to the server of the index to play
	public void selectIndex(int index) {
		if (playlist.indexIsSet())
			clientSock.send("IX" + index);
	}//end selectIndex()
	
	
	//Sends a message to the server to go to the next title
	public void nextTitle() {
		
		clientSock.send("NX");
	}//end nextTitle()
	
	
	//Sends a message to the server to go to the next title
	public void prevTitle() {
		
		clientSock.send("PV");
	}//end nextTitle()
	
	
	public void play() {
		clientSock.send("PY");
	}
	
	
	public void pause() {
		clientSock.send("PU");
	}
	// UI Functions End
	///////////////////////////////////////////////////////////////////////////
	
	

	///////////////////////////////////////////////////////////////////////////
	//Gets
	
	//Get the current index
	public int getMaxTime() {
		
		return playlist.getCurrentLength();
	}
	
	//Get the current index
	public int getTimeElaspsed() {
		
		return playlist.getCurrentLength();
	}
	
	//Get the current index
	public int getIndex() {
		
		return playlist.getIndex();
	}
	
	//Get the current title
	public String getCurrentTitle() {
		
		return playlist.getCurrentTitle();
	}
	
	//Get the current artist
	public String getCurrentArtist() {
		
		return playlist.getCurrentArtist();
	}
	
	//Get the current album
	public String getCurrentAlbum() {
		
		return playlist.getCurrentAlbum();
	}
	
	//Returns the paused state of the playlist
	public boolean audioPaused() {
		return playlist.audioPaused();
	}
	// Gets End
	///////////////////////////////////////////////////////////////////////////


}
