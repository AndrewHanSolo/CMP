#Cell Migration Analysis Platform (CMP)

##About
CMP is a lightweight and easily extendible python library for chemotaxis data analysis. It was designed primarily to improve the conclusive throughput of novel chemotaxis experiments developed by H. Mao et. al., and performed at the Johns Hopkins Translational Tissue Engineering Center and the Johns Hopkins Institute for Computational Medicine. A presentation detailing the experiment setup can be found [here](www.google.com). In brief, the experiments are high-population nuclear-stain single-cell environment-cue-modulation chemotaxis studies. CMP was designed for use in tangent with the [TrackMate](https://github.com/fiji/TrackMate/) particle-tracking plugin available in the FIJI image processing program. CMP was written to provide non-programmers access to a streamlined cell-tracking analysis pipeline with simple yet powerful analysis functions and features. 

##Functions and Features
- Multi-file experiment reconstruction
- Cross-experiment measurement comparison functions
- Polynotic-multi-binned measurement filtering and scanning/iterative analysis
- Single and multi-experiment level measurement correlation functions
- Result serialization in excel
- Scripts for batch-file TrackMate processing and generating mock chemotaxis image data
- Simple code and file structure for easy extension and interfacing
- Turn-key ready for analysis

##Installation and Dependencies
CMP seems to be stable on Windows 10, Ubuntu 14.04, and Fedora 24. The program is written with Python 3.5.2, but the TrackMate and mock-data scripts are in Python 2 and IJM, respectively.
The required libraries for analysis are
- numpy 1.8.2
- xlsxwriter 0.5.2
- scipy 0.13.3
- matplotlib 1.3.1

Running the TrackMate plugin script requires
- Python 2

Generating mock image data requires
- Python 2
- pygame

##Getting Started
###Importing image sequence data to CMP
1. Install FIJI
2. Open FIJI and press '[' to open the scripting window. Run *TrackMate Helpers/FIJI/ImageSequenceToTiff.ijm* to convert any image sequences to TiffStacks as necessary.
2. Run *TrackMate Helpers/FIJI/TrackMateBatchScript.py* on each experiment's TiffStack folder
3. Move the xml output files into appropriate experiment subdirectories within one parent directory
   * (Optional) Add settings.txt with experiment parameters into any experiment subdirectories.
   * (Optional) Add coordinates.txt with xml filenames corresponding to their relative physical position in microns

###Running ExampleDriver.py
*ExampleDriver.py* is a boilerplate script that calls an analysis job within *jobs/*. The Driver and jobs are working examples that analyze test data (*data/test*), and can be copied and modified as needed.
1. Within ExampleDriver.py... 
   * set IMPORT_PATH to point to the experiment set directory path
   * set SAVE_PATH to point to the directory in which all plots and excel files are saved
   * set SAVE_DATA to an appropriate name for the experiment set. The experiment set data will be saved to CMP/data/ and can be loaded without importing the xml files again.

2. Run the script. Plots and excel files should be saved to SAVE_PATH

###Customizing your analysis
####Setting Experiment Parameters
####Data Filtering
Any track measurement defined in *lib/TrackMeasurementFunctions* may be filtered.

```python
	dataCopy = deepcopy(data)

	filters = {}
	filters['frames'] = [[5, 147]]
	filters['xPos'] = [[100, 1390]]
	filters['yPos'] = [[50, 700], [[800, 1050]]
	filters['age'] = [[15, float('inf')]]
	filters['directionality'] = [[-1, -0.8], [0.8, 1]]
	
	dataCopy.selectData(filters)
```
Data is filtered in the order of frames, area, and measurements. The spatial and temporal filter functions recompute measurements after filtering. To create a fresh copy of the data for a different set of filters is simply 
```python
datacopy = deepcopy(data)
datacopy.selectData(newFilters)
```
####Analysis Functions
```python
experiment = data.experiments['test']

#basic functions
experiment.plotScatter("xStartPos", "yStartPos")
experiment.plotScatter("xStartPos", "yStartPos", "avgMov")
experiment.plotHistogram("velocity", None)

#Split tracks into bins of xpos and compute average velocity in each bin.
experiment.plotBinData("xpos", "velocity")

#Scan through frames 0 to 150 with 10 steps, and perform the same analysis as above.
experiment.scan("frames", 0, 10000, 10, TrackFile.plotBinData, "xPos", "velocity")

#Perform the two analyses above on all experiments in the set. 
data.iterate(TrackFile.plotBinData, "xPos", "velocity")
data.iterate(TrackFile.scan, "frames", 0, 10000, 10, TrackFile.plotBinData, "xPos", "velocity")

#Compare experiments for an analysis.
data.compare(TrackFile.plotBinData, "xPos", "velocity")

#Write summary data to a workbook
data.writeData()

#Write data for an analysis function
xpos_velocity_book = createWorkbook()
experiment.plotBinData("xpos", "velocity", workbook = [xpos_velocity_book, "plotBinData"])
experiment.plotHistogram("veocity", None, workbook = [xpos_velocity_book, "histogram"])
experiment.scan(TrackFile.plotBinData, "xpos", "velocity", workbook = createWorkbook())

#Render the data spatial movement
experiment.render()
```
####Add new track measurement
Adding new measurements to CMP is very simple.

1. Declare a new measurement in *lib/TrackMeasurements.py*
2. Implement the measurement calculation function in *lib/TrackMeasurementFunctions.py*
3. Add your new measurement to the list of DefaultTrackMeasurements in *lib/TrackClassGlobals.py*

You're Done! You can now filter and analyze your measurement.



