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



def Example_Job(DATA_SAVE_NAME, importpath = 0, filters = {}, ps = TCG.PlotDefaults):

	if not os.path.exists(TCG.SAVE_DIRECTORY):
		os.makedirs(TCG.SAVE_DIRECTORY)

	#save data from folder path if given
	if importpath:
		data = importAndSave(importpath, DATA_SAVE_NAME)

	vprint('Running Analysis of %s...' %(DATA_SAVE_NAME))

	####################################
	#LOAD DATA
	with open('./data/' + DATA_SAVE_NAME, 'rb') as input:
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



