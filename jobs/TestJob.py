"""
Execution Tests
"""

from TrackClass import *
import TrackClassGlobals as TCG
import xlsxwriter
import _pickle as pickle
DATA_SAVE_PATH

#TRACK_FILES_IMPORT_PATH
#ANALYSIS_SAVE_PATH
#ANALYSIS_SAVE_NAME

def Test_Job(DATA_SAVE_NAME, importpath = 0, filters = {}, ps = TCG.PlotDefaults):

	JOB_ANALYSIS_SAVE_PATH = ANALYSIS_SAVE_PATH + '/' + ANALYSIS_SAVE_NAME + '/'

	#TEST MODULES
	SAVE                      = True
	TrackFile_Test            = False
	TrackFolder_Test          = True

	#TEST BOOLS
	TEST_writeData            = False
	TEST_plotScatter          = False
	TEST_plotBinData          = False
	TEST_plotHistogram        = False
	TEST_plotPercentHistogram = False
	TEST_scan                 = False
	TEST_cellVisualization    = False
	TEST_heatmapVisualization = False
	TEST_compare              = True
	TEST_iterate              = False
	TEST_individual           = False

	if not os.path.exists(JOB_ANALYSIS_SAVE_PATH):
		os.makedirs(JOB_ANALYSIS_SAVE_PATH)

	#save data from folder path if given
	if importpath:
		data = importAndSave(importpath, DATA_SAVE_NAME)

	vprint('Running Analysis of %s...' %(DATA_SAVE_NAME))

	####################################
	#LOAD DATA
	with open('./data/' + DATA_SAVE_NAME, 'rb') as input:
		data = pickle.load(input)


	#SELECT FILTERS
	filters = {}
	filters['age'] = [[5, float('inf')]]
	#filters['frames'] = [[40, 50], [60, 70]]
	#filters['frames'] = [[30, float('inf')]]
	#filters['age'] = [[40, float('inf')]]
	#filters['xPos'] = [[0, 3000],[6000, 10000]]
	#filters['yPos'] = [[200, 500]]

	#SELECT SETTINGS
	ps = TCG.PlotDefaults.copy()
	ps["show"] = False
	#ps["colorSettings"] = { "vmin": 20, "vmax": 40, "separation": 10, "colorMap": "jet"}

	#FILTER DATA
	data.selectData(filters)

	#################################
	#FOR INDIVIDUAL TRACKFILE TESTING
	if TrackFile_Test:

		workbook = xlsxwriter.Workbook(JOB_ANALYSIS_SAVE_PATH + "fileTest.xlsx", {'nan_inf_to_errors': True, 'in_memory': True})

		for experiment, v in sorted(data.experiments.items()):
			print("\n\nExperiment:", experiment)
			print("Track Count: ", len(v.tracks))

			if TEST_writeData:
				writeData(v, workbook, "")

			if TEST_plotScatter:
				v.plotScatter("xStartPos", "avgMov")
				v.plotScatter('xStartPos', 'avgMov')
				v.plotScatter("age", "velocity")
				v.plotScatter('xStartPos', 'yStartPos')
				#v.plotScatter("xEndPos", "directionality")

			if TEST_plotBinData:
				v.plotBinData("xStartPos", "avgMov", ps, workbook = [workbook, experiment, True])
				v.plotBinData("age", "directionality", ps)
				v.plotBinData("avgMov", "velocity", ps)

			if TEST_plotHistogram:
				v.plotHistogram("xStartPos")
				v.plotHistogram("firstFrame")
				v.plotHistogram("avgMov")

			if TEST_plotPercentHistogram:
				v.plotPercentHistogram("directionality", "avgMov", ps, workbook = [workbook, experiment, True])
				v.plotPercentHistogram("age", "xStartPos", ps)
				v.plotPercentHistogram("mp", "yStartPos", ps)

			if TEST_scan:
				#v.scan("xStartPos", 0, 10000, 5, TrackFile.plotScatter, "avgMov", "directionality", ps)
				#v.scan("frames", 0, 100, 5, TrackFile.plotScatter, "firstFrame", "age", ps)
				#v.scan("xPos", 0, 10000, 5, TrackFile.plotScatter, "xStartPos", "avgMov", ps)
				#v.scan("xPos", 0, 10000, 5, TrackFile.plotBinData, "age", "firstFrame", ps)
				v.scan("frames", 0, 100, 10, TrackFile.plotBinData, "xStartPos", "avgMov", ps)
				v.scan("xStartPos", 0, 10000, 4, TrackFile.plotBinData, "avgMov", "directionality", ps) #<-- error
				v.scan("xStartPos", 0, 10000, 5, TrackFile.plotHistogram, "avgMov", None, ps)
				v.scan("avgMov", 0, 10000, 5, TrackFile.plotHistogram, "directionality", None, ps)
				#v.scan("firstFrame", 0, 10000, 5, TrackFile.plotHistogram, "age", None, ps)

			if TEST_cellVisualization:
				v.cellVisualization("avgMov", 10, ps)

			if TEST_heatmapVisualization:
				v.heatmapVisualization("xStartPos", "yStartPos", "avgMov", ps)

			if TEST_individual:
				v.plotBinData('xStartPos', 'concentration', ps)
				v.plotBinData('concentration', 'avgMov', ps)
				v.plotBinData('xStartPos', 'avgMov')
				v.plotScatter("xStartPos", 'yStartPos', ps)
				v.plotScatter("xStartPos", "directionality", ps)
				#pass

		workbook.close()

	########################
	#FOR TRACKFOLDER TESTING
	if TrackFolder_Test:

		workbook = xlsxwriter.Workbook(JOB_ANALYSIS_SAVE_PATH + "foldTest.xlsx", {'nan_inf_to_errors': True, 'in_memory': True})

		if TEST_writeData:
			data.writeData()
			
		if TEST_compare:
			data.compare(TrackFile.plotHistogram, "avgMov", None, ps)
			data.compare(TrackFile.plotBinData, "avgMov", "velocity", ps)
			data.compare(TrackFile.plotScatter, "avgMov", "velocity", ps)

		if TEST_iterate:
			#data.iterate(TrackFile.plotScatter, "firstFrame", "age", ps)
			data.iterate(TrackFile.plotHistogram, "velocity", None, ps)
			data.iterate(TrackFile.plotScatter, 'xStartPos', "velocity", ps)
			#data.iterate(TrackFile.plotPercentHistogram, "directionality", "avgMov", ps)
			#data.iterate(TrackFile.scan, "xStartPos", 0, 10000, 5, TrackFile.plotScatter, "avgMov", "directionality", ps)
			#data.iterate(TrackFile.cellVisualization, "avgMov", 10, ps)
			data.iterate(TrackFile.heatmapVisualization, "xStartPos", "yStartPos", "velocity", ps)
			data.iterate(TrackFile.plotHistogram, "directionality", None, ps)
			data.iterate(TrackFile.plotHistogram, "mp", None, ps)

		if TEST_individual:
			pass
			#data.iterate(TrackFile.heatmapVisualization, "xStartPos", "yStartPos", "avgMov", ps)
			#data.iterate(TrackFile.plotHistogram, "xStartPos", None, ps, [workbook, "hist", True])
			#data.compare(TrackFile.plotHistogram, "avgMov", None, ps)


		workbook.close()

