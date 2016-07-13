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
ALL_EXP_FOLDER_PATH = '/home/andrewhan/Desktop/analysis/nfs/'
DATA_SAVE_NAME      = './../data/gradient'

#SAVE DATA
if SAVE is True:
	data = importAndSave(ALL_EXP_FOLDER_PATH, DATA_SAVE_NAME)


#LOAD DATA
with open(DATA_SAVE_NAME, 'rb') as input:
	data = pickle.load(input)

	#SELECT FILTERS
	filters = TCG.DefaultFilters.copy()
	filters["frames"] = [[30, float('inf')]]
	filters['age'] = [[40, float('inf')]]

	#SELECT SETTINGS
	ps = TCG.PlotDefaults.copy()
	ps["show"] = True
	ps["xStartPosBins"] = [0, 200, 300, 500, 10000]
	#ps['percent'] = True
	#ps['bins'] = 5
	#ps['xStartPosBins'] = 5
	#ps['directionalityBins'] = 5
	#ps['migrationPersistenceBins'] = np.linspace(0, 1, 6)
	#ps['norm'] = True

	#FILTER DATA
	data.selectData(filters)


#FOR INDIVIDUAL TRACKFILE TESTING
if TrackFile_Test:

	for experiment, v in data.experiments.items():
		print(experiment)
		avgMovVals = np.array(v.d['avgMov'])
		velocityVals = np.array(v.d['velocity'])
		directionalityVals = np.array(v.d['directionality'])


		#3D PLOTS
		#fig = plt.figure()
		#ax = fig.gca(projection='3d')
		#ax.plot_trisurf(avgMovVals, velocityVals, directionalityVals, cmap = cm.jet)
		#ax.scatter(avgMovVals, velocityVals, directionalityVals)

		# CMP PLOTS
		v.plotBinData('xStartPos', 'avgMov', ps)
		#v.plotBinDataSummary('xStartPos', ps)
		#v.plotHistogram('directionality', ps)
		#v.plotHistogramSummary(ps)
		#v.plotWeightedAverageCorr('xStartPos', 'directionality', ps)
		#v.plotWeightedAverageCorr('xStartPos', 'velocity', ps)
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
	#data.plotWeightedAverageCorr('xStartPos', 'avgMov', ps)
	#data.plotWeightedAverageCorrSummary(ps)
	#data.plotHistograms('avgMov', ps)
	#data.comparisonAnalysis(ps)






