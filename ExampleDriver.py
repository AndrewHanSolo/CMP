'''
Example driver of streamlined analysis. Structured for easy customization.
'''
#add CMP directory paths
import sys
import os
sys.path.insert(0, './lib')
sys.path.insert(0, './data')
sys.path.insert(0, './jobs')
sys.path.insert(0, './TrackMate XMLs')
from TrackClass import *
import TrackClassGlobals as TCG
from ExampleJob import Example_Job
from TestJob import Test_Job



'''Custom Test Analysis'''
if 1:

	#TCG.SAVE_DIRECTORY = "C:/Users/Andrew Han/Desktop/analysis/test/" #'/home/ahan/Desktop/analysis/Example_Job/'
	#trackfilesPath = 'C:\\Users\\Andrew Han\\Desktop\\CMP\\TrackMate XMLs\\test\\' #'/home/ahan/Desktop/track files/test/'
	
	#Filter settings
	filters = {}
	filters['age'] = [[15, float('inf')]]
	filters['frames'] = [[0, float('inf')]]

	#Plot settings
	ps = TCG.PlotDefaults.copy()
	ps['startFrame'] = 0
	ps['endFrame'] = 50
	ps['bins'] = 15
	ps['title'] = 'old'

	#Analysis

	TCG.AVALYSIS_SAVE_NAME = 'shorttest-analysis'
	Example_Job('testData', TRACKMATE_FOLDERNAME = 'testData_XMLs', filters = filters, ps = ps)

	TCG.AVALYSIS_SAVE_NAME = 'fulltest-analysis'
	Test_Job('testData', filters = filters, ps = ps)
