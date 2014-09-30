/******************************************************************************
 * This file is for the MusicControllerService class. It controls the 
 * threads for this application. It helps to continue the threads when the
 * application is running in the background. This class inherits Service
 * so that it can be control threads.
 * 
 * ******************This will be implemented in the future
 * 
 * Date: 	Summer 2014
 * Class:	CSC464 
 * Author   Thomas Bare
 * 
******************************************************************************/

package rasppi.musiccontroller;

import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.Handler;
import android.os.IBinder;

//////////////////This service will be implemented later on.

public class MusicControllerService extends Service  {

	public static final String NOTIFICATION = "raspi.musiccontroller";
	public static final String TITLE = "title";
	public static final String TODO = "title";
	public static final String NEXTTITLE = "nextsong";
	private Handler uiHandler;
	private boolean isStarted = false;
//	private boolean started = false;
	MusicController controllerThread;
	MusicController controller;
	String serverIP = "192.168.0.7";
	
	//Binder given to MainActiviy
	private final IBinder mBinder = new LocalBinder();


    //This is used to give the MainAcivity access to this service
    public class LocalBinder extends Binder {
    	//This will allow MainActivity to call public functions in MusicControllerService
    	MusicControllerService getService() {
            return MusicControllerService.this;
        }
    }


	@Override
	public IBinder onBind(Intent intent) {
		startController();
		
		return mBinder;
	}
	
	
	
	private void startController() {
		if(!isStarted) {
			controllerThread = new MusicController(serverIP, uiHandler);
			//Start connection with server
			controllerThread.start(); 
				System.out.println("HERE: Start new thread.");
			
			isStarted = true;
		}
	}
	
	
	public void nextTitle() {
		controllerThread.nextTitle();
	}
	
}
