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
Any track measurement defined in *lib/TrackMeasurementFunctions* may be filtered

```python
	filters = {}
	filters['frames'] = [[5, 147]]
	filters['xPos'] = [[100, 1390]]
	filters['yPos'] = [[50, 700], [[800, 1050]]
	filters['age'] = [[15, float('inf')]]
	filters['directionality'] = [[-1, -0.8], [0.8, 1]]
	
	data.selectData(filters)
```
Data is filtered in the order of frames, area, and measurements. The spatial and temporal filter functions recompute measurements after filtering. To create a fresh copy of the data for a different set of filters is simply 
```python
datacopy = deepcopy(data)
datacopy.selectData(newFilters)
```
####Functions
There are 4 core functions for inspecting correlations at the Experiment level.
#####plotBinData
```python
data.plotBinData("xPos", "velocity")
```bins tracks based on the first measurement argument, and computes the age-weighted average of the second measurement argument within each bin. The weight can be changed to any measurement. 
####plotHistogram
```python
data.plotHistogram("avgMov", None)
```
####plotPercentHistogram
```python
data.plotPercentHistogram("avgMov", "directionality", percents = [0, 25, 50, 75, 100])
```
Sorts tracks into bins (defined by optional argument percents) by their percentile of the first measurement argument, and computes number or weighted averages of the second measurement argument.
#####plotHistogram
#####plotPercentHistogram
#####scan
There are an additional 2 visualization functions that do no support scanning.
#####cellVisualization
#####heatmapVisualization
There are 2 core functions for correlating and comparing experiments in the set.
#####compare
#####iterate

####Plotting, Serializing and Saving
####Adding measurements


