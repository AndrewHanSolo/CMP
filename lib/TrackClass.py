from __future__ import division
from ImportTrackMateData import *
import TrackClassGlobals as TCG
import TrackFilterFunctions as TFF
from Serializers import *
from General import *
import sys, traceback, datetime, os.path, math
import numpy as np
import pylab as P
from copy import deepcopy
import matplotlib.cm as cm
from scipy import stats
import _pickle as pickle
from colorsys import *



##
## @brief      { Holds raw position and frame data for 1 cell-track }
##
class Track():

	##
	## @brief      { Constructor }
	##
	## @param      self  The object
	## @param      x     { 1xN array of x pos, where index corresonds to frame# }
	## @param      y     { 1xN array of y pos, where index corresonds to frame# }
	## @param      z     { 1xN array of z pos, where index corresonds to frame# }
	## @param      t     { 1xN array of t pos, where index corresonds to frame# }
	##
	def __init__(self, x, y, z, t):
		self.x = x
		self.y = y
		self.z = z
		self.t = t


##
## @brief      { Holds all Tracks contained in a single TrackMate xml output file }
##
class TrackFile():

	##
	## @brief      { Constructor }
	##
	## @param      self      The object
	## @param      tracks    1xN array of Track objects
	## @param      fileName  name of the xml file
	## @param      fields    the Track measurements to be included in
	##                       computation/analysis
	## @param      filters   a filter settings object (Default has no active
	##                       filters)
	## @param      path      the full path to the xml file's parent directory
	## @param      master    Bool to flag a merged Trackfile, representing a
	##                       full experiment containing all tracks. When this is
	##                       set to true, the experiment x and y dimensions are
	##                       found, and initial analysis is performed to prep
	##                       for filtering.
	##
	def __init__(self, tracks, 
				 fileName, 
				 expParams = TCG.DefaultExpParams,
				 path = 0, 
				 master = False):

		self.fileName = fileName
		self.path = path
		self.importTime = None

		self.fields = TCG.DefaultTrackMeasurements
		self.filters = {}
		self.expParams = expParams
		self.tracks = tracks
		self.d = {} #Dictionary of Track measurement lists, 
		            #where indices across lists correlate to 
		            #the same Track
		self.meta = {} #Dict in which track measurement metadata is stored
		self.axisLimits = expParams['DefaultAxisLimits'] #Dict in which track measurement min and max values are stored
		               
		self.master = master #True means the trackfile contains full experiment data
		                     #and is ready for analysis
		
		#to be done on TrackFile that has merged tracks
		#first analysis performed, field axislimits are updated
		if self.master:
			self.analysis()
		return
   

	# Filters tracks and reanalyzes
	#
	# @param      self     The object
	# @param      filters  The filters
	# 
	# @exception  <exception_object> { Error occured while filtering }
	#
	def selectData(self, filters):
		#for filterInstance in filters:
		updateFilterSettings(self, filters)
		
		try:
			TFF.selectFrames(self, filters)
			TFF.selectArea(self, filters)
			TFF.selectDictBins(self, filters)
		except:
			#pass
			vprint('Warning: exception hit in track filtering. Possibly no tracks to filter.')
			traceback.print_exc(file = sys.stdout)

		return


	# Recomputes track measurement dict d. Updates
	# axislimits of all trackmeasurements
	#
	# @param      self    The object
	# @param      fields  The fields
	#
	def analysis(self):
		#if no tracks analysis cannot be performed. clear data and return
		if len(self.tracks) == 0:
			clear(self)
			return

		for key, measurementClass in self.fields.items():
			if measurementClass.function:
				dataBuffer = []
				for track in self.tracks:
					dataBuffer.append(measurementClass.function(track, **self.expParams))
				if len(dataBuffer) == 0:
					clear(self)
					return
				else:
					self.d[key] = dataBuffer
					self.meta[key] = self.getAverage(key)
					self.axisLimits[key] = [min(dataBuffer), max(dataBuffer)]

		self.axisLimits["xPos"] = [min(self.d["xStartPos"]), max(self.d["xEndPos"])]
		self.axisLimits["yPos"] = [min(self.d["yStartPos"]), max(self.d["yEndPos"])]
		self.axisLimits["frames"] = [min(self.d["firstFrame"]), max(self.d["lastFrame"])]

		return




	##
	## Scans over tracks by propertyName, and computes function on them
	## at each slice
	##
	## @param      self          The object
	## @param      propertyName  The property name
	## @param      minVal        The minimum value
	## @param      maxVal        The maximum value
	## @param      resolution    The resolution
	## @param      function      The function
	## @param      args     	 The scan settings
	##
	def scan(self,
			 propertyName,
			 minVal,
			 maxVal,
			 resolution,
			 function,
			 *args):

		vprint("Scanning %s by %s..." % (self.fileName, propertyName))
		#check that scanning range is valid and update if otherwise
		minVal, maxVal = scanAxesClampHelper(self, propertyName, minVal, maxVal)

		#Instantiate workbook for writing data from this function
		workBookName = "%s %s scan of %s vs %s by %s.xlsx" % (TCG.SAVE_DIRECTORY, self.fileName, args[0], args[1], propertyName)
		workbook = xlsxwriter.Workbook(workBookName, {'nan_inf_to_errors': True, 'in_memory': True})

		bins = np.linspace(minVal, maxVal, resolution+1)
		settings = args[2]
		title = "%s, %s vs %s scanned by %s" % (self.fileName , args[0], args[1], propertyName)
		legendStrings = []
		colorIndices = np.linspace(0, 1, resolution)
		fig = constructFig(self, title)
		
		writeData(self, workbook, "binData")

		keepOpen = True #flag for whether to close the excel workbook on the next write
		for index, colorIdx in zip (range(0, len(bins)-1), colorIndices):

			#get filter instance range
			lowerVal = bins[index]
			upperVal = bins[index+1]

			
			#copy data
			filtersCopy = {}
			filtersCopy[propertyName] = [[lowerVal, upperVal]]
			trackFileCopy = deepcopy(self)
			trackFileCopy.selectData(filtersCopy)

			#turn off settings new fig
			settings["show"] = False
			settings["newFig"] = False
			settings["save"] = False

			#get plot instance legend name
			legendString = "%.1f to %.1f" % (lowerVal, upperVal)
			legendStrings.append(legendString)

			if (index == len(bins)-1):
				keepOpen = False
			
			#plot
			P = function(trackFileCopy, *args, color = cm.cool(colorIdx), workbook = [workbook, legendString, keepOpen])
			P.legend(legendStrings, title=(self.fields[propertyName]).axisLabel, loc = settings['legendLoc'], prop = {'size': 9})

		savePlot(fig, title)
		P.close()


	# returns weightedAverage and standard deviation 
	# or number average and standard error of a measurement in Trackfile
	# 
	# no standard method for calculating weighted average standard error
	# 
	# TODO: Maybe nAvg should also have stdDev
	# TODO: handle errors, don't return 0. will have to do for now
	# TODO: rename to getAverage()
	#
	# @param      self          TrackFile
	# @param      propertyName  measurementName
	# @param      settings      The settings
	#
	# @return     either wAvg and stdErr or nAvg and stdDev
	#
	def getAverage(self, propertyName, weights = False):
		if len(self.tracks) == 0:
			vprint("Notice: getAverage called on 0 tracks")
			return float('nan'), float('nan'), float('nan')
		try:
			if not weights:
				avg = np.average(self.d[propertyName])
				stdDev = np.std(self.d[propertyName])
				stdErr = stats.sem(self.d[propertyName])
				return avg, stdDev, stdErr

			weightedAvg = np.average(self.d[propertyName], weights = self.d[weights])
			stdDev = sqrt(np.average((self.d[propertyName] - weightedAvg)**2, weights = self.d[weights]))
			return weightedAvg, stdDev, 0

		except:
			print("Warning: Exception hit in getAverage")
			return float('nan'), float('nan'), float('nan')


	##
	## BEGIN SCAN COMPATIBLE FUNCTIONS
	##

	# Bins dataPropertyName values by binnedPropertyName
	# calculates avg, stdDev, stdErr for n bins and returns size N lists
	# 
	# Does same thing as getWieightedAverageCorr, but non-monotonically increasing bins can
	# be used with this one.
	# 
	# TODO: switch getWieghtedAverageCorr to getBinData
	# 		should be able to choose scanning mode. e.g. by monotonic or by percentiles
	# 		Right now only supports nonmonotonic/scalar bins defined in settings
	#
	# @param      self                The object
	# @param      binnedPropertyName  The binned property name
	# @param      dataPropertyName    The data property name
	# @param      settings            The settings
	#
	# @return     averages, stdDevs, stdErrs, trackCounts, countPercents (bin# to experiment#), bincenters
	#
	def getBinData(self, binnedPropertyName, dataPropertyName, settings = TCG.PlotDefaults):
		if len(self.d[binnedPropertyName]) == 0:
			return 0, 0, 0, 0, 0, 0

		avgs = []
		stdDevs = []
		stdErrs = []
		trackCounts = []
		countPercents = []
		binCenters = []

		#format bin setting to iterator (hacky)
		binArray = (self.fields[binnedPropertyName]).bins
		if type(binArray) == int:
			minValueProperty = (self.axisLimits[binnedPropertyName])[0] #min value
			maxValueProperty = (self.axisLimits[binnedPropertyName])[1] #max value
			binArray = np.linspace(minValueProperty, maxValueProperty, binArray+1)

		#iterate across bins, select data, get dataPropertyName avgs, stdDevs, stderrs and 
		#add to array
		for index in range(len(binArray) - 1):
			minVal = binArray[index]
			maxVal = binArray[index+1]
			filters = {}
			filters[binnedPropertyName] = [[minVal, maxVal]]

			copy = deepcopy(self)
			copy.selectData(filters)
			wAvg, stdDev, stdErr = copy.getAverage(dataPropertyName, weights = settings['weights'])

			if not math.isnan(wAvg):
				avgs.append(wAvg)
				stdDevs.append(stdDev)
				stdErrs.append(stdErr)
				trackCounts.append(len(copy.d[binnedPropertyName]))
				#countpercents are #cellsInBin/#totalCells
				if len(self.d[binnedPropertyName]) != 0:
					countPercents.append(100 * len(copy.d[binnedPropertyName])/len(self.d[binnedPropertyName]))
				else:
					countPercents.append(0)
				binCenters.append((minVal + maxVal)/2)

		return avgs, stdDevs, stdErrs, trackCounts, countPercents, binCenters



	# Plots getBinData. Error bars are stdError right now.
	# 
	# TODO: choose stdDev or stdErr, based on getAverage settings
	# TODO: plot a high-order polynomial smooth-fit curve
	#
	# @param      self                The object
	# @param      binnedPropertyName  The binned property name
	# @param      dataPropertyName    The data property name
	# @param      settings            The settings
	#
	def plotBinData(self, binnedPropertyName, dataPropertyName, settings = TCG.PlotDefaults, workbook = None, **kwargs):
		vprint("Plotting binData: %s scanned by %s" % (dataPropertyName, binnedPropertyName))

		#plot info
		plotTitle = "%s, avgs of %s binned by %s %s" % (self.fileName, dataPropertyName, binnedPropertyName, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)
				
		P.xlabel((self.fields[binnedPropertyName]).axisLabel)
		P.ylabel((self.fields[dataPropertyName]).axisLabel)

		avgs, stdDevs, stdErrs, trackCounts, countPercents, binCenters = self.getBinData(binnedPropertyName, dataPropertyName, settings = settings)
		
		if not avgs:  #(type(avgs) is not int) and len(avgs) == 0:
			vprint("Warning: No tracks to plot. Exiting plotBinData call instance.")
			return P

		P.errorbar(binCenters, avgs, yerr = stdErrs, **kwargs)

		if workbook:
			worksheetName = workbook[1]
			writeBinData(workbook[0], worksheetName, avgs, stdDevs, stdErrs, trackCounts, countPercents, binCenters)
			if not workbook[2]:
				workbook[0].close()

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	# Gets histogram values
	# 
	# TODO: confirm density plot options
	#
	# @param      self          The object
	# @param      propertyName  The property name
	# @param      settings      The settings
	#
	# @return     y values and corresponding bincenters
	#
	def getHistogram(self, propertyName1, propertyName2 = None, settings = TCG.PlotDefaults, workbook = None, **kwargs):

		values = self.d[propertyName1]
		data = np.array(values)
		y, binEdges = np.histogram(data, bins = settings['bins'], density = settings['norm'])
		bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
		return y, bincenters


	# Plots a histogram, using getHistogram
	#
	# @param      self       FH   The object
	# @param      propertyName  The property name
	# @param      settings      The settings
	#
	# @return     The Pylab plot
	#
	def plotHistogram(self, propertyName1, propertyName2 = None, settings = TCG.PlotDefaults, workbook = None, **kwargs):
		vprint("Plotting histogram: %s" % (propertyName1))

		#plot info
		plotTitle = "%s %s histogram%s" % (self.fileName, propertyName1, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)

		normStr = {True : "normalized count", False : "count"}
		P.ylabel(normStr[settings['norm']])
		P.xlabel((self.fields[propertyName1]).axisLabel)

		#histogram generation
		y, bincenters = self.getHistogram(propertyName1, settings = settings)
		P.plot(bincenters, y, **kwargs)

		if workbook:
			writeTrackData(self, workbook[0], workbook[1])
			writeMetaData(self, workbook[0], workbook[1])
			if not workbook[2]:
				workbook[0].close()

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	# Simple scatter plot
	#
	# @param      self           The object
	# @param      propertyName1  x axisLimits
	# @param      propertyName2  y axisLimits
	# @param      settings       The settings
	# @param      kwargs         The kwargs
	#
	# @return     the plot object
	#
	def plotScatter(self, propertyName1, propertyName2, settings = TCG.PlotDefaults, workbook = None, **kwargs):
		vprint("Plotting scatterplot: %s vs %s" % (propertyName1, propertyName2))

		#plot info
		plotTitle = "%s scatterplot of %s and %s, %s" % (self.fileName, propertyName1, propertyName2, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)
		P.xlabel((self.fields[propertyName1]).axisLabel)
		P.ylabel((self.fields[propertyName2]).axisLabel)

		#plot generation
		xValues = self.d[propertyName1]
		yValues = self.d[propertyName2]
		P.scatter(xValues, yValues, **kwargs)

		if workbook:
			writeTrackData(self, workbook[0], workbook[1])
			writeMetaData(self, workbook[0], workbook[1])
			if not workbook[2]:
				workbook[0].close()

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P

	##
	## END SCAN COMPATIBLE FUNCTIONS
	##


	# bin tracks based on the percentile of their propertyName value. e.g. for
	# getting avgMov of top 10% avgMov
	#
	# @param      self                 The object
	# @param      propertyName         The property name
	# @param      percentPropertyName  The percent property name
	# @param      settings             The settings
	#
	# @return     lists of histogram values, bincenters, and label lists
	#
	def getPercentHistogram(self, propertyName, percentPropertyName, settings = TCG.PlotDefaults):
		allHistogramValues = {}
		allHistogramBincenters = {}
		allHistogramLabels = {}

		#for each percent range, get histogram
		percents = settings['percents']
		for i in range(len(percents) - 1):
			tmp = deepcopy(self)
			perLow = percents[i]
			perHigh = percents[i+1]
			percentValues = TFF.selectPercentile(tmp, percentPropertyName, percentRange = [perLow, perHigh])
			y, bincenters = tmp.getHistogram(propertyName, settings = settings)
			allHistogramValues[i] = y
			allHistogramBincenters[i] = bincenters
			allHistogramLabels[i] = "%s: %d-%d%%, (%.3f to %.3f)" % (percentPropertyName[0:5], perLow, perHigh, percentValues[0], percentValues[1])
			
		return allHistogramValues, allHistogramBincenters, allHistogramLabels


	# plots getPercentHistogram
	def plotPercentHistogram(self, propertyName, percentPropertyName, settings = TCG.PlotDefaults, workbook = None, **kwargs):
		vprint("Plotting percent histogram: %s scanned by %s" % (propertyName, percentPropertyName))

		#plot info
		plotTitle = "%s %s histograms by %% %s; %s" % (self.fileName, propertyName, percentPropertyName, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)
		normStr = {True : "normalized count", False : "count"}
		P.ylabel(normStr[settings['norm']])
		P.xlabel((self.fields[propertyName]).axisLabel)

		y, bincenters, labels = self.getPercentHistogram(propertyName, percentPropertyName, settings = settings)

		#histogram generation
		for i in range(0, len(y)):
			P.plot(bincenters[i], y[i],'-', label = labels[i])
		if settings['legend']:
			P.legend(loc = settings['legendLoc'], prop = {'size': 9})


		if workbook:
			worksheetName = workbook[1]
			writePercentHistogramData(workbook[0], worksheetName, y, bincenters, labels)
			if not workbook[2]:
				workbook[0].close()

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P



	# generates heatmap movie of all tracks in experiment, where each dot is
	# placed at xStartPos, yStartPos. colors represent propertyName values of each track
	#
	# @param      self          The object
	# @param      propertyName  The property name
	# @param      snapshots     The snapshots
	# @param      settings      The settings
	#
	# @return     { description_of_the_return_value }
	#
	def cellVisualization(self, propertyName, snapshots = None, settings = TCG.PlotDefaults):
		print("Generating movie for %s with framerate %d" % (self.fileName, snapshots))
		#check or set snapshot value
		firstFrame = (self.axisLimits['firstFrame'])[0]
		lastFrame = (self.axisLimits['lastFrame'])[1]
		maxPossibleSnaps = lastFrame - firstFrame
		if not snapshots:
			snapshots = maxPossibleSnaps / 3
		if snapshots > maxPossibleSnaps or snapshots < 1:
			print("Invalid snapshot number for moving cell visualization.")

		#print status

		Blues = P.get_cmap('jet')
		xPositionsAllFrames = []
		yPositionsAllFrames = []
		propertyAllFrames = []

		#for each frame
		frames = np.linspace(int(firstFrame), int(lastFrame), int(snapshots))
		for frame in frames:
			frame = int(frame)
			xPositionsPerFrame = []
			yPositionsPerFrame = []
			propertyPerFrame = []
			#for all tracks
			trackIndex = 0
			propList = self.d[propertyName]
			for track in self.tracks:
				for frameNumber, x, y in zip(track.t, track.x, track.y):
					frameNumber = int(frameNumber)
					#if track exists on the current iterating frame
					if frame == frameNumber:
						#save its x,y position to array of positions for all other cells existing in this frame
						xPositionsPerFrame.append(x)
						yPositionsPerFrame.append(y)
						propertyPerFrame.append(propList[trackIndex]) 
				trackIndex = trackIndex + 1

			xPositionsAllFrames.append(xPositionsPerFrame)
			yPositionsAllFrames.append(yPositionsPerFrame)
			propertyAllFrames.append(propertyPerFrame)

		maxXPos = max(map(max, xPositionsAllFrames))
		maxYPos = max(map(max, yPositionsAllFrames))

		for xFrame, yFrame, cFrame, frameNum in zip(xPositionsAllFrames, yPositionsAllFrames, propertyAllFrames, frames):
			plotTitle = "%s cellVisual, %s, Frame %d, %s" % (self.fileName, propertyName, int(frameNum), settings['title'])
			fig = constructFig(self, plotTitle)
			settingsCopy = settings.copy()

			vmin, vmax, separation, colormap = getColorMapPlotSettings(self, propertyName, settings)

			sc = P.scatter(xFrame, yFrame, c = cFrame, vmin = vmin, vmax = vmax, s = separation, cmap = colormap)
			P.colorbar(sc, label = (self.fields[propertyName]).axisLabel)
			P.xlim(xmin = 0, xmax = maxXPos)
			P.xlabel('microns')
			P.ylim(ymin = 0, ymax = maxYPos)
			P.ylabel('microns')
			savePlot(fig, plotTitle)
		return


	def heatmapVisualization(self, xPropertyName, yPropertyName, colorPropertyName, settings = TCG.PlotDefaults):
		vprint("Plotting heatmapVisualization of %s, %s vs %s colored by %s" % (self.fileName, xPropertyName, yPropertyName, colorPropertyName))

		plotTitle = "%s x=%s y=%s c=%s heatmap %s" % (self.fileName, xPropertyName, yPropertyName, colorPropertyName, settings['title'])
		fig = constructFig(self, plotTitle)


		xPositionsAllFrames = []
		yPositionsAllFrames = []
		propertyAllFrames = []

		vmin, vmax, separation, colormap = getColorMapPlotSettings(self, colorPropertyName, settings)

		sc = P.scatter(self.d[xPropertyName], self.d[yPropertyName], c = self.d[colorPropertyName], vmin = vmin, vmax = vmax, s = separation, cmap = colormap)
		P.colorbar(sc, label = (self.fields[colorPropertyName]).axisLabel)

		maxXPos = max(self.d[xPropertyName])
		maxYPos = max(self.d[yPropertyName])
		minXPos = min(self.d[xPropertyName])
		minYPos = min(self.d[yPropertyName] )


		P.xlim(xmin = minXPos, xmax = maxXPos)
		P.xlabel((self.fields[xPropertyName]).axisLabel)
		P.ylim(ymin = minYPos, ymax = maxYPos)
		P.ylabel((self.fields[yPropertyName]).axisLabel)

		savePlot(fig, plotTitle)




########################
########################
class AllExperimentData():

	def __init__(self, foldername):
		self.folderPath = TCG.TRACK_FILES_IMPORT_PATH + foldername
		self.importTime = datetime.datetime.now()
		self.experiments = {}
		self.filters = {}
		#get all files from folderpath and sort in numerical order
		files = (os.listdir(self.folderPath + '/')) 
		sort_nicely(files)
		#iterate over all experiment folders, and add merged TrackFile experiments
		#to AllExperimentData object
		for experimentName in files: 
			fullExperimentPath = self.folderPath + '/' + experimentName
			experimentTrackFolder = importTracksFromFolder(fullExperimentPath)
			experimentFile = experimentTrackFolder.toTrackFile()
			experimentFile.importTime = self.importTime
			experimentFile.path = fullExperimentPath
			self.experiments[experimentName] = experimentFile


	def selectData(self, filters):
		#for filterInstance in filters:
		updateFilterSettings(self, filters)

		for experiment in self.experiments:
			self.experiments[experiment].selectData(filters)

	#print out all track property values
	def writeData(self, settings = TCG.PlotDefaults):
		workbook = createWorkbook("summary data")
		for experiment, v in sorted(self.experiments.items()):
			writeData(v, workbook, "")
		workbook.close()


	def compare(self, plotFunction, *args):
		vprint("Comparing %s for all experiments" % (plotFunction.__name__))

		settings = args[2]
		title = "Comparison of %s" % plotFunction.__name__
		fig = constructFig(self, title)
		settings["show"] = False
		settings["newFig"] = False
		settings["save"] = False

		legendStrings = []
		for experiment, v in sorted(self.experiments.items()):
			P = plotFunction(v, *args)
			legendStrings.append(experiment)

		P.legend(legendStrings, title="experiment", loc = settings['legendLoc'], prop = {'size': 9})
		savePlot(fig, title)
		P.close()

	def iterate(self, plotFunction, *args):
		vprint("Iterating through %s for all experiments" % (plotFunction.__name__))

		for experiment, v in sorted(self.experiments.items()):
			if len(args)==4:
				args[3][1] = experiment
			plotFunction(v, *args)