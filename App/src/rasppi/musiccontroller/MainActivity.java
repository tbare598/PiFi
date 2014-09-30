/******************************************************************************
 * 
 * This file is for the MainActivity class. It is the main GUI class for
 * the application. It uses a MusicController to send messages to a server
 * to control the audio on that server. This class extends Activity, so 
 * that it can create a GUI
 * 
 * Date: 	Summer 2014
 * Class:	CSC464 
 * Author   Thomas Bare
 * 
******************************************************************************/

package rasppi.musiccontroller;

import android.app.Activity;
import android.content.res.Configuration;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.SeekBar;
import android.widget.Spinner;
import android.widget.TextView;

public class MainActivity extends Activity {

	
	String serverIP = "";
	MusicController controllerThread;
	MusicController controller;
	Handler sbHandler = new Handler();
	
	//Views
	public static TextView txtCurrentTitle;
	public static TextView txtCurrentArtist;
	public static TextView txtCurrentAlbum;
	static EditText etxtIPAddress;
	public static ImageButton ibtnPausePlay;
	public static Spinner dropdown;
	public static SeekBar sbPlaytime;
	
	private String[] playlistTitles;
	private ArrayAdapter<String> adapter;
	


	
	
	
	//Handles messages from the MusicController thread.
	final Handler controllerHandler = new Handler(Looper.getMainLooper()) {
		@Override
		public void handleMessage(Message outputMessage) {

			//Use these variables to check if the Music Controller thread
			//has sent that information to be updated
			String title, artist, album, pausedStr, indexStr, seekbarStr;
			title = outputMessage.getData().getString("Title");
			artist = outputMessage.getData().getString("Artist");
			album = outputMessage.getData().getString("Album");
			
			//I can test if a string is null, but not int or Boolean
			pausedStr = outputMessage.getData().getString("PausedStr");
			indexStr = outputMessage.getData().getString("IndexStr");
			seekbarStr = outputMessage.getData().getString("SeekBarStr");
			////////////////////////////////seekbarStartStr = outputMessage.getData().getString("SeekBarStartStr");
			
			if(title != null)
				setCurrentTitle(title);
			
			else if(artist != null)
				setCurrentArtist(artist);
			
			else if(album != null)
				setCurrentAlbum(album);
			
			//Checks if the paused button should be updated
			else if(pausedStr != null)
				setPausePlayBtn(outputMessage.getData().getBoolean("Paused"));
			
			
			//Checks to see if the playlist dropdown should be updated
			else if(outputMessage.getData().getString("Title0") != null) {
				
				int i = 0;
				String nextTitle;
				while(true){
					nextTitle = outputMessage.getData().getString("Title" + i);
					if(nextTitle != null)
						addTitleToDropdown(nextTitle);
					else
						break;
					
					i++;
				}
			}
			
			
			//Checks if the the index should be set
			else if(indexStr != null){
				//This next line is here for future use
				//int index = outputMessage.getData().getInt("SetIndex"); 
				setDropdown();
			}
			
		/*	************************************************************************************************
			//Checks if the seekbar should be updated
			else if(seekbarStr != null){
				seekUpdation(outputMessage.getData().getInt("SeekBarStart"));
			}
			
			
			//Checks if the seekbar should be updated
			else if(seekbarStartStr != null){
				seekUpdation();
			}
			*************************************************************************************************/
			
		}
	};
	
	/////////////MusicControllerService controllerService; //I intend to implement Services eventually
														   //need to learn how they work first
	
	

		

	/**
	 * Function:   onCreate
	 * Parameters: savedInstanceState - This is the bundle of information from
	 * 									last time the UI had changed.
	 * Return:     None.
	 * Purpose:    Gets called when the GUI is created
	**/
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		//setContentView(R.layout.activity_main);
		setContentView(R.layout.main);
		
		setUpViews();
		
		//Checks if there is any saved content to load
	    if (savedInstanceState != null) {
	        serverIP = savedInstanceState.getString("serverIP", "");
	        
			etxtIPAddress = (EditText) findViewById(R.id.etxt_ip_address);
			etxtIPAddress.setText(savedInstanceState.getString("etxtIP", ""));
	    }
	    else {
			//This is my server's IP////////////////////Will need to implement a function that will search for open servers
			etxtIPAddress.setText("192.168.0.6");
	    }

		//Start connection with server
		connectToServer();
		
	}


	/**
	 * Function:   setUpViews
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    To do all the sets needed to set up the Views
	**/
	private void setUpViews() {
		txtCurrentTitle = (TextView) findViewById(R.id.txt_current_title);
		txtCurrentArtist = (TextView) findViewById(R.id.txt_current_artist);
		txtCurrentAlbum = (TextView) findViewById(R.id.txt_current_album);
		
		etxtIPAddress = (EditText) findViewById(R.id.etxt_ip_address);
		
		ibtnPausePlay = (ImageButton) findViewById(R.id.ibtn_pause_play);
		
		sbPlaytime = (SeekBar) findViewById(R.id.sb_playtime);
		
		dropdown = (Spinner)findViewById(R.id.dd_playlist);
		playlistTitles = new String[]{};
		adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, playlistTitles);
		dropdown.setAdapter(adapter);
		
		/**
		 * This will be used to validate that the user has inputed a valid IP address
		 *
		etxtIPAddress.addTextChangedListener(new TextWatcher(){

			@Override
			public void afterTextChanged(Editable e) {
				
			}

			@Override
			public void beforeTextChanged(CharSequence arg0, int arg1,
					int arg2, int arg3) {
				//This is here because it has to be implemented
			}

			@Override
			public void onTextChanged(CharSequence arg0, int arg1, int arg2,
					int arg3) {
				//This is here because it has to be implemented
			}
			
		});
		*/
		
	}
	
	

	/**
	 * Function:   connectToServer
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    Starts the MusicController thread, if it isn't already
	 * 					started.
	**/
	private void connectToServer() {
		if(controllerThread != null && !controllerThread.isAlive()){
			try {
				controllerThread.disconnectFromServer();
				controllerThread.join();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}

		

		if(serverIP != ""){
			controllerThread = new MusicController(serverIP, controllerHandler);
			controllerThread.start();
		}
	}
	
	
	
	
	

	
	/*******************************************************************************************
	 * 
	 * View Information Sets
	 * 
	 *******************************************************************************************/

	/**
	 * Function:   setCurrentTitle
	 * Parameters: currTitle - The current title
	 * Return:     None.
	 * Purpose:    Set the title
	**/
	private void setCurrentTitle(String currTitle) {
		//Change title name in view
		txtCurrentTitle = (TextView) findViewById(R.id.txt_current_title);
		if(txtCurrentTitle != null)
			txtCurrentTitle.setText(currTitle);
	}

	/**
	 * Function:   setCurrentArtist
	 * Parameters: currArtist - The current artist
	 * Return:     None.
	 * Purpose:    Set the artist
	**/
	private void setCurrentArtist(String currArtist) {
		//Change artist name in view
		txtCurrentArtist = (TextView) findViewById(R.id.txt_current_artist);
		if(txtCurrentArtist != null)
			txtCurrentArtist.setText(currArtist);
	}
	

	/**
	 * Function:   setCurrentAlbum
	 * Parameters: currAlbum - The current album
	 * Return:     None.
	 * Purpose:    Set the album
	**/
	private void setCurrentAlbum(String currAlbum) {
		//Change album name in view
		txtCurrentAlbum = (TextView) findViewById(R.id.txt_current_album);
		if(txtCurrentAlbum != null)
			txtCurrentAlbum.setText(currAlbum);
	}
	

	/**
	 * Function:   setPausePlayBtn
	 * Parameters: isPaused - The current paused state
	 * Return:     None.
	 * Purpose:    Set the pause/play image to match the paused state
	**/
	private void setPausePlayBtn(boolean isPaused) {
		if(isPaused)
			ibtnPausePlay.setImageResource(R.drawable.play);
		else
			ibtnPausePlay.setImageResource(R.drawable.pause);
	}

	/**
	 * Function:   addTitleToDropdown
	 * Parameters: title - title to be added to the drop down
	 * Return:     None.
	 * Purpose:    add another title to the drop down
	**/
	//TODO:
	////////Might be able to set temp to the head of playlistTitles array instead of iterating
	////////through it. Have to test this.
	private void addTitleToDropdown(String title) {
		String[] temp = new String[playlistTitles.length + 1];
		for(int i = 0; i < playlistTitles.length; i++)
			temp[i] = playlistTitles[i];
		
		temp[playlistTitles.length] = title;
		playlistTitles = temp;
		
	}
	

	/**
	 * Function:   setDropdown
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    Sets the drop down to an arraylist, and sets what to do when
	 * 					an item in the drop down is selected.
	**/
	private void setDropdown(){
			
		adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, playlistTitles);
		dropdown.setAdapter(adapter);
		dropdown.setSelection(controllerThread.getIndex());
		
		
		dropdown.setOnItemSelectedListener(new OnItemSelectedListener() {
			public boolean uiIndexSet = false;
			
		    @Override
		    public void onItemSelected(AdapterView<?> parentView, View selectedItemView, int position, long id) {

		    	if(uiIndexSet)
		    		controllerThread.selectIndex(position);
	    		
		    	uiIndexSet = true; //TODO:////////////Need to figure out where onItemSelected is
	    		/////////////////////////////////being called the first time. and set this
	    		/////////////////////////////////variable true there.
		    }

		    @Override
		    public void onNothingSelected(AdapterView<?> parentView) {
		        // your code here
		    }

		});
		
		
		
		
	}
	
	
/************************************************************************************************
	//These next two are for updating the play time seek bar
	public void seekUpdation() {
		
		sbPlaytime.setMax(controller.getMaxTime());
		
		if(!controller.audioPaused()){
			sbPlaytime.setProgress(controller.getTimeElaspsed());
			sbHandler.postDelayed(run, 1000);
		}
	}
	
	
	public void seekUpdation(int startTime) {

		sbPlaytime.setMax(controller.getMaxTime());
		
		if(!controller.audioPaused()){
			sbPlaytime.setProgress(controller.getTimeElaspsed());
			sbHandler.postDelayed(run, 1000);
		}
	}

	Runnable run = new Runnable() {

		@Override
		public void run() {
			seekUpdation();
		}
	};


	************************************************************************************************/
	
	
	
	
	
	/*******************************************************************************************
	 * 
	 * Button Actions
	 * 
	 *******************************************************************************************/

	public void nextTitle(View v) {
		if(controllerThread != null)
			controllerThread.nextTitle();
	}

	public void prevTitle(View v) {
		if(controllerThread != null)
			controllerThread.prevTitle();
	}

	public void btnPausePlay(View v) {
		if(controllerThread != null){
			if(controllerThread.audioPaused())
				controllerThread.play();
			else 
				controllerThread.pause();
		}
	}

	/**
	 * Function:   btnConnect
	 * Parameters: v - the view affected
	 * Return:     None.
	 * Purpose:    Start the connection with the server.
	**/
	public void btnConnect(View v) {
		//Gets the IP address entered by the user, then call the function  to connect to server
		etxtIPAddress = (EditText) findViewById(R.id.etxt_ip_address);
		if(etxtIPAddress != null)
			serverIP = etxtIPAddress.getText().toString();
		
		connectToServer();
	}
	
	
	
	

	
	/*******************************************************************************************
	 * 
	 * Android Lifecycle Handlers
	 * 
	 *******************************************************************************************/
	
	@Override
	public void onStart() {
		super.onStart();
		
	}
	
	
	
	@Override
	protected void onStop() {
		super.onStop();
	}
	
	
	
	@Override
	protected void onPause() {
		super.onStop();
	}
	
	
	
	@Override
	protected void onDestroy() {
		super.onStop();
		try {
				if(controllerThread != null){
					controllerThread.disconnectFromServer();
					controllerThread.join();
				}
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	
	@Override
	protected void onSaveInstanceState(Bundle outState) {
	    super.onSaveInstanceState(outState);
	    
		etxtIPAddress = (EditText) findViewById(R.id.etxt_ip_address);
	    outState.putString("etxtIP", etxtIPAddress.getText().toString());
	    
	    outState.putString("serverIP", serverIP);
	}

    @Override
    public void onConfigurationChanged(Configuration newConfig) 
    {
        super.onConfigurationChanged(newConfig);

        if(newConfig.orientation == Configuration.ORIENTATION_LANDSCAPE){
        	txtCurrentTitle.setVisibility(View.INVISIBLE);
	    	txtCurrentArtist.setVisibility(View.INVISIBLE);
	    	txtCurrentAlbum.setVisibility(View.INVISIBLE);
	    	dropdown.setVisibility(View.INVISIBLE);
        }
        else if(newConfig.orientation == Configuration.ORIENTATION_PORTRAIT){
        	txtCurrentTitle.setVisibility(View.VISIBLE);
	    	txtCurrentArtist.setVisibility(View.VISIBLE);
	    	txtCurrentAlbum.setVisibility(View.VISIBLE);
	    	dropdown.setVisibility(View.VISIBLE);
        }

    }

}
