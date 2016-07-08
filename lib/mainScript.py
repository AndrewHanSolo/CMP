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
from FullAnalysis_Job import *

#ALL FILTERS AGE>5
allFilters = TCG.DefaultFilters.copy()
allPlotSettings = TCG.PlotDefaults.copy()
allPlotSettings['title'] = 'all'
aps = allPlotSettings


#OLD FILTERS AGE>MAXAGE-2
oldFilters = TCG.DefaultFilters.copy()
oldPlotSettings = TCG.PlotDefaults.copy()
oldPlotSettings['title'] = 'old'
ops = oldPlotSettings





'''
#Topographical guidance
ps = TCG.PlotDefaults.copy()
ps['startFrame'] = 0
ps['endFrame'] = 30
ps['frameInterval'] = 10
ps['bins'] = 15

youngFilters = TCG.DefaultFilters.copy()
oldFilters = TCG.DefaultFilters.copy()
allFilters = TCG.DefaultFilters.copy()

#youngFilters['age'] = [[5, 37]]
#youngFilters['frames'] = [[0, float('inf')]]

oldFilters['age'] = [[28, float('inf')]]
oldFilters['frames'] = [[0, float('inf')]]

allFilters['age'] = [[5, float('inf')]]
allFilters['frames'] = [[0, float('inf')]]


#TCG.SAVE_DIRECTORY = 'C:/Users/Andrew Han/Desktop/analysis images/NFs/'
#fullAnalysis('2-11-16 Exp', filters = allFilters, ps = ps)

#TCG.SAVE_DIRECTORY = 'C:/Users/Andrew Han/Desktop/analysis images/diameter/age 5 to 37/'
#fullAnalysis('2-11-16 Exp', filters = youngFilters, ps = ps)

TCG.SAVE_DIRECTORY = 'C:/Users/Andrew Han/Desktop/analysis images/diameter/'
fullAnalysis('fibers', filters = oldFilters, ps = ps)
'''



#NF analysis

ps = TCG.PlotDefaults.copy()
ps['startFrame'] = 14
ps['endFrame'] = 70
ps['frameInterval'] = 14
ps['bins'] = 15

youngFilters = TCG.DefaultFilters.copy()
oldFilters = TCG.DefaultFilters.copy()
allFilters = TCG.DefaultFilters.copy()

#youngFilters['age'] = [[5, 37]]
#youngFilters['frames'] = [[0, float('inf')]]

oldFilters['age'] = [[40, float('inf')]]
oldFilters['frames'] = [[30, float('inf')]]

allFilters['age'] = [[5, float('inf')]]
allFilters['frames'] = [[30, float('inf')]]


TCG.SAVE_DIRECTORY = 'C:/Users/Andrew Han/Desktop/analysis images/NFs/'
fullAnalysis('bestNFs', filters = allFilters, ps = ps)

#TCG.SAVE_DIRECTORY = 'C:/Users/Andrew Han/Desktop/analysis images/diameter/age 5 to 37/'
#fullAnalysis('bestNFs', filters = youngFilters, ps = ps)

#TCG.SAVE_DIRECTORY = 'C:/Users/Andrew Han/Desktop/analysis images/NFs/'
#fullAnalysis('bestNFs', filters = oldFilters, ps = ps)