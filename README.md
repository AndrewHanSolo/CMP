#Cell Migration Analysis Platform (CMP)

##About
CMP is a lightweight python script library that offers a streamlined chemotaxis data analysis pipeline. It was designed primarily to improve the conclusive throughput of novel chemotaxis experiments developed by H. Mao et. al., which are performed at the Johns Hopkins Translational Tissue Engineering Center and the Johns Hopkins Institute for Computational Medicine. A presentation detailing the experiment setup can be found [here](www.google.com). In brief, these experiments were high-population nuclear-stain single-cell environment-cue-modulation time-lapse chemotaxis studies. CMP was designed for use in tangent with the open source [TrackMate](https://github.com/fiji/TrackMate/) particle-tracking plugin available within the FIJI image processing program. CMP offers powerfully simple functions and features that make complex chemotaxis experiment analysis accessible even to non-programmers.

##Functions and Features
- Multi-file experiment reconstruction
- Streamlined batch-experiment analysis and cross-experiment comparisons
- Multi-bin measurement filtering and iterative scanning analysis
- Single and multi-experiment level analysis functions
- Analysis serialization
- Scripts for batch-file TrackMate processing and generating mock chemotaxis image data
- Simple code and file structure for easy extension and interfacing
- Easy addition of new measurements
- Ready out of of box

##Installation and Dependencies
CMP is stable on Windows 10, Ubuntu 14.04, and Fedora 24. The program is written with Python 3.5.2, but the TrackMate and mock-data scripts are in Python 2 and IJM, respectively.
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
###Obtaining track data from time lapse images and importing to CMP
1. Install FIJI
2. Open FIJI and press '[' to open the scripting window. Run *TrackMate Helpers/FIJI/ImageSequenceToTiff.ijm* to convert folders of image sequences to TiffStacks.
2. Run *TrackMate Helpers/FIJI/TrackMateBatchScript.py* on each experiment's TiffStack folder
3. Move the xml output files into appropriate experiment subdirectories within one parent directory
   * (Optional) Add settings.txt with experiment parameters into any experiment subdirectories.
   * (Optional) Add coordinates.txt with xml filenames corresponding to their relative physical position in microns
4. Open *ExampleDriver.py* in a text editor and set the following paths
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
5. Run the script. Plots and excel files should be saved to ANALYSIS_SAVE_PATH

###Customizing your analysis
*ExampleDriver.py* is a boilerplate script that calls an analysis job within *jobs/*. The Driver and jobs are working examples that analyze *data/test*, and they can be copied and modified as needed.

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
Data is filtered in the order of frames, area, and measurements. The spatial and temporal filter functions recompute measurements after filtering. To create a fresh copy of the data for a different set of filters is
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



