import TrackClassGlobals as TCG
import general as gen
import numpy as np


#DEFAULT TRACK FIELD CALCULATION FUNCTIONS

#the mean of absolute travel distance between frames. right now only does x and y dims
def getAverageMovement(track, **kwargs):
	avgMov = []
	diff = []
	frameDistanceBetweenFrames = []
	positionalDistanceBetweenFrames = []
	for index in range(0, len(track.x) - 1):
		#the number of frames by which two adjacent elements in track are separated
		frameDistanceBetweenFrames = track.t[index + 1] - track.t[index] 
		#the absolute positional distance between adjacent tracked frames
		positionalDistanceBetweenFrames = gen.getDistance(track.x[index], track.x[index + 1], track.y[index], track.y[index + 1])
		#the distance traveled per frame between adjacent tracked frames
		diff.append(positionalDistanceBetweenFrames / frameDistanceBetweenFrames)
	return gen.nanMean(diff) * TCG.SPEED_CONVERSION_FACTOR


#finalX-initialX position / age
def getVelocity(track, **kwargs):
	age = getAge(track)
	xTravel = track.x[-1] - track.x[0]
	yTravel = track.y[-1] - track.y[0]
	return (gen.pythagorean(xTravel, yTravel) / age) * TCG.SPEED_CONVERSION_FACTOR

#finalY-initialY position / age
def getxMigrationSpeed(track, **kwargs):
	age = getAge(track)
	return (track.x[-1] - track.x[0])/age  	

#finalY-initialY position / age
def getyMigrationSpeed(track, **kwargs):
	age = getAge(track)
	return (track.y[-1] - track.y[0])/age  

def getAbsVelocity(track, **kwargs):
	velocity = getVelocity(track)
	return abs(velocity)

#range of frames over which track exists
def getAge(track, **kwargs):
	return track.t[-1] - track.t[0]

#number of frames in which track data actually exists
def getNumFrames(track, **kwargs):
	return len(track.x)

#directionality calculated based on field vector
def getDirectionality(track, **kwargs):
	fieldVector = TCG.FIELD_VECTOR_INSTANCE
	#TODO: change way field vec is assigned
	xDiffs = gen.getDifferenceArray(track.x)
	yDiffs = gen.getDifferenceArray(track.y)

	directedness = []
	#calculate instantenous directionality between frames
	for dx, dy in zip(xDiffs, yDiffs):
		vector = [dx, dy]
		normVector = gen.normalizeVector(vector)
		if normVector != 0:
			normFieldVector = gen.normalizeVector(fieldVector)
			#print(normFieldVector)
			directionality = gen.dotProduct(vector, fieldVector) / normVector * normFieldVector
			directedness.append(directionality)
		else:
			directedness.append(0)
	return gen.nanMean(directedness)

def getxStartPos(track, **kwargs):
	return track.x[0]

def getxEndPos(track, **kwargs):
	return track.x[-1]

def getyStartPos(track, **kwargs):
	return track.y[0]

def getyEndPos(track, **kwargs):
	return track.y[-1]

def getFirstFrame(track, **kwargs):
	return track.t[0]

def getLastFrame(track, **kwargs):
	return track.t[-1]

def getMigrationPersistence(track, **kwargs):
	travel = []
	xDiffs = gen.getDifferenceArray(track.x)
	yDiffs = gen.getDifferenceArray(track.y)

	for x, y in zip(xDiffs, yDiffs):
		travel.append(gen.pythagorean(x, y))

	totalTravel = np.sum(travel)

	xDistance = track.x[-1] - track.x[0]
	yDistance = track.y[-1] - track.y[0]

	if totalTravel == 0:
		return 0

	return gen.pythagorean(xDistance, yDistance) / totalTravel

def getConcentration(track, maxX = None, gradient = None):
	if maxX and gradient:
		return ((gradient) / maxX) * (maxX - getxStartPos(track))
	return 0
