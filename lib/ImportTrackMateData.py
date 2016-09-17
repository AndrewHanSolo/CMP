#Functions for importing TrackMate output data to CMP

import TrackClass as TC
from General import *
from TrackClassGlobals import *
import ExperimentParams as EP
import os
import csv
import xml.etree.ElementTree as ET
from pathlib import Path


#returns TrackFile object of TrackMate tracking output file
def importTracksFromFile(filepath):
	tree = ET.parse(filepath)
	trackFile = tree.getroot()
	tracks = []
	for track in trackFile:
		x = []
		y = []
		z = []
		t = []
		for element in track:
			x.append(float(element.attrib['x']))
			y.append(float(element.attrib['y']))
			z.append(float(element.attrib['z']))
			t.append(float(element.attrib['t']))
		trackObject = TC.Track(x, y, z, t) 
		tracks.append(trackObject)
	fileName = os.path.basename(filepath)
	return TC.TrackFile(tracks, fileName)


#Iterate over all TrackMate output files in a folder,
#convert them all to TrackFile objects and add them to a TrackFolder object
def importTracksFromFolder(folderpath):
	trackFiles = []
	#get all files from folderpath and sort in numerical order
	files = (os.listdir(folderpath)) 
	sort_nicely(files)
	#iterate over all files and append TrackFile object for that file to array
	for fileName in files: 
		fullPath = os.path.join(folderpath, fileName)
		if not fileName.endswith('.xml'): continue #get full path name and if file is xml format
		trackFiles.append(TC.importTracksFromFile(os.path.abspath(fullPath))) #import trackFileData from xml to python
	#assign trackFiles and foldlerName to TrackFolder object
	folderName = os.path.basename(folderpath)
	return TrackFolder(trackFiles, folderName, folderpath)


####################################
#TrackFolder objects holds all TrackFiles for one experiment. This object
#is used for preprocessing data and combining all TrackFiles into one TrackFile
#data structure holding all data for Trackmate xml files in a single folder
#path is full filepath for folder (for finding coordinates.txt file in folder directory)
class TrackFolder():

	def __init__(self, trackFiles, folderName, folderPath):
		self.trackFiles = trackFiles
		self.folderName = folderName
		self.path = folderPath
		self.filters = {}
		self.expParams = TCG.DefaultExpParams.copy()


	def getExperimentParameters(self):
		if self.folderName in EP.ExpParams:
			vprint("Applying experiment parameters from python definition\n")
			self.expParams = EP.ExpParams[self.folderName]
		elif os.path.isfile(self.path + '/settings.txt'):
			settingsFilePath = self.path + '/settings.txt'
			vprint("Applying experiment parameters from settings file\n")
			with open(settingsFilePath) as f:
				reader = csv.reader(f, delimiter='\t')
				d = list(reader)

				for line in d:

					try:

						if line[0] == 'id':
							self.expParams['id'] = line[1]

						if line[0] == 'gradientStrength':
							self.expParams['gradientStrength'] = float(line[1])

						if line[0] == 'gradientVector':
							self.expParams['gradientVector'] = [float(line[1]), float(line[2])]

						if line[0] == 'reverse':
							self.expParams['reverse'] = bool(float(line[1]))

						if line[0] == 'spatialConversionFactor':
							self.expParams['spatialConversionFactor'] = float(line[1])

						if line[0] == 'frameInterval':
							self.expParams['frameInterval'] = float(line[1])

						#override calculated value if present in settings
						if line[0] == 'speedConversionFactor':
							self.expParams['speedConversionFactor'] = float(line[1])
					except:
						pass
		
		#calculate and set speedConversionFactor (pixels/frame -> microns/hour) if it is
		#not already in settings file.
		if not self.expParams['speedConversionFactor']:
			spatialFactor = self.expParams['spatialConversionFactor']
			frameInterval = self.expParams['frameInterval']
			self.expParams['speedConversionFactor'] = spatialFactor / frameInterval * 60

		vprint("Setting %s experiment params as %s\n\n" %(self.folderName, sorted(self.expParams.items())))
		return
			


	#returns TrackFile object (TrackFiles merged and metadata updated)
	def toTrackFile(self):
		self.getExperimentParameters()
		self.convertSpatialCoords()
		self.updateTrackFilePositions()
		self.shiftTracksToOrigin()
		if self.expParams['reverse']:
			self.reverseCoords()

		#merge all TrackFile Track objects together to one list
		mergedTracks = []
		for trackFile in self.trackFiles:
			for track in trackFile.tracks:
				mergedTracks.append(track)

		#transfers attributes from TrackFolder to newly merged TrackFile (transfer of metadata)
		print("merging....")
		mergedTrackFile =  TC.TrackFile(mergedTracks, self.folderName, path = self.path, master = True)
		mergedTrackFile.expParams = self.expParams
		return mergedTrackFile


	#update TrackFile track coordinates based on corresponding entries in
	#coordinates.txt if it exists in the experiment data folder
	def updateTrackFilePositions(self):
		coordFilePath = self.path + '/coordinates.txt'
		print(coordFilePath)
		if os.path.isfile(coordFilePath):
			with open(coordFilePath) as f:
				reader = csv.reader(f, delimiter='\t')
				d = list(reader)
			vprint("Updating TrackFile positions...")
			vprint(str(d))
			for xAdjustment, trackFile in zip(d, self.trackFiles):
				if xAdjustment[0] == trackFile.fileName:
					for track in trackFile.tracks:
						for i, xValue in enumerate(track.x):
							track.x[i] = (track.x[i] + float(xAdjustment[1]))
				else:
					print(trackFile.fileName + ': TrackFile position updates failed. TrackFile and coordinates fileName do not match:')
					print('\tCoordinates filename: ' + xAdjustment[0] + ', Trackfile filename: ' + trackFile.fileName);


	#convert positions from pixels to microns
	def convertSpatialCoords(self):
		for trackFile in self.trackFiles:
			for track in trackFile.tracks:
				for index in range(0, len(track.x)):
					track.x[index] = track.x[index] * self.expParams['spatialConversionFactor']
					track.y[index] = track.y[index] * self.expParams['spatialConversionFactor']
		vprint(self.folderName + " track positions changing by spatial conversion factor " + str(self.expParams['spatialConversionFactor']))


	def reverseCoords(self):
		#set new positions based on min and max x positions over all tracks
		for trackFile in self.trackFiles:
			for track in trackFile.tracks:
				for index in range(0, len(track.x)):
					track.x[index] = self.expParams['maxX'] - track.x[index]
		vprint(self.folderName + " track positions reversed")


	#find the max x position across all tracks in all TrackFiles
	#(this should be done after updateTrackFilePositions)
	def shiftTracksToOrigin(self):
		#find the minX and maxX to do shift track positions for consolidation
		minX = []
		maxX = []
		minY = []
		maxY = []
		for trackFile in self.trackFiles:
			for track in trackFile.tracks:
				if not minX or (minX > min(track.x)): minX = min(track.x)
				if not maxX or (maxX < max(track.x)): maxX = max(track.x)
				if not minY or (minY > min(track.y)): minY = min(track.y)
				if not maxY or (maxY < max(track.y)): maxY = max(track.y)

		#shift tracks relative to 0,0 position (origin)
		for trackFile in self.trackFiles:
			for track in trackFile.tracks:
				for index in range(0, len(track.x)):
					track.x[index] = track.x[index] - minX
					track.y[index] = track.y[index] - minY

