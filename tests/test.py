#for remove redundancy - getWeightedAvgCorr vs plotBinData (getBinData)

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

	ps = TCG.PlotDefaults.copy()

	keyProperty1 = 'avgMov'
	keyProperty2 = 'velocity'
	keyProperty3 = 'directionality'
	keyProperty4 = 'migrationPersistence'
	properties = [keyProperty1, keyProperty2, keyProperty3, keyProperty4]



	for experiment, v in data.experiments.items():
		v.plotBinData('xStartPos', 'avgMov')
		#v.plotWeightedAverageCorr('xStartPos', 'avgMov')

