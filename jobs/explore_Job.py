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
from PlotScripts import *

SAVE = True

ALL_EXP_FOLDER_PATH = "C:\\Users\Andrew Han\\Desktop\\track files\select fibers/"
DATA_SAVE_NAME = 'nanofiberDiameter'

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
	ps['directionalityBins'] = [-1, -0.6, -0.3, -0.1, 0.1, 0.3, 0.6, 1]
	ps['xStartPosBins'] = 5
	ps['mpBins'] = np.linspace(0, 1, 6)
	#ps['norm'] = True

	data.selectData(filters)
	data.writeData()

	#HOW YOU CAN ACCESS INDIVIDUAL EXPERIMENT FILES
	#v1 = data.experiments['VEGF0_10']
	#v1.plotBinData('xStartPos', 'directionality', ps)


	#data.histogramTemporalAnalysis(ps)
	#data.spatialTemporalAnalysis(ps)
	data.plotBinDataSummary(ps)
	data.comparisonAnalysis(ps)
	#data.cellVisualization('mp', ps)

	P.close()

	for experiment, v in data.experiments.items():
		#v.plotBinData('age', 'velocity')
		#v.plotScatter('age', 'velocity')
		v.plotScatter('xStartPos', 'velocity')
		#v.plotBinData('yStartPos', 'velocity')

		#plotBinDataSummary(v, 'directionality', ps)
		#v.plotBinData('xStartPos', 'directionality', ps)

		#plotBinDataSummary(v, 'xStartPos', ps);
		#v.histogramScan('directionality', 'xStartPos', ps)
		#v.histogramScan('directionality', 'concentration', ps)

		P.close()




