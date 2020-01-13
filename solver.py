
import os

#We don't want to show the pygmy version and welcome message. Snif
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


from random  import uniform,randint
import tqdm

"""
We import pygame in order to create a patch for the long calculations
If the QLearning calculation time or the creation of the path is too long, the application crashes.
So we need to create a patch to avoid this
This patch is not too resource-intensive and is not necessary if you don't use the graphical interface
"""
import pygame

class Solver:
	def __init__(self,maze,learning_rate=0.8,discount_factor=0.5,maxstep=1000,epsilon=0.3,interface=True):
		"""
			Initiate the solver
			Hyperparameters :
			- maze : the maze which is a 2-dimensional array containing only numerical values
			- learning_rate : the learning rate of the QLearning algorithm, must be between 0 and 1
			- discount_factor : the discount factor of the QLearning algorithm, must be between 0 and 1
			- maxstep : Number of explorations the agent will perform. 
						An exploration starts at the start and must find the exit.
			- epsilon : the value of the espilon-greedy method, must be between 0 and 1
			- interface : if you are using the solver with an application (True) or not (False)
		"""

		self.learning_rate = learning_rate
		self.discount_factor = discount_factor
		self.maxstep = int(maxstep)
		self.epsilon = epsilon

		#Variable indicating whether an interface is used
		self.interface = interface

		"""
			Maze code :
			path = 0
			start = 1
			end = 2
			trap = 3
			wall = 4
		"""
		self.maze = maze

		#Create constants of the maze
		self.length = len(maze)
		self.width = len(maze[0])

		#Explore the maze
		self.start = None
		self.end = None
		self.trap = []
		for i in range(self.length):
			for j in range(self.width):
				ele = maze[i][j]
				if ele == 1:
					self.start = (i,j)
				elif ele == 2:
					self.end = (i,j)
				elif ele == 3:
					self.trap.append((i,j))

		#The maze must have an enter and an exit
		if self.start==None or self.end==None:
			print("Maze must have a start (code1) and an end (code 2)")
			quit()

	def learning(self):
		"""
			Algorithm of QLearning you can find in 
			"Reinforcement learning : An Introduction" of Sutton and Barto
		"""

		#Init the QTable
		self.createQ()

		#Until all the episodes are completed
		for i in tqdm.trange(self.maxstep):

			#Begin the episode at the start of the maze
			posX = self.start[0]
			posY = self.start[1]

			#The episode runs until the agent arrives at his destination
			while(not(posX==self.end[0] and posY==self.end[1]) and 
				not ((posX,posY) in self.trap)):

				#Application control
				if self.interface :

					#The crash proof patch
					events = pygame.event.get()
					for event in events:
						if event.type == pygame.QUIT:
							pygame.quit()
							exit()

				#The next position of the agent depend on a greedy choice
				choice = self.greedyChoice(posX,posY)

				#Update the next position of the agent
				newX,newY = self.updatePosition(choice,posX,posY)

				#Test if the new position is the exit
				if newX==self.end[0] and newY==self.end[1]:
					reward = 1

				#Test of the new position is a trap
				elif (newX,newY) in self.trap:
					reward = -1
				else:
					reward = 0

				#Coordinates in the QTable of the last and new position 
				t_pos = posX*self.width+posY
				tpos = newX*self.width+newY

				#Update the QTable
				self.Qtable[t_pos][choice] = self.Qtable[t_pos][choice] + self.learning_rate * (reward + self.discount_factor*max(self.Qtable[tpos]) - self.Qtable[t_pos][choice])

				#Position of the agent is update
				posX=newX
				posY=newY
		
		#When the algorithm is over, create the path the agent has to follow from the start to the end
		path = []
		posX = self.start[0]
		posY = self.start[1]

		#Create a counter while creating the path
		count = 0

		#Create the path until it finds the exit
		#OR it reaches a limit :
		#	The Q-Learning might not reach the best solution with the maxstep we fixed so you can't find the best way to the exit
		while not(posX==self.end[0] and posY==self.end[1]) and count<=self.length*self.width:

			#Application control
			if self.interface :

				#The crash proof patch
				events = pygame.event.get()
				for event in events:
					if event.type == pygame.QUIT:
						pygame.quit()
						exit()

			#Coordinates in the QTable of the position 
			pos = posX*self.width+posY

			#Take the best direction
			direction = self.Qtable[pos].index(max(self.Qtable[pos]))

			#Update the path
			path.append(direction)

			#Update the next position
			posX,posY = self.updatePosition(direction,posX,posY)

			count+=1

		return path,self.start


	def updatePosition(self,direction,posX,posY):
		"""
			Update (x,y) coordinates depend on a direction
		"""
		if direction==0:
			posX-=1
		elif direction==1:
			posX+=1
		elif direction==2:
			posY+=1
		elif direction==3:
			posY-=1
		return posX,posY

	def greedyChoice(self,posX,posY):
		"""
			Epsilon-Greedy choice
		"""
		#Take the line in QTable correspondint to the position
		ligne = self.Qtable[posX*self.width+posY]

		if uniform(0,1)>=self.epsilon:

			#best choice of the line
			return ligne.index(max(ligne))
		else:

			#Or take a random position 
			#Not the most elegant way to do it
			choice = []
			for i in range(4):
				if ligne[i]!=-1:
					choice.append(i)
			pos = randint(0,len(choice)-1)
			return choice[pos]

	def createQ(self):
		"""
			Create the Qtable
			Globaly, just have to test if the value at a specific position is a wall or not
		"""
		self.Qtable = []
		for i in range(self.length):
			for j in range(self.width):
				ligne = []
				#up
				if i-1<0 or self.maze[i-1][j]==4:
					ligne.append(-1)
				else:
					ligne.append(0)
				#bottom
				if i+1>=self.length or self.maze[i+1][j]==4:
					ligne.append(-1)
				else:
					ligne.append(0)
				#right
				if j+1>=self.width or self.maze[i][j+1]==4:
					ligne.append(-1)
				else:
					ligne.append(0)
				#left
				if j-1<0 or self.maze[i][j-1]==4:
					ligne.append(-1)
				else:
					ligne.append(0)
				self.Qtable.append(ligne)

if __name__ == "__main__":
	"""
		Test a maze
	"""
	maze = [
	[0,0,0,0,0,0,0,4,2],
	[0,0,0,0,0,4,0,4,0],
	[0,0,0,0,3,4,0,0,0],
	[0,0,0,0,0,4,4,4,0],
	[1,0,0,0,0,0,0,4,3]
	]
	solver = Solver(maze,interface=False)
	print(solver.learning())