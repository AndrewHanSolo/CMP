#main module initializer
import os

CMP_PATH = os.getcwd()
DATA_PATH = CMP_PATH + '/data/'
TRACK_FILES_IMPORT_PATH = CMP_PATH + '/TrackFile XMLs/'
ANALYSIS_PATH = CMP_PATH + '/analysis/'

from ExampleDriver import *






print(locals())