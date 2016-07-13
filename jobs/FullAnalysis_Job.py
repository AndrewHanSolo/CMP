#Lindsay_Job1 - analysis script
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
from enum import Enum
from matplotlib import *



def fullAnalysis(DATA_SAVE_NAME, PATH = 0, filters = TCG.DefaultFilters, ps = TCG.PlotDefaults, funcs = TCG.AnalysisDefaults):

	#save data from folder path if given
	if PATH:
		data = importAndSave(PATH, DATA_SAVE_NAME)

	vprint('Starting Analysis of %s...' %(DATA_SAVE_NAME))

	####################################
	#LOAD DATA
	with open(DATA_SAVE_NAME, 'rb') as input:
		data = pickle.load(input)

		data.selectData(filters)

		keyProperty1 = 'avgMov'
		keyProperty2 = 'velocity'
		keyProperty3 = 'directionality'
		keyProperty4 = 'mp'
		properties = [keyProperty1, keyProperty2, keyProperty3, keyProperty4]

		if funcs['writeData']:
			data.writeData(ps)

		if funcs['histogramTemporalAnalysis']:
			data.histogramTemporalAnalysis(ps)

		if funcs['spatioTemporalAnalysis']:
			data.spatialTemporalAnalysis(ps)

		if funcs['plotWeightedAverageCorrSummary']:
			data.plotWeightedAverageCorrSummary(ps)

		if funcs['comparisonAnalysis']:
			data.comparisonAnalysis(ps)	

		for experiment, v in sorted(data.experiments.items()):

			if funcs['heatMaps']:
				v.heatmapVisualization('xStartPos', 'yStartPos', 'avgMov', ps)
				v.heatmapVisualization('xStartPos', 'yStartPos', 'directionality', ps)	
				v.heatmapVisualization('avgMov', 'velocity', 'directionality', ps)	
				v.heatmapVisualization('xStartPos', 'avgMov', 'directionality', ps)
				v.heatmapVisualization('age', 'avgMov', 'directionality', ps)	

			if funcs['plotScatter']:
				v.plotScatter(keyProperty1, keyProperty3)
				v.plotScatter('age', keyProperty2)
				v.plotScatter('age', keyProperty3)
				v.plotScatter('xStartPos', keyProperty2)
				v.plotScatter(keyProperty2, keyProperty3)

			if funcs['weightedAverageCorr']:
				v.plotWeightedAverageCorr('xStartPos', 'avgMov', ps)
				v.plotWeightedAverageCorr('xStartPos', 'velocity', ps)
				v.plotWeightedAverageCorr('xStartPos', 'directionality', ps)

			if funcs['binDataSummary']:
				v.plotBinDataSummary('xStartPos', ps)
				v.plotBinDataSummary('avgMov', ps)
				v.plotBinDataSummary('directionality', ps);

			if funcs['histogramScan']:
				v.histogramScan('xStartPos', 'avgMov', ps)
				v.histogramScan('xStartPos', 'directionality', ps)
				v.histogramScan('avgMov', 'directionality', ps)





