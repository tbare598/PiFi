import java.net.*;
import java.io.*;
import java.awt.image.*;
import javax.imageio.ImageIO;

public class ImageReader {

	public static void main(String[] args) throws IOException {
        
        int portNumber = 5678;

        try { 
			//Create a local socket
            Socket clientSocket = new Socket("localhost", portNumber);
			
			//Create a stream that will pull in bytes
			InputStream stream = clientSocket.getInputStream();
			
            // Make a file writer
            OutputStream out = new FileOutputStream("picture.png");
			
			System.out.println("Connection Established");
			
			
			pipe(stream, out);
				
			
			out.flush();
			out.close();
			clientSocket.close();
			
            System.out.println("File Received");
			
			
        } catch (IOException e) {
            System.out.println("Exception caught when trying to listen on port "
                + portNumber + " or listening for a connection");
            System.out.println(e.getMessage());
        }
    }
	
	private static void pipe(InputStream in, OutputStream out) throws IOException
	{
		byte buffer[] = new byte[8192];
		while (true)
		{
			int read = in.read(buffer);
			if (read < 0)
			{
				break;
			}
			out.write(buffer, 0, read);
		}
	}
}