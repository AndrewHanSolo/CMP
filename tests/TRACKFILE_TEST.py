#File for testing all TrackFile and TrackFolder functions

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
from PlotScripts import *

SAVE = False
TrackFile_Test = True
TrackFolder_Test = False

ALL_EXP_FOLDER_PATH = 'C:/Users/Andrew Han/Desktop/lindsay trackfiles/'
DATA_SAVE_NAME = 'lindsayData'

#SAVE DATA
if SAVE is True:
	data = importAndSave(ALL_EXP_FOLDER_PATH, DATA_SAVE_NAME)

####################################
#LOAD DATA
with open(DATA_SAVE_NAME, 'rb') as input:
	data = pickle.load(input)

	filters = TCG.DefaultFilters.copy()
	filters['age'] = [[5, float('inf')]]

	ps = TCG.PlotDefaults.copy()
	ps['percent'] = True
	ps['bins'] = 5
	ps['xStartPosBins'] = 5
	ps['directionalityBins'] = 5
	ps['migrationPersistenceBins'] = np.linspace(0, 1, 6)
	#ps['norm'] = True

	data.selectData(filters)



if TrackFile_Test:

	for experiment, v in data.experiments.items():
		print(experiment)
		v.plotBinDataSummary('xStartPos', ps)
		#v.plotHistogram('directionality', ps)
		#v.plotHistogramSummary(ps)
		v.plotWeightedAverageCorr('xStartPos', 'directionality', ps)
		v.plotWeightedAverageCorr('xStartPos', 'velocity', ps)
		v.plotWeightedAverageCorr('xStartPos', 'avgMov', ps)
		#v.plotScatter('directionality', 'avgMov', ps)
		#v.plotPercentHistogram('directionality', 'avgMov', ps)
		#v.plotWeightedAverageCorrTemporalScan('xStartPos', 'avgMov', ps)
		#v.plotHistogramScan('directionality', 'avgMov', ps)
		#v.plotHistogramTemporalScan('directionality', ps)
		#v.temporalHistogramAnalysis(ps)
		#v.spatialTemporalAnalysis(ps)
		#v.plot3d('xStartPos', 'directionality', 'avgMov', ps)
		#v.cellVisualization('directionality', ps)
		#v.scatterVisualization('xStartPos', 'avgMov', ps)
		#v.getNumbers('directionality', ps)

		P.close()

		break




#if TrackFolder_Test:

	#data.histogramTemporalAnalysis(ps)
	#data.spatialTemporalAnalysis(ps)
	#data.histogramSummary(ps)
	#data.cellVisualization('avgMov', ps)
	#data.plotScatter('xStartPos', 'avgMov', ps)
	#data.scatterVisualization('xStartPos', 'avgMov', ps)
	#data.plotWeightedAverageCorr('xStartPos', 'avgMov', ps)
	#data.plotWeightedAverageCorrSummary(ps)
	#data.plotHistograms('avgMov', ps)
	#data.comparisonAnalysis(ps)






