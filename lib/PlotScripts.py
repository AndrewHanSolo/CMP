###Holds static plot scripts.

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
from matplotlib.ticker import FuncFormatter
import xlsxwriter
import _pickle as pickle

####################################
#TrackFile

#plots several plotBinData plots in one figure. not dynamic
#propertyName is for first histogram plot and bins for plotBinData functions
def plotBinDataSummary(trackFile, propertyName, settings = TCG.PlotDefaults):
	#plot info
	plotTitle = "%s, %s dir bin analysis %s" % (trackFile.fileName, propertyName, settings['title'])
	P.figure(figsize = (24.0, 10.0))
	fig = constructFig(trackFile, plotTitle)

	setInst = settings.copy()
	setInst['save'] = False
	setInst['newFig'] = False

	if type(settings[propertyName + 'Bins']) == int:
		no, bins = np.histogram(trackFile.d[propertyName], bins = settings[propertyName + 'Bins'])
	else:
		bins = settings[propertyName + 'Bins']

	P.subplot(2,3,1)
	ax1 = P.hist(trackFile.d[propertyName], bins = bins)
	P.title("histograms")
	P.xlabel((trackFile.fields[propertyName]).axisLabel[propertyName])
	P.ylabel("count")

	P.subplot(2,3,2)
	ax2 = P.hist(trackFile.d['avgMov'], bins = 15)
	P.xlabel((trackFile.fields[propertyName]).axisLabel['avgMov'])
	P.ylabel("count")

	P.subplot(2,3,3)
	ax3 = P.hist(trackFile.d['velocity'], bins = 15)	
	P.xlabel((trackFile.fields[propertyName]).axisLabel['velocity'])
	P.ylabel("count")

	P.subplot(2,3,4)
	P.title("wAvgs,stdErr of each dir bin")
	ax4 = trackFile.plotBinData(propertyName, 'directionality', bins = bins, settings = setInst)
	P.ylim([-1, 1])

	P.subplot(2,3,5)
	ax5 = trackFile.plotBinData(propertyName, 'avgMov', bins = bins, settings = setInst)	
	P.ylim([0, 40])

	P.subplot(2,3,6)
	ax6 = trackFile.plotBinData(propertyName, 'velocity', bins = bins, settings = setInst)	
	P.ylim([0, 40])

	trackFile.getNumbers(propertyName, settings = setInst)

	if settings['show']: P.show()
	if settings['save']: savePlot(fig, plotTitle)
	return P

#plots multiple histogram plots in 1 figure. not dynamic
def plotHistogramSummary(trackFile, settings = TCG.PlotDefaults):
	#plot info
	plotTitle = "%s, histogram summary %s" % (trackFile.fileName, settings['title'])
	P.figure(figsize = (24.0, 5.0))
	fig = constructFig(trackFile, plotTitle)

	setInst = settings.copy()
	setInst['save'] = False
	setInst['newFig'] = False

	P.subplot(1,3,1)
	ax1 = P.hist(trackFile.d['directionality'], bins = settings['directionalityBins'])

	P.subplot(1,3,2)
	ax2 = P.hist(trackFile.d['avgMov'], bins = settings['avgMovBins'])

	P.subplot(1,3,3)
	ax3 = P.hist(trackFile.d['velocity'], bins = settings['velocityBins'])	

	if settings['show']: P.show()
	if settings['save']: savePlot(fig, plotTitle)
	return P







##
## { item_description }
	#plots general comparison analysis of all experiments
def comparisonAnalysis(trackFile, settings = TCG.PlotDefaults):
	#plot info
	plotTitle = 'Experiment Histogram Comparison ' + settings['title']
	P.figure(figsize = (24.0, 5.0))
	if settings['newFig']: fig = constructFig(trackFile, plotTitle)

	
	setInst = settings.copy()
	setInst['newFig'] = False
	setInst['show'] = False
	setInst['save'] = False
	setInst['legendLoc'] = 1
	
	P.subplot(1,3,1)
	ax1 = trackFile.plotHistograms('velocity', settings = setInst)

	setInst['legend'] = False

	P.subplot(1,3,2)
	ax2 = trackFile.plotHistograms('avgMov', settings = setInst)

	P.subplot(1,3,3)
	ax3 = trackFile.plotHistograms('directionality', settings = setInst)

	if settings['show']: P.show()
	if settings['save']: savePlot(fig, plotTitle)
	
	P.clf()
	P.close()


	P.figure(figsize = (16.0, 10.0))
	plotTitle = 'Experiment WeightedAvgCorr Comparison ' + settings['title']
	if settings['newFig']: fig = constructFig(trackFile, plotTitle)

	P.subplot(2,2,1)
	setInst['legend'] = True
	ax1 = trackFile.plotBinData('xStartPos', 'velocity', settings = setInst)

	P.subplot(2,2,2)
	setInst['legend'] = False
	ax2 = trackFile.plotBinData('xStartPos', 'avgMov', settings = setInst)

	P.subplot(2,2,3)
	ax3 = trackFile.plotBinData('xStartPos', 'directionality', settings = setInst)

	P.subplot(2,2,4)
	ax4 = trackFile.plotBinData('avgMov', 'directionality', settings = setInst)

	if settings['show']: P.show()
	if settings['save']: savePlot(fig, plotTitle)
##


###########TRACKFOLDER SCRIPTS
#TODO: include errorbars
def plotBinData(self, propertyName1, propertyName2, settings = TCG.PlotDefaults):
	#plot info
	plotTitle = 'wAvgCorr comp of ' + propertyName1 + ' and ' + propertyName2 + ', weight = ' + settings['weight'] + settings['title']
	if settings['newFig']: fig = constructFig(self, plotTitle)
		
	P.xlabel(cpoconfig[propertyName1])
	P.ylabel((self.fields[propertyName]).axisLabel[propertyName2])

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
	P.xlabel((self.fields[propertyName]).axisLabel[propertyName])

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


