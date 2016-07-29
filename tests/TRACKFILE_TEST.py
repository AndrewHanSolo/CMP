#File for testing all TrackFile and TrackFolder functions

import sys
sys.path.insert(0, './../lib')
sys.path.insert(0, './../data')
sys.path.insert(0, './../tests')
sys.path.insert(0, './../jobs')

from TrackClass import *
from general import *
import _pickle as pickle
from copy import deepcopy
import pylab as P
import numpy as np
from scipy import stats
import csv
import xlsxwriter
from scipy import stats
import TrackClassGlobals as TCG
from mpl_toolkits.mplot3d import Axes3D
from PlotScripts import *

SAVE                = False
TrackFile_Test      = True
TrackFolder_Test    = False
ALL_EXP_FOLDER_PATH = '/home/ahan/Desktop/track files/Nov experiments data/'
DATA_SAVE_NAME      = '/home/ahan/Desktop/CMP/data/test'

#TEST BOOLS
TEST_plotBinData = True
TEST_writeData = True
TEST_plotScatter = True
TEST_plotBinData = True
TEST_plotHistogram = True
TEST_plotPercentHistogram = True
TEST_scan = True

#SAVE DATA
if SAVE is True:
	data = importAndSave(ALL_EXP_FOLDER_PATH, DATA_SAVE_NAME)


#LOAD DATA
with open(DATA_SAVE_NAME, 'rb') as input:
	data = pickle.load(input)

	#SELECT FILTERS
	filters = {}
	filters["frames"] = [[30, float('inf')]]
	filters['age'] = [[40, float('inf')]]

	#SELECT SETTINGS
	ps = TCG.PlotDefaults.copy()
	ps["show"] = False


	#FILTER DATA
	data.selectData(filters)


#FOR INDIVIDUAL TRACKFILE TESTING
if TrackFile_Test:

	for experiment, v in data.experiments.items():

		if TEST_writeData:
			v.writeData()

		if TEST_plotScatter:
			v.plotScatter("firstFrame", "age")
			v.plotScatter("xStartPos", "yStartPos")
			v.plotScatter("xEndPos", "directionality")

		if TEST_plotBinData:
			v.plotBinData("xStartPos", "avgMov", ps)
			v.plotBinData("age", "directionality", ps)
			v.plotBinData("avgMov", "velocity", ps)

		if TEST_plotHistogram:
			v.plotHistogram("xStartPos")
			v.plotHistogram("firstFrame")
			v.plotHistogram("avgMov")

		if TEST_plotPercentHistogram:
			v.plotPercentHistogram("directionality", "avgMov", ps)
			v.plotPercentHistogram("age", "xStartPos", ps)
			v.plotPercentHistogram("mp", "yStartPos", ps)

		if TEST_scan:
			v.scan("xStartPos", 0, 10000, 5, TrackFile.plotScatter, "avgMov", "directionality", ps)
			v.scan("frames", 0, 100, 5, TrackFile.plotScatter, "firstFrame", "age", ps)
			v.scan("xPos", 0, 10000, 5, TrackFile.plotScatter, "xStartPos", "avgMov", ps)
			v.scan("xPos", 0, 10000, 5, TrackFile.plotBinData, "age", "firstFrame", ps)
			v.scan("frames", 0, 100, 10, TrackFile.plotBinData, "xStartPos", "avgMov", ps)
			v.scan("xStartPos", 0, 10000, 4, TrackFile.plotBinData, "avgMov", "directionality", ps)
			v.scan("xStartPos", 0, 10000, 5, TrackFile.plotHistogram, "avgMov", None, ps)
			v.scan("avgMov", 0, 10000, 5, TrackFile.plotHistogram, "directionality", None, ps)
			v.scan("firstFrame", 0, 10000, 5, TrackFile.plotHistogram, "age", None, ps)

		#P.scatter(v.d['xStartPos'], v.d['yStartPos'])
		#function = TrackFile.plotCurve(, "xStartPos", "avgMov")
		#v.writeData()
		
		#v.iterate('frames', 30, 70, 10, TrackFile.heatmapVisualization, "xStartPos", "yStartpos", "avgMov", ps)
		#v.scan('xStartPos', 0, 11000, 4, TrackFile.plotBinData, "avgMov", "directionality", ps)
		#v.scan('frames', 0, 100, 10, TrackFile.plotBinData, "xStartPos", "avgMov", ps)
		#v.scan('frames', 30, 70, 10, TrackFile.plotScatter, "firstFrame", "avgMov", ps)
		#v.scan('xStartPos', 0, 10000, 3, TrackFile.plotHistogram, "avgMov", None, ps)
		#v.scan('xStartPos', 0, 10000, 5, TrackFile.plotHistogram, "avgMov", ps)
		#v.scan('xPos', 0, 10000, 5, TrackFile.plotBinData, "avgMov", "directionality", ps)
		#v.cellVisualization('avgMov')
		#v.heatmapVisualization('xStartPos', 'yStartPos', 'avgMov')
		#v.plotPercentHistogram('directionality', 'avgMov')
		#3D PLOTS
		#fig = plt.figure()
		#ax = fig.gca(projection='3d')
		#ax.plot_trisurf(avgMovVals, velocityVals, directionalityVals, cmap = cm.jet)
		#ax.scatter(avgMovVals, velocityVals, directionalityVals)

		# CMP PLOTS
		#v.plotBinData('xStartPos', 'avgMov', ps)
		#v.plotBinDataSummary('xStartPos', ps)
		#v.plotHistogram('directionality', ps)
		#v.plotHistogramSummary(ps)
		#v.plotBinData('xStartPos', 'directionality', ps)
		#v.plotBinData('xStartPos', 'velocity', ps)
		#v.plotBinData('xStartPos', 'avgMov', ps)
		#v.plotScatter('directionality', 'avgMov', ps)
		#v.plotPercentHistogram('directionality', 'avgMov', ps)
		#v.plotBinDataTemporalScan('xStartPos', 'avgMov', ps)
		#v.plotHistogramScan('directionality', 'avgMov', ps)
		#v.plotHistogramTemporalScan('directionality', ps)
		#v.temporalHistogramAnalysis(ps)
		#v.spatialTemporalAnalysis(ps)
		#v.plot3d('xStartPos', 'directionality', 'avgMov', ps)
		#v.cellVisualization('directionality', ps)
		#v.scatterVisualization('xStartPos', 'avgMov', ps)
		#v.getNumbers('directionality', ps)
		
		P.show()
		#P.close()
		break 		#to test only one function



#FOR TRACKFOLDER TESTING
#if TrackFolder_Test:

	#data.histogramTemporalAnalysis(ps)
	#data.spatialTemporalAnalysis(ps)
	#data.histogramSummary(ps)
	#data.cellVisualization('avgMov', ps)
	#data.plotScatter('xStartPos', 'avgMov', ps)
	#data.scatterVisualization('xStartPos', 'avgMov', ps)
	#data.plotBinData('xStartPos', 'avgMov', ps)
	#data.plotBinDataSummary(ps)
	#data.plotHistograms('avgMov', ps)
	#data.comparisonAnalysis(ps)






