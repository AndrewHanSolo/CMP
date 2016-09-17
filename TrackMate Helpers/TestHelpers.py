#!python2

import pygame
from pygame.locals import *
import random
import os
import io
import math




DEFAULT_IMAGE_WIDTH            = 1400 #
DEFAULT_IMAGE_HEIGHT           = 1400 #
DEFAULT_FILE_NUM               = 5    # number of files
DEFAULT_FRAME_NUM              = 50   # frames per file
DEFAULT_RADIUS                 = 20   #
DEFAULT_FILE_VELOCITY_INCREMENT = 0    #

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)




class Track():

	def __init__(self, velocity, velocityVariance, angle, angleVariance, acceleration):
		self.xpos = [random.randint(0, DEFAULT_IMAGE_WIDTH)]
		self.ypos = [random.randint(0, DEFAULT_IMAGE_HEIGHT)]
		self.velocity = velocity
		self.velocityVariance = velocityVariance
		self.angle = angle + random.randint(-angleVariance, angleVariance) #in degrees. direction for velocity
		self.acceleration = acceleration

	def generateNextFrame(self, velocityIncrement = None):

		radians = math.radians(self.angle)

		#acceleration but not velocityVariance affects track.velocity
		self.velocity = self.velocity + self.acceleration
		velocityVariance = random.randint(-self.velocityVariance, self.velocityVariance)
		velocity = self.velocity + velocityVariance
		if velocityIncrement:
			velocity = velocity + velocityIncrement

		xVel = velocity * math.cos(radians)
		yVel = velocity * math.sin(radians)

		xPos = (self.xpos[-1] + xVel) % DEFAULT_IMAGE_WIDTH
		yPos = (self.ypos[-1] + yVel) % DEFAULT_IMAGE_HEIGHT

		self.xpos.append(xPos)
		self.ypos.append(yPos)

	def draw(self, window, frameNum):
		pygame.draw.circle(window, WHITE, (int(self.xpos[frameNum]), int(self.ypos[frameNum])), DEFAULT_RADIUS, 0)



def generateData(velocity = 0,
				 velocityVariance = 0,
				 angle = 0,
				 angleVariance = 0,
				 acceleration = 0,
				 trackCount = 180,
				 folderName = "unnamed folder",
				 readmeMessage = "",
				 fileNum = DEFAULT_FILE_NUM,
				 fileVelocityIncrement = DEFAULT_FILE_VELOCITY_INCREMENT, 
				 frameNum = DEFAULT_FRAME_NUM): 
				 

	params = locals()

	pygame.init()
	random.seed()

	directory = "test-%s" % (folderName)
	if not os.path.exists(directory):
		os.makedirs(directory)
	else:
		print("Warning: Overwriting data in existing directory %s." % (folderName))

	#FOR EACH FILE
	for fileIndex in range(0, fileNum):
		#GENERATE DATA
		tracks = []
		tmpVel = velocity + (fileVelocityIncrement * fileIndex)
		#generate NUMBER of tracks
		for trackIndex in range(0, trackCount):
			tracks.append(Track(velocity, velocityVariance, angle, angleVariance, acceleration))
			#for each track, generate their path
			for frameIndex in range(0, frameNum):
				tracks[trackIndex].generateNextFrame(fileVelocityIncrement*fileIndex)

		#DRAW AND SAVE IMAGE
		pygame.display.set_caption("%s, %s" % (directory, fileIndex))
		window = pygame.display.set_mode((DEFAULT_IMAGE_HEIGHT, DEFAULT_IMAGE_WIDTH), 0, 32)
		for frameIndex in range(0, frameNum):
			window.fill(BLACK)
			for trackIndex in range(0, trackCount):
				tracks[trackIndex].draw(window, frameIndex)

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.update()

			subfolder = "file%s" % (fileIndex)
			filepath = "%s/%s" % (directory, subfolder)
			if not os.path.exists(filepath):
				os.makedirs(filepath)
			pygame.image.save(window, "%s/%s.png" % (filepath, frameIndex))

	#README FOR THIS DATA
	with io.FileIO("%s/readme.txt" % (directory), "w") as file:
		file.write("%s" % (str(sorted(params.items()))))

	file.close()
	pygame.quit()