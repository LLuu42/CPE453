

public class Process
{
	private int runtime;
	private int arrivalTime;

	public Process(int runtime, int arrivalTime)
	{
		this.runtime = runtime;
		this.arrivalTime = arrivalTime;
	}

	public int get_runtime()
	{
		return this.runtime;
	}

	public int get_arrivalTime()
	{
		return this.arrivalTime;
	}
}