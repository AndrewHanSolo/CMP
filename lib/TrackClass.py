from __future__ import division
from importTrackMateData import *
from general import *
from math import *
import os.path
import csv
import numpy as np
import pylab as P
from copy import deepcopy
import sys, traceback
from mpl_toolkits.mplot3d import Axes3D
from TrackClassGlobals import *
import TrackClassGlobals as TCG
import TrackFilterFunctions as TFF
import matplotlib
import matplotlib.cm as cm
from scipy import stats
from scipy.stats import gaussian_kde
from matplotlib.ticker import FuncFormatter
import xlsxwriter
import _pickle as pickle
import sys
from colorsys import *
import matplotlib.pyplot as plt




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

		self.fields = TCG.DefaultTrackMeasurements
		self.filters = {}
		self.expParams = expParams
		self.tracks = tracks
		self.d = {} #Dictionary of Track measurement lists, 
		            #where indices across lists correlate to 
		            #the same Track
		self.meta = {} #Dict in which track measurement metadata is stored
		self.axisLimits = {} #Dict in which track measurement min and max values are stored
		               
		self.master = master #True means the trackfile contains full experiment data
		                     #and is ready for analysis
		
		#to be done on TrackFile that has merged tracks
		#first analysis performed, axeslimits are updated
		if self.master:
			self.expParams['maxX'], self.expParams['maxY'] = getTrackFileDimensions(self)
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
		if not filters:
			return
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


	# Recomputes track measurement dict d
	#
	# @param      self    The object
	# @param      fields  The fields
	#
	def analysis(self):

		for key, measurementClass in self.fields.items():
			dataBuffer = []
			for track in self.tracks:
				dataBuffer.append(measurementClass.function(track, **self.expParams))
			self.d[key] = dataBuffer
			self.meta[key] = self.getAverage(key)
			if len(dataBuffer) == 0:
				self.axisLimits[key] = [0, 0]
			else:
				self.axisLimits[key] = [min(dataBuffer), max(dataBuffer)]

		return


	# prints all track measurement data to excel file
	# TODO: Add sheet and write metadata for experiment
	#
	# @param      self      The object
	# @param      settings  The settings
	#
	def writeData(self, settings = TCG.PlotDefaults):
		workbookName = "%s%s measurement data %s.xlsx" % (TCG.SAVE_DIRECTORY, self.fileName, settings['title'])
		workbook = xlsxwriter.Workbook(workbookName, {'nan_inf_to_errors': True})
		worksheet = workbook.add_worksheet()
		colindex = 0
		rowindex = 0
		#label track ids
		worksheet.write(rowindex, colindex, 'id')
		for trackCount in range(len(self.tracks)):
			rowindex += 1
			worksheet.write(rowindex, colindex, trackCount)
		#list each propertyName value by col
		for propertyName, na in sorted(self.d.items()):
			colindex += 1
			rowindex = 0
			worksheet.write(rowindex, colindex, propertyName)
			propertyValues = self.d[propertyName]
			#write all values of propertyNames to rows
			for value in propertyValues:
				rowindex += 1
				worksheet.write(rowindex, colindex, value)


		worksheet2 = workbook.add_worksheet("Metadata")
		worksheet2.write(0, 0, "propertyName")
		worksheet2.write(0, 1, "wAvg")
		worksheet2.write(0, 2, "nAvg")
		worksheet2.write(0, 3, "stdDev")
		worksheet2.write(0, 4, "stdErr")
		worksheet2.write(0, 5, "nAvg")
		worksheet2.write(0, 6, "nAvg")

		rowIndex = 1
		for propertyName, na in sorted(self.d.items()):
			print(propertyName)
			worksheet2.write(rowIndex, 0, propertyName)
			rowIndex += 1

		workbook.close()
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

		#check that scanning range is valid and update if otherwise
		if minVal < (self.axisLimits[propertyName])[0]:
			minVal = (self.axisLimits[propertyName])[0]
			vprint("Notice: scan of %s was started at lowest value %.1f instead" % (propertyName, minVal))

		if maxVal > (self.axisLimits[propertyName])[0]:
			maxVal = (self.axisLimits[propertyName])[0]
			vprint("Notice: scan of %s was ended at highest value %.1f instead" % (propertyName, maxVal))


		bins = np.linspace(minVal, maxVal, resolution+1)
		settings = args[2]
		title = "%s, %s scan of %s vs %s" % (self.fileName , propertyName, args[0], args[1])
		legendStrings = []
		colorIndices = np.linspace(0, 1, resolution)
		fig = constructFig(self, title)
		
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

			#plot
			P = function(trackFileCopy, *args, color = plt.cm.cool(colorIdx))
			P.legend(legendStrings)

		savePlot(fig, title)
		P.close()



	##
	## Scans over tracks by propertyName, and computes function on them at each
	## slice
	##
	## @param      self          The object
	## @param      propertyName  The property name
	## @param      minVal        The minimum value
	## @param      maxVal        The maximum value
	## @param      resolution    The resolution
	## @param      function      The function
	## @param      args          The scan settings
	##
	## @return     { description_of_the_return_value }
	##
	def iterate(self,
				propertyName,
				minVal,
				maxVal,
				resolution,
				function,
				*args):

		bins = np.linspace(minVal, maxVal, resolution+1)
		settings = args[2]
		title = "%s, %s scan of %s vs %s" % (self.fileName , propertyName, args[0], args[1])

		for index in range(0, len(bins)-1):
			lowerVal = bins[index]
			upperVal = bins[index+1]

			#copy data
			filtersCopy = {}
			filtersCopy[propertyName] = [[lowerVal, upperVal]]
			trackFileCopy = deepcopy(self)
			trackFileCopy.selectData(filtersCopy)
			settings['title'] = ("%s: %.1f to %.1f" % (propertyName, lowerVal, upperVal))
			settings["newFig"] = True
			settings["save"] = True
			P = function(trackFileCopy, *args)
			P.close()

	# returns weightedAverage and standard deviation 
	# or number average and standard error of a measurement in Trackfile
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
		try:
			if not weights:
				avg = np.average(self.d[propertyName])
				stdErr = stats.sem(self.d[propertyName])
				return avg, 0, stdErr

			weightedAvg = np.average(self.d[propertyName], weights = self.d[weights])
			stdDev = sqrt(np.average((self.d[propertyName] - weightedAvg)**2, weights = self.d[weights]))
			stdErr = stdErr = stats.sem(self.d[propertyName])
			return weightedAvg, stdDev, stdErr

		except:
			print("exception hit in getAverage")
			return 0, 0, 0


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

		wAvgs = []
		stdDevs = []
		stdErrs = []
		trackCounts = []
		countPercents = []
		binCenters = []

		#format bin setting to iterator (hacky)
		binArray = (self.fields[binnedPropertyName]).bins
		if type(binArray) == int:
			minValueProperty = 0
			maxValueProperty = max(self.d[binnedPropertyName])
			binArray = np.linspace(minValueProperty, maxValueProperty, binArray+1)

		#iterate across bins, select data, get dataPropertyName wavgs, stdDevs, stderrs and 
		#add to array
		for index in range(len(binArray) - 1):
			minVal = binArray[index]
			maxVal = binArray[index+1]
			filters = {}
			filters[binnedPropertyName] = [[minVal, maxVal]]

			copy = deepcopy(self)
			copy.selectData(filters)
			wAvg, stdDev, stdErr = copy.getAverage(dataPropertyName, weights = settings['weights'])

			wAvgs.append(wAvg)
			stdDevs.append(stdDev)
			stdErrs.append(stdErr)
			trackCounts.append(len(copy.d[binnedPropertyName]))
			#countpercents are #cellsInBin/#totalCells
			if len(self.d[binnedPropertyName]) != 0:
				countPercents.append(100 * len(copy.d[binnedPropertyName])/len(self.d[binnedPropertyName]))
			else:
				countPercents.append(0)
			binCenters.append((minVal + maxVal)/2)

		return wAvgs, stdDevs, stdErrs, trackCounts, countPercents, binCenters



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
	def plotBinData(self, binnedPropertyName, dataPropertyName, settings = TCG.PlotDefaults, **kwargs):
		#plot info
		plotTitle = "%s, wAvgs of %s binned by %s %s" % (self.fileName, dataPropertyName, binnedPropertyName, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)
				
		P.xlabel(axesLabels[binnedPropertyName])
		P.ylabel(axesLabels[dataPropertyName])

		wAvgs, stdDevs, stdErrs, trackCounts, countPercents, binCenters = self.getBinData(binnedPropertyName, dataPropertyName, settings = settings)
		P.errorbar(binCenters, wAvgs, yerr = stdErrs, **kwargs)

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
	def getHistogram(self, propertyName1, propertyName2 = None, settings = TCG.PlotDefaults, **kwargs):
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
	def plotHistogram(self, propertyName1, propertyName2 = None, settings = TCG.PlotDefaults, **kwargs):
		#plot info
		plotTitle = "%s %s histogram, %s" % (self.fileName, propertyName1, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)

		normStr = {True : "normalized count", False : "count"}
		P.ylabel(normStr[settings['norm']])
		P.xlabel(axesLabels[propertyName1])

		#histogram generation
		y, bincenters = self.getHistogram(propertyName1, settings = settings)
		P.plot(bincenters, y, **kwargs)

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
	def plotScatter(self, propertyName1, propertyName2, settings = TCG.PlotDefaults, **kwargs):
		#plot info
		plotTitle = "%s scatterplot of %s and %s, %s" % (self.fileName, propertyName1, propertyName2, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)
		P.xlabel(axesLabels[propertyName1])
		P.ylabel(axesLabels[propertyName2])

		#plot generation
		xValues = self.d[propertyName1]
		yValues = self.d[propertyName2]
		P.scatter(xValues, yValues, **kwargs)

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
	def plotPercentHistogram(self, propertyName, percentPropertyName, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = "%s %s histograms by %% %s; %s" % (self.fileName, propertyName, percentPropertyName, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)
		normStr = {True : "normalized count", False : "count"}
		P.ylabel(normStr[settings['norm']])
		P.xlabel(axesLabels[propertyName])

		y, bincenters, labels = self.getPercentHistogram(propertyName, percentPropertyName, settings = settings)

		#histogram generation
		for i in range(0, len(y)):
			P.plot(bincenters[i], y[i],'-', label = labels[i])
		if settings['legend']:
			P.legend(loc = settings['legendLoc'], prop = {'size': 9})

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P



	# generates heatmap movie of all tracks in experiment, where each dot is
	# placed at xStartPos. colors represent propertyName values of each track
	#
	# @param      self          The object
	# @param      propertyName  The property name
	# @param      snapshots     The snapshots
	# @param      settings      The settings
	#
	# @return     { description_of_the_return_value }
	#
	def cellVisualization(self, propertyName, snapshots = None, settings = TCG.PlotDefaults):
		#check or set snapshot value
		firstFrame = (self.axisLimits['firstFrame'])[0]
		lastFrame = (self.axisLimits['lastFrame'])[1]
		maxPossibleSnaps = lastFrame - firstFrame
		if not snapshots:
			snapshots = maxPossibleSnaps / 3
		if snapshots > maxPossibleSnaps or snapshots < 1:
			print("Invalid snapshot number for moving cell visualization.")

		#print status
		print("Generating movie for %s with %d frames..." % (self.fileName, snapshots))

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
			plotTitle = "%s cellVisual, %s: Frame %d, %s" % (self.fileName, propertyName, int(frameNum), settings['title'])
			fig = constructFig(self, plotTitle)
			cm = P.cm.get_cmap('jet')
			settingsCopy = settings.copy()
			sc = P.scatter(xFrame, yFrame, c = cFrame, vmin = axesLimits[propertyName][0], vmax = axesLimits[propertyName][1], s = 35, cmap = cm)
			P.colorbar(sc)
			P.xlim(xmin = 0, xmax = maxXPos)
			P.xlabel('microns')
			P.ylim(ymin = 0, ymax = maxYPos)
			P.ylabel('microns')
			savePlot(fig, plotTitle)
		return


	def heatmapVisualization(self, xPropertyName, yPropertyName, colorPropertyName, settings = TCG.PlotDefaults):

		plotTitle = "%s x=%s y=%s c=%s heatmap %s" % (self.fileName, xPropertyName, yPropertyName, colorPropertyName, settings['title'])
		fig = constructFig(self, plotTitle)

		cm = P.get_cmap('jet')
		xPositionsAllFrames = []
		yPositionsAllFrames = []
		propertyAllFrames = []
		sc = P.scatter(self.d[xPropertyName], self.d[yPropertyName], c = self.d[colorPropertyName], vmin = axesLimits[colorPropertyName][0], vmax = axesLimits[colorPropertyName][1], s = 35, cmap = cm)
		P.colorbar(sc)

		maxXPos = max(self.d[xPropertyName])
		maxYPos = max(self.d[yPropertyName])
		minXPos = min(self.d[xPropertyName])
		minYPos = min(self.d[yPropertyName] )
		P.xlim(xmin = minXPos, xmax = maxXPos)
		P.xlabel(axesLabels[xPropertyName])
		P.ylim(ymin = minYPos, ymax = maxYPos)
		P.ylabel(axesLabels[yPropertyName])

		savePlot(fig, plotTitle)



	#generates animation frames for scatterPlots of propertyName1 and 2, where each frame
	#corresponds to a range of frames
	def scatterVisualization(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		filterInst = self.filters.copy()

		for i in range(settings['startFrame'], settings['endFrame'], settings['frameInterval']):
			filterInst['frames'] = [[i, i+settings['frameInterval']]]
			plotTitle = "scatter of %s and %s, frames %d to %d, %s" % (propertyName1, propertyName2, i, i+settings['frameInterval'], settings['title'])
			fig = constructFig(self, plotTitle)

			copy = deepcopy(self)
			copy.selectData(filterInst)
			setInst = settings.copy()
			setInst['title'] = 'Frames ' + str(i) + ' to ' + str(i + settings['frameInterval'])
			copy.plotScatter(propertyName1, propertyName2, settings = setInst)
			del(copy)

		return


	#plots several plotBinData plots in one figure. not dynamic
	#propertyName is for first histogram plot and bins for plotBinData functions
	def plotBinDataSummary(self, propertyName, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = "%s, %s dir bin analysis %s" % (self.fileName, propertyName, settings['title'])
		P.figure(figsize = (24.0, 10.0))
		fig = constructFig(self, plotTitle)

		setInst = settings.copy()
		setInst['save'] = False
		setInst['newFig'] = False

		if type(settings[propertyName + 'Bins']) == int:
			no, bins = np.histogram(self.d[propertyName], bins = settings[propertyName + 'Bins'])
		else:
			bins = settings[propertyName + 'Bins']

		P.subplot(2,3,1)
		ax1 = P.hist(self.d[propertyName], bins = bins)
		P.title("histograms")
		P.xlabel(axesLabels[propertyName])
		P.ylabel("count")

		P.subplot(2,3,2)
		ax2 = P.hist(self.d['avgMov'], bins = 15)
		P.xlabel(axesLabels['avgMov'])
		P.ylabel("count")

		P.subplot(2,3,3)
		ax3 = P.hist(self.d['velocity'], bins = 15)	
		P.xlabel(axesLabels['velocity'])
		P.ylabel("count")

		P.subplot(2,3,4)
		P.title("wAvgs,stdErr of each dir bin")
		ax4 = self.plotBinData(propertyName, 'mp', settings = setInst)
		P.ylim([-1, 1])

		P.subplot(2,3,5)
		ax5 = self.plotBinData(propertyName, 'avgMov', settings = setInst)	
		P.ylim([0, 40])

		P.subplot(2,3,6)
		ax6 = self.plotBinData(propertyName, 'velocity', settings = setInst)	
		P.ylim([0, 40])

		self.getNumbers(propertyName, settings = setInst)

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P

	#plots multiple histogram plots in 1 figure. not dynamic
	def plotHistogramSummary(self, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = "%s, histogram summary %s" % (self.fileName, settings['title'])
		P.figure(figsize = (24.0, 5.0))
		fig = constructFig(self, plotTitle)

		setInst = settings.copy()
		setInst['save'] = False
		setInst['newFig'] = False

		P.subplot(1,3,1)
		ax1 = P.hist(self.d['mp'], bins = settings['mpBins'])

		P.subplot(1,3,2)
		ax2 = P.hist(self.d['avgMov'], bins = settings['avgMovBins'])

		P.subplot(1,3,3)
		ax3 = P.hist(self.d['velocity'], bins = settings['velocityBins'])	

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P





########################
########################
class AllExperimentData():

	def __init__(self, directoryPath):
		self.experiments = {}
		self.filters = {}
		#get all files from folderpath and sort in numerical order
		files = (os.listdir(directoryPath)) 
		sort_nicely(files)
		#iterate over all experiment folders, and add merged TrackFile experiments
		#to AllExperimentData object
		for experimentName in files: 
			fullExperimentPath = directoryPath + '/' + experimentName
			experimentTrackFolder = importTracksFromFolder(fullExperimentPath)
			experimentFile = experimentTrackFolder.toTrackFile()
			self.experiments[experimentName] = experimentFile


	def selectData(self, filters = {}):
		for experiment in self.experiments:
			self.experiments[experiment].selectData(filters)

	#print out all track property values
	def writeData(self, settings = TCG.PlotDefaults):
		for experiment, v in self.experiments.items():
			v.writeData(settings)

	def comparePlots(self, plotFunction, settings = TCG.PlotDefaults):
		for experiment, v in self.experiments.items():
			v.plotFunction(settings = settings)


	def histogramTemporalAnalysis(self, settings = TCG.PlotDefaults):
		for experiment, v in self.experiments.items():
			v.temporalHistogramAnalysis(settings = settings)

	def plotCurve(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		for experiment, v in self.experiments.items():
			v.plotCurve(propertyName1, propertyName2, settings = settings)


	def spatialTemporalAnalysis(self, settings = TCG.PlotDefaults):
		for experiment, v in self.experiments.items():
			v.spatialTemporalAnalysis(settings = settings)


	def histogramSummary(self, settings = TCG.PlotDefaults):
		for experiment, v in self.experiments.items():
			experimentCopy = deepcopy(v)
			experimentCopy.plotHistogramSummary(settings = settings)


	def cellVisualization(self, propertyName, settings = TCG.PlotDefaults):
		vprint('Saving cell visualization annimations of ' + propertyName + ' for all experiments.')
		for experiment, v in self.experiments.items():
			v.cellVisualization(propertyName, settings = settings)


	def plotScatter(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		vprint('Saving scatter plots of ' + str(propertyName1) + ' vs ' + str(propertyName2) + ' for all experiments.')
		for experiment, v in self.experiments.items():
			v.plotScatter(propertyName1, propertyName2, settings = settings)


	def scatterVisualization(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		vprint('Saving temporal scatter plot animation of ' + str(propertyName1) + ' vs ' + str(propertyName2) + ' for all experiments.')
		for experiment, v in self.experiments.items():
			v.scatterVisualization(propertyName1, propertyName2, settings = TCG.PlotDefaults)


	#TODO: include errorbars
	def plotBinData(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = 'wAvgCorr comp of ' + propertyName1 + ' and ' + propertyName2 + ', weight = ' + settings['weight'] + settings['title']
		if settings['newFig']: fig = constructFig(self, plotTitle)
			
		P.xlabel(axesLabels[propertyName1])
		P.ylabel(axesLabels[propertyName2])

		for experiment in sorted(self.experiments.items()):
			xAxisValues, weightedAverages, na = experiment[1].getBinData(propertyName1, propertyName2, settings = settings)
			P.plot(xAxisValues, weightedAverages, label = experiment[0])
			
		if settings['legend']: P.legend(loc = settings['legendLoc'], prop = {'size': 9})
		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	#general summary of weightedAvgCorrelations. not dynamic
	def plotBinDataSummary(self, settings = TCG.PlotDefaults):
		
		vprint('Plotting weightedAverageCorr experiment comparisons.')

		plotTitle = 'weightedAvg Corr Summary ' + settings['title']
		P.figure(figsize = (16.0, 10.0))
		if settings['newFig']: fig = constructFig(self, plotTitle)

		setInst = settings.copy()
		setInst['newFig'] = False
		setInst['show'] = False
		setInst['save'] = False

		P.subplot(2,2,1)
		ax1 = self.plotBinData('xStartPos', 'velocity', settings = setInst)

		setInst['legend'] = False

		P.subplot(2,2,2)
		ax2 = self.plotBinData('xStartPos', 'avgMov', settings = setInst)
		
		P.subplot(2,2,3)
		ax3 = self.plotBinData('xStartPos', 'directionality', settings = setInst)

		P.subplot(2,2,4)
		ax4 = self.plotBinData('avgMov', 'directionality', settings = setInst)

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	#get histograms of propertyName for each experiment
	def getHistograms(self, propertyName, settings = TCG.PlotDefaults):

		allHistogramValues = {}
		allHistogramBincenters = {}
		allHistogramLabels = {}
		index = 0

		for experiment, v in self.experiments.items():
			y, bincenters = v.getHistogram(propertyName, settings = settings)
			allHistogramValues[index] = y
			allHistogramBincenters[index] = bincenters
			allHistogramLabels[index] = v.fileName
			index += 1
			
		return allHistogramValues, allHistogramBincenters, allHistogramLabels


	#plots getHistograms
	def plotHistograms(self, propertyName, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = 'Comparison histogram of ' + propertyName + ' ' + settings['title']
		if settings['newFig']: fig = constructFig(self, plotTitle)


		normStr = {True : "(normalized count)", False : "(count)"}
		P.ylabel('% of total cell count ' + normStr[settings['norm']])
		P.xlabel(axesLabels[propertyName])

		y, bincenters, labels = self.getHistograms(propertyName, settings = settings)
		
		sortedVals = []
		for i in range(0, len(labels)):
			sortedVals.append((labels[i], bincenters[i], y[i]))
		
		#print(sortedVals)
		sortedVals = sorted(sortedVals,key=lambda x: x[0])

		for i in range(0, len(y)):
			P.plot(sortedVals[i][1], np.multiply(np.divide(sortedVals[i][2], sum(sortedVals[i][2])), 100),'-', label = sortedVals[i][0])
		if settings['legend'] == True:
			P.legend(loc = settings['legendLoc'], prop = {'size': 9})

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	#plots general comparison analysis of all experiments
	def comparisonAnalysis(self, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = 'Experiment Histogram Comparison ' + settings['title']
		P.figure(figsize = (24.0, 5.0))
		if settings['newFig']: fig = constructFig(self, plotTitle)

		
		setInst = settings.copy()
		setInst['newFig'] = False
		setInst['show'] = False
		setInst['save'] = False
		setInst['legendLoc'] = 1
		
		P.subplot(1,3,1)
		ax1 = self.plotHistograms('velocity', settings = setInst)

		setInst['legend'] = False

		P.subplot(1,3,2)
		ax2 = self.plotHistograms('avgMov', settings = setInst)

		P.subplot(1,3,3)
		ax3 = self.plotHistograms('directionality', settings = setInst)

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		
		P.clf()
		P.close()


		P.figure(figsize = (16.0, 10.0))
		plotTitle = 'Experiment WeightedAvgCorr Comparison ' + settings['title']
		if settings['newFig']: fig = constructFig(self, plotTitle)

		P.subplot(2,2,1)
		setInst['legend'] = True
		ax1 = self.plotBinData('xStartPos', 'velocity', settings = setInst)

		P.subplot(2,2,2)
		setInst['legend'] = False
		ax2 = self.plotBinData('xStartPos', 'avgMov', settings = setInst)

		P.subplot(2,2,3)
		ax3 = self.plotBinData('xStartPos', 'directionality', settings = setInst)

		P.subplot(2,2,4)
		ax4 = self.plotBinData('avgMov', 'directionality', settings = setInst)

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)





##generic Trackfile plot wrapper
#def plotHelper(trackfile, function, propertyName1, propertyName2, settings):
#	xaxis = trackfile.d[propertyname1]
#	yaxis = trackfile.d[propertyName3]
#	function(xaxis, yaxis, settings)
#
