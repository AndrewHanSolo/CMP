#Cell Migration Analysis Platform (CMP)

##About
CMP is a lightweight and easily extendible python library for chemotaxis data analysis. It was designed primarily to improve the conclusive throughput of novel chemotaxis experiments developed by H. Mao et. al., and performed at the Johns Hopkins Translational Tissue Engineering Center and the Johs Hopkins Institute for Computational Medicine. A brief presentation detailing the experiment setup can be found [here](www.google.com). In brief, the experiments are high-population single-cell environment-cue-variation nuclear-stain chemotaxis studies. CMP was designed for use in tangent with the [TrackMate](https://github.com/fiji/TrackMate/) particle-tracking plugin available in the FIJI image processing program. CMP was written to provide non-programmers access to a streamlined cell-tracking analysis pipeline with simple yet powerful analysis functions and features. 

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
and generating mock chemotaxis image data requires
- Python 2 and pygame library (for Python 2)

##Getting Started
###Preparing Data for Import to CMP
1. Install FIJI
2. Open FIJI and press '[' to open the scripting window. Run *TrackMate Helpers/FIJI/ImageSequenceToTiff.ijm* to convert any image sequences to TiffStacks as necessary.
2. Run *TrackMate Helpers/FIJI/TrackMateBatchScript.py* on each experiment's TiffStack folder
3. Move the xml output files into appropriate experiment subdirectories within one parent directory
   * (Optional) Add settings.txt with experiment parameters into any experiment subdirectories.
   * (Optional) Add coordinates.txt with xml filenames corresponding to their relative physical position in microns

###Running ExampleDriver.py
*ExampleDriver.py* contains two example analysis jobs, where each job is defined in its own file within *jobs/*. The Driver and jobs are working examples that can be copied and modified as needed.
1. Within ExampleDriver.py... 
   * set IMPORT_PATH to point to the experiment set directory path
   * set SAVE_PATH to point to the directory in which all plots and excel files are saved
   * set SAVE_DATA to an appropriate name for the experiment set. The experiment set data will be saved to CMP/data/ and can be loaded without importing the xml files again.
2. Run the script. Plots and excel files should be saved to SAVE_PATH


####Filters
Any TrackMeasurement defined in *lib/TrackMeasurementFunctions" may be filtered by setting the measurement key within a dictionary to [[min, max], [min, max], ...]

####Analysis Functions
6. Insert any additional analyses to perform.
7. Run ExampleDriver.py


##Getting Started
###Pre-import Data File Structure

###Importing Data to CMP

###Filtering

###Plotting and Saving

###Serializing Analysis Data

###Adding measurements



useful for comparing the migration behavior of thousands of cells within various environments. 

The analysis pipeline involves 5 stages: 
a. Cell-Tracking and Migration Data Generation
b. Data Preprocessing (experiment reconstruction and grouping)
1. Data Filtering
2. Analysis

Stage a: A script runs automated tracking on batches of time-lapse microscopy video files using the TRACKMATE plugin within FIJI. TRACKMATE outputs cell centroid spatial and frame data in xml format.

Stage b: TRACKMATE output files are grouped to appropriate experiment directories. One experiment should contain all data files corresponding to all the video files for that experiment. Additionally, within each experiment directory there may be a coordinates.txt file and a settings.txt file. The coordinates file is used to combine migration data from multiple data files in order to reconstruct the full experiment. The settings file is used to specify various parameters specific to the experiment. All experiment directories should be contained in one parent directory. The parent directory is then loaded and saved into CMP for analysis.

Stage 1: Data filtering may be performed to select cells with specific qualities or within a specific spatiotemporal ranges for analysis.

Stage 2: CMP serves as a powerful library for performing custom analysis, and offers easy extensibility of track filters, measurement functions, and analysis scripting. Users not comfortable with programming have various “comprehensive” analysis scripts that can be performed with a single execution that will produce vast quantities of graphs and excel sheets reporting…

1. Spatiotemporal correlations to cell track measurements, including average movement speed, average velocity, migration persistence, and directionality.

2. Cell-track measurement binning and other-measurement correlations

3. Experiment summaries and cross-experiment comparisons
Stage 1 and 2 may be an iterative process, where preliminary analysis is performed before filtering and more analysis.




Cell Track Attributes:
Cell Track Filter Functions:
Current Measurement Functions:

Directionality:  ( ) where “Cell vector” is the positional vector a cell has moved in one frame and “Field vector” is the vector defined as the direction of the gradient. The percent (decimal) of movement in the direction of increasing concentration within a chemical gradient.
Migration persistence (): The percent (decimal) of movement in one direction, as opposed to any direction
Mean velocity (): The average movement over the entire temporal range
Mean migration speed (): The average distance travelled per frame
