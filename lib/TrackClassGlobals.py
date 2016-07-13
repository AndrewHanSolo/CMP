from TrackMeasurementFunctions import *

VERBOSE = True
DEBUG = False
SAVE_DIRECTORY = '/home/andrewhan/Desktop'
#MIGRATION_DIRECTORY = 'C:/Users/Andrew Han/Desktop/CMP/migrationData' //not being used right now
SPEED_CONVERSION_FACTOR = 6
FIELD_VECTOR_SPECIAL = [1, 0]
GLOBAL_FIELD_VECTOR = [-1, 0]
FIELD_VECTOR_INSTANCE = [-1, 0]


'''Default_Track_Measurements = { 

	'absVelocity'          : getAbsVelocity,
	'age'                  : getAge,
	'avgMov'               : getAverageMovement,
	'concentration'        : getConcentration,
	'directionality'       : getDirectionality,
	'mp' : getmp,
	'velocity'             : getVelocity,
	'xMigrationSpeed'      : getxMigrationSpeed,
	'yMigrationSpeed'      : getyMigrationSpeed,
	'xStartPos'            : getxStartPos,
	'xEndPos'              : getxEndPos,
	'yStartPos'            : getyStartPos,
	'yEndPos'              : getyEndPos,
	'numFrames'            : getNumFrames,
	'firstFrame'           : getFirstFrame,
	'lastFrame'            : getLastFrame

}'''

DEAULT_TRACK_FILE_FIELDS = {
	
	'fileName': '',
	'path': ''

}

Default_Exp_Params = {
	
	'gradient'                : 0,
	'reverse'                 : False,
	'maxX'                    : 0,
	'maxY'                    : 0,
	'spatialConversionFactor' : 0.64


}

AnalysisDefaults = {

	'writeData'                      : 0,
	'histogramTemporalAnalysis'      : 0,
	'spatioTemporalAnalysis'         : 0,
	'plotWeightedAverageCorrSummary' : 0,
	'comparisonAnalysis'             : 0,
	'heatMaps'                       : 1,
	'plotScatter'                    : 0,
	'weightedAverageCorr'            : 0,
	'binDataSummary'                 : 0,
	'histogramScan'                  : 0

}



axesLabels = {

	'absVelocity'          : 'absVelocity: microns/hour',
	'age'                  : 'age: frames',
	'avgMov'               : 'avgMov: microns/hour',
	'concentration'        : 'concentration: ug',
	'directionality'       : 'directionality',
	'mp' : 'migration persistence',
	'velocity'             : 'velocity: microns/hour',
	'xMigrationSpeed'      : 'xMigrationSpeed: microns/hour',
	'yMigrationSpeed'      : 'yMigrationSpeed: microns/hour',
	'xStartPos'            : 'xStartPos: microns',
	'xEndPos'              : 'xEndPos: microns',
	'yStartPos'            : 'yStartPos: microns',
	'yEndPos'              : 'yEndPos: microns',
	'numFrames'            : 'numFrames: frames',
	'firstFrame'           : 'firstFrame: frame',
	'lastFrame'            : 'lastFrame: frame'

}


axesLimits = {
	
	'xStartPos'            : (0, 10000),
	'yStartPos'            : (0, 10000),
	'directionality'       : (-1, 1),
	'avgMov'               : (0, 10),
	'age'                  : (0, 100),
	'mp' : (0, 1),
	'velocity'             : (0, 20)

}


ColorMapPropertyDict = {
	#diverging colormap
	'directionality'       : 'jet',
	'mp' : 'jet',

	#sequential colormap
	'velocity'             : 'YlOrRd',
	'avgMov'               : 'YlOrRd',
	'xStartPos'            : 'YlOrRd',
	'yStartPos'            : 'YlOrRd',
	'startFrame'           : 'YlOrRd',
	'endFrame'             : 'YlOrRd'
}


maxRange = [[float('-inf'), float('inf')]]

DefaultFilters = {
	
	'frames'               : maxRange,
	'xPos'                 : maxRange,
	'yPos'                 : maxRange,

	#enter scalar field values. multiple ranges possible
	'absVelocity'          : maxRange,
	'age'                  : maxRange,
	'avgMov'               : maxRange,
	'concentration'        : maxRange,
	'directionality'       : maxRange,
	'mp' : maxRange,
	'velocity'             : maxRange,
	'xMigrationSpeed'      : maxRange,
	'yMigrationSpeed'      : maxRange,

	'xStartPos'            : maxRange,
	'xEndPos'              : maxRange,
	'yStartPos'            : maxRange,
	'yEndPos'              : maxRange,
	'numFrames'            : maxRange,
	'firstFrame'           : maxRange,
	'lastFrame'            : maxRange,

		}

#plot defualts
PlotDefaults = {
	
	#general plot settings
	'show'                     : False,
	'save'                     : True,
	'bins'                     : 20,
	'norm'                     : False,
	'percent'                  : False,
	'title'                    : '',
	'weight'                   : 'age',
	'legend'                   : True,
	'legendLoc'                : 1,
	'newFig'                   : True,
	'stdErrorBars'             : True,
	"average"				   : "weighted",

	#movie settings
	'movie'                    : True,

	#temporal analysis settings
	'startFrame'               : 0,
	'endFrame'                 : 30,
	'frameInterval'            : 10, #TODO: MAKE THIS FRAMBINS. RIGHT NOW THIS SPECIFIES EXACT FRAMES IN EACH BIN
	'startConcentration'       : 0,
	'endConcentration'         : 10,
	'concentrationInterval'    : 2,
	'xStartPosBins'            : 20,
	'directionalityBins'       : 10,
	'mpBins' : 10,
	'velocityBins'             : 10,
	'avgMovBins'               : 10,
	'concentrationBins'        : 10,


	#spatial analysis settings
	'spatialBins'              : 10,

	#rotation angles for 3dPlotMovie
	'rotStartAngle'            : 220,
	'rotEndAngle'              : 221,
	'rotResolution'            : 1,


	#cellVisualization settings
	'colorMin'                 : -1,
	'colorMax'                 : 1,

	#percents
	'percents'                 : [0, 25, 50, 75, 100]

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
		         axisLimits,
		         colorMap,
		         description):		

		self.name = name
		self.function = function
		self.axisLabel = axisLabel
		self.axisLimits = axisLimits
		self.function == axesLimits
		self.colorMap = colorMap





avgMov          = TrackMeasurement("avgMov", getAvgMov, "um/hour", maxRange, "jet", "average distance travelled per frame")
velocity        = TrackMeasurement("velocity", getVelocity, "um/hour", maxRange, "jet", "average migration distance per frame")
concentration   = TrackMeasurement("concentration", getConcentration, "ug", maxRange, "jet", "local chemical concentration at starting pos")
directionality  = TrackMeasurement("directionality", getDirectionality, "%", maxRange, "jet", "ratio of movement in direction of increasing gradient")
getMP           = TrackMeasurement("mp", getMP, "um/%", maxRange, "jet", "ratio of movement in one direction")
getXStartPos    = TrackMeasurement("xStartPos", getxStartPos, "microns", maxRange, "jet", "x starting position")
getYStartPos    = TrackMeasurement("yStartPos", getyStartPos, "microns", maxRange, "jet", "y starting position")
firstFrame      = TrackMeasurement("firstFrame", getFirstFrame, "microns", maxRange, "jet", "first frame of track")
lastFrame       = TrackMeasurement("lastFrame", getLastFrame, "microns", maxRange, "jet", "last frame of track")
xMigrationSpeed = TrackMeasurement("xMigrationSpeed", getxMigrationSpeed, "microns", maxRange, "jet", "xMigrationSpeed")
yMigrationSpeed = TrackMeasurement("yMigrationSpeed", getyMigrationSpeed, "microns", maxRange, "jet", "yMigrationSpeed")
numFrames       = TrackMeasurement("numFrames", getNumFrames, "# frames", maxRange, "jet", "range of tracks over which track exists")
age             = TrackMeasurement("age", getAge, "microns", maxRange, "jet", "number of frames in which track exists")




Default_Track_Measurements = {

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