from __future__ import division
import argparse
import sys
import struct
import collections
import UserDict
import os.path




# Simulates Virtual Memory inside of a processor
class VirtualMemory: 

	def __init__(self, replacementAlgorithm, numFrames):
		self.algorithms = {"FIFO": 0, "LRU": 1, "OPT": 2} # Assigns values to each of the algorithms
		self.replacementAlgorithm = replacementAlgorithm

		# Updates frames
		self.numFrames = numFrames
		self.numRequests = 0

		# Updates pages
		self.pageNum = -1
		self.pageRequests = 0
		self.pageMisses = 0

		# Assign replacement algorithms to pages hurr
		if (self.algorithms[replacementAlgorithm] == 0):
			self.pages = FIFOCache(numFrames, {})
		elif (self.algorithms[replacementAlgorithm] == 1):
			self.pages = LRUCache(numFrames)
		elif (self.algorithms[replacementAlgorithm] == 2):
			self.pages = OPTCache(numFrames)

		# Assign tlb values
		self.tlb = FIFOCache(16, {})
		self.tlbRequests = 0
		self.tlbMisses = 0

	# Handle page requests by address
	def handleRequest(self, address):
		self.numRequests += 1 #increment number of addresses
		pageNum, offset = maskAddress(address)
		page = self.getPageTable(pageNum)
		referenceByte = getByteValue(page.frame, offset)
		self.printAddress(address, referenceByte, page.pageNum, page.frame)

	# Handles the page replacement algorithm (Method depending on the algorithm)
	def handleOPT(self, addresses):
		self.pages.initOPT(addresses)
		self.pages.calculateOPT()

	# Returns the page from the page table
	def getPageTable(self, pageNum):	
		self.pageRequests += 1 #Increment number of page requests
		tlbMiss = 0

		page = self.getTlb(pageNum)

		# Account for tlb miss
		if page is None:
			tlbMiss = 1
		else:
			return page

		page = self.pages.getValue(pageNum)

		# Account for page miss
		if page is None and tlbMiss == 1:
			self.pageNum += 1
			self.pageMisses += 1

			frame = readBinFrame(pageNum)
			newPage = Page(self.pageNum, frame)
			self.pages.setValue(pageNum, newPage)
			self.tlb.setValue(pageNum, newPage)

			return newPage

		else:
			return page
	

	# Returns page number and frame in the form of a tuple
	def getTlb(self, page):
		self.tlbRequests += 1
		#checks if page is a miss
		if (self.tlb.getValue(page) is None):
			self.tlbMisses += 1 
		else: 
			return self.tlb.getValue(page)

	# Prints the address
	def printAddress(self, address, num, frameNum, frame):
		#account for sign bit
		if (num > 127):
			num = num - 256
		print("{0}, {1}, {2}, {3}").format(address, num, frameNum, frame.encode("hex").upper())

	# Prints the overall lab-specified stats in a program
	def printStats(self):
		print("Number of Translated Adresses = {0}").format(self.numRequests)
		print("Page Faults = {0}").format(self.pageMisses)
		print("Page Fault Rate = {:3.3f}").format(self.pageMisses / self.numRequests)
		print("TLB Hits = {0}").format(self.tlbRequests - self.tlbMisses)
		print("TLB Misses = {0}").format(self.tlbMisses)
		print("TLB Hit Rate = {:3.3f}").format((self.tlbRequests - self.tlbMisses) / (self.tlbRequests))


# Makes calculations based on FIFO algorithm
class FIFOCache(object, UserDict.DictMixin):

	def __init__(self, numEntries, dic = ( )):
		self.numEntries = numEntries
		self.dictionary = dict(dic)
		self.list = []

	# Returns the FIFO dictionary value by key value (page)
	def getValue(self, page):
		try:
			return self.dictionary[page]
		except KeyError:
			return None

	# Sets a new value at the given page address
	def setValue(self, page, newValue):
		tmpDict = self.dictionary
		tmpList = self.list

		if(page in tmpDict):
			tmpList.remove(page)

		tmpDict[page] = newValue
		tmpList.append(page)

		if (len(tmpList) > self.numEntries):
			del tmpDict[tmpList.pop(0)]

	# pops the value at the given value
	def pop(self, key):
		self.dictionary.pop(key)
		self.list.remove(key)


# Makes calculations based on LRU algorithm
class LRUCache:

	def __init__(self, numFrames):
		self.numFrames = numFrames
		self.cache = collections.OrderedDict()

	def getValue(self, page):
		try:
			retValue = self.cache.pop(page)
			self.cache[page] = retValue
			return retValue
		except KeyError:
			return None

	def setValue(self, page, newValue):
		try:
			self.cache.pop(page)
		except KeyError:
			if (len(self.cache) >= self.numFrames):
				self.cache.popitem(last = False)
		self.cache[page] = newValue

# Makes calculations based on OPT algorithm
class OPTCache:

	def __init__(self, numFrames):
		self.numFrames = numFrames
		self.cache = collections.OrderedDict()
		self.priority = {}
		self.remove = []

	# Returns the value of the key in cache, and returns null if key is not found
	def getValue(self, getKey):
		try:
			retValue = self.cache.pop(getKey)
			self.cache[getKey] = retValue
			return retValue
		except KeyError:
			return None

	# Sets the value specified at the cache
	def setValue(self, setKey, setValue):
		try:
			self.cache.pop(setKey)
		except KeyError:
			if (len(self.cache) >= self.numFrames):
				self.popOPT()
		self.cache[setKey] = setValue

	def popOPT(self):
		for r in self.remove:
			if (self.cache.get(r[0]) is None):
				continue
			else:
				self.cache.pop(v[0])

	# Creates the OPT priority list
	def initOPT(self, inputAddresses):
		service = 0
		for i in inputAddresses:
			pageNum, offsett = maskAddress(i)
			try:
				pn = self.priority[pageNum]
				self.priority[pageNum].numRequests += 1
			except KeyError:
				ip = RmPage(pageNum, 1, service)
				self.priority[pageNum] = pn
			service += 1

	def calculateOPT(self):
		for(x, y) in self.priority.iteritems():
			self.remove.append(y.pageNum, y.numRequests, y.service)
		self.remove - sorted(self. remove, key = lambda z: (z[1], -z[2]))


# Class holding data for a page
class Page: 
	def __init__(self, pageNum, frame):
		self.pageNum = pageNum
		self.frame = frame


# Class holding data for a table entry
class TLBEntry:
	def __init__(self, pageNum, frame):
		self.pageNum = pageNum
		self.frame = frame


# Class holding data for a page that does not have prioirity (by OPT algorithm)
class RmPage: 
	def __init__(self, pageNum, numRequests, service):
			self.pageNum = pageNum
			self.numRequests = numRequests
			self.service = service

# Get value of byte in the frame (with offset)
def getByteValue(frame, offset):
	return int(frame[offset].encode('hex'), 16)

# Parses the command line arguments by the 3 specified inpurs
def parseArgs(args):
    return [int(line) for line in args["rsf"]], args["f"], args["p"]

# Reads from BACKING_STORE by 256 * number_of_frames
def readBinFrame(numFrames):
	file = open("BACKING_STORE.bin", 'rb')
	size = 256
	file.seek(size * numFrames)
	return file.read(size)

# Returns the page and logical offset based on the logical, 32-bit address inputted
def maskAddress(address):
	return (address >> 8), (address & 0xFF)

# Initializes virtual memory based on the nnumber of frames and the replacement algorithm
def createVirtualMemory(infile, numFrames, replacementAlgorithm):
	return VirtualMemory(replacementAlgorithm, numFrames)

# Does argument parsing and calls functions to replicate virtual memory
def main():

	# Check to see if BACKING_STORE.bin is available
	if os.path.isfile("BACKING_STORE.bin") == False:
		print("BACKING_STORE.bin cannot be found, exiting program ):")
		sys.exit(0)

	# Set command line arguements and their corresponding default values 
	parser = argparse.ArgumentParser(description = "Virtual Memory Simulator (memSim)")
	parser.add_argument("rsf", metavar = "RSF", type = argparse.FileType(), help = "Reference sequence file")
	parser.add_argument("-f", metavar = "FRAMES", type = int, default = 256, help = "# of frames in memory; default = 256")
	parser.add_argument("-p", metavar = "PRA", type = str, default = "FIFO", help = "PRA choices: FIFO, LRU, OPT; default = FIFO")

	# Parse the arguments into their appropriate types
	inputAddresses, numFrames, replacementAlgorithm = parseArgs(vars(parser.parse_args()))

	# Check numFrames to see if value is in range
	if (numFrames > 256 or numFrames < 0):
		numFrames = 256

	# Check replacementAlgorithm to see if user input is available
	if (replacementAlgorithm not in ["FIFO", "OPT", "LRU"]):
		replacementAlgorithm = "FIFO"

	print replacementAlgorithm #Check to make sure replacement algorithm was functioning

	virtualMem = VirtualMemory(replacementAlgorithm, numFrames)

	for address in inputAddresses:
		virtualMem.handleRequest(address)

	virtualMem.printStats()





if __name__ == '__main__':
	main()