import math as m
import pygame
import pygame.draw
import numpy as np
pygame.init()
screenSize = (800, 800)
screen = pygame.display.set_mode(screenSize)
while not pygame.display.get_active():
	time.sleep(0.1)
pygame.display.set_caption("4D viewer", "4D viewer")
clock = pygame.time.Clock()
framerate = 60

def translate(d, points):
	transPoints = np.zeros(shape=(len(points), 4))
	transPoints[:,0] = points[:,0]+d[0]
	transPoints[:,1] = points[:,1]+d[1]
	transPoints[:,2] = points[:,2]
	transPoints[:,3] = points[:,3]
	return transPoints

def rotate(a, points):
	rotPoints = np.zeros(shape=(len(points), 4))
	rotPoints[:,0] = points[:,0]*m.cos(a) - points[:,1]*m.sin(a)
	rotPoints[:,1] = points[:,1]*m.cos(a) + points[:,0]*m.sin(a)
	rotPoints[:,2] = points[:,2]
	rotPoints[:,3] = points[:,3]
	return rotPoints

x = np.arange(-250, 250, 15)
mapList = []
for i in x:
	for j in x:
		for k in x:
			mapList.append([k, j, i, 0])
mapList = np.array(mapList)

trashList = np.array([251 for i in range(len(mapList))])

##### change the code here for a different function
#for point in mapList:
#	 point[3] = 10*m.sin(point[0]/40) + 10*m.sin(point[1]/40) + 10*m.sin(point[2]/40)

#for point in mapList:
#	 point[3] = 10*m.sin(point[0]/20) + 10*m.sin(point[1]/20) + point[2]

#for point in mapList:
#	 point[3] = 10*m.sin(point[0]/20) + -(point[1]/10)**2/4 + (point[2]/10)**2/4

for point in mapList:
	 point[3] = point[0] + -(point[1]/10)**2/4 + 5*(point[2]/10)**3/480
#####

camAngle = m.pi/4
horizAngle = 2

fourthViewRadius = 10
fourthViewPos = 0
hi = max(mapList[:, 3])-fourthViewRadius
lo = min(mapList[:, 3])+fourthViewRadius
const = (hi-lo)/2
offset = const+lo
while True:
	clock.tick(framerate)
	events = pygame.event.get()

	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

	camAngle += 0.01
	if camAngle >= 2*m.pi:
		camAngle -= 2*m.pi
	rotMap = rotate(camAngle, mapList)
	transMap = translate([screenSize[0]/2, screenSize[1]/2*horizAngle], rotMap)

	fourthViewPos += 0.02
	if fourthViewPos >= 2*m.pi:
		fourthViewPos -= 2*m.pi
	pos = const*m.sin(fourthViewPos)+offset
	constrainedMap = np.where(transMap[:,3] >= pos-fourthViewRadius, transMap[:,3], trashList)
	constrainedMap = np.where(constrainedMap <= pos+fourthViewRadius, constrainedMap, trashList)
	transMap[:,3] = constrainedMap[:]

	screen.fill((0, 0, 0))

	for p in transMap:
		if p[3] == 251:
			continue
		pygame.draw.circle(screen, (255, 0, 0), [p[0], p[1]/horizAngle - p[2]], 1)

	pygame.display.flip()
