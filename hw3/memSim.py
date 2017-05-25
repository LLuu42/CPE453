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

	# returns page number and frame in the form of a tuple
	def get_tlb(self, page):
		self.tlbRequests += 1
		#checks if page is a miss
		if (self.tlb.get(page) is None):
			self.tlbMisses += 1 
		else: 
			return self.tlb.get(page)	


class FIFOCache(object, UserDict.DictMixin):

	def __init__(self, numEntries, dic = ()):
		self.numEntries = numEntries
		self.dictionary = dict(dic)
		self.list = []

class LRUCache:

	def __init__(self, numFrames):
		self.numFrames = numFrames
		self.cache = collections.OrderedDict()

class OPTCache:

	def __init__(self, numFrames):
		self.numFrames = numFrames
		self.cache = collections.OrderedDict()
		self.priority = {}
		self.victims - []

def parseArgs(args):
    return [int(line) for line in args["rsf"]], args["f"], args["p"]

# Does argument parsing and calls functions to replicate virtual memory
def main():

	# Check to see if BACKING_STORE.bin is available
	if os.path.isfile("BACKING_STORE.bin") == False:
		print("BACKING_STORE.bin cannot be found, exiting program ):")
		sys.exit(0)

	# Set command line arguements and their corresponding default values 
	parser = argparse.ArgumentParser(description = "Virtual Memory Simulator (memSim)")
	parser.add_argument("rsf", metavar = "RSF", type = argparse.FileType(), help = "Reference sequence file")
	parser.add_argument("f", metavar = "F", type = int, default = 256, help = "# of frames in memory; default = 256")
	parser.add_argument("p", metavar = "PRA", type = str, default = "FIFO", help = "PRA choices: FIFO, LRU, OPT; default = FIFO")

	# Parse the arguments into their appropriate types
	inputAddresses, numFrames, replacementAlgorithm = parseArgs(vars(parser.parse_args()))

	# Check numFrames to see if value is in range
	if (numFrames > 256 or numFrames < 0):
		numFrames = 256

	# Check replacementAlgorithm to see if user input is available
	if (replacementAlgorithm not in ["FIFO", "OPT", "LRU"]):
		replacementAlgorithm = "FIFO"

	print replacementAlgorithm

	virtualMem = VirtualMemory(replacementAlgorithm, numFrames)





if __name__ == '__main__':
	main()