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
		self.x = random.randint(0+self.size/2.,AREASIZE-self.size/2)
		self.y = random.randint(0,AREASIZE)

	def draw(self,colour):
		pygame.draw.rect(DISPLAYSURF, colour, (self.x, self.y, self.size, self.size))




class Herbivore(object):
	def __init__(self):
		self.size = 10
		self.speed = random.randint(1,5)
		self.direction = [random.uniform(-1.00,1.00),random.uniform(-1.00,1.00)]
		self.targetFood = None

		self.randomPosition = random.randint(self.size,AREASIZE-2*self.size)
		self.randomDistribution = random.randint(0,100)
		self.randomEdge = random.choice([self.size,AREASIZE-2*self.size])

		if self.randomDistribution < 50:
			self.x = self.randomPosition
			self.y = self.randomEdge
		else:
			self.y = self.randomPosition
			self.x = self.randomEdge



	def draw(self,colour):
		pygame.draw.rect(DISPLAYSURF, colour, (self.x, self.y, self.size, self.size))


	def move(self):
			self.x += self.speed * self.direction[0]
			self.y += self.speed * self.direction[1]

	
	def lookForFood(self):
		sortedFood = sorted(food.keys(), key=lambda e: distance(food[e], self))
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

		else:
			self.direction[0] = -self.x/math.hypot(self.x,self.y)
			self.direction[1] = -self.y/math.hypot(self.x,self.y)

			




			

		
	



eatenFood = []
food = {}
for x in xrange(20):
	food[x] = Food(x)

for item in food.keys():
	food[item].draw(GREEN)


herbivores = []
for x in xrange(10):
	herbivores.append(Herbivore())


def updateFoodList(food):
	for item in eatenFood:
		del food[item]

	return food



while True: # main game loop
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()


	for item in food.keys():
		food[item].draw(GREEN)

	
	for herbie in herbivores:
		herbie.draw(BLACK)
		herbie.lookForFood()
		herbie.move()
		herbie.draw(RED)	
	food = updateFoodList(food)
	eatenFood = []

	time.sleep(0.1)

	
		

	
	pygame.display.update()
