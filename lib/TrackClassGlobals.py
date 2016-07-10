from TrackMeasurementFunctions import *
from enum import Enum

VERBOSE = True
DEBUG = False
SAVE_DIRECTORY = '/home/andrewhan/Desktop'
#MIGRATION_DIRECTORY = 'C:/Users/Andrew Han/Desktop/CMP/migrationData' //not being used right now
SPEED_CONVERSION_FACTOR = 6
FIELD_VECTOR_SPECIAL = [1, 0]
GLOBAL_FIELD_VECTOR = [-1, 0]
FIELD_VECTOR_INSTANCE = [-1, 0]


DEFAULT_TRACK_FIELDS = { 

	'absVelocity'          : getAbsVelocity,
	'age'                  : getAge,
	'avgMov'               : getAverageMovement,
	'concentration'        : getConcentration,
	'directionality'       : getDirectionality,
	'migrationPersistence' : getMigrationPersistence,
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

}

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

	'writeData'                      : 1,
	'histogramTemporalAnalysis'      : 0,
	'spatioTemporalAnalysis'         : 0,
	'plotWeightedAverageCorrSummary' : 0,
	'comparisonAnalysis'             : 0,
	'heatMaps'                       : 0,
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
	'migrationPersistence' : 'migration persistence',
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
	'migrationPersistence' : (0, 1),
	'velocity'             : (0, 20)

}


ColorMapPropertyDict = {
	#diverging colormap
	'directionality'       : 'jet',
	'migrationPersistence' : 'jet',

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
	'migrationPersistence' : maxRange,
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
	'migrationPersistenceBins' : 10,
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
