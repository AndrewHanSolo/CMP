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
	def __init__(self, tracks, fileName, 
				 fields = TCG.Default_Track_Measurements, 
				 filters = TCG.DefaultFilters, 
				 path = 0, 
				 master = False):

		self.tracks = tracks
		self.fileName = fileName
		self.filters = filters
		self.path = path
		self.gradient = 0
		self.d = {} #Dictionary of Track measurement lists, 
		            #where indices across lists correlate to 
		            #the same Track
		self.maxX = 0,
		self.maxY = 0
		self.master = master
		
		#to be done on TrackFile that has merged tracks
		if self.master:
			print("hit")
			self.maxX, self.maxY = getTrackFileDimensions(self)
			self.analysis(fields)
		return
   

	# Filters tracks and reanalyzes
	#
	# @param      self     The object
	# @param      filters  The filters
	# 
	# @exception  <exception_object> { Error occured while filtering }
	#
	def selectData(self, filters = TCG.DefaultFilters):
		#for filterInstance in filters:
		updateFilterSettings(self, filters)
		try:
			TFF.selectFrames(self, filters)
			TFF.selectArea(self, filters)
			TFF.selectDictBins(self, filters)
		except:
			vprint('Exception hit in track filtering.')
			traceback.print_exc(file = sys.stdout)
		return


	# Recomputes track measurement dict d
	#
	# @param      self    The object
	# @param      fields  The fields
	#
	def analysis(self, fields = TCG.Default_Track_Measurements):

		##REMOVE
		if self.fileName == 'b GDNF 10':
			TCG.FIELD_VECTOR_INSTANCE = TCG.FIELD_VECTOR_SPECIAL
			print('hit')
		else: 
			TCG.FIELD_VECTOR_INSTANCE = TCG.GLOBAL_FIELD_VECTOR
		########

		for key, measurementClass in fields.items():
			fieldBuffer = []
			for track in self.tracks:
				fieldBuffer.append(measurementClass.function(track, maxX = self.maxX, gradient = self.gradient))
			self.d[key] = fieldBuffer
		return


	# returns weightedAverage and standard deviation 
	# or number average and standard error of a measurement in Trackfile
	# TODO: Maybe nAvg should also have stdDev
	# TODO: handle errors, don't return 0. will have to do for now
	#
	# @param      self          TrackFile
	# @param      propertyName  measurementName
	# @param      settings      The settings
	#
	# @return     either wAvg and stdErr or nAvg and stdDev
	#
	def getWeightedAverage(self, propertyName, settings = TCG.PlotDefaults):
		try:
			if settings["average"] == "weighted":
				weightedAvg = np.average(self.d[propertyName], weights = self.d[settings['weight']])
				stdDev = sqrt(np.average((self.d[propertyName] - weightedAvg)**2, weights = self.d[settings['weight']]))
				return weightedAvg, stdDev, stdErr
			if settings["average"] == "number":
				avg = np.average(self.d[propertyName])
				stdErr = stats.sem(self.d[propertyName])
				return avg, 0, stdErr
		except:
			return 0, 0, 0

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

		workbook.close()
		return


	#bins values based on binnedPropertyName, and calculates wAvg, stdDev, stdErr, #tracks, %tracks in bin, binCenters
	#of dataPropertyName. Does same thing as getWeightedAvgCorr, except non-monotonically increasing bins can be used
	def getBinData(self, binnedPropertyName, dataPropertyName, settings = TCG.PlotDefaults):
		wAvgs = []
		stdDevs = []
		stdErrs = []
		trackCounts = []
		countPercents = []
		binCenters = []

		#convert bin
		binValSettingsArray = binnedPropertyName + 'Bins'; 
		binArray = settings[binValSettingsArray]
		if type(binArray) == int:
			minValueProperty = 0
			maxValueProperty = max(self.d[binnedPropertyName])
			binArray = np.linspace(minValueProperty, maxValueProperty, 1+binArray)

		#iterate across bins, select data, get dataPropertyName wavgs, stdDevs, stderrs and 
		#add to array
		for index in range(len(binArray) - 1):
			minVal = binArray[index]
			maxVal = binArray[index+1]
			filters = TCG.DefaultFilters.copy()
			filters[binnedPropertyName] = [[minVal, maxVal]]

			copy = deepcopy(self)
			copy.selectData(filters)
			wAvg, stdDev, stdErr = copy.getWeightedAverage(dataPropertyName)

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


	#plots getBinData. Error bars are stdError right now 
	def plotBinData(self, binnedPropertyName, dataPropertyName, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = "%s, wAvgs of %s binned by %s %s" % (self.fileName, dataPropertyName, binnedPropertyName, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)
				
		P.xlabel(axesLabels[binnedPropertyName])
		P.ylabel(axesLabels[dataPropertyName])

		wAvgs, stdDevs, stdErrs, trackCounts, countPercents, binCenters = self.getBinData(binnedPropertyName, dataPropertyName)
		#P.errorbar(binCenters, wAvgs, yerr = stdErrs)
		density = gaussian_kde(wAvgs)
		print(binCenters)
		xs = binCenters#np.linspace(binCenters[0], binCenters[-1], len(binCenters))
		density.covariance_factor = lambda : .25
		density._compute_covariance()
		P.plot(xs,density(xs))

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)


	#returns y, bincenters values that compose histogram
	def getHistogram(self, propertyName, settings = TCG.PlotDefaults):
		values = self.d[propertyName]
		data = np.array(values)
		y, binEdges = np.histogram(data, bins = settings['bins'], density = settings['norm'])
		bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
		return y, bincenters


	#plots histogram of propertyName values
	def plotHistogram(self, propertyName, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = self.fileName + ', ' + propertyName + ', histogram' + ' ' + settings['title']
		if settings['newFig']: fig = constructFig(self, plotTitle)

		normStr = {True : "normalized count", False : "count"}
		P.ylabel(normStr[settings['norm']])
		P.xlabel(axesLabels[propertyName])

		#histogram generation
		y, bincenters = self.getHistogram(propertyName, settings = settings)
		print(bincenters)
		P.hist(y, bincenters)

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	#correlates weighted averages of property2 to property 1. propertyName1 is the xaxis (the dependent propertyName being scanned), 
	#propertyName2 is the yaxis, weightpropertyName are the weights used to find the weighted average
	#of propertyName2 within the scanned range of prpertyName1
	def getWeightedAverageCorr(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		xValues = self.d[propertyName1]
		yValues = self.d[propertyName2]
		weightValues = self.d[settings['weight']]

		#sort all values by their xValue (not to be confused with xPos)
		sortedTuples = sorted(zip(xValues, yValues, weightValues))
		sortedxValues = [x for (x,y,z) in sortedTuples]
		sortedyValues = [y for (x,y,z) in sortedTuples]
		sortedWeightValues = [z for (x,y,z) in sortedTuples]
		weightedAverages = []
		#get evenly spaced bins for scanning analysis
		hist, bins = np.histogram(sortedxValues, settings['bins'])
		for binIndex in range(0, len(bins)):
			bins[binIndex] = bins[binIndex]
		#get weighted averages (by weightpropertyName) of propertyName2 for every bin of propertyName1
		xAxisValues = []
		stdErrs = []
		for binIndex in range(0, len(bins)-1):
			selectedxValues = []
			selectedyValues = []
			selectedWeightValues = []

			minbinValue = bins[binIndex]
			maxbinValue = bins[binIndex + 1]
			xAxisValues.append((maxbinValue + minbinValue)/2)

			sortedxValues = np.array(sortedxValues)
			tmp = []; tmp = np.where(np.logical_and(sortedxValues > minbinValue, sortedxValues < maxbinValue))
			tmp = tmp[0]

			for index in tmp:
				selectedxValues.append(sortedxValues[index])
				selectedyValues.append(sortedyValues[index])
				selectedWeightValues.append(sortedWeightValues[index])
			try:
				weightedAverage = np.average(selectedyValues, weights = selectedWeightValues)
				stdErr = stats.sem(selectedyValues)
			except:
				weightedAverage = float('nan')
				stdErr = 0
			weightedAverages.append(weightedAverage)
			stdErrs.append(stdErr)

		return xAxisValues, weightedAverages, stdErrs #weightedAverages is yAxisValue


	#plots weightedAverageCorr values
	def plotWeightedAverageCorr(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = "%s corr of %s and %s; weight = %s; %s" % (self.fileName, propertyName1, propertyName2, settings['weight'], settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)
			
		P.xlabel(propertyName1)
		P.ylabel(propertyName2)

		xValues, yValues, stdErrs = self.getWeightedAverageCorr(propertyName1, propertyName2, settings = settings)
		P.errorbar(xValues, yValues, stdErrs)

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)

		return P

	#plots weightedAverageCorr values
	def plotCurve(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = "%s corr of %s and %s; weight = %s; %s" % (self.fileName, propertyName1, propertyName2, settings['weight'], settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)
			
		P.xlabel(propertyName1)
		P.ylabel(propertyName2)
		
		P.plot(self.d[propertyName1], self.d[propertyName2])

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)

		return P

	#propertyName1 is xAxis, propertyName2 is yAxis
	def plotScatter(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = "%s scatterplot of %s and %s; %s" % (self.fileName, propertyName1, propertyName2, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)
		P.xlabel(axesLabels[propertyName1])
		P.ylabel(axesLabels[propertyName2])

		#plot generation
		xValues = self.d[propertyName1]
		yValues = self.d[propertyName2]
		P.scatter(xValues, yValues)
		#P.xlim(axesLimits[propertyName1])
		#P.ylim(axesLimits[propertyName2])

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)


	#bin tracks based on the percentile of their propertyName value. e.g. for getting wAvg of avgMov of top 10% avgMov
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


	#plots getPercentHistogram
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


	#for each range of frames, do getWeightedAverageCorr of propertyName2 with propertyName1 as weights
	def weightedAverageCorrTemporalScan(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):

		xAxisValues = {}
		weightedAverages = {} #yAxisValues
		index = 0

		#for each frameBin, getweightedAverageCorr with spatialBins
		for frame in range(settings['startFrame'], settings['endFrame'], settings['frameInterval']):
			minFrame = frame
			maxFrame = frame + settings['frameInterval']
			#copy data
			fileCopy = []
			fileCopy = deepcopy(self)
			#select new frames
			filtersCopy = TCG.DefaultFilters.copy()
			filtersCopy['frames'] = [[minFrame, maxFrame]]
			fileCopy.selectData(filtersCopy)
			xAxisValues[index], weightedAverages[index], na = fileCopy.getWeightedAverageCorr(propertyName1, propertyName2, settings = settings)
			index += 1

		return xAxisValues, weightedAverages


	#plots weightedAverageCorrTemporalScan
	def plotWeightedAverageCorrTemporalScan(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = self.fileName + ', weightedAverageCorrTemporalScan of ' + propertyName1 + ' and ' + propertyName2 + ' ' + settings['title']
		if settings['newFig']: fig = constructFig(self, plotTitle)

		P.xlabel(axesLabels[propertyName1])
		P.ylabel(axesLabels[propertyName2])

		#get the data
		xAxisValues, weightedAverages = self.weightedAverageCorrTemporalScan(propertyName1, propertyName2, settings = settings)

		#add each temporal bin weightedAverageCorr values to plot
		for plotIndex in range(0, len(xAxisValues)):
			minFrame = settings['startFrame'] + plotIndex * settings['frameInterval']
			maxFrame = settings['startFrame'] + (plotIndex + 1) * settings['frameInterval']
			xValues = xAxisValues[plotIndex]
			yValues = weightedAverages[plotIndex]
			P.plot(xValues, yValues, label = ('frames ' + str(minFrame) + ' to ' + str(maxFrame)))
		if settings['legend'] == True: P.legend(loc = settings['legendLoc'], prop = {'size': 9})

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	#get bins for propertyNameToScan, and for each of those bins,
	#get histogram of propertyNameToFocus
	#e.g. for multiple xStartPos bins, get histogram values of directionality for each bin
	def histogramScan(self, propertyNameToScan, propertyNameToFocus, settings = TCG.PlotDefaults):
		allHistogramValues = {}
		allHistogramBincenters = {}
		allHistogramLabels = {}
		index = 0

		#for each frameBin, getHistogram
		binValSettingsArray = propertyNameToScan + 'Bins'; 
		binArray = settings[binValSettingsArray]
		if type(binArray) == int:
			minValueProperty = 0
			maxValueProperty = max(self.d[propertyNameToScan])
			binArray = np.linspace(minValueProperty, maxValueProperty, 1+binArray)


		for binIndex in range(0, len(binArray)-1):
			minVal = binArray[binIndex]
			maxVal = binArray[binIndex+1]
			#copy data
			fileCopy = []
			fileCopy = deepcopy(self)
			#select new frames
			filtersCopy = TCG.DefaultFilters.copy()
			filtersCopy[propertyNameToScan] = [[minVal, maxVal]]
			fileCopy.selectData(filtersCopy)
			plotInstance = settings.copy()
			plotInstance['title'] = '%s %.2f to %.2f' % (propertyNameToScan, minVal, maxVal)
			try:
				fileCopy.plotBinDataSummary(propertyNameToFocus, settings = plotInstance)
				fileCopy.getNumbers(propertyNameToFocus, settings = plotInstance)
			except:
				continue

			y, bincenters = fileCopy.getHistogram(propertyNameToFocus, settings)
			newY = []
			if settings['percent']:
				for i in range(0, len(y)):
					newY.append(100 * y[i] / len(fileCopy.tracks))
			if newY: y = newY

			allHistogramValues[index] = y
			allHistogramBincenters[index] = bincenters
			allHistogramLabels[index] = "%s %.1f to %.1f" % (propertyNameToScan, minVal, maxVal)
			newY = []
			index += 1
		
		P.close()
		return allHistogramValues, allHistogramBincenters, allHistogramLabels


	#plots histogramScan
	def plotHistogramScan(self, propertyNameToFocus, propertyNameToScan, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = "%s, histograms of %s scanned by %s, %s" % (self.fileName, propertyNameToFocus, propertyNameToScan, settings['title'])
		if settings['newFig']: fig = constructFig(self, plotTitle)

		normStr = {True : "normalized count", False : "count"}
		P.ylabel(normStr[settings['norm']])
		if settings['percent']:
			P.ylabel("% of cells within select xStartPos range")
		P.xlabel(axesLabels[propertyNameToFocus])

		y, bincenters, labels = self.histogramScan(propertyNameToFocus, propertyNameToScan, settings = settings)
		#histogram generation
		for i in range(0, len(y)):
			P.plot(bincenters[i], y[i],'-', label = labels[i])
		if settings['legend']:
			P.legend(loc = settings['legendLoc'], prop = {'size': 9})

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	#for each range of frames, get histograms of propertyName
	def histogramTemporalScan(self, propertyName, settings = TCG.PlotDefaults):
		allHistogramValues = {}
		allHistogramBincenters = {}
		allHistogramLabels = {}
		index = 0

		#for each frameBin, getHistogram
		for frame in range(settings['startFrame'], settings['endFrame'], settings['frameInterval']):
			minFrame = frame
			maxFrame = frame + settings['frameInterval']
			#copy data
			fileCopy = []
			fileCopy = deepcopy(self)
			#select new frames
			filtersCopy = TCG.DefaultFilters.copy()
			filtersCopy['frames'] = [[minFrame, maxFrame]]
			fileCopy.selectData(filtersCopy)
			y, bincenters = fileCopy.getHistogram(propertyName, settings)
			allHistogramValues[index] = y
			allHistogramBincenters[index] = bincenters
			allHistogramLabels[index] = 'frames ' + str(minFrame) + ' to ' + str(maxFrame)
			index += 1
			
		return allHistogramValues, allHistogramBincenters, allHistogramLabels


	#plots histogramTemporalScan
	def plotHistogramTemporalScan(self, propertyName, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = self.fileName + ', ' + propertyName + ', temporal histogram' + settings['title']
		if settings['newFig']: fig = constructFig(self, plotTitle)

		normStr = {True : "normalized count", False : "count"}

		P.ylabel(normStr[settings['norm']])
		P.xlabel(axesLabels[propertyName])

		y, bincenters, labels = self.histogramTemporalScan(propertyName, settings = settings)
		#histogram generation
		for i in range(0, len(y)):
			P.plot(bincenters[i], y[i],'-', label = labels[i])
		if settings['legend']:
			P.legend(loc = settings['legendLoc'], prop = {'size': 9})

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	#plots general temporal analysis. not dynamic
	def temporalHistogramAnalysis(self, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = self.fileName + ', full temporal histogram analysis ' + settings['title']
		P.figure(figsize = (24.0, 5.0))
		fig = constructFig(self, plotTitle)

		setInst = settings.copy()
		setInst['save'] = False
		setInst['newFig'] = False

		P.subplot(1,3,1)
		ax1 = self.plotHistogramTemporalScan('velocity', settings = setInst)	

		setInst['legend'] = False

		P.subplot(1,3,2)
		ax2 = self.plotHistogramTemporalScan('avgMov', settings = setInst)

		P.subplot(1,3,3)
		ax3 = self.plotHistogramTemporalScan('directionality', settings = setInst)

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	#plots general spatialTemporalAnalysis. not dynamic
	def spatialTemporalAnalysis(self, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = self.fileName + ', spatial temporal analysis ' + settings['title']
		P.figure(figsize = (16.0, 10.0))
		if settings['newFig']: fig = constructFig(self, plotTitle)
			
		setInst = settings.copy()
		setInst['save'] = False
		setInst['newFig'] = False

		#plot temporal scan
		P.subplot(2,2,1)
		ax1 = self.plotWeightedAverageCorrTemporalScan('xStartPos', 'velocity', settings = setInst)

		setInst['legend'] = False

		P.subplot(2,2,2)
		ax2 = self.plotWeightedAverageCorrTemporalScan('xStartPos', 'avgMov', settings = setInst)

		P.subplot(2,2,3)
		ax3 = self.plotWeightedAverageCorrTemporalScan('xStartPos', 'directionality', settings = setInst)

		P.subplot(2,2,4)
		ax3 = self.plotWeightedAverageCorrTemporalScan('avgMov', 'directionality', settings = setInst)

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	#3d plot of 3 propertyNames. if movie==True in settings, saves frames of rotating plot
	def plot3d(self, propertyName1, propertyName2, propertyName3, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = self.fileName + ', ' + propertyName1 + " " + propertyName2 + " " + propertyName3 + ' 3dplot' + ' ' + settings['title']
		if settings['newFig']: fig = constructFig(self, plotTitle)
		
		ax = Axes3D(fig)
		ax.scatter(self.d[propertyName1], self.d[propertyName2], self.d[propertyName3], marker='o', s=20, c="goldenrod", alpha=0.6)
		ax.set_xlabel(propertyName1)
		ax.set_ylabel(propertyName2)
		ax.set_zlabel(propertyName3)

		if settings['movie'] == True:
			for ii in range(settings['rotStartAngle'],settings['rotEndAngle'],settings['rotResolution']):
				ax.view_init(elev=10., azim=ii)
				if settings['save']:
					savePlot(fig, plotTitle + ' ' + str(ii))
		else:
			ax.view_init(elev=10., azim=settings['rotStartAngle'])
			if settings['save']:
				savePlot(fig, plotTitle)

		return P


	#generates heatmap movie of all tracks in experiment, where each dot is placed
	#at xStartPos. colors represent propertyName values of each track
	def cellVisualization(self, propertyName, settings = TCG.PlotDefaults):
		print('Generating movie for ' + self.fileName)

		Blues = P.get_cmap('jet')
		xPositionsAllFrames = []
		yPositionsAllFrames = []
		propertyAllFrames = []

		#for each frame
		for frame in range(settings['startFrame'], settings['endFrame'], settings['frameInterval']):
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
		#	maxXPos = 10000
		#	maxYPos = 10000

		frameIndex = 0
		for xFrame, yFrame, cFrame in zip(xPositionsAllFrames, yPositionsAllFrames, propertyAllFrames):
			plotTitle = self.fileName + ' movie of ' + propertyName + ', Frame ' + str(settings['startFrame'] + frameIndex) + ' ' + settings['title']
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
			frameIndex += settings['frameInterval']
		return


	def heatmapVisualization(self, xPropertyName, yPropertyName, colorPropertyName, settings = TCG.PlotDefaults):
		print('Generating movie for ' + self.fileName)

		plotTitle = "%s x=%s y=%s c=%s heatmap %s" % (self.fileName, xPropertyName, yPropertyName, colorPropertyName, settings['title'])
		fig = constructFig(self, plotTitle)

		cm = P.get_cmap(TCG.ColorMapPropertyDict[colorPropertyName])
		xPositionsAllFrames = []
		yPositionsAllFrames = []
		propertyAllFrames = []
		sc = P.scatter(self.d[xPropertyName], self.d[yPropertyName], c = self.d[colorPropertyName], vmin = axesLimits[colorPropertyName][0], vmax = axesLimits[colorPropertyName][1], s = 35, cmap = cm)
		P.colorbar(sc)

		maxXPos = max(self.d[xPropertyName])
		maxYPos = max(self.d[yPropertyName])
		minXPos = min(self.d[xPropertyName])
		minYPos = min(self.d[yPropertyName])
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


	#ugly function for getting excel sheets of data. not dynamic
	def getNumbers(self, propertyName, settings = TCG.PlotDefaults):
		#bins = settings['bins']
		directs = []
		directsStd = []
		avgMovs = []
		avgMovsStd = []
		vels = []
		velsStd = []
		count = []
		printBins = []

		bins = settings[propertyName + 'Bins']
		if type(bins) == int:
			maxBin = max(self.d[propertyName])
			bins = np.arange(0, maxBin, maxBin/bins)

		for index in range(len(bins) - 1):
			minVal = bins[index]
			maxVal = bins[index+1]
			filters = TCG.DefaultFilters.copy()
			filters[propertyName] = [[minVal, maxVal]]

			copy = deepcopy(self)
			copy.selectData(filters)
			wAvg1, stdDev1, stdErr1 = copy.getWeightedAverage('directionality')
			wAvg2, stdDev2, stdErr2 = copy.getWeightedAverage('avgMov')
			wAvg3, stdDev3, stdErr3 = copy.getWeightedAverage('velocity')

			directs.append(wAvg1)
			directsStd.append(stdErr1)
			avgMovs.append(wAvg2)
			avgMovsStd.append(stdErr2)
			vels.append(wAvg3)
			velsStd.append(stdErr3)
			count.append(len(copy.d[propertyName]))
			printBins.append([minVal, maxVal])


		workbook = xlsxwriter.Workbook(TCG.SAVE_DIRECTORY + self.fileName + " " + propertyName + " " + settings['title'] + '.xlsx',  {'nan_inf_to_errors': True})
		worksheet = workbook.add_worksheet()
		colindex = 0
		rowindex = 0

		worksheet.write(rowindex, colindex, 'histogram of ' + propertyName + " " + settings['title'])

		rowindex = 2

		worksheet.write(rowindex, colindex, 'bins')
		worksheet.write(rowindex, colindex+1, 'trackCount')
		worksheet.write(rowindex, colindex+2, 'count %')
		worksheet.write(rowindex, colindex+3, 'wAvg, stdErr...')
		worksheet.write(rowindex, colindex+4, 'mp')
		worksheet.write(rowindex, colindex+5, 'mpStdErr')
		worksheet.write(rowindex, colindex+6, 'avgMov')
		worksheet.write(rowindex, colindex+7, 'avgMovStdErr')
		worksheet.write(rowindex, colindex+8, 'vel')
		worksheet.write(rowindex, colindex+9, 'velStdErr')

		rowindex = rowindex + 1

		for b, d, d1, a, a1, v, v1, c in zip(printBins, directs, directsStd, avgMovs, avgMovsStd, vels, velsStd, count):
			
			if b: worksheet.write(rowindex, colindex, str(b))
			if c: worksheet.write(rowindex, colindex+1, c)
			if c: worksheet.write(rowindex, colindex+2, 100 * c / len(self.d[propertyName]))
			if d: worksheet.write(rowindex, colindex+4, d)
			if d1: worksheet.write(rowindex, colindex+5, d1)
			if a: worksheet.write(rowindex, colindex+6, a)
			if a1: worksheet.write(rowindex, colindex+7, a1)
			if v: worksheet.write(rowindex, colindex+8, v)
			if v1: worksheet.write(rowindex, colindex+9, v1)
			rowindex = rowindex + 1

		completeDirWeightedAvg, stdDev, stdErr1 = self.getWeightedAverage('directionality', settings = settings);
		completeAvgMovWeightedAvg, stdDev, stdErr2 = self.getWeightedAverage('avgMov', settings = settings);
		completeVelocityWeightedAvg, stdDev, stdErr3 = self.getWeightedAverage('velocity', settings);

		rowIndex = rowindex

		worksheet.write(rowIndex+3, 0, 'wAvg dir over exp')
		worksheet.write(rowIndex+4, 0, completeDirWeightedAvg)
		worksheet.write(rowIndex+5, 0, 'stdErr')
		worksheet.write(rowIndex+6, 0, stdErr1)
		worksheet.write(rowIndex+3, 1, 'wAvg avgMov over exp')
		worksheet.write(rowIndex+4, 1, completeAvgMovWeightedAvg)
		worksheet.write(rowIndex+5, 1, 'stdErr')
		worksheet.write(rowIndex+6, 1, stdErr2)
		worksheet.write(rowIndex+3, 2, 'wAvg Vel over exp')
		worksheet.write(rowIndex+4, 2, completeVelocityWeightedAvg)
		worksheet.write(rowIndex+5, 2, 'stdErr')
		worksheet.write(rowIndex+6, 2, stdErr3)

		workbook.close()
		return



		#TrackFile

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
		self.filters = TCG.DefaultFilters
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


	def selectData(self, filters = TCG.DefaultFilters):
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
	def plotWeightedAverageCorr(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
		#plot info
		plotTitle = 'wAvgCorr comp of ' + propertyName1 + ' and ' + propertyName2 + ', weight = ' + settings['weight'] + settings['title']
		if settings['newFig']: fig = constructFig(self, plotTitle)
			
		P.xlabel(axesLabels[propertyName1])
		P.ylabel(axesLabels[propertyName2])

		for experiment in sorted(self.experiments.items()):
			xAxisValues, weightedAverages, na = experiment[1].getWeightedAverageCorr(propertyName1, propertyName2, settings = settings)
			P.plot(xAxisValues, weightedAverages, label = experiment[0])
			
		if settings['legend']: P.legend(loc = settings['legendLoc'], prop = {'size': 9})
		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)
		return P


	#general summary of weightedAvgCorrelations. not dynamic
	def plotWeightedAverageCorrSummary(self, settings = TCG.PlotDefaults):
		
		vprint('Plotting weightedAverageCorr experiment comparisons.')

		plotTitle = 'weightedAvg Corr Summary ' + settings['title']
		P.figure(figsize = (16.0, 10.0))
		if settings['newFig']: fig = constructFig(self, plotTitle)

		setInst = settings.copy()
		setInst['newFig'] = False
		setInst['show'] = False
		setInst['save'] = False

		P.subplot(2,2,1)
		ax1 = self.plotWeightedAverageCorr('xStartPos', 'velocity', settings = setInst)

		setInst['legend'] = False

		P.subplot(2,2,2)
		ax2 = self.plotWeightedAverageCorr('xStartPos', 'avgMov', settings = setInst)
		
		P.subplot(2,2,3)
		ax3 = self.plotWeightedAverageCorr('xStartPos', 'directionality', settings = setInst)

		P.subplot(2,2,4)
		ax4 = self.plotWeightedAverageCorr('avgMov', 'directionality', settings = setInst)

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
		ax1 = self.plotWeightedAverageCorr('xStartPos', 'velocity', settings = setInst)

		P.subplot(2,2,2)
		setInst['legend'] = False
		ax2 = self.plotWeightedAverageCorr('xStartPos', 'avgMov', settings = setInst)

		P.subplot(2,2,3)
		ax3 = self.plotWeightedAverageCorr('xStartPos', 'directionality', settings = setInst)

		P.subplot(2,2,4)
		ax4 = self.plotWeightedAverageCorr('avgMov', 'directionality', settings = setInst)

		if settings['show']: P.show()
		if settings['save']: savePlot(fig, plotTitle)

