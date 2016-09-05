#Cell Migration Analysis Platform (CMP)

##INTRO
CMP is a lightweight and easily extendible python library for cell migration data analysis. It was designed primarily to facilitate conclusive throughput for novel high-population single-cell combinatorial topographical and biochemical gradient guidance cue migration experiments developed by H. Mao et. al, and performed at the Johns Hopkins Translational Tissue Engineering Center and Johns Hopkins Institute for Computational Medicine. The experimental setup and the need for CMP's development is explained further below. CMP was designed for use in tangent with the TrackMate cell-tracking plugin available in the FIJI image processing program, but analyzing data from other tracking softwares is also possible. Furthermore, CMP was designed to offer comprehensive cell-tracking analysis to non-programmers.

##Features
- Full experiment reconstruction from multiple data files.
- Easy extension of the Track measurements list
- Customizable Track data filtering
- A small but powerful set of functions for correlating...
   - Track measurement vs Track measurement 
   - Track measurement vs Experimental/Environmental parameter
   - Experiment track metadata vs Experimental/Environmental parameter
- Iterative spatiotemporal and measurement scanning with adjustable scope and resolution
- Excel serialization of analysis results
- Scripts for batch-file TrackMate processing and test-data generation
- Simple code and file structure, and well commented

##Operating Systems and Dependencies
CMP runs on Windows 10, Ubuntu 14.04, and Fedora24. The core library uses Python3, but some additional scripts included use Python2 and IJM.
- numpy 1.8.2
- xlsxwriter 0.5.2
- scipy 0.13.3
- matplotlib 1.3.1
- pygame (python2, optional. Used in the TrackMate test-data generation script)

##Brief Summary of the Analysis Pipeline



This program is designed to facilitate high-population single-cell
migration analysis. It is used to analyze cell-track data outputted by the
FIJI TrackMate plugin. Multiple data files belonging to one experiment can be 
combined for full experimental reconstruction, and 

@ANALYSIS STAGES




@CAPABILITIES
-



@CODE STRUCTURE


@DEPENDENCIES





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
