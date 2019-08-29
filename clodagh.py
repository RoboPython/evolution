import pygame, sys, random, time, math
from pygame.locals import *
pygame.init()

AREASIZE = 400
NUMBER_OF_FOOD = 300
NUMBER_OF_HERBIVORES = 1


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
		self.sucessful = False
		self.colour = RED
		self.alive = True;
		self.energy = 500;

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


	def move(self,finishedOrDeadHerbivores):
		
		if not(self.sucessful ==True or self.alive == False):

			if (self.x < 10 or self.y <10 or self.x >AREASIZE-10-self.size or self.y >AREASIZE-10-self.size) and self.eaten >=1:
				self.sucessful = True
				self.colour = BLUE
				finishedOrDeadHerbivores +=1

			else:
				self.sucessful = False
				self.colour = RED



			if not (self.sucessful):
				self.x += self.speed * self.direction[0]
				self.y += self.speed * self.direction[1]
				self.energy -= self.speed*self.speed


				if (self.energy<0):
					self.alive = False
					self.colour = WHITE
					self.speed = 0;
					finishedOrDeadHerbivores +=1

		return finishedOrDeadHerbivores
		


	
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

for x in xrange(NUMBER_OF_FOOD):
	food[x] = Food(x)

for item in food.keys():
	food[item].draw(GREEN)


herbivores = {}
herbIDcounter =0
for x in xrange(NUMBER_OF_HERBIVORES):
	herbivores[herbIDcounter] = Herbivore(herbIDcounter)
	herbIDcounter +=1



def updateFoodList(food):
	for item in eatenFood:
		food[item].draw(BLACK)
		del food[item]
	return food

def nextDay(food,herbivores,herbIDcounter):
	for item in herbivores.keys():
		herbivores[item].undraw()

	
	new_herbivores = {}

	for item in herbivores.keys():
		herbie = herbivores[item]
		if (herbie.sucessful):
			herbie.targetFood = None
			herbie.eaten = 0
			herbie.sucessful = False
			herbie.colour = RED
			herbie.alive = True;
			herbie.energy = 10000000;
			new_herbivores[herbie.idNumber] = herbie
			new_herbivores[herbIDcounter] = Herbivore(herbIDcounter)
			new_herbivores[herbIDcounter].speed = new_herbivores[herbie.idNumber].speed
			herbIDcounter +=1












	for item in food.keys():
		food[item].draw(BLACK)

	food = {}

	for x in xrange(NUMBER_OF_FOOD):
		food[x] = Food(x)

	for item in food.keys():
		food[item].draw(GREEN)


	return [food,new_herbivores,herbIDcounter]



finishedOrDeadHerbivores = 0
while True: # main game loop
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()


	for item in food.keys():
		food[item].draw(GREEN)

	
	for item in herbivores.keys():
		herbie = herbivores[item]
		herbie.undraw()
		herbie.chooseDirection()
		finishedOrDeadHerbivores = herbie.move(finishedOrDeadHerbivores)
		herbie.draw()	

	food = updateFoodList(food)
	eatenFood = []


	#idea is to get rid of those that havent eaten but will not find food
	'''
	if (len(food) ==0):
		for item in herbivores.keys():
			if herbivores[item].eaten == 0:
				herbivores[item].alive = False
				herbivores[item].colour = WHITE
				finishedOrDeadHerbivores += 1

	'''


	print finishedOrDeadHerbivores
	print len(herbivores)
	print "  "
	print "-----------------"


	if(finishedOrDeadHerbivores == len(herbivores)):
		nextDayReturns = nextDay(food,herbivores,herbIDcounter)
		food = nextDayReturns[0]
		herbivores = nextDayReturns[1]
		herbIDcounter = nextDayReturns[2]
		finishedOrDeadHerbivores = 0

		total = 0.00
		for item in herbivores.keys():
			herbie = herbivores[item]
			total += herbie.speed
		print total/len(herbivores)





			



	

	time.sleep(0.01)

	
		

	
	pygame.display.update()
