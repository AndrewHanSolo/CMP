import TrackClassGlobals as TCG
import general as gen
import TrackMeasurementFunctions as TMF
import numpy as np
from itertools import cycle

###Functions only work on TrackFile objects

#updates track x,y,z,t arrays so that it has data for frames only between minFrame and maxFrame
def selectFrames(self, filters):
	if "frames" not in filters:
		return
	for frameBin in filters['frames']:
		goodTracks = []
		for track in self.tracks:
			newXarray = []
			newYarray = []
			newZarray = []
			newTarray = []
			for x, y, z, t in zip(track.x, track.y, track.z, track.t):
				if gen.withinRange(t, frameBin[0], frameBin[1]):
					newXarray.append(x)
					newYarray.append(y)
					newZarray.append(z)
					newTarray.append(t)
			track.x = []; track.x = newXarray
			track.y = []; track.y = newYarray
			track.z = []; track.z = newZarray
			track.t = []; track.t = newTarray
			if len(track.x) >= 2:
				goodTracks.append(track)

		self.tracks = goodTracks
		self.analysis()


#updates track x,y,z,t array so that it has data for xPos between minX and maxX
def selectArea(self, filters):
	if ("xPos" not in filters) and ("yPos" not in filters):
		return

	try: xFilters = filters["xPos"] 
	except: xFilters =  [[float("-inf"), float("inf")]]

	try: yFilters = filters["yPos"] 
	except: yFilters = [[float("-inf"), float("inf")]]	 

	for xFilter, yFilter in zip(xFilters, cycle(yFilters)) if len(xFilters) > len(yFilters) else zip(cycle(xFilters), yFilters):
		goodTracks = []
		for track in self.tracks:
			newXarray = []
			newYarray = []
			newZarray = []
			newTarray = []
			for x, y, z, t in zip(track.x, track.y, track.z, track.t):
				if xFilter[0] <= x <= xFilter[1] and \
				   yFilter[0] <= y <= yFilter[1]:
					newXarray.append(x)
					newYarray.append(y)
					newZarray.append(z)
					newTarray.append(t)
			track.x = []; track.x = newXarray
			track.y = []; track.y = newYarray
			track.z = []; track.z = newZarray
			track.t = []; track.t = newTarray
			if TMF.getNumFrames(track) > 0 and TMF.getAge(track) >=2:
				goodTracks.append(track)

		self.tracks = goodTracks
		self.analysis()


#removes tracks that are not within specified percentile of propertyName. similar to selectData, edits
#self so WARNING!. percent range is a pair of numbers, min and max percent inclusive
def selectPercentile(self, propertyName, percentRange = [0, 100]):
	percentileVals = np.percentile(self.d[propertyName], percentRange)
	goodTracks = []
	fieldValues = self.d[propertyName]
	for index in range(0, len(self.tracks)):
		if gen.withinRange(fieldValues[index], percentileVals[0], percentileVals[1]):
			goodTracks.append(self.tracks[index])

	self.tracks = goodTracks
	self.analysis()
	return percentileVals


def selectDictBins(self, filters):
	for field in self.d:
		if field in filters:
			selectDictBinsHelper(self, field, filters[field])
	self.analysis()

#rangeArray is a list of size 2 arrays that are min and max values of bin
def selectDictBinsHelper(self, propertyName, rangeArray):
	#instantiate list of tracks that meet criteria
	goodTracks = []
	fieldValues = self.d[propertyName]
	#for each range bin
	for array in rangeArray:
		#if track is within range, add it to goodTracks
		for index in range(0, len(self.tracks)):
			if gen.withinRange(fieldValues[index], array[0], array[1]):
				goodTracks.append(self.tracks[index])

	self.tracks = goodTracks



