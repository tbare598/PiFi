import java.net.*;
import java.io.*;

public class JavaServer {

	public static void main(String[] args) throws IOException {
        
        int portNumber = 5000;

        try ( 
            ServerSocket serverSocket = new ServerSocket(portNumber);
            Socket clientSocket = serverSocket.accept();
            // Connect the BufferReader to the client's socket
            BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream()));
        ) {
        
			System.out.println("Connection Established");
			
            String inputLine;
			
			//Read in as a string, data sent from client
            inputLine = in.readLine();
            System.out.println(inputLine);

            while (true) {
				inputLine = in.readLine();
				if(inputLine.equals("Q") || inputLine.equals("q")) {
					serverSocket.close();
					clientSocket.close();
					in.close();
					System.out.println("Connection Ended");
				}
				
				else
					System.out.println(inputLine);
				
			}
        } catch (IOException e) {
            System.out.println("Exception caught when trying to listen on port "
                + portNumber + " or listening for a connection");
            System.out.println(e.getMessage());
        }
    }
}