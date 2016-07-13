

##
## @brief      { Class that holds measurement calculation function, and analysis/plot settings }
##
## @return     { description_of_the_return_value }
##
def TrackMeasurement():

	def __init__(self, 
		         name,
		         function,
		         axisLabel = "",
		         axisLimits = maxRange
		         colorMap = "",
		         description = ""):		

		self.name = name
		self.function = function
		self.axisLabel = axisLabel
		self.axisLimits = axisLimits
		self.function == axesLimits
		self.colorMap = colorMap


Default_Track_Measurements = {

"avgMov"          : TrackMeasurement("avgMov", avgMov, "um/hour", maxRange, "jet", "average distance travelled per frame"),
"velocity"        : TrackMeasurement("velocity", velocity, "um/hour", maxRange, "jet", "average migration distance per frame"),
"concentration"   : TrackMeasurement("concentration", concentration, "ug", maxRange, "jet", "local chemical concentration at starting pos"),
"directionality"  : TrackMeasurement("directionality", directionality, "%", maxRange, "jet", "ratio of movement in direction of increasing gradient"),
"mp"              : TrackMeasurement("mp", mp, "um/%", maxRange, "jet", "ratio of movement in one direction"),
"xStartPos",      : TrackMeasurement("xStartPos", xStartPos, "microns", maxRange, "jet", "x starting position"),
"yStartPos"       : TrackMeasurement("yStartPos", yStartPos, "microns", maxRange, "jet", "y starting position"),
"firstFrame"      : TrackMeasurement("firstFrame", firstFrame, "microns", maxRange, "jet", "first frame of track"),
"lastFrame"       : TrackMeasurement("lastFrame", , "microns", maxRange, "jet", "last frame of track"),
"xMigrationSpeed" : TrackMeasurement("xMigrationSpeed", xMigrationSpeed, "microns", maxRange, "jet", "xMigrationSpeed"),
"yMigrationSpeed" : TrackMeasurement("yMigrationSpeed", yMigrationSpeed, "microns", maxRange, "jet", "yMigrationSpeed"),
"numFrames"       : TrackMeasurement("numFrames", numFrames, "# frames", maxRange, "jet", "range of tracks over which track exists"),
"age"             : TrackMeasurement("age", age, "microns", maxRange, "jet", "number of frames in which track exists"),

}


	
