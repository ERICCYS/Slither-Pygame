import pygame
import time # import time to display the text for a while before closing
import random # We want the apple appear randomly on the screen

pygame.init()

display_width = 800
display_height = 600

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Silither')

block_size = 20 # block_size is the thickness of the snake
move_size = 10 # The move_size control the difficulty of the game

FPS = 25
AppleThickness = 30 # This variable define the size of the apple.

clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms",25) # Create the font object
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",80)

icon = pygame.image.load('Apple.png')
pygame.display.set_icon(icon) # Set the icon,  The best size the icon picture is 32*32

img = pygame.image.load('snakeHead.png')
apppleimg = pygame.image.load('Apple.png')

direction = 'up'

def pause():
	paused = True 

	message_to_screen("Paused",
				   black,
				   -100,
				   size = 'large')
	message_to_screen("Press C to continue or Q to quit",
					   black,
					   25,
					   size = 'medium')
	pygame.display.update()

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()
		clock.tick(5)

def score(score):
	text = smallfont.render("Score:" + str(score),True, black)
	gameDisplay.blit(text,[0,0])

def game_intro():
	intro = True

	while intro:
		for event in pygame.event.get():
		 	if event.type == pygame.QUIT:
		 		pygame.quit()
		 		quit()
		 	if event.type == pygame.KEYDOWN:
		 		if event.key == pygame.K_c:
		 			intro = False
		 		if event.key == pygame.K_q:
		 			pygame.quit()
		 			quit()

		gameDisplay.fill(white)
		message_to_screen("Welcome to Slither",
						  green,
						  -200,
						  "large")
		message_to_screen("The objective of the game is to eat apples",
						  black,
						  -30,
						  "small")
		message_to_screen("The more apple you eat, the longer you get",
						  black,
						  10,
						  "small")

		message_to_screen("If you run into yourself or the edges, you die",
						  black,
						  50,
						  "small")

		message_to_screen("Press C to play, P to pause or Q to quit",
						  black,
						  180,
						  "small")

		pygame.display.update()
		clock.tick(15) # If the intro contains a vedio, this is important.

def snake(direction,block_size,snakeList):
	if direction == 'left':
		head = pygame.transform.rotate(img,90)
	elif direction == 'right':
		head = pygame.transform.rotate(img,270)
	elif direction == 'down':
		head = pygame.transform.rotate(img,180)
	else:
		head = img 
	# The snake head is append in the list, this shows that the snakeList[-1] is the snakeHead
	gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))
	for XnY in snakeList[:-1]:
		pygame.draw.rect(gameDisplay,green,[XnY[0],XnY[1],block_size,block_size]) 

def randAppleGen():
	randAppleX = round(random.randrange(0,display_width - AppleThickness))
	randAppleY = round(random.randrange(0,display_height - AppleThickness))
	return randAppleX, randAppleY

def text_object(text,color,size):
	if size == 'small':
		textSurf = smallfont.render(text,True,color)
	elif size == 'medium':
		textSurf = medfont.render(text,True,color)
	elif size == 'large':
		textSurf = largefont.render(text,True,color)	 
	return textSurf, textSurf.get_rect()

def message_to_screen(msg,color,y_displace = 0,size ='small'):
	# screen_text = font.render(msg,True,color)
	# gameDisplay.blit(screen_text,[display_width/2-50,display_height/2-50])
	textSurf, textRect = text_object(msg,color,size)
	textRect.center = (display_width/2),(display_height/2) + y_displace
	gameDisplay.blit(textSurf,textRect)
	#Funtion: gameDisplay.blit()

randAppleX, randAppleY = randAppleGen()

def game_loop():
	gameExit = False
	gameOver = False

	lead_x = display_width/2
	lead_y = display_height/2 

	lead_x_change = 0
	lead_y_change = 0

	snakeList = []
	snakeLength = 1
	global direction
	global previous_direction
	previous_direction = ''

	randAppleX,randAppleY = randAppleGen()

	while not gameExit: # Game loop, we will use built-in event to handle that.
		# Enter the logit loop.
		if gameOver == True: # Here, we make this block of code in this 'if' block just to make sure the message will not paint on the screen over and over again
			message_to_screen("Game over"
							  ,red,
							  -50,
							  size = 'large')
			message_to_screen("Press C to play again or Q to quit",
							  black,
							  50,
							  size = 'medium')
			pygame.display.update()
		while gameOver == True:
			for event in pygame.event.get(): # This loop can make the user continue with C and quit with Q
				if event.type == pygame.QUIT:
					gameExit = True
					gameOver = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					elif event.key == pygame.K_c:
						gameOver = False
						game_loop()

		for event in pygame.event.get(): #Check the documentation of the pygame.event.get()
			# Entering the event loop (Differnt from the game loop)
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					if previous_direction == 'left' or previous_direction == 'right':
						pass
					else:
						direction = 'left'
						previous_direction = direction
						lead_x_change = -move_size 
						lead_y_change = 0 
				elif event.key == pygame.K_RIGHT:
					if previous_direction == 'left' or previous_direction == 'right':
						pass
					else:
						direction = 'right'
						previous_direction = direction
						lead_x_change = move_size
						lead_y_change = 0
				elif event.key == pygame.K_UP:
					if previous_direction == 'up' or previous_direction == 'down':
						pass
					else:
						direction = 'up'
						previous_direction = direction
						lead_y_change = -move_size
						lead_x_change = 0
				elif event.key == pygame.K_DOWN:
					if previous_direction == 'up' or previous_direction == 'down':
						pass
					else:
						direction = 'down'
						previous_direction = direction
						lead_y_change = move_size
						lead_x_change = 0
				elif event.key == pygame.K_p:
					pause()
			
		if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
				gameOver = True # the 0,0 location of the box is the topleft corner, so here we just make sure the position of that corner.

		lead_x += lead_x_change
		lead_y += lead_y_change
	
		gameDisplay.fill(white) 
		# pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,AppleThickness,AppleThickness]) # We should draw the apple befor the snake. otherwise the snake will be hidden under the apple.
		gameDisplay.blit(apppleimg,(randAppleX,randAppleY))

		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakeList.append(snakeHead)
		
		if len(snakeList) > snakeLength:
			del snakeList[0] # Deletet the oldest element in the snake list

		for Segment in snakeList[:-1]: # The reason why we delete the last one is that the last element in the gamelist is the position of the head of the snake. We must delete this position.
			if snakeHead == Segment:
				gameOver = True
				
		snake(direction,block_size,snakeList)
		
		score(snakeLength-1)

		pygame.display.update()
		# Check whether the snake's eaten the apple
		if (lead_x > randAppleX and lead_x < randAppleX + AppleThickness) or (lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness):
			if (lead_y > randAppleY and lead_y < randAppleY + AppleThickness) or (lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness): # One reminder: the positive y dimension is downwards 
				randAppleX,randAppleY = randAppleGen()
				snakeLength += 1

		clock.tick(FPS) 

	pygame.quit()
	quit()

game_intro()
game_loop()