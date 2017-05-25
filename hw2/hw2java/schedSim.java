import java.util.*;
import java.lang.*;
import java.io.*;


public class schedSim
{

	private static ArrayList<Process> processes;

	public static void main(String args[]) throws FileNotFoundException
	{
		File file = new File(args[0]);
		Scanner in = new Scanner(file);
		PrintStream userDisplay = new PrintStream(System.out);
		String algoritm = "FIFO";

		try
		{
			algoritm = args[1];
		}
		catch(){};

		while(in.hasNextLine())
		{
			String line = in.nextLine();
			String splitLine[] = line.split(" ");

			Process myProcess = new Process(Integer.parseInt(splitLine[0]), Integer.parseInt(splitLine[1]));

			processes.add(myProcess);
		}

		switch(algoritm)
		{
			case "SRJN":
			{
				userDisplay.println("SJRN");
			}
			case "FIFO":
			{
				userDisplay.println("RR");
			}
			default:
			{
				userDisplay.println("FIFO");
			}
		}


		

	}


}