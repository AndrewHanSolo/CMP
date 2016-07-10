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



def fullAnalysis(DATA_SAVE_NAME, PATH = 0, filters = TCG.DefaultFilters, ps = TCG.PlotDefaults):
	
	print(DATA_SAVE_NAME)

	#save data if folder path to load from is specified
	if PATH:
		data = importAndSave(PATH, DATA_SAVE_NAME)

	####################################
	#LOAD DATA
	with open(DATA_SAVE_NAME, 'rb') as input:
		data = pickle.load(input)

		data.selectData(filters)

		keyProperty1 = 'avgMov'
		keyProperty2 = 'velocity'
		keyProperty3 = 'directionality'
		keyProperty4 = 'migrationPersistence'
		properties = [keyProperty1, keyProperty2, keyProperty3, keyProperty4]

		#data.writeData(ps)
		'''data.histogramTemporalAnalysis(ps)
		data.spatialTemporalAnalysis(ps)
		data.plotWeightedAverageCorrSummary(ps)
		data.comparisonAnalysis(ps)'''

		P.close()

		for experiment, v in sorted(data.experiments.items()):


			v.heatmapVisualization('xStartPos', 'avgMov', 'migrationPersistence', ps)
			#v.heatmapVisualization('xStartPos', 'yStartPos', keyProperty3, ps)	
			#v.heatmapVisualization(keyProperty1, keyProperty2, keyProperty3, ps)	
			#v.heatmapVisualization('xStartPos', keyProperty3, 'xStartPos', ps)	

			#v.plotScatter(keyProperty1, keyProperty3)
			#v.plotWeightedAverageCorr('age', keyProperty2)
			#v.plotScatter('age', keyProperty2)
			#v.plotScatter('age', keyProperty3)
			#v.plotScatter('xStartPos', keyProperty2)
			#v.plotScatter(keyProperty2, keyProperty3)
			#v.plotWeightedAverageCorr('yStartPos', keyProperty2)

			#v.plotBinDataSummary(keyProperty3, ps)
			#v.plotBinDataSummary(keyProperty2, ps)
			#v.plotWeightedAverageCorr('xStartPos', keyProperty3, ps)

			#v.plotBinDataSummary('xStartPos', ps);
			#v.histogramScan(keyProperty3, 'xStartPos', ps)
			#v.histogramScan(keyProperty3, 'concentration', ps)
			#v.histogramScan(keyProperty2, 'xStartPos', ps)

			
			#v.plotCurve('xStartPos', 'avgMov', ps)

			'''print(experiment)
			for i in range(0,4):
				item = properties[i]
				x, y, z = v.getWeightedAverage(item)
				data = "%d\t%f\t%f\t%f" % (len(v.tracks), x, y, z)
				print(item+'\t'+data)

				#print(np.mean(v.d[item]))'''

			'''#print(experiment)
			
			#print(data)
			#print('velocity ', v.getWeightedAverage('velocity'))
			#print('avgMov ', v.getWeightedAverage('avgMov'))
			#print('directionality ', v.getWeightedAverage('directionality'))

			P.close()'''




