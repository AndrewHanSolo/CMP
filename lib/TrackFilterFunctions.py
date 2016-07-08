import TrackClassGlobals as TCG
import general as gen
import TrackMeasurementFunctions as TMF
import numpy as np

###Functions only work on TrackFile objects

#updates track x,y,z,t arrays so that it has data for frames only between minFrame and maxFrame
def selectFrames(self, filters):
	for frameBin in filters['frames']:
		minFrame, maxFrame = frameBin[0], frameBin[1]
		if minFrame == float('-inf') and maxFrame == float('inf'):
			continue
		goodTracks = []
		for track in self.tracks:
			newXarray = []
			newYarray = []
			newZarray = []
			newTarray = []
			for x, y, z, t in zip(track.x, track.y, track.z, track.t):
				if gen.withinRange(t, minFrame, maxFrame):
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
	for xArray, yArray in zip(filters['xPos'], filters['yPos']):
		minX, maxX = xArray[0], xArray[1]
		minY, maxY = yArray[0], yArray[1]
		if minX == float('-inf') and maxX == float('inf') \
		 and minY == float('-inf') and maxY == float('inf'):
			continue
		goodTracks = []
		for track in self.tracks:
			newXarray = []
			newYarray = []
			newZarray = []
			newTarray = []
			for x, y, z, t in zip(track.x, track.y, track.z, track.t):
				if gen.withinRange(x, minX, maxX) \
				 and gen.withinRange(y, minY, maxY):
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
		selectDictBinsHelper(self, field, filters[field])
	self.analysis()

#rangeArray is a list of size 2 arrays that are min and max values of bin
def selectDictBinsHelper(self, propertyName, rangeArray):
	#instantiate list of tracks that meet criteria
	goodTracks = []
	fieldValues = self.d[propertyName]
	#for each range bin
	for array in rangeArray:
		if array[0] == float('-inf') and array[1]== float('inf'):
			return
		#if track is within range, add it to goodTracks
		for index in range(0, len(self.tracks)):
			if gen.withinRange(fieldValues[index], array[0], array[1]):
				goodTracks.append(self.tracks[index])

	self.tracks = goodTracks



