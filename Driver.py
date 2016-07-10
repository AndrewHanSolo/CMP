'''
Main driver that runs streamlined analysis. Structured for easy customization.
'''
#add CMP directory paths
import sys
sys.path.insert(0, './lib')
sys.path.insert(0, './data')
sys.path.insert(0, './tests')
sys.path.insert(0, './jobs')
from TrackClass import *
import os
from copy import deepcopy
import TrackClassGlobals as TCG
from FullAnalysis_Job import *



'''Custom Nanofiber Analysis'''
if 1:

	#Filter settings
	oldFilters = TCG.DefaultFilters.copy()
	oldFilters['age'] = [[25, float('inf')]]
	oldFilters['frames'] = [[0, float('inf')]]

	#Plot settings
	ps = TCG.PlotDefaults.copy()
	ps['startFrame'] = 0
	ps['endFrame'] = 30
	ps['frameInterval'] = 10
	ps['bins'] = 15
	ps['title'] = 'old'

	#Analysis
	TCG.SAVE_DIRECTORY = '/home/andrewhan/Desktop/analysis/nanofibers/'
	fullAnalysis('data/fibers', filters = oldFilters, ps = ps)



'''Custom NF Analysis'''
if 1:

	#Filter settings
	oldFilters = TCG.DefaultFilters.copy()
	oldFilters['age'] = [[40, float('inf')]]
	oldFilters['frames'] = [[30, float('inf')]]

	#Plot settings
	ps = TCG.PlotDefaults.copy()
	ps['startFrame'] = 30
	ps['endFrame'] = 70
	ps['frameInterval'] = 10
	ps['bins'] = 10
	ps['title'] = 'old'

	#Analysis
	TCG.SAVE_DIRECTORY = '/home/andrewhan/Desktop/analysis/nfs/'
	fullAnalysis('data/gradient', filters = oldFilters, ps = ps)
