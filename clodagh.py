import pygame, sys, random, time, math
from pygame.locals import *
pygame.init()

AREASIZE = 400


DISPLAYSURF = pygame.display.set_mode((AREASIZE, AREASIZE))
pygame.display.set_caption('Hello World!')

WHITE = (255,   255,   255)
RED = (255,   0,   0)
BLACK = (0,   0,   0)
GREEN = (0, 255, 0)
BLUE=(0,0,255)

def distance(p1, p2):
	return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


class Food(object):
	def __init__(self,idNumber):
		self.idNumber = idNumber
		self.size = 4
		self.x = random.randint(40,AREASIZE-40-self.size)
		self.y = random.randint(40,AREASIZE-40-self.size)

	def draw(self,colour):
		pygame.draw.rect(DISPLAYSURF, colour, (self.x, self.y, self.size, self.size))




class Herbivore(object):
	def __init__(self,idNumber):
		self.idNumber = idNumber
		self.size = 10
		self.speed = random.randint(1,5)
		self.direction = [random.uniform(-1.00,1.00),random.uniform(-1.00,1.00)]
		self.targetFood = None
		self.eaten = 0
		self.done = False
		self.colour = RED
		self.alive = True;
		self.energy = 1000;

		self.randomPosition = random.randint(self.size,AREASIZE-self.size/2)
		self.randomDistribution = random.randint(0,100)
		self.randomEdge = random.choice([self.size,AREASIZE-2*self.size])

		if self.randomDistribution < 50:
			self.x = self.randomPosition
			self.y = self.randomEdge
		else:
			self.y = self.randomPosition
			self.x = self.randomEdge

	def draw(self):
		pygame.draw.rect(DISPLAYSURF, self.colour, (self.x, self.y, self.size, self.size))


	def undraw(self):
		pygame.draw.rect(DISPLAYSURF, BLACK, (self.x, self.y, self.size, self.size))


	def move(self):
		


		if (self.x < 10 or self.y <10 or self.x >AREASIZE-10-self.size or self.y >AREASIZE-10-self.size) and self.eaten >=1:
			self.done = True
			self.colour = BLUE
		else:
			self.done = False
			self.colour = RED


		if not (self.done):
			self.x += self.speed * self.direction[0]
			self.y += self.speed * self.direction[1]
			self.energy -= self.speed*self.speed

		if (self.energy<0):
			self.alive = False
			self.colour = WHITE
			self.speed = 0;



	
	def chooseDirection(self):
		
		sortedFood = sorted(food.keys(), key=lambda e: distance(food[e], self))
		if self.eaten <1:
			if len(food) >= 1:
				self.targetFood = food[sortedFood[0]]

				xDiff = self.targetFood.x -self.x
				yDiff = self.targetFood.y -self.y


				if math.hypot(xDiff,yDiff) !=0:
					self.direction[0] = xDiff/math.hypot(xDiff,yDiff)
					self.direction[1] = yDiff/math.hypot(xDiff,yDiff)


				if math.fabs(xDiff) < 4 and math.fabs(yDiff) < 4:
					if self.targetFood.idNumber not in eatenFood:
						eatenFood.append(sortedFood[0])
						self.eaten +=1
			else:
				#they run around aimlessly...they're fucked anyway
				self.direction = [random.uniform(-1.00,1.00),random.uniform(-1.00,1.00)]

				
		else:
			closestEdgeDirection = {self.x:[-1,0],self.y:[0,-1],AREASIZE-self.x:[1,0],AREASIZE-self.y:[0,1]}
			sortedClosestEdge = sorted(closestEdgeDirection.keys())
			self.direction = closestEdgeDirection[sortedClosestEdge[0]]


eatenFood = []
food = {}
for x in xrange(5):
	food[x] = Food(x)

for item in food.keys():
	food[item].draw(GREEN)


herbivores = []
for x in xrange(10):
	herbivores.append(Herbivore(x))


def updateFoodList(food):
	for item in eatenFood:
		food[item].draw(BLACK)
		del food[item]
	return food

def nextDay(food):
	#not done yet
	for item in food.keys():
		food[item].draw(BLACK)

	food = {}

	for x in xrange(5):
		food[x] = Food(x)

	for item in food.keys():
		food[item].draw(GREEN)


	return food









while True: # main game loop
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()


	for item in food.keys():
		food[item].draw(GREEN)

	
	for herbie in herbivores:
		herbie.undraw()
		herbie.chooseDirection()
		herbie.move()
		herbie.draw()	

	food = updateFoodList(food)
	eatenFood = []

	if(len(food) ==0):
		canFinish = True
		for herbie in herbivores:
			if (herbie.eaten and herbie.alive and not herbie.done):
				canFinish = False

		if canFinish == True:
			food = nextDay(food)



		

	

	time.sleep(0.1)

	
		

	
	pygame.display.update()
