#Runs calc and plot tests on TrackFile

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

SAVE = False
ALL_EXP_FOLDER_PATH = 'C:/Users/Andrew Han/Desktop/track files/best scenario'
DATA_SAVE_NAME = 'NFs' #'lindsayData'

#SAVE DATA
if SAVE is True:
	data = importAndSave(ALL_EXP_FOLDER_PATH, DATA_SAVE_NAME)

####################################
#LOAD DATA
with open(DATA_SAVE_NAME, 'rb') as input:
	data = pickle.load(input)


	filters = TCG.DefaultFilters.copy()
	filters['frames'] = [[30, float('inf')]]
	filters['age'] = [[5, float('inf')]]
	#filters['concentration'] = [[0, 1]]

	ps = TCG.PlotDefaults.copy()
	ps['percent'] = True
	ps['bins'] = 10
	ps['directionalityBins'] = [-1, -0.6, -0.3, -0.1, 0.1, 0.3, 0.6, 1]
	ps['xStartPosBins'] = 6
	ps['migrationPersistenceBins'] = np.linspace(0, 1, 6)
	#ps['norm'] = True

	data.selectData(filters)


	#v1 = data.experiments['a GDNF 1 ug per cm']
	#v1.plotHistogramScan('directionality', 'directionality', ps)
	#v1.plotHistogramScan('directionality', 'xStartPos', ps)
	#v1.plotHistogramScan('directionality', 'concentration', ps)
	#v1.getNumbers('directionality', settings = ps)
	
	#v1.histogramScan('directionality', 'xStartPos', ps)
	#v1.histogramScan('directionality', 'concentration', ps)
	#v1.scan2D('directionality', 'concentration', ps)
	#data.spatialTemporalAnalysis(ps)
	#data.histogramTemporalAnalysis(ps)
	#data.comparisonAnalysis(ps)
	#data.cellVisualization('directionality', ps)
	#data.cellVisualization('avgMov', ps)


	for experiment, v in data.experiments.items():
		#v.plotHistogramScan('directionality', 'directionality', ps)
		#v.plotHistogramScan('directionality', 'xStartPos', ps)
		#v.plotHistogramScan('directionality', 'concentration', ps)
		v.plotScatter('xStartPos', 'velocity')
		#v.plotBinDataSummary('directionality', ps)
		#v.cellVisualization('directionality', ps)
		#v.cellVisualization('avgMov', ps)
		#v.getNumbers('directionality', settings = ps)
		#v.plotBinDataSummary('directionality', ps)
		#v.plotWeightedAverageCorr('xStartPos', 'directionality', settings = ps)
		#v.plotBinDataSummary('xStartPos', settings = ps);
		#v.histogramScan('directionality', 'xStartPos', ps)
		#v.histogramScan('directionality', 'concentration', ps)



