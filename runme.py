#TODO
"""
	- add a "stop" button to stop the solver witohut leaving the app
	- don't leave the app when maze is incorrect (no enter or exit)
"""

import os

#We don't want to show the pygmy version and welcome message. Snif
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from solver import Solver
import pygame
import time
from textinput import textInput

############### Function part ###############

def reset():
	"""
		Reset the mlaze with only white square
	"""
	for i in range(0,500,20):
		for j in range(400,800,20):
			rect = pygame.rect.Rect( (i+1,j+1) , (19,19) )
			pygame.draw.rect(screen, (255,255,255), rect)

	#We also reset the maze which contains the codes of the structure
	maze = [[0 for i in range(25)] for j in range(20)]

	return maze

def draw_rect(surface, fill_color, outline_color, rect, border=1):
	"""
		Draw a rectangle with a border
		These two lines will be called several times, so a function is created for them.
	"""
	surface.fill(outline_color, rect)
	surface.fill(fill_color, rect.inflate(-border*2, -border*2))

def print_solution(screen,solution,start):
	"""
		Create the path connecting the input and the output.
		The path is calculated with the QLearning algorithm (see solver.py).

		screen : the screen of the app
		solution : the path returned by the solver (a list)
		start : the start of the path
	"""
	x = (start[0]*20)+400
	y = start[1]*20
	for ele in solution:
		if ele==0:
			x-=20
		elif ele==1:
			x+=20
		elif ele==2:
			y+=20
		elif ele==3:
			y-=20
		rect = pygame.rect.Rect( (y+1,x+1) , (19,19) )

		#The solution will be draw with a green rect
		pygame.draw.rect(screen, (0,255,0), rect)

		pygame.display.update()

		#Little animation to show the construction of the path
		time.sleep(0.1)

###########################################


#General variables when creating an app with pygame
#We also set a title
pygame.init()
pygame.display.set_caption('Maze solver with QLearning')
pygame.font.init()

#Size and police of the app
maze_font = pygame.font.SysFont('Calibri', 20)
button_font = pygame.font.SysFont('Calibri', 25)

#Window size
screen = pygame.display.set_mode((500, 800))

#Reseting the maze will create it
maze = reset()

#The line which split the window
pygame.draw.line(screen, (255,255,255), (280,0), (280,400), 3)

#Text to the custom hyperparamters part
textsurface = button_font.render('CUSTOM PARAMETERS', False, (255, 255, 255))
screen.blit(textsurface,(25,10))

#Text to the custom maze part
textsurface = button_font.render('CREATE THE MAZE', False, (255, 255, 255))
screen.blit(textsurface,(300,10))

#Name and color of the different structures of the maze
name_rect = {
"Wall":(78,78,57),
"Exit":(0,0,153),
"Start":(0,255,0),
"Trap":(255,0,0),
"Path":(255,255,255)
}

#The dict is used in oder to reduced the size of the code
i = 80
for k in name_rect:
	rect = pygame.rect.Rect( (320,i) , (25,25) )
	pygame.draw.rect(screen, name_rect[k], rect)
	textsurface = maze_font.render(k, False, (255, 255, 255))
	screen.blit(textsurface,(360,i+2))
	i+=60

#Button start (launch the Solver)
rect = pygame.rect.Rect( (50,330) , (70,40) )
draw_rect(screen,(0,0,0),(255,255,255),rect)
textsurface = button_font.render('START', False, (255, 255, 255))
screen.blit(textsurface,(55,340))

#Button reset (reset the maze)
rect = pygame.rect.Rect( (130,330) , (70,40) )
draw_rect(screen,(0,0,0),(255,255,255),rect)
textsurface = button_font.render('RESET', False, (255, 255, 255))
screen.blit(textsurface,(135,340))

#List of the hyperparameters
#Creation of the different text field
parameters = ["Learning rate","Discount factor","Maxstep","Epsilon"]
allInput = {}
i=80
for k in parameters:
	allInput[k] = textInput(screen,150,i,100,50)
	textsurface = maze_font.render(k, False, (255, 255, 255))
	screen.blit(textsurface,(10,i+12))
	i+=60

#Update the screen to show all the elements
pygame.display.update()

#Init the colo with white and code with path
color = (255,255,255)
code = 0

while True:

	#Get all the events
	events = pygame.event.get()

	for event in events:

		#Closes the application if the user clicks on the cross
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	#Get the positino of the mouse
	value = pygame.mouse.get_pos()
	x = value[0]
	y = value[1]

	#Coordiantes are converted for the maze
	posX = int((y-400)/20)
	posY = int(x/20)

	#If left button of the mouse is pressed
	if pygame.mouse.get_pressed()[0]==1:
		if y>=400:

			#Draw a the actual structure on the maze and update the maze's matrix
			rect = pygame.rect.Rect( (int(x/20)*20+1,int(y/20)*20+1) , (19,19) )
			pygame.draw.rect(screen, color, rect)
			maze[posX][posY] = code

		if x>=320 and x <=345:

			#Wall
			if y>=80 and y<=105:
				color=(78,78,57)
				code = 4

			#Exit
			if y>=140 and y<=165:
				color=(0,0,153)
				code = 2

			#Start
			if y>=200 and y<=225:
				color=(0,255,0)
				code = 1

			#Trap
			if y>=270 and y<=295:
				color=(255,0,0)
				code = 3

			#Path
			if y>=320 and y<=345:
				color=(255,255,255)
				code = 0

		#If the user click on the reset button area
		if x>=130 and x<=200 and y>=330 and y <=370:
			maze = reset()

		#If the user click on the start button area
		if x>=50 and x<=120 and y>=330 and y <=370:

			"""
				A new solver is created
				The value in each field is retrieved
				The learning process has begun
			"""
			solver = Solver(maze,
				learning_rate = allInput["Learning rate"].getValue(),
				discount_factor = allInput["Discount factor"].getValue(),
				maxstep = allInput["Maxstep"].getValue(),
				epsilon = allInput["Epsilon"].getValue())
			solution,start = solver.learning()

			#Call the print solution
			print_solution(screen,solution,start)

	#Update the content of each field
	for k in allInput:
		allInput[k].update(events,x,y)

	#Update the different changes on the screen
	pygame.display.update()
