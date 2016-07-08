import TrackClassGlobals as TCG
import general as gen
import numpy as np


#DEFAULT TRACK FIELD CALCULATION FUNCTIONS

#the mean of absolute travel distance between frames. right now only does x and y dims
def getAverageMovement(self):
	avgMov = []
	diff = []
	frameDistanceBetweenFrames = []
	positionalDistanceBetweenFrames = []
	for index in range(0, len(self.x) - 1):
		#the number of frames by which two adjacent elements in track are separated
		frameDistanceBetweenFrames = self.t[index + 1] - self.t[index] 
		#the absolute positional distance between adjacent tracked frames
		positionalDistanceBetweenFrames = gen.getDistance(self.x[index], self.x[index + 1], self.y[index], self.y[index + 1])
		#the distance traveled per frame between adjacent tracked frames
		diff.append(positionalDistanceBetweenFrames / frameDistanceBetweenFrames)
	return gen.nanMean(diff) * TCG.SPEED_CONVERSION_FACTOR


#finalX-initialX position / age
def getVelocity(self):
	age = getAge(self)
	xTravel = self.x[-1] - self.x[0]
	yTravel = self.y[-1] - self.y[0]
	return (gen.pythagorean(xTravel, yTravel) / age) * TCG.SPEED_CONVERSION_FACTOR

#finalY-initialY position / age
def getxMigrationSpeed(self):
	age = getAge(self)
	return (self.x[-1] - self.x[0])/age  	

#finalY-initialY position / age
def getyMigrationSpeed(self):
	age = getAge(self)
	return (self.y[-1] - self.y[0])/age  

def getAbsVelocity(self):
	velocity = getVelocity(self)
	return abs(velocity)

#range of frames over which track exists
def getAge(self):
	return self.t[-1] - self.t[0]

#number of frames in which track data actually exists
def getNumFrames(self):
	return len(self.x)

#directionality calculated based on field vector
def getDirectionality(self):
	fieldVector = TCG.FIELD_VECTOR_INSTANCE
	#TODO: change way field vec is assigned
	xDiffs = gen.getDifferenceArray(self.x)
	yDiffs = gen.getDifferenceArray(self.y)

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

def getxStartPos(self):
	return self.x[0]

def getxEndPos(self):
	return self.x[-1]

def getyStartPos(self):
	return self.y[0]

def getyEndPos(self):
	return self.y[-1]

def getFirstFrame(self):
	return self.t[0]

def getLastFrame(self):
	return self.t[-1]

def getMigrationPersistence(self):
	travel = []
	xDiffs = gen.getDifferenceArray(self.x)
	yDiffs = gen.getDifferenceArray(self.y)

	for x, y in zip(xDiffs, yDiffs):
		travel.append(gen.pythagorean(x, y))

	totalTravel = np.sum(travel)

	xDistance = self.x[-1] - self.x[0]
	yDistance = self.y[-1] - self.y[0]

	if totalTravel == 0:
		return 0

	return gen.pythagorean(xDistance, yDistance) / totalTravel

def getConcentration(self, maxX = 0, gradient = 0):
	if gradient == 0 and maxX == 0:
		return 0
	return (gradient / maxX) * (maxX - getxStartPos(self))

