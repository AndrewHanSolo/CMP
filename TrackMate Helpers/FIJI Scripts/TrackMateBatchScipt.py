from fiji.plugin.trackmate import Model
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate.detection import LogDetectorFactory
from fiji.plugin.trackmate.tracking.sparselap import SparseLAPTrackerFactory
from fiji.plugin.trackmate.tracking.sparselap import SimpleSparseLAPTrackerFactory
from fiji.plugin.trackmate.tracking import LAPUtils
from ij import IJ
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
import sys
import fiji.plugin.trackmate.features.track.TrackDurationAnalyzer as TrackDurationAnalyzer
from ij import IJ, ImagePlus, ImageStack
import fiji.plugin.trackmate.Settings as Settings
import fiji.plugin.trackmate.Model as Model
import fiji.plugin.trackmate.SelectionModel as SelectionModel
import fiji.plugin.trackmate.TrackMate as TrackMate
import fiji.plugin.trackmate.Logger as Logger
import fiji.plugin.trackmate.detection.DetectorKeys as DetectorKeys
import fiji.plugin.trackmate.detection.DogDetectorFactory as DogDetectorFactory
import fiji.plugin.trackmate.tracking.sparselap.SparseLAPTrackerFactory as SparseLAPTrackerFactory
import fiji.plugin.trackmate.tracking.LAPUtils as LAPUtils
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
import fiji.plugin.trackmate.features.FeatureAnalyzer as FeatureAnalyzer
import fiji.plugin.trackmate.features.spot.SpotContrastAndSNRAnalyzerFactory as SpotContrastAndSNRAnalyzerFactory
import fiji.plugin.trackmate.action.ExportStatsToIJAction as ExportStatsToIJAction
import fiji.plugin.trackmate.io.TmXmlReader as TmXmlReader
import fiji.plugin.trackmate.action.ExportTracksToXML as ExportTracksToXML
import fiji.plugin.trackmate.io.TmXmlWriter as TmXmlWriter
import fiji.plugin.trackmate.features.ModelFeatureUpdater as ModelFeatureUpdater
import fiji.plugin.trackmate.features.SpotFeatureCalculator as SpotFeatureCalculator
import fiji.plugin.trackmate.features.spot.SpotContrastAndSNRAnalyzer as SpotContrastAndSNRAnalyzer
import fiji.plugin.trackmate.features.spot.SpotIntensityAnalyzerFactory as SpotIntensityAnalyzerFactory
import fiji.plugin.trackmate.features.track.TrackSpeedStatisticsAnalyzer as TrackSpeedStatisticsAnalyzer
import fiji.plugin.trackmate.util.TMUtils as TMUtils
import fiji.plugin.trackmate
import fiji.plugin.trackmate.gui.TrackMateGUIController as TrackMateGUIController
import java.io.File as File
import os
import fiji.plugin.trackmate.action.AbstractTMAction
import fiji.plugin.trackmate.action.CaptureOverlayAction as CaptureOverlayAction
import ij.WindowManager as WindowManager;
import ij.io.FileSaver as FileSaver
import glob, os




def analyze(tempFile):
# Get currently selected image
#imp = WindowManager.getCurrentImage()
	imp = IJ.openImage(tempFile)
	imp.show()
	dims = imp.getDimensions();
	imp.setDimensions(dims[2], dims[4], dims[3]);
	#----------------------------
	# Create the model object now
	#----------------------------
	# Some of the parameters we configure below need to have
	# a reference to the model at creation. So we create an
	# empty model now.
	model = Model()
	# Send all messages to ImageJ log window.
	model.setLogger(Logger.IJ_LOGGER)
	#------------------------
	# Prepare settings object
	#------------------------
	settings = Settings()
	settings.setFrom(imp)
	print(settings.imageFileName)   
	# Configure detector - We use the Strings for the keys
	settings.detectorFactory = LogDetectorFactory()
	settings.detectorSettings = { 
    	'DO_SUBPIXEL_LOCALIZATION' : False,
    	'RADIUS' : 20.,
    	'TARGET_CHANNEL' : 1,
    	'THRESHOLD' : 0.95,
    	'DO_MEDIAN_FILTERING' : True,
	}  
	# Configure spot filters - Classical filter on quality
	#filter1 = FeatureFilter('QUALITY', 0.5, True)
	#settings.addSpotFilter(filter1)
	# Configure tracker - We want to allow merges and fusions
	settings.trackerFactory = SimpleSparseLAPTrackerFactory()
	settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap() #probably good enough
	#settings.trackerSettings['ALLOW_TRACK_SPLITTING'] = False
	#settings.trackerSettings['ALLOW_TRACK_MERGING'] = False
	settings.trackerSettings['LINKING_MAX_DISTANCE'] = 35.0
	settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE']= 60.0
	settings.trackerSettings['MAX_FRAME_GAP']= 2
	# Configure track analyzers - Later on we want to filter out tracks 
	# based on their displacement, so we need to state that we want 
	# track displacement to be calculated. By default, out of the GUI, 
	# not features are calculated.   
	# The displacement feature is provided by the TrackDurationAnalyzer.
	settings.addTrackAnalyzer(TrackDurationAnalyzer())
	#-------------------
	# Instantiate plugin
	#-------------------
	trackmate = TrackMate(model, settings)
	ok = trackmate.process()
	if not ok:
		sys.exit(str(trackmate.getErrorMessage()))
	#----------------
	# Display results
	#----------------
	selectionModel = SelectionModel(model)
	displayer =  HyperStackDisplayer(model, selectionModel, imp)
	displayer.render()
	displayer.refresh()
	# Echo results with the logger we set at start:
	model.getLogger().log(str(model))
	print(str(settings))
	filename = os.path.splitext(settings.imageFileName)
	pathname = settings.imageFolder + "" + filename[0] + "tracks.xml"
	guicontroller = TrackMateGUIController(trackmate)
	newFile = File(pathname)
	ExportTracksToXML(guicontroller).export(model, settings, newFile)
	actionObject = CaptureOverlayAction()
	actionObject.execute(trackmate)
	imp = WindowManager.getCurrentImage()
	fileSaver = FileSaver(imp)
	fileSaver.saveAsTiffStack(settings.imageFolder + "" + filename[0] + "overlay.tif")
	WindowManager.closeAllWindows()
	guicontroller.quit()
	selectionModel.clearSelection();
	model.clearTracks(1)
	

os.chdir("C:\Users\Andrew Han\Desktop/TrackMate Tests/test-accelToRight/tiffs/")
for file in glob.glob("*.tif"):	
	print(file)
	tempFile = "C:\Users\Andrew Han\Desktop/TrackMate Tests/test-accelToRight/tiffs/" + file
	analyze(tempFile)

