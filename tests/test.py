from TrackMeasurementFunctions import *

##
## @brief      { Class that holds measurement calculation function, and analysis/plot settings }
##
## @return     { description_of_the_return_value }
##
class TrackMeasurement():

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
directionality  = TrackMeasurement("directionality", getdirectionality, "%", maxRange, "jet", "ratio of movement in direction of increasing gradient")
getMP           = TrackMeasurement("mp", getMP, "um/%", maxRange, "jet", "ratio of movement in one direction")
getXStartPos    = TrackMeasurement("xStartPos", getXStartPos, "microns", maxRange, "jet", "x starting position")
getYStartPos    = TrackMeasurement("yStartPos", getYStartPos, "microns", maxRange, "jet", "y starting position")
firstFrame      = TrackMeasurement("firstFrame", getFirstFrame, "microns", maxRange, "jet", "first frame of track")
lastFrame       = TrackMeasurement("lastFrame", getLastFrame, "microns", maxRange, "jet", "last frame of track")
xMigrationSpeed = TrackMeasurement("xMigrationSpeed", getXMigrationSpeed, "microns", maxRange, "jet", "xMigrationSpeed")
yMigrationSpeed = TrackMeasurement("yMigrationSpeed", getYMigrationSpeed, "microns", maxRange, "jet", "yMigrationSpeed")
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