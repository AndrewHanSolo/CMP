#Contains constructions of Track measurement analysis fields
#measurements may be added

from TrackMeasurementFunctions import *


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
	## @param      description  The description
	## @param      colorMap     The color map
	## param	   bins         The default number of bins used for histograms
	## 							It can be a scalar or 2d array in the format [[], [], ...]
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

#primitive fields (Track dimensions)
xPos            = TrackMeasurement("xPos", None, "xPos: um", "fundamental track dimension")
yPos            = TrackMeasurement("yPos", None, "xPos: um", "fundamental track dimension")
frames          = TrackMeasurement("frame", None, "frame #", "fundamental track dimension")

#nonprimitive fields (Track calculated values)
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



axesLimits = {
	
	'xStartPos'      : (0, 10000),
	'yStartPos'      : (0, 10000),
	'directionality' : (-1, 1),
	'avgMov'         : (0, 10),
	'age'            : (0, 100),
	'mp'             : (0, 1),
	'velocity'       : (0, 20),
	'frames'         : (0, 100),
	'xPos'           : (0, 10000),
	'yPos'           : (0, 10000),
	'firstFrame'     : (0, 72),
	'lastFrame'      : (0, 72)


}