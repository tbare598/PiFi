/******************************************************************************
 * 
 * This file is for the ClientSockets class. It combines ReveivingSocket
 * and SendingSocket together, and manages messages being sent and received.
 * This class inherits Thread so that it can be run inside a thread.
 * 
 * Date: 	Summer 2014
 * Class:	CSC464 
 * Author   Thomas Bare
 * 
******************************************************************************/

package rasppi.musiccontroller;


import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
	

public class ClientSockets extends Thread {
	
	private static String serverIP;
	private static int sendPort = 5000;
	private static int recvPort = 5001;
	private static SendingSocket sendSock;
	private static ReceivingSocket recvSock;
	private static BlockingQueue<String> receivedQueue = new LinkedBlockingQueue<String>();
	

	//////////////////////////////////////////////////////////////////
	//Constructors
	ClientSockets() {
		serverIP = "192.168.0.7";
	}
	
	ClientSockets(String initIP) {
		serverIP = initIP;
	}
	//Constructors End
	//////////////////////////////////////////////////////////////////
	
	

	/**
	 * Function:   run
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    This function is was it called when the thread starts
	**/
	//When .start() is called on a ClientSockets object, it will start a new thread
	@Override
	public void run() {
		
		connect();
		addServerMsgsToQueue();
		
	}
	

	/**
	 * Function:   
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    
	**/
	public void connect() {
		
		sendSock = new SendingSocket(sendPort, serverIP);
		recvSock = new ReceivingSocket(recvPort, serverIP);
		
		sendSock.start();
		recvSock.start();
	}
	
	

	/**
	 * Function:   addServerMsgsToQueue
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    This add messages from the server to a queue
	 * 					of messages to be handled
	**/
	private void addServerMsgsToQueue() {		
		String msgFromServer = recvSock.getNextMsg();
	
		while(!msgFromServer.equals("")) {
			
			//Adding message to queue
			receivedQueue.add(msgFromServer);
			

			//Prints the server message out
			//Used for debugging
			if(msgFromServer != null && !msgFromServer.isEmpty()) {
			
				if(msgFromServer.equals("EXIT")) {
					try {
						closeConnection();
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					System.out.println("Connection Ended");
				}
				if(msgFromServer.startsWith("CT")) {
					System.out.println("Current Title: " + 
						msgFromServer.substring(2, msgFromServer.length()));
				
				}
				else
					System.out.println(msgFromServer);
			}
			
			msgFromServer = recvSock.getNextMsg();
			
		}
		
	}
	
	
	
	/**
	 * Function:   listenerLoop
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    This function is a loop to listen for messages sent from the server
	**/
	public static void listenerLoop() {
		Boolean cont = true;
		
		//Loop will continue until the server has sent 'EXIT'
		while (cont) {
			
			cont = receiveServerMsgs();
		}
	
	}
	
	

	/**
	 * Function:   receiveServerMsgs
	 * Parameters: None.
	 * Return:     True if the server has not sent "EXIT"
	 * Purpose:    This is used to display server information when not 
	 * 					using a MusicController
	**/
	private static Boolean receiveServerMsgs() {
		String msgFromServer = recvSock.getNextMsg();
			
		if(!msgFromServer.equals("")) {
		
			//Makes sure that the server sent something
			if(msgFromServer != null && !msgFromServer.isEmpty()) {
			
				if(msgFromServer.equals("EXIT")) {
					//closeConnection();
					System.out.println("Connection Ended");
					return false;
				}
				if(msgFromServer.startsWith("CT")) {
					System.out.println("Current Title: " + 
						msgFromServer.substring(2, msgFromServer.length()));
				
				}
				else
					System.out.println(msgFromServer);
			}
		}
		
		return true;
	
	}
	
	
	/**
	 * Function:   closeConnection
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    Closes the connections and threads connected to the server
	**/
	public void closeConnection() throws InterruptedException {
		sendSock.closeConnection(); 
		recvSock.closeConnection();
		
		sendSock.join();
		recvSock.join();
		
	}
	
	

	/**
	 * Function:   send
	 * Parameters: msg - This is the message to send to the server
	 * Return:     None.
	 * Purpose:    Used to send messages to the server
	**/
	public void send(String msg) {
		
		sendSock.addMsgToSendingQueue(msg);
	}
	
	


	/**
	 * Function:   getNextMsg
	 * Parameters: None.
	 * Return:     Returns the next message that was recieved by the server
	 * Purpose:    Gets the next message that was received from the server
	**/
	public String getNextMsg() {
		//This will take all the messages from the recvSock's queue and put
		//them in receivedQueue
		addServerMsgsToQueue();
		
		if(isQueueEmpty())
			return "";
		else
			return receivedQueue.poll();
	}//End getNextMsg()
	
	

	/**
	 * Function:   isQueueEmpty
	 * Parameters: None.
	 * Return:     None.
	 * Purpose:    Checks if there are any messages from the server, that
	 * 				 have not be read yet
	**/
	public Boolean isQueueEmpty() {
		//This will take all the messages from the recvSock's queue and 
		//put them in receivedQueue
		addServerMsgsToQueue();
		
		if (receivedQueue.peek() == null)
			return true; 
		
		return false;
	}//isQueueEmpty()
	
	

	/**
	 * Function:   readLine
	 * Parameters: None.
	 * Return:     The next server message in the queue
	 * Purpose:    Checks the queue for server messages.
	**/
	public String readLine() {
		//This will take all the messages from the recvSock's queue and put
		//them in receivedQueue
		addServerMsgsToQueue();
		
		if(isQueueEmpty())
			return "";
		else
			return (receivedQueue.poll() + '\n');
	}
	
	

	/**
	 * Function:   readLineBlocking
	 * Parameters: None.
	 * Return:     returns the next song in the server message queue
	 * Purpose:    Looks in the queue for a message, and blocks until
	 * 					one is put into the queue
	**/
	public String readLineBlocking() {
		//This will take all the messages from the recvSock's queue and put
		//them in receivedQueue
		addServerMsgsToQueue();
		
		//Blocks until there is something in the queue
		while(isQueueEmpty()){}
		
		return (receivedQueue.poll() + '\n');
	}

}
