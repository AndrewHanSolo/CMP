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
	P.xlabel((self.fields[propertyName]).axisLabel[propertyName])
	P.ylabel("count")

	P.subplot(2,3,2)
	ax2 = P.hist(self.d['avgMov'], bins = 15)
	P.xlabel((self.fields[propertyName]).axisLabel['avgMov'])
	P.ylabel("count")

	P.subplot(2,3,3)
	ax3 = P.hist(self.d['velocity'], bins = 15)	
	P.xlabel((self.fields[propertyName]).axisLabel['velocity'])
	P.ylabel("count")

	P.subplot(2,3,4)
	P.title("wAvgs,stdErr of each dir bin")
	ax4 = self.plotBinData(propertyName, 'directionality', bins = bins, settings = setInst)
	P.ylim([-1, 1])

	P.subplot(2,3,5)
	ax5 = self.plotBinData(propertyName, 'avgMov', bins = bins, settings = setInst)	
	P.ylim([0, 40])

	P.subplot(2,3,6)
	ax6 = self.plotBinData(propertyName, 'velocity', bins = bins, settings = setInst)	
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
	ax1 = P.hist(self.d['directionality'], bins = settings['directionalityBins'])

	P.subplot(1,3,2)
	ax2 = P.hist(self.d['avgMov'], bins = settings['avgMovBins'])

	P.subplot(1,3,3)
	ax3 = P.hist(self.d['velocity'], bins = settings['velocityBins'])	

	if settings['show']: P.show()
	if settings['save']: savePlot(fig, plotTitle)
	return P








TC.TrackFile.plotBinDataSummary = plotBinDataSummary;
TC.TrackFile.plotHistogramSummary = plotHistogramSummary;



####################################