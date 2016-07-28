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

SAVE = False

ALL_EXP_FOLDER_PATH = 'C:/Users/Andrew Han/Desktop/track files/Nov experiments data/'
DATA_SAVE_NAME = 'gradient'

#SAVE DATA
if SAVE is True:
	data = importAndSave(ALL_EXP_FOLDER_PATH, DATA_SAVE_NAME)

####################################
#LOAD DATA
with open(DATA_SAVE_NAME, 'rb') as input:
	data = pickle.load(input)
	#data2 = deepcopy(data)


	filters = {}
	filters['age'] = [[5, 37]]
	filters['frames'] = [[30, float('inf')]]
	#filters['xStartPos'] = [[20, 9980]]
	#filters['xEndPos'] = [[20, 9980]]

	gps = TCG.PlotDefaults.copy()
	gps['startFrame'] = 30
	gps['endFrame'] = 70
	gps['frameInterval'] = 40

	gps['percent'] = True
	gps['bins'] = 10
	gps['directionalityBins'] = [-1, -0.6, -0.3, -0.1, 0.1, 0.3, 0.6, 1]
	gps['xStartPosBins'] = 10
	gps['mpBins'] = np.linspace(0, 1, 10)
	#gps['norm'] = True

	data.selectData(filters)

	#v1 = data.experiments['a GDNF 1 ug per cm']
	#print(v1.getWeightedAverage('velocity', gps))


	'''data.writeData()

	#HOW YOU CAN ACCESS INDIVIDUAL EXPERIMENT FILES
	#v1 = data.experiments['VEGF0_10']
	#v1.plotBinData('xStartPos', 'directionality', gps)


	data.histogramTemporalAnalysis(gps)
	data.spatialTemporalAnalysis(gps)
	data.plotBinDataSummary(gps)
	data.comparisonAnalysis(gps)
	#data.cellVisualization('velocity', gps)
	#data.cellVisualization('directionality', gps)

	P.close()'''

	#data.cellVisualization('directionality', gps)
	#data.plotBinDataSummary(gps)
	#data.comparisonAnalysis(gps)

	for experiment, v in data.experiments.items():
		#v.heatmapVisualization('xStartPos', 'yStartPos', 'directionality', gps)	
		#v.heatmapVisualization('avgMov', 'directionality', 'velocity', gps)	
		#v.heatmapVisualization('avgMov', 'directionality', 'xStartPos', gps)	

	'''for experiment, v in data.experiments.items():
		v.plotScatter('avgMov', 'directionality')
		v.totalVisualization('directionality', gps)
		v.totalVisualization('avgMov', gps)
		v.plotBinData('age', 'velocity')
		v.plotScatter('age', 'velocity')
		v.plotScatter('age', 'directionality')
		v.plotScatter('xStartPos', 'velocity')
		v.plotScatter('velocity', 'directionality')
		v.plotBinData('yStartPos', 'velocity')

		#plotBinDataSummary(v, 'directionality', gps)
		#plotBinDataSummary(v, 'velocity', gps)
		v.plotBinData('xStartPos', 'directionality', gps)

		#plotBinDataSummary('xStartPos', gps);
		v.histogramScan('directionality', 'xStartPos', gps)
		v.histogramScan('directionality', 'concentration', gps)
		v.histogramScan('velocity', 'xStartPos', gps)

		P.close()'''




