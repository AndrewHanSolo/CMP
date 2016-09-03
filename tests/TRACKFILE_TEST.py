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

#DATA IMPORT AND SAVE PATHS
ALL_EXP_FOLDER_PATH = '/home/ahan/Desktop/track files/Nov experiments data/'
DATA_SAVE_NAME      = '/home/ahan/Desktop/CMP/data/test'

#TEST MODULES
SAVE                      = True
TrackFile_Test            = True
TrackFolder_Test          = True

#TEST BOOLS
TEST_writeData            = True
TEST_plotScatter          = True
TEST_plotBinData          = True
TEST_plotHistogram        = True
TEST_plotPercentHistogram = True
TEST_scan                 = True
TEST_cellVisualization    = True
TEST_heatmapVisualization = True
TEST_comparePlots         = True
TEST_iterate              = True
TEST_individual           = True


###############################################
#BEGIN TEST SCRIPT#############################
###############################################

#SAVE DATA
if SAVE is True:
	data = importAndSave(ALL_EXP_FOLDER_PATH, DATA_SAVE_NAME)

#LOAD DATA
with open(DATA_SAVE_NAME, 'rb') as input:
	data = pickle.load(input)

	#SELECT FILTERS
	filters = {}
	#filters['frames'] = [[40, 50], [60, 70]]
	filters['frames'] = [[30, float('inf')]]
	filters['age'] = [[40, float('inf')]]
	#filters['xPos'] = [[0, 3000],[6000, 10000]]
	#filters['yPos'] = [[200, 500]]

	#SELECT SETTINGS
	ps = TCG.PlotDefaults.copy()
	ps["show"] = False
	#ps["colorSettings"] = { "vmin": 20, "vmax": 40, "separation": 10, "colorMap": "jet"}

	#FILTER DATA
	data.selectData(filters)

#################################
#FOR INDIVIDUAL TRACKFILE TESTING
if TrackFile_Test:

	workbook = xlsxwriter.Workbook(TCG.SAVE_DIRECTORY + "fileTest.xlsx", {'nan_inf_to_errors': True, 'in_memory': True})

	for experiment, v in sorted(data.experiments.items()):
		print("Experiment:", experiment)
		print("Track Count: ", len(v.tracks))

		if TEST_writeData:
			writeData(v, workbook, "")

		if TEST_plotScatter:
			v.plotScatter("firstFrame", "age")
			v.plotScatter("xStartPos", "yStartPos")
			v.plotScatter("xEndPos", "directionality")

		if TEST_plotBinData:
			v.plotBinData("xStartPos", "avgMov", ps, workbook = [workbook, experiment, True])
			v.plotBinData("age", "directionality", ps)
			v.plotBinData("avgMov", "velocity", ps)

		if TEST_plotHistogram:
			v.plotHistogram("xStartPos")
			v.plotHistogram("firstFrame")
			v.plotHistogram("avgMov")

		if TEST_plotPercentHistogram:
			v.plotPercentHistogram("directionality", "avgMov", ps, workbook = [workbook, experiment, True])
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

		if TEST_cellVisualization:
			v.cellVisualization("avgMov", 10, ps)

		if TEST_heatmapVisualization:
			v.heatmapVisualization("xStartPos", "yStartPos", "avgMov", ps)

		if TEST_individual:
			print("") #syntax requires statement within conditional

	workbook.close()

########################
#FOR TRACKFOLDER TESTING
if TrackFolder_Test:

	workbook = xlsxwriter.Workbook(TCG.SAVE_DIRECTORY + "foldTest.xlsx", {'nan_inf_to_errors': True, 'in_memory': True})

	if TEST_writeData:
		data.writeData()
		
	if TEST_comparePlots:
		data.comparePlots(TrackFile.plotHistogram, "avgMov", None, ps)
		data.comparePlots(TrackFile.plotBinData, "avgMov", "velocity", ps)
		data.comparePlots(TrackFile.plotScatter, "avgMov", "velocity", ps)

	if TEST_iterate:
		data.iterate(TrackFile.plotScatter, "firstFrame", "age", ps)
		data.iterate(TrackFile.plotHistogram, "xStartPos", None, ps)
		data.iterate(TrackFile.plotPercentHistogram, "directionality", "avgMov", ps)
		data.iterate(TrackFile.scan, "xStartPos", 0, 10000, 5, TrackFile.plotScatter, "avgMov", "directionality", ps)
		data.iterate(TrackFile.cellVisualization, "avgMov", 10, ps)
		data.iterate(TrackFile.heatmapVisualization, "xStartPos", "yStartPos", "avgMov", ps)

	if TEST_individual:
		#data.iterate(TrackFile.heatmapVisualization, "xStartPos", "yStartPos", "avgMov", ps)
		data.iterate(TrackFile.plotHistogram, "xStartPos", None, ps, [workbook, "hist", True])
		data.comparePlots(TrackFile.plotHistogram, "avgMov", None, ps)


	workbook.close()

