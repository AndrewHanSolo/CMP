#General Functions File

from TrackClassGlobals import *
import TrackClass as TC
from math import *
import matplotlib.pyplot as plt
import re
import pylab as P
import _pickle as pickle
import traceback
import sys


#imports, preprocesses, and saves all data from Full Experiment Folder for analysis
def importAndSave(folderPath, saveName):
	print('Importing, processing, and saving data for analysis...')
	data = TC.AllExperimentData(folderPath)
	with open(saveName, 'wb') as output:
		pickle.dump(data, output, -1)
	print('Done.')
	return data


#constructs new figure with window and figure titles
def constructFig(self, title):
	P.clf()
	fig = P.gcf()
	fig.canvas.set_window_title(title)
	fig.suptitle(title + getSettingsLabel(self), fontsize = 8)
	return fig


#returns true if value is between min and max, inclusive
def withinRange(value, minVal, maxVal):
	return value >= minVal and value <= maxVal

#if VERBOSE is True, string will be printed
def vprint(string):
	if VERBOSE is True:
		print(string)

#if DEBUG is True, string will be printed
def dprint(string):
	if DEBUG is True:
		print(string)		

#saves the figure to SAVE_DIRECTORY/title.extension
def savePlot(fig, title, extension = '.png'):
	savePath = TCG.SAVE_DIRECTORY + title + extension
	try:
		fig.savefig(savePath)
		P.close() #CAREFUL
	except:
		print('Could not save to path ' + savePath)
		traceback.print_exc(file = sys.stdout)
		pass

def updateFilterSettings(self, filterSettings, printFilters = False):
	for key in filterSettings:
		self.filters[key] = filterSettings[key]
		if printFilters: print(key, self.filters[key])


def getSettingsLabel(self):
	settingsString = ''
	try:
		for key in self.filters:
			for array in self.filters[key]:
				minVal, maxVal = array[0], array[1]
				if minVal != float('-inf') or maxVal != float('inf'):
					settingsString = settingsString + ', ' + str(key) + ': ' + str(self.filters[key])
	except:
		print("Failed to generate settings label.")
		traceback.print_exc(file = sys.stdout)
	return settingsString


def nanMean(list):
	return float(sum(list))/len(list) if len(list) > 0 else float('nan')

def getDifferenceArray(list):
	difference = []
	for index in range(0, len(list)-1):
		dx = list[index+1] - list[index]
		difference.append(dx)
	return difference

#size 2 vector (x, y)
def normalizeVector(vector):
	return pythagorean(vector[0], vector[1])

#returns dot product of two vectors
def dotProduct(array1, array2):
	ans = 0
	for i, j in zip(array1, array2):
		ans += i * j
	return ans

#gets distance between two points (2D coordinates right now)
def getDistance(x1,x2,y1,y2):
	return pythagorean((x1-x2), (y1-y2))

#Pythagorean theorem operation
def pythagorean(dx, dy):
	return sqrt(pow(dx, 2) + pow(dy, 2))


#################################
#SORT_NICELY
def tryint(s):
    try: 
    	return int(s)
    except: 
    	return s

# Turn a string into a list of string and number chunks. "z23a" -> ["z", 23, "a"]
def alphanum_key(s):
	return [ tryint(c) for c in re.split('([0-9]+)', s) ]

#Sort the given list in the way that humans expect.
def sort_nicely(l):
	l.sort(key=alphanum_key)



#################################
#More TrackClass helper functions

#Gets max x and y position of all tracks in a trackFile. self must be trackFile.
#finds greatest startPos or endPos, does not check all x positions. same for y
def getTrackFileDimensions(self):
	maxX = 0
	maxY = 0
	for track in self.tracks:
		maxXofTrack = max(getxStartPos(track), getxEndPos(track))
		maxYofTrack = max(getyStartPos(track), getyEndPos(track))
		if maxXofTrack > maxX:
			maxX = maxXofTrack
		if maxYofTrack > maxY:
			maxY = maxYofTrack

	return maxX, maxY

#Enumerate over an iterable in reverse order while retaining proper indexes
def reverse_enumerate(iterable):
	return zip(reversed(range(len(iterable))), reversed(iterable))




