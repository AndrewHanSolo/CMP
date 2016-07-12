#Functions for importing TrackMate output data to CMP

import os
import csv
import TrackClass as TC
import xml.etree.ElementTree as ET
from pathlib import Path
from general import *
from TrackClassGlobals import *


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
		self.filters = TCG.DefaultFilters
		self.expParams = TCG.Default_Exp_Params.copy()


	def getExperimentParameters(self):
		#apply settings to all tracks (now merged to single list)
		settingsFilePath = self.path + '/settings.txt'
		if os.path.isfile(settingsFilePath):
			with open(settingsFilePath) as f:
				reader = csv.reader(f, delimiter='\t')
				d = list(reader)
				for line in d:
				#Reverse track positions if Reverse exists in settings.txt
					if line[0] == 'Reverse':
						self.expParams['reverse'] = True
					if line[0] == 'Gradient':
						self.expParams['gradient'] = float(line[1])
					if line[0] == 'SpatialConversion':
						self.expParams['spatialConversionFactor'] = float(line[1])


	#returns TrackFile object (TrackFiles merged and metadata updated)
	def toTrackFile(self):
		self.getExperimentParameters()
		self.convertSpatialCoords()
		self.updateTrackFilePositions()
		self.setMaxX()
		if self.expParams['reverse']:
			self.reverseCoords()
		#print("\n") #for separating preprocessing outputs for 
				  #each individual experiment

		#merge all TrackFile Track objects together to one list
		mergedTracks = []
		for trackFile in self.trackFiles:
			for track in trackFile.tracks:
				mergedTracks.append(track)

		#transfers attributes from TrackFolder to newly merged TrackFile (transfer of metadata)
		print("merging....")
		mergedTrackFile =  TC.TrackFile(mergedTracks, self.folderName, path = self.path, filters = self.filters, master = True)
		for key, val in self.expParams.items():
			setattr(mergedTrackFile, key, val)
		return mergedTrackFile


	#update TrackFile track coordinates based on corresponding entries in
	#coordinates.txt if it exists in the experiment data folder
	def updateTrackFilePositions(self):
		print("updating coords...")
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
		if self.expParams['spatialConversionFactor']:
			self.expParams['maxX'] = self.expParams['maxX'] * self.expParams['spatialConversionFactor']
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
	def setMaxX(self):
		#find the minX and maxX to do shift track positions for consolidation
		minX = []
		maxX = []
		for trackFile in self.trackFiles:
			for track in trackFile.tracks:
				if not minX or (minX > min(track.x)): minX = min(track.x)
				if not maxX or (maxX < max(track.x)): maxX = max(track.x)

		#shift the tracks to prep for consolidation, set new maxX
		print(minX, maxX)
		for trackFile in self.trackFiles:
			for track in trackFile.tracks:
				for index in range(0, len(track.x)):
					#continue
					track.x[index] = track.x[index] - minX

		self.expParams['maxX'] = maxX - minX



