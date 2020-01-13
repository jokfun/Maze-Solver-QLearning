import pygame

class textInput:
	def __init__(self,screen,axex,axey,length,height,
		maxdigit = 8,
		textsize=20,
		textcolor=(255,255,255),
		bordercolor=(255,255,255),
		bordercolor_click=(0,0,255),
		fontcolor=(7,9,44) ):

		"""
			Hyperparameters :
			- screen of your game/app (created with pygame.display.set_mode)
			- axex = position x of the top left corner of the box
			- axexy = position y of the top left corner of the box
			- length = length of the box
			- height = height of the box

			Default hyperparameters :
			- maxdigit = number of digits allowed in the content (incl. point)
			- textsize = size of the text
			- textcolor = color of the text display
			- bordercolor = color of the outer edge of the field
			- bordercolor_click = color of the outer edge of the field when you click on
			- fontcolor = field background color
		"""

		#Fix the values of the different color
		self.bordercolor = bordercolor
		self.fontcolor = fontcolor
		self.textcolor = textcolor
		self.textsize = textsize
		self.bordercolor_click = bordercolor_click

		#Fix your screen used in your app
		self.screen = screen

		#Fix the number of digits allowed in the content
		self.maxdigit = maxdigit

		#Fix positions of the field
		self.axex = axex
		self.axey = axey
		self.length = length
		self.height = height

		#Create the field
		self.rect = pygame.rect.Rect( (axex,axey) , (length,height) )
		screen.fill(self.bordercolor, self.rect)
		screen.fill(self.fontcolor, self.rect.inflate(-2, -2))

		#Init the content
		self.content = "0"

		#Create the font of the text
		self.textfont = pygame.font.SysFont('Calibri', self.textsize)

		#Show the field
		self.displaytext()

		#boolean to test if you click on the field
		self.click = False

		#Values allow in the content
		self.allow = [str(i) for i in range(10)]

	def displaytext(self):
		"""
			Function to update the content on the field
		"""
		self.screen.fill(self.fontcolor, self.rect.inflate(-2, -2))
		self.textsurface = self.textfont.render(self.content, False, self.textcolor)
		self.screen.blit(self.textsurface,(self.axex+5,self.axey+15))

	def update(self,events,posx,posy):
		"""
			Method for updating content based on user actions

			Parameters :
			- events : list of pygame event
			- posx = position x of the mouse
			- posy = position y of the mouse
		"""

		#Test if the mouse is in the text field
		if not (posx>=self.axex and posx<=self.axex+self.length and posy>=self.axey and posy<=self.axey+self.height):
			if pygame.mouse.get_pressed()[0]==1:

				#If you click outside the field, it will reset the border and prevent it from being changed
				self.click = False
				self.screen.fill(self.bordercolor, self.rect)
				self.screen.fill(self.fontcolor, self.rect.inflate(-2, -2))

		elif pygame.mouse.get_pressed()[0]==1:

			#If you click in the field, the border will change and you will be able to modify it
			self.click=True
			self.screen.fill(self.bordercolor_click, self.rect)
			self.screen.fill(self.fontcolor, self.rect.inflate(-2, -2))

		#If you can change the content
		if self.click == True:
			for event in events:

				#If a key is pressed
				if event.type == pygame.KEYDOWN:

					#Delete content if it exists
					if event.key == pygame.K_BACKSPACE and len(self.content)>0:
						self.content = self.content[:-1]

					#Add a dot (for decimal numbers)
					elif (event.key == pygame.K_KP_PERIOD or event.key == pygame.K_PERIOD) and len(self.content)<self.maxdigit:

						#Cannot add dot if it's already in
						if "." not in self.content:
							self.content = self.content + "."
					#Take the value of the pressed key and convert it into readable data
					value = pygame.key.name(event.key)
					value = value.split("[")[-1].split("]")[0]

					#If the value is allowed, it is added to the content.
					if value in self.allow and len(self.content)<self.maxdigit:
						self.content = self.content + value

		#Update the text of the field
		self.displaytext()

	def getValue(self):
		"""
			Return the value of the content
		"""
		return float(self.content)


if __name__ == "__main__":

	import time

	pygame.init()
	pygame.font.init()
	screen = pygame.display.set_mode((300, 100))

	#We create the text field
	text = textInput(screen,20,30,200,50,maxdigit=15)

	while True:

		pygame.display.update()

		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
		mouse = pygame.mouse.get_pos()
		x = mouse[0]
		y = mouse[1]

		#We update the text
		text.update(events,x,y)



