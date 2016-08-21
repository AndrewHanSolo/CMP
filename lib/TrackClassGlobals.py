from TrackMeasurements import *

#Degree of output from CMP to console
VERBOSE = True  #very talkative
DEBUG = False	#most talkative
SAVE_DIRECTORY = '/home/ahan/Desktop/analysis/'


#TODO: REMOVE THESE GUYS
SPEED_CONVERSION_FACTOR = 6
FIELD_VECTOR_SPECIAL = [1, 0]
GLOBAL_FIELD_VECTOR = [-1, 0]
FIELD_VECTOR_INSTANCE = [-1, 0]



#Default experiment params used when loading 
#experiment data folder to CMP
DefaultExpParams = {
	
	'id'                      : None,
	'path'                    : "",
	'gradientStrength'        : 0,
	'gradientVector'          : [-1, 0],
	'reverse'                 : False,
	'maxX'                    : 10000,
	'maxY'                    : 10000,
	'spatialConversionFactor' : 0.64, #microns per pixel
	'frameInterval'	  		  : 10,   #time between frames (in minutes)
	'speedconversionfactor'   : None,  #computed
	'axesLimits'			  : axesLimits #key: TrackMeasurement name, value: min max tuple

}

#Default analysis plots run using
#Driver scripts
#TODO: update Driver scripts
DefaultAnalysis = {

	'writeData'                      : 0,
	'histogramTemporalAnalysis'      : 0,
	'spatioTemporalAnalysis'         : 0,
	'plotBinDataSummary' 			 : 0,
	'comparisonAnalysis'             : 0,
	'heatMaps'                       : 0,
	'plotScatter'                    : 0,
	'weightedAverageCorr'            : 1,
	'binDataSummary'                 : 1,
	'histogramScan'                  : 0

}

#Default track measurements available for analyis
#Must exist in TrackMeasurementClass
DefaultTrackMeasurements = {

	"avgMov"          : avgMov         ,
	"velocity"        : velocity       ,
	"concentration"   : concentration  ,
	"directionality"  : directionality ,
	"mp"              : getMP          ,
	"xStartPos"       : getXStartPos   ,
	"xEndPos"         : getXEndPos     ,
	"yStartPos"       : getYStartPos   ,
	"yEndPos"         : getYEndPos     ,
	"firstFrame"      : firstFrame     ,
	"lastFrame"       : lastFrame      ,
	"xMigrationSpeed" : xMigrationSpeed,
	"yMigrationSpeed" : yMigrationSpeed,
	"numFrames"       : numFrames      ,
	"age"             : age

}


#plot defualts
PlotDefaults = {
	
	#general plot settings
	'show'                  : False,
	'save'                  : True,
	'bins'                  : 20,
	'norm'                  : False,
	'percent'               : False,
	'title'                 : '',
	'weights'               : 'age',
	'legend'                : True,
	'legendLoc'             : 1,
	'fontsize'				: 9,
	'newFig'                : True,
	'stdErrorBars'          : True,
	"average"				: "weighted",

	#cellVisualization settings
	'colorMin'              : -1,
	'colorMax'              : 1,

	#percents
	'percents'              : [0, 25, 50, 75, 100]

}



