/******************************************************************************
 * This file is for the SendingSocket class. The SendingSocket class is 
 * used only for sending messages to a server. This class inherits Thread
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

public class SendingSocket extends Thread {

    private static int sendPort;
	private static String serverIP;
	private volatile boolean running = true;
	private static BlockingQueue<String> sendingQueue = new LinkedBlockingQueue<String>();
	

	//////////////////////////////////////////////////////////////////
	//Constructors
	public SendingSocket(int initSendingPort, String initServerIP) {
		sendPort = initSendingPort;
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
	@Override
	public void run() {
		try {
			connect();
		} catch (UnknownHostException e) {
			System.out.println("ERROR in SendingSocket.java");
	        System.out.println("Exception caught when trying to listen on port "
	                + sendPort + " or listening for a connection");
	            System.out.println(e.getMessage());
		} catch (IOException e) {
			System.out.println("ERROR in SendingSocket.java");
	        System.out.println("Exception caught when trying to listen on port "
	                + sendPort + " or listening for a connection");
	            System.out.println(e.getMessage());
		}
	}
	

	/**
	 * Function:   connect
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    This starts the connection with the server
	**/
	public void connect() throws UnknownHostException, IOException{
		
        Socket clientSocket = new Socket(serverIP, sendPort);
		
		//A PrintWriter to the Socket
		PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
		
        // Connect the BufferedReader to the client's command line
        BufferedReader inputUser = new BufferedReader(
			new InputStreamReader(System.in));
        
    
		System.out.println("Sending Connection Established");
		
        
		//Continues until ClientSend is told to stop running
        while (running) {
            
			if(!sendingQueue.isEmpty())
				sendQueuedMsgs(out);
		}
        
		out.print("EXIT");
		out.flush();
		clientSocket.close();
		inputUser.close();

	
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
	 * Function:   addMsgToSendingQueue
	 * Parameters: msg - This is the message to send to the server
	 * Return:     None.
	 * Purpose:    Add a message to the queue to be handle in order
	**/
	public void addMsgToSendingQueue(String msg){
		sendingQueue.add(msg);	
	}
	
	

	/**
	 * Function:   sendQueuedMsgs
	 * Parameters: printWriterOut - This is printer that is connected to
	 * 								the server.
	 * Return:     None.
	 * Purpose:    Gets a message from the queue, then sends it.
	**/
	public void sendQueuedMsgs(PrintWriter printWriterOut) {
		//Continues sending messages while there are still items in the queue
		while(sendingQueue.peek() != null) {
			//Sends the message on the front of the queue
			printWriterOut.print(sendingQueue.poll());
			printWriterOut.flush();
		}
	}
		
    
}
