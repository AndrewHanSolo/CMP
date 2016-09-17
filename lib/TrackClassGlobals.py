from TrackMeasurements import *
import os

#Degree of output from CMP to console
VERBOSE = True  #very talkative
DEBUG = True	#most talkative
SAVE_DIRECTORY = None #'/home/ahan/Desktop/analysis/' #'C:\\Users\\Andrew Han\\Desktop/analysis/'

#setting paths for reading and writing files
CMP_PATH = os.getcwd()
DATA_SAVE_PATH = CMP_PATH + '/data/'
TRACK_FILES_IMPORT_PATH = CMP_PATH + r"/TrackMate XMLs/"
ANALYSIS_SAVE_PATH = CMP_PATH + '/analysis/'
ANALYSIS_SAVE_NAME = ''



#Default experiment params used when loading 
#experiment data folder to CMP
DefaultExpParams = {
	
	'id'                      : None,
	'gradientStrength'        : 0,
	'gradientVector'          : [-1, 0],
	'reverse'                 : False,
	'maxX'                    : 10000, #must be defined. defines the width (um, chemical gradient dimension) of the experiment
	'maxY'                    : 665, #must be defined. defines the height (um) of the experiment
	'spatialConversionFactor' : 0.64, #microns per pixel
	'frameInterval'	  		  : 10,   #time between frames (in minutes)
	'speedConversionFactor'   : 3.84,  #computed. 
	'DefaultAxisLimits'	      : DefaultAxesLimits #key: TrackMeasurement name, value: min max tuple

}

#Default track measurements available for analyis
#Must exist in TrackMeasurementClass
DefaultTrackMeasurements = {

	"xPos"            : xPos,
	"yPos"            : yPos,
	"frames"          : frames,

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



