from TrackMeasurementFunctions import *

VERBOSE = True
DEBUG = False
SAVE_DIRECTORY = '/home/andrewhan/Desktop/'
SPEED_CONVERSION_FACTOR = 6
FIELD_VECTOR_SPECIAL = [1, 0]
GLOBAL_FIELD_VECTOR = [-1, 0]
FIELD_VECTOR_INSTANCE = [-1, 0]


DefaultExpParams = {
	
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




avgMov          = TrackMeasurement("avgMov", getAvgMov, "um/hour", "average distance travelled per frame")
velocity        = TrackMeasurement("velocity", getVelocity, "um/hour", "average migration distance per frame")
concentration   = TrackMeasurement("concentration", getConcentration, "ug", "local chemical concentration at starting pos")
directionality  = TrackMeasurement("directionality", getDirectionality, "%", "ratio of movement in direction of increasing gradient")
getMP           = TrackMeasurement("mp", getMP, "um/%", "ratio of movement in one direction")
getXStartPos    = TrackMeasurement("xStartPos", getxStartPos, "microns", "x starting position")
getYStartPos    = TrackMeasurement("yStartPos", getyStartPos, "microns", "y starting position")
firstFrame      = TrackMeasurement("firstFrame", getFirstFrame, "microns", "first frame of track")
lastFrame       = TrackMeasurement("lastFrame", getLastFrame, "microns", "last frame of track")
xMigrationSpeed = TrackMeasurement("xMigrationSpeed", getxMigrationSpeed, "microns", "xMigrationSpeed")
yMigrationSpeed = TrackMeasurement("yMigrationSpeed", getyMigrationSpeed, "microns", "yMigrationSpeed")
numFrames       = TrackMeasurement("numFrames", getNumFrames, "# frames", "range of tracks over which track exists")
age             = TrackMeasurement("age", getAge, "microns", "number of frames in which track exists")




DefaultTrackMeasurements = {

"avgMov"          : avgMov         ,
"velocity"        : velocity       ,
"concentration"   : concentration  ,
"directionality"  : directionality ,
"mp"              : getMP          ,
"xStartPos"       : getXStartPos   ,
"yStartPos"       : getYStartPos   ,
"firstFrame"      : firstFrame     ,
"lastFrame"       : lastFrame      ,
"xMigrationSpeed" : xMigrationSpeed,
"yMigrationSpeed" : yMigrationSpeed,
"numFrames"       : numFrames      ,
"age"             : age

}


axesLabels = {

	'absVelocity'     : 'absVelocity: microns/hour',
	'age'             : 'age: frames',
	'avgMov'          : 'avgMov: microns/hour',
	'concentration'   : 'concentration: ug',
	'directionality'  : 'directionality',
	'mp'              : 'migration persistence',
	'velocity'        : 'velocity: microns/hour',
	'xMigrationSpeed' : 'xMigrationSpeed: microns/hour',
	'yMigrationSpeed' : 'yMigrationSpeed: microns/hour',
	'xStartPos'       : 'xStartPos: microns',
	'xEndPos'         : 'xEndPos: microns',
	'yStartPos'       : 'yStartPos: microns',
	'yEndPos'         : 'yEndPos: microns',
	'numFrames'       : 'numFrames: frames',
	'firstFrame'      : 'firstFrame: frame',
	'lastFrame'       : 'lastFrame: frame'

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


