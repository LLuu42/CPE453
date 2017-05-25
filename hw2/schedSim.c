#include "schedSim.h"

int main(int argc, char* argv[])
{
	FILE *file;

	file = fopen(argv[1], "r"); //First argument in program = file name
	char *line, *splitLine;
	int runtime, arrivalTime;
	struct process processTable[];

	if(!file)
	{
		/* Check to see if file exists */
		printf("File not found. Program terminating.\n");
		return 1;
	}	

	while(readline(file, &line))
	{
		printf("Line: %s\n", line);

		/* Obtain runtime and arrival times from each line */
		splitLine = strtok(line, " ");
		runtime = atoi(splitLine);
		splitLine = strtok(NULL, " \n");
		arrivalTime = atoi(splitLine);




		printf("Running time: %d\n arrival time: %d\n\n", runtime, arrivalTime);

		free(line);
	} 

	fclose(file);
	return 0;
}

