'''
Example driver of streamlined analysis. Structured for easy customization.
'''
#add CMP directory paths
import sys
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

	TCG.SAVE_DIRECTORY = '/home/ahan/Desktop/analysis/Example_Job/'
	trackfilesPath = '/home/ahan/Desktop/track files/test/'
	
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
	Example_Job('test', importpath = trackfilesPath, filters = filters, ps = ps)

	TCG.SAVE_DIRECTORY = '/home/ahan/Desktop/analysis/fullTest/'
	Test_Job('test', filters = filters, ps = ps)