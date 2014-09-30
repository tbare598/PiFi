/******************************************************************************
 * This file is for the ReceivingSocket class. This class is used just
 * for receiving messages from the server.This class inherits Thread
 * so that it can be run inside a thread.
 * 
 * Date: 	Summer 2014
 * Class:	CSC464 
 * Author   Thomas Bare
 * 
******************************************************************************/

package rasppi.musiccontroller;

import java.net.*;
import java.io.*;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class ReceivingSocket extends Thread {

    private static int receivePort;
	private static String serverIP;
	private volatile boolean running = true;
	private static BlockingQueue<String> receivedQueue = new LinkedBlockingQueue<String>();
	
	

	//////////////////////////////////////////////////////////////////
	//Constructors
	
	public ReceivingSocket(int initReceivePort, String initServerIP) {
		receivePort = initReceivePort;
		serverIP = initServerIP;	
	}
	
	//Constructors End
	//////////////////////////////////////////////////////////////////
	
	


	/**
	 * Function:   run
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    This gets called when the thread is started.
	**/
	//When .start() is called on a SendingSockets object, it will start a new thread
	@Override
	public void run() {
		try {
			connect();
			
		} catch (UnknownHostException e) {
			System.out.println("ERROR in ReceivingSocket.java");
	        System.out.println("Exception caught when trying to listen on port "
	                + receivePort + " or listening for a connection");
	            System.out.println(e.getMessage());
		} catch (IOException e) {
			System.out.println("ERROR in ReceivingSocket.java");
	        System.out.println("Exception caught when trying to listen on port "
	                + receivePort + " or listening for a connection");
	            System.out.println(e.getMessage());
		}catch (NullPointerException e) {
			System.out.println("ERROR in ReceivingSocket.java");
	        System.out.println("Exception caught when trying to listen on port "
	                + receivePort + " or listening for a connection");
	        System.out.println("Client may have disconnected or the");
	        System.out.println("connection may have been dropped...");
	        //System.out.println(e.getMessage());
		}
	} 
	
	

	/**
	 * Function:   connect
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    This starts the connection with the server
	**/
	//This connects the socket to the receiving socket
	public void connect() throws UnknownHostException, IOException, NullPointerException{
        Socket clientSocket = new Socket(serverIP, receivePort);
		
		// Connect BufferedReader to Server input
        BufferedReader inputFromServer = new BufferedReader(
            new InputStreamReader(clientSocket.getInputStream()));
    
		System.out.println("Receiving Connection Established");
		
        String inFrmServer;

        while (running) {
			//Read in the next line from the server
			inFrmServer = inputFromServer.readLine();
			receivedQueue.add(inFrmServer);
		}
		
		inputFromServer.close();
		clientSocket.close();			
		
	} 
	

	/**
	 * Function:   closeConnection
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    This tells the connection to stop looping
	**/
	public void closeConnection() {
		running = false;
	}
	

	/**
	 * Function:   getNextMsg
	 * Parameters: None.
	 * Return:     Returns the next message in the queue.
	 * Purpose:    Gets the next message in the queue that was sent 
	 * 					from the server.
	**/
	public String getNextMsg() {
		if(isQueueEmpty())
			return "";
		else
			return receivedQueue.poll();
	}
	
	

	/**
	 * Function:   isQueueEmpty
	 * Parameters: None.
	 * Return:     Returns true if the server message queue is empty
	 * Purpose:    This gets called when the thread is started.
	**/
	public Boolean isQueueEmpty() {
		if (receivedQueue.peek() == null)
			return true; 
		
		return false;
	}
	
	

}
