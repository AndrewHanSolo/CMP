#Cell Migration Analysis Pipeline (CMP)

##About
CMP is a lightweight python scripting library that offers a streamlined and versatile chemotaxis experiment data analysis pipeline. It was developed primarily for improving conclusive throughput of novel chemotaxis experimemts conducted at the Johns Hopkins Translational Tissue Engineering Center and the Johns Hopkins Institute of Computational Medicine. In brief, these experiments are high-population single-cell time-lapse microscopy chemotaxis studies. A presentation detailing the experiment setup can be found [here](www.google.com).  CMP was developed for use in tangent with the open source [TrackMate](https://github.com/fiji/TrackMate/) particle-tracking tool available as a plugin in the FIJI image processing program. CMP offers powerfully simple functions and features that make complex chemotaxis experiment analysis accessible even to non-programmers.

##Functions and Features
- Multi-file experiment spatial reconstruction
- Batch-experiment tracking and analysis scripts
- Iterative measurement bin selection and scanning with adjustable scope and resolution
- Combinatorial single and multi-experiment level analysis functions
- Analysis Output to Excel and CSV
- Full-loop pipeline testing tools
- Simplistic and minimal for easy extension and interfacing
- Seamless addition of new track dimensions, experiment parameters, and measurements

##Installation and Dependencies
CMP is stable on Windows 10, Ubuntu 14.04, and Fedora 24. The core analysis library runs with Python 3.4.0, but TrackMate and testing scripts are in Python 2.7.12 and IJM.

Install the following dependencies (Python 3.4.0) for the core analysis library.
- numpy 1.8.2
- xlsxwriter 0.5.2
- scipy 0.13.3
- matplotlib 1.5.1

Install Python 2.7.0 and the pygame library for generating mock image data.
Install TrackMate (FIJI plugin) for an automated cell-tracking tool that is used in our experiments. CMP provides scripts for batch-file processing images through TrackMate.

Open [*ExampleDriver.py*](www.google.com) and set your data import, save, and analysis output paths. You should now be able to run the example script. It analyzes a mock experiment data set generated using [*FIJI/MockExperimentDataGenerator.py*](www.google.com) that was passed through the automated-tracking process.

##Getting Started
###Obtaining track data from time lapse images and importing to CMP
1. Install FIJI
2. Open FIJI and press '[' to open the scripting window. Run [*FIJI/ImageSequenceToTiff.ijm*](https://github.com/AndrewHanSolo/CMP/blob/master/lib/TrackMateBatchScript.py) to convert folders of image sequences to TiffStacks.
3. Run [*FIJI/TrackMateBatchScript.py*] (https://github.com/AndrewHanSolo/CMP/blob/master/lib/TrackMateBatchScript.py) on each experiment's TiffStack folder
4. Move the xml output files into appropriate experiment subdirectories within one parent directory. A example experiment set folder is given [here](www.google.com).
   * (Optional) Add settings.txt with experiment parameters into any experiment subdirectories.
   * (Optional) Add coordinates.txt with xml filenames corresponding to their relative physical position in microns
5. Open *ExampleDriver.py* in a text editor and set the following paths.
```python
#folder path to experiment-set track data
FILE_IMPORT_PATH = 'C:\Users/Andrew/CMP/Trackdata XMLs/test

#name of a saved copy of the imported trackfile data. 
#Once the data is saved to data/, trackmate file import 
#is not necessary and the data #can be reloaded with its name.
DATA_SAVE_NAME = 'test-files'

#folder path for analysis output
ANALYSIS_SAVE_PATH = 'C:\Users/ahan/Desktop/analysis/
```

###Customizing your analysis
[*ExampleDriver.py*](www.google.com) is a boilerplate script that runs analysis jobs. The Driver and jobs are working examples that analyze [*data/test*](www.google.com), and they can be copied and modified as needed.

####Importing, Loading, Filtering, Saving
```python
	#import the experiment set from the xml files 
	data = import("C:\ahan\Desktop\test-experiment-dataset/, "testset") #path and savename.
	
	#imported data is saved to CMP/data/ and can be loaded
	data = load("testset")
	
	#create a copy 
	dataCopy = deepcopy(data)

	#filter any measurement defined in TrackMeasurements.py
	filters = {}
	
	#slices of experiment dimensions
	filters['frames'] = [[5, 147]]
	filters['xpos'] = [[100, 1390]]
	filters['ypos'] = [[100, 1390]]
	
	#track measurements calculated within those slices
	filters['age'] = [[15, float('inf')]]
	filters['directionality'] = [[-1, -0.8], [0.8, 1]]
	
	#keep only tracks that pass the filters and dimensions
	#select frames 5 to 147, and delete any track paths 
	#outside of xpos and ypox coordinates witih the experimentin microns.
	#then calculate age and directionality of tracks, and keep only tracks
	#the pass measurement filters
	dataCopy.selectData(filters)
	
	#save data whenever
	save(dataCopy, 'filteredData')
	
	
```

Data is filtered in the order of frames, area, and measurements. The spatial and temporal filter functions recompute measurements after filtering. To create a fresh copy of the data for a different set of filters is

####Analyzing
```python
#select only one experiment to analyze
experimentA = data.experiments['experimentA']

#render the experiment
render(experimentA)

#plotScatter can be given 2 or 3 measurements to visualize
experimentA.plotScatter("xStartPos", "yStartPos", "avgMov")

#make a histogram of any measurement
experimentA.histogram("velocity")

#bin tracks by one measurement, and calculate number and age-weighted
#averages of another measurement
experiment.plotBinData("xpos", "velocity")

#bin tracks by measurement percentiles
experiment.plotPercentHistogram("avgMov", "directionality", percents = [0, 25, 75, 90, 100])

#Scan through frames 0 to 150 with 10 steps, and perform the same analysis as above.
experiment.scan("frames", 0, 10000, 10, TrackFile.plotBinData, "xPos", "velocity")

#Run your analysis functions on an entire set of experiments
data.iterate(TrackFile.plotBinData, "xPos", "velocity")
data.iterate(TrackFile.scan, "frames", 0, 10000, 10, TrackFile.plotBinData, "xPos", "velocity")
data.iterate(TrackFile.render)

#Compare results of your analyses
data.compare(TrackFile.plotBinData, "xPos", "velocity")
data.compare(TrackFile.plotScatter, "avgMov", "directionality")

#Write your project data to an excel file
data.writeData()

#Write analysis data to a specific excel file
xpos_velocity_book = createWorkbook()
experiment.plotBinData("xpos", "velocity", workbook = [xpos_velocity_book, "plotBinData"])
experiment.plotPercentHistogram("avgMov", "directionality", workbook = [xpos_velocity_book, "percHist"])
```

####Adding new measurements
There are a ton of measurements already available for track data and experiment parameter data, and adding new measurements to CMP is very simple.

1. Define a new measurement in [*CMP/lib/TrackMeasurements.py*](https://github.com/AndrewHanSolo/CMP/blob/master/lib/TrackMeasurements.py)
2. Implement the measurement calculation function in [*CMP/lib/TrackMeasurementFunctions.py*] ( https://github.com/AndrewHanSolo/CMP/blob/master/lib/TrackMeasurementFunctions.py)
3. Add your new measurement to DefaultTrackMeasurements in [*CMP/lib/TrackClassGlobals.py*] (https://github.com/AndrewHanSolo/CMP/blob/master/lib/TrackClassGlobals.py)

```python
DefaultTrackMeasurements = {

#track-dimensions measurements. defined for slicing tracks and scanning

	"xPos"            : xPos,            # x-coordinate of the track
	"yPos"            : yPos,            # y-coordinate of the track
	"frames"          : frames,          # frame-coordinate of the track


#track measurements calculated with track-dimensions and experiment parameters

	"age"             : age,             # range of frames over which track exists
	"avgMov"          : avgMov         , # average movement of the track per frame
	"velocity"        : velocity       , # average migration distance of the track per frame
	"concentration"   : concentration  , # local chemical concentration of xStartPos
	"directionality"  : directionality , # uphill gradient track movement / total track movement
	"mp"              : getMP          , # degree that track moves in one direction
	"xMigrationSpeed" : xMigrationSpeed, # total x-direction migration distance
	"yMigrationSpeed" : yMigrationSpeed, # total y-direciton migration distance
	"numFrames"       : numFrames      , # number of frames in the track
	"xStartPos"       : getXStartPos   , 
	"xEndPos"         : getXEndPos     ,
	"yStartPos"       : getYStartPos   ,
	"yEndPos"         : getYEndPos     ,
	"firstFrame"      : firstFrame     ,
	"lastFrame"       : lastFrame  
}

```
You're Done! You can use your new measurement like any other.


