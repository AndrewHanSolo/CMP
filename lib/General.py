#General Functions File

from TrackClassGlobals import *
import TrackClassGlobals as TCG
from TrackClass import *
import TrackClass as TC
from math import *
import re, sys, traceback
import pylab as P
import _pickle as pickle
import xlsxwriter
import os



#imports, preprocesses, and saves all data from Full Experiment Folder for analysis
def importAndSave(foldername, saveName):
	print('Importing, processing, and saving data for analysis...')
	data = TC.AllExperimentData(foldername)
	print(saveName)
	with open(TCG.DATA_SAVE_PATH + saveName, 'wb') as output:
		pickle.dump(data, output, -1)
	print('Done.')
	return data

def createWorkbook(name):
	return xlsxwriter.Workbook(TCG.ANALYSIS_SAVE_PATH + "/" + name + ".xlsx", {'nan_inf_to_errors': True, 'in_memory': True})

#clear any remaining data out of TrackFile object
def clear(self):
	#if type(self).__name__ not "TrackFile":
	#	dprint("Clear not being called on TrackFile")
	#	return
	if len(self.tracks) == 0:
		self.axisLimits = {}
		for key, values in self.fields.items():
			self.d[key] = []
		return

# constructs new figure with window and figure titles	
def constructFig(self, title):
	P.clf()
	fig = P.gcf()
	fig.canvas.set_window_title(title)
	fig.suptitle(title + getSettingsLabel(self), fontsize = 8)
	return fig

#set all keys in dict to value
def setAllDictVals(self, value):
	for key in self:
		self[key] = value


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
	savePath = TCG.ANALYSIS_SAVE_PATH + '/' + TCG.ANALYSIS_SAVE_NAME + '/' + title + extension
	try:
		fig.savefig(savePath)
		P.close() #CAREFUL
	except:
		print('Could not save to path ' + savePath)
		traceback.print_exc(file = sys.stdout)
		pass

def updateFilterSettings(self, filterSettings):
	for key in filterSettings:
		self.filters[key] = filterSettings[key]

def getSettingsLabel(self):
	settingsString = ''
	try:
		for key in self.filters:
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
	

#helper for appropriate property clamping in scan function
def scanAxesClampHelper(self, propertyName, minVal, maxVal):
	if not self.axisLimits:
		vprint("Warning: scan called on TrackFile with no axisLimits.")
		vprint("	TrackFile has %d tracks." % (len(self.tracks)))
		return

	if minVal < (self.axisLimits[propertyName])[0]:
		minVal = (self.axisLimits[propertyName])[0]
		vprint("Notice: scan of %s was started at lowest value %.1f instead" % (propertyName, minVal))

	if maxVal > (self.axisLimits[propertyName])[1]:
		maxVal = (self.axisLimits[propertyName])[1]
		vprint("Notice: scan of %s was ended at highest value %.1f instead" % (propertyName, maxVal))

	return minVal, maxVal

#returns the parameters necessary for constructing a colormap scatterplot
#checks for colorMap key in settings, returns default values if not exist
def getColorMapPlotSettings(trackFile, colorPropertyName, settings):
	if 'colorSettings' in settings:
		colorSettings = settings['colorSettings']
		vmin = colorSettings['vmin']
		vmax = colorSettings['vmax']
		separation = colorSettings['separation']
		colormap = P.get_cmap(colorSettings['colorMap'])
	else:
		vmin = (trackFile.axisLimits[colorPropertyName])[0]
		vmax = (trackFile.axisLimits[colorPropertyName])[1]
		separation = 35
		colormap = P.get_cmap('jet')

	return vmin, vmax, separation, colormap

def get_spaced_colors(n):
    max_value = 16581375 #255**3
    interval = int(max_value / n)
    colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]

    return [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colors]



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




