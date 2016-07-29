from TrackMeasurementFunctions import *

VERBOSE = True
DEBUG = False
SAVE_DIRECTORY = '/home/ahan/Desktop/analysis/'
SPEED_CONVERSION_FACTOR = 6
FIELD_VECTOR_SPECIAL = [1, 0]
GLOBAL_FIELD_VECTOR = [-1, 0]
FIELD_VECTOR_INSTANCE = [-1, 0]


DefaultExpParams = {
	
	'id'                      : None,
	'gradientStrength'        : 0,
	'gradientVector'          : [-1, 0],
	'reverse'                 : False,
	'maxX'                    : 10000,
	'maxY'                    : 10000,
	'spatialConversionFactor' : 0.64, #microns per pixel
	'frameInterval'	  		  : 10,   #time between frames (in minutes)

}


AnalysisDefaults = {

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

AnimationDefaults = {
		
	#temporal analysis settings
	'startFrame'    : 0,
	'endFrame'      : 0,
	'frameInterval' : 0, #TODO: MAKE THIS FRAMBINS. RIGHT NOW THIS SPECIFIES EXACT FRAMES IN EACH BIN



}




##
## @brief      { Class that holds measurement calculation function, and analysis/plot settings }
##
## @return     { description_of_the_return_value }
##
class TrackMeasurement():

	##
	## @brief      { constructor}
	##
	## @param      self         The measurement
	## @param      name         measurement name
	## @param      function     measurement function
	## @param      axisLabel    The axis label
	## @param      axisLimits   The axis limits
	## @param      colorMap     The color map
	## @param      description  The description
	##
	def __init__(self, 
		         name,
		         function,
		         axisLabel,
		         description,
		         colorMap = "jet",
		         bins = 5):		

		self.name = name
		self.function = function
		self.axisLabel = axisLabel
		self.description = description
		self.colorMap = colorMap
		self.bins = bins




avgMov          = TrackMeasurement("avgMov", getAvgMov, "avgMov: um/hour", "average distance travelled per frame")
velocity        = TrackMeasurement("velocity", getVelocity, "velocity: um/hour", "average migration distance per frame")
concentration   = TrackMeasurement("concentration", getConcentration, "concentration: ug", "local chemical concentration at starting pos")
directionality  = TrackMeasurement("directionality", getDirectionality, "directionality: %", "ratio of movement in direction of increasing gradient")
getMP           = TrackMeasurement("mp", getMP, "mp: %", "ratio of movement in one direction")
getXStartPos    = TrackMeasurement("xStartPos", getxStartPos, "xStartPos: um", "x starting position")
getXEndPos      = TrackMeasurement("xEndPos", getxEndPos, "xEndPos: um", "x ending position")
getYStartPos    = TrackMeasurement("yStartPos", getyStartPos, "yStartPos: um", "y starting position")
getYEndPos      = TrackMeasurement("yEndPos", getyEndPos, "yEndPos: um", "y ending position")
firstFrame      = TrackMeasurement("firstFrame", getFirstFrame, "firstFrame: frame#", "first frame of track")
lastFrame       = TrackMeasurement("lastFrame", getLastFrame, "lastFrame: frame#", "last frame of track")
xMigrationSpeed = TrackMeasurement("xMigrationSpeed", getxMigrationSpeed, "xMigrationSpeed: um/hour", "xMigrationSpeed")
yMigrationSpeed = TrackMeasurement("yMigrationSpeed", getyMigrationSpeed, "yMigrationSpeed: um/hour", "yMigrationSpeed")
numFrames       = TrackMeasurement("numFrames", getNumFrames, "numFrames: # of frames", "range of tracks over which track exists")
age             = TrackMeasurement("age", getAge, "age: range of frames", "number of frames in which track exists")




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




axesLimits = {
	
	'xStartPos'      : (0, 10000),
	'yStartPos'      : (0, 10000),
	'directionality' : (-1, 1),
	'avgMov'         : (0, 10),
	'age'            : (0, 100),
	'mp'             : (0, 1),
	'velocity'       : (0, 20)

}


