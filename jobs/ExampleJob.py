"""
Helper / Example Job that is called by ExampleDriver
"""

import TrackClassGlobals as TCG
from TrackClass import *
from General import *
import _pickle as pickle
from copy import deepcopy
from matplotlib import *
import os



def Example_Job(DATA_SAVE_NAME, TRACKMATE_FOLDERNAME = None, filters = {}, ps = TCG.PlotDefaults):

	JOB_ANALYSIS_SAVE_PATH = TCG.ANALYSIS_SAVE_PATH + '/' + TCG.ANALYSIS_SAVE_NAME

	if not os.path.exists(JOB_ANALYSIS_SAVE_PATH):
		os.makedirs(JOB_ANALYSIS_SAVE_PATH)

	#save data from folder path if given
	if TRACKMATE_FOLDERNAME:
		data = importAndSave(TRACKMATE_FOLDERNAME, DATA_SAVE_NAME)

	vprint('Running Analysis of %s...' %(DATA_SAVE_NAME))

	####################################
	#LOAD DATA
	with open(TCG.DATA_SAVE_PATH + DATA_SAVE_NAME, 'rb') as input:
		data = pickle.load(input)

		data.selectData(filters)

		#create workbooks here for writing data
		percentWorkbook = createWorkbook("percentHistograms")
		binDataWorkbook = createWorkbook("binData")

		#analysis funcs
		data.writeData(ps)
		data.iterate(TrackFile.plotPercentHistogram, "velocity", "directionality", ps, [percentWorkbook, "", True])
		data.iterate(TrackFile.heatmapVisualization, "xStartPos", "yStartPos", "avgMov", ps)
		data.iterate(TrackFile.plotBinData, "xStartPos", "velocity", ps, [binDataWorkbook, "", True])
		data.iterate(TrackFile.scan, "frames", 0, 100, 10, TrackFile.plotBinData, "xStartPos", "avgMov", ps)
		data.compare(TrackFile.plotHistogram, "directionality", None, ps)
		data.compare(TrackFile.plotBinData, "xStartPos", "velocity", ps)

		#close any open workbooks
		percentWorkbook.close()
		binDataWorkbook.close()

	vprint("Done.")



