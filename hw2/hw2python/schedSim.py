from __future__ import division
import argparse
import sys

incomingProcesses = {}
processes = []
algorithm = ""
quantum = 1;
num_processes = 0;
count = 0;

# Class contatining all the viable information in order to make process calculations
class Process:

	number = 0; #Process Number (by order of appearance)
	arrivalTime = 0; #Process arrival time
	runTime = 0; #Process runtime
	finishTime = 0;

	waitTime = 0;
	responseTime = 0;
	turnaroundTime = 0;
	checked = False;
	remaining = 0;

	def __init__(self, number, runTime, arrivalTime):
		self.number = number
		self.runTime = runTime
		self.arrivalTime = arrivalTime

		#Process is initiated with all of its time remaining
		self.remaining = runTime 

# Takes in the user-inputted algorithm and quantum and processes it for use in the program.
def processArguments(inputAlg, inputQuantum):

	algorithm = ""
	quantum_num = 0;

	#Set Algorithm
	if inputAlg is None:
		algorithm = "FIFO"
	else: 
		algorithm = inputAlg

	#set Quantum (defaults to 1)
	if inputQuantum is None:
		quantum = 1 #default
	else:
		quantum = inputQuantum

	return(algorithm, inputQuantum)


# Takes in the user input, opens the file, and parses the contents inside.
# Error message is displayed and program quits if the input file is incorrect/missing.
def readFile(arguments):
	global incomingProcesses

	try:
		with open(arguments.inputfile) as file: #attempts to open file
			incomingProcesses = [map(int, line.split()) for line in file] #parses files and stores as jobs

			incomingProcesses = sorted(incomingProcesses, key = lambda x: x[1])
			for x in incomingProcesses:
				print(x)

	except IOError as e:
		print 'Input error detected. Exiting program.'
		sys.exit(0);


# Schedules processes based on the chosen algorithm
def scheduler(algorithm):
	chosenAlgorithm = ''.join(algorithm)

	#Shortest Remaining Job First
	if(chosenAlgorithm == 'SRJN'):
		shortestRemainingJob()

	#Round Robin 
	elif(chosenAlgorithm == 'RR'):
		roundRobin()

	#Default: FIFO
	else: 
		firstInFirstOut()

# Schedules jobs based on Shortest Job First
def shortestRemainingJob():
	#jobs = processes
	time = 0
	counter = 0
	flag = False
	done = False

	#Make sure we keep track of what processes are left/finished
	processesLeft = len(processes)
	finishedProcesses = []

	for x in processes:
		if time == 0:
			time += 1
			x.remaining -= 1

		if x in finishedProcesses:
			continue

		for x1 in processes:
			if x1 in finishedProcesses:
				continue
			if(x.runTime < x1.runTime):
				current = x
			else: 
				current = x1

			time += current.remaining
			current.remaining = 0
			flag = True

			if current.remaining == 0 and flag == True:
				current.waitTime = time - current.runTime - current.arrivalTime
				current.responseTime = current.waitTime + 1
				current.turnaroundTime = time
				printProcessTimes(current)
				finishedProcesses.append(current)

			if(len(finishedProcesses) == len(processes)):
				done = True
			else:
				break

	if(done == True):
		#Calculate average times of processes running
		averageResponseTime = sum([process.responseTime for process in processes]) / len(processes)
		averageTurnaroundTime = sum([process.turnaroundTime for process in processes]) / len(processes)
		averageWaitTime = sum([process.waitTime for process in processes]) / len(processes)

		printAllProcessTimes(averageResponseTime, averageTurnaroundTime, averageWaitTime)


# Schedules jobs based on Round Robin scheduling + specified quantum
# If no quantum is given, default = 1
def roundRobin():
	global quantum, incomingProcesses
	quantumInt = int(quantum[0])

	sortedProcesses = sorted(processes, key = lambda process: process.number) 

	#Begin counting time 
	time = 0;

	#Set variables up for Round Robin
	counter = 0;
	flag = False;

	processesLeft = len(sortedProcesses)

	while processesLeft != 0 :
		for process in sortedProcesses:
			while(process.remaining >0):
				#Schedule a process that has time remaining but will run out before the quantum ends
				if(process.remaining <= quantumInt and process.remaining > 0):
					if(process.checked == False):
						process.waitTime = time - process.arrivalTime
						process.checked = True

					time += process.remaining #Run process(and take up time) only for duration of the process
					process.remaining = 0
					flag = True

				#Schedule a process that has time remaining but will not run out before the quantum ends
				elif(process.remaining > 0):
					if(process.checked == False):
						process.waitTime = time - process.arrivalTime
						process.checked = True
					
					process.remaining -= quantumInt #subtract the quantum amount from time remaining
					time += quantumInt #quantum finishes

				#Process has ended
				if(process.remaining == 0 and flag == True):
					#Update process variables
					processesLeft -= 1
					#process.waitTime = time - process.arrivalTime
					#process.waitTime = process.arrivalTime + quantum #(time - process.runTime - process.arrivalTime) / (process.arrivalTime)
					process.responseTime = process.waitTime - process.arrivalTime +1
					process.turnaroundTime = time - process.arrivalTime	

					#Print out process stats
					printProcessTimes(process)

	#Calculate average times of processes running
	averageResponseTime = sum([process.responseTime for process in sortedProcesses]) / len(sortedProcesses)
	averageTurnaroundTime = sum([process.turnaroundTime for process in sortedProcesses]) / len(sortedProcesses)
	averageWaitTime = sum([process.waitTime for process in sortedProcesses]) / len(sortedProcesses)

	printAllProcessTimes(averageResponseTime, averageTurnaroundTime, averageWaitTime)




# Schedules jobs by order of which they appear
# Default method to use!
def firstInFirstOut():
	global processes
	time = 0 #Start keeping track of time

	#Sort the processes based on process number (Assigned sequentially)
	sortedProcesses = sorted(processes, key = lambda process: process.number)

	for process in sortedProcesses:
		if(time == 0):
			process.waitTime = 0
			process.responseTime = process.waitTime + 1
			process.turnaroundTime = process.runTime

			#update time
			time += process.runTime

		else:
			print(time)
			process.waitTime = time - process.arrivalTime
			process.responseTime = process.waitTime - process.arrivalTime + 1
			process.turnaroundTime = time + process.runTime - process.arrivalTime
			time += process.runTime

	for process in sortedProcesses:
		printProcessTimes(process)

	#Calculate average times of processes running
	averageResponseTime = sum([process.responseTime for process in sortedProcesses]) / len(sortedProcesses)
	averageTurnaroundTime = sum([process.turnaroundTime for process in sortedProcesses]) / len(sortedProcesses)
	averageWaitTime = sum([process.waitTime for process in sortedProcesses]) / len(sortedProcesses)

	printAllProcessTimes(averageResponseTime, averageTurnaroundTime, averageWaitTime)

#Prints all the calculated times of a single process (Formatting specified in lab)
def printProcessTimes(process):
	print('Job: {:3.2f}'.format(process.number) + ' -- '
		+ 'Response: ' + '{:3.2f} '.format(process.responseTime)
		+ 'Turnaround: ' + '{:3.2f} '.format(process.turnaroundTime)
		+ 'Wait: {:3.2f}'.format(process.waitTime))

#Prints the total time of all the processes (Formatting specified in lab)
def printAllProcessTimes(responseTime, turnaroundTime, waitTime):
	print('Average: ' + '-- '
		+ 'Response: {:3.2f} '.format(responseTime)
		+ 'Turnaround: {:3.2f} '.format(turnaroundTime)
		+ 'Wait: {:3.2f}'.format(waitTime))


def main():
	global incomingProcesses, quantum, processes, num_processes, count

	#Reads in user arguments / displays help for user arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('inputfile', help = 'Input file for program to read from')
	parser.add_argument('-p', nargs = 1, help = 'scheduling method to use')
	parser.add_argument('-q', nargs = 1, help = 'quantum value (ignored if not round robin)')

	#parsing arguments and setting Algorithm + Quantum
	arguments = parser.parse_args()

	readFile(arguments)

	algorithm, quantum = processArguments(arguments.p, arguments.q)

	#iterates through incomingProcesses and appends them to the list of processes
	for process in incomingProcesses:
		p = Process(count, process[0], process[1])
		processes.append(p)
		count += 1 


	scheduler(algorithm)



if __name__ == '__main__':
	main()