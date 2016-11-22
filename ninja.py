#!/usr/bin/python

import pygame, sys
from pygame.locals import *
import math
import random

FPS = 30
WINDOWWIDTH = 600 
WINDOWHEIGHT = 1000 

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)  
RED       = (255,   0,   0)  
GREEN     = (  0, 255,   0)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

MAXHEALTH = 3

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
		global FPSCLOCK, DISPLAYSURF, BASICFONT, NINJA_STAND_IMG, SWORD_IMG, NINJA_ATTACK_IMG, ENEMY1_IMG, BACKGROUND_IMG, ENEMIES, POINTS, HEALTH

		pygame.init()
		FPSCLOCK = pygame.time.Clock()
		DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
		BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
		pygame.display.set_caption('NINJA')
		
		BACKGROUND_IMG = pygame.image.load('truebackground.png')
		NINJA_STAND_IMG = pygame.image.load('standing_ninja.png')
		SWORD_IMG = pygame.image.load('sword.png')
		NINJA_ATTACK_IMG = pygame.image.load('attacking_ninja.png')
		ENEMY1_IMG = pygame.image.load('enemy1.png')

		ENEMIES = []
		POINTS = 0
		HEALTH = MAXHEALTH
			
		while True:
			runGame()

def runGame():
	startx = 0
	starty = 800
	init_jump_v = 95
	jump_v = init_jump_v
	fall_v = 0

	moveRight = False
	moveLeft = False
	jump = False
	jump_count = 0
	fall = False

	SWORD_TIMER = 0


	playerObj = {'texture': NINJA_STAND_IMG,
							 'x': startx,
							 'y': starty,
							 'moveRate': 20,
							 'health': MAXHEALTH,
							 'width': NINJA_STAND_IMG.get_width(),
							 'height': NINJA_STAND_IMG.get_height(),
							 'direction': 'left'}
	swordObj = {'texture': SWORD_IMG,
							'x': 0,
							'y': 0}

	spawnEnemy()
	#enemies = []
	#random.seed()
	#for x in range(10):
	#	enemyObj = {'texture': ENEMY1_IMG,
	#							'x': random.randrange(0, WINDOWWIDTH - ENEMY1_IMG.get_width()),
	#							'y': 0,
	#							'moveRate': 20,
	#							'status': 'alive'}
	#	enemies.append(enemyObj)
	while True:
		background_rect = pygame.Rect( (0, 
																	  0,
																	  WINDOWWIDTH,
																	  WINDOWHEIGHT,) )

		DISPLAYSURF.blit(BACKGROUND_IMG, background_rect)
		for event in pygame.event.get():
				if event.type == QUIT:
					terminate()
				elif event.type == KEYDOWN:
					if (event.key == K_RIGHT or event.key == K_d):
						moveRight = True
						playerObj['direction'] = 'right'
						playerObj['texture'] = NINJA_STAND_IMG
					if (event.key == K_LEFT or event.key == K_a):
						moveLeft = True
						playerObj['direction'] = 'left'
						playerObj['texture'] = pygame.transform.flip(NINJA_STAND_IMG, True, False)
					if (event.key == K_UP or event.key == K_w):
						if (jump_count == 0):
							jump = True
							jump_start = playerObj['y']
							jump_count += 1
							fall_v = 0
						elif (jump_count == 1):
							jump_v = init_jump_v
							fall_v = 0
							jump_count += 1
					if ( (event.key == K_DOWN or event.key == K_s) and (jump == False) ):
						fall = True
					if ( (event.key == K_SPACE) ):
						SWORD_TIMER = 10
					

				elif event.type == KEYUP:
					if (event.key == K_RIGHT or event.key == K_d): moveRight = False
					if (event.key == K_LEFT or event.key == K_a):
						moveLeft = False



		# Move Logic
		if (moveRight and playerObj['x'] + playerObj['width'] < WINDOWWIDTH):
			playerObj['x'] += playerObj['moveRate']
		if (moveLeft and playerObj['x'] > 0):
			playerObj['x'] -= playerObj['moveRate']

		


		# Jump Logic
		if jump == True:
			F = ( 0.5 * (jump_v) )
		
			playerObj['y'] -= F
			jump_v -= 5
			
			if ( (playerObj['x'] <= 0 or playerObj['x'] + playerObj['width'] >= WINDOWWIDTH ) and (moveRight == True or moveLeft == True) ):
				jump = False
				jump_v = init_jump_v
				jump_count = 0
		

		# Fall if not on wall or platform
		if (playerObj['x'] > 0 and  playerObj['x'] + playerObj['width'] < WINDOWWIDTH):
			fall = True

		# Fall Logic
		if fall == True:
			W = ( 0.5 * (fall_v) )

			playerObj['y'] -= W
			fall_v -= 5

			if ( (playerObj['x'] <= 0 or playerObj['x'] + playerObj['width'] >= WINDOWWIDTH ) and (moveRight == True or moveLeft == True) ):
				fall = False
				fall_v = 0


		
		
		# Attack animation logic
		if (SWORD_TIMER > 0):
			if (playerObj['direction'] == 'left'):
				swordObj['texture'] = pygame.transform.flip(SWORD_IMG, True, False)
				swordObj['x'] = playerObj['x'] - SWORD_IMG.get_width()
			else:
				swordObj['texture'] = SWORD_IMG
				swordObj['x'] = playerObj['x'] + NINJA_STAND_IMG.get_width()
			swordObj['y'] = playerObj['y']
			SWORD_TIMER -= 1
		else:
				swordObj['x'] = WINDOWWIDTH
				swordObj['y'] = WINDOWHEIGHT

		swordObj_rect = pygame.Rect( (swordObj['x'],
																	swordObj['y'],
																	SWORD_IMG.get_width(),
																	SWORD_IMG.get_height()) )

		playerObj_rect = pygame.Rect( (playerObj['x'], 
																	 playerObj['y'],
																	 NINJA_STAND_IMG.get_width(),
																	 NINJA_STAND_IMG.get_height(),) )

		DISPLAYSURF.blit(playerObj['texture'],playerObj_rect)
		if (SWORD_TIMER > 0):
			DISPLAYSURF.blit(swordObj['texture'],swordObj_rect)
		

		enemySpawn = random.randrange(0, 120)
		if (enemySpawn > 100):
			spawnEnemy()

		collisionDetect(playerObj,swordObj_rect)

		endOfScreen(playerObj)
		
		drawEnemies()
		
		pointsFont = pygame.font.SysFont("umpush", 30, bold=True)
		pointsLabel = pointsFont.render(str(POINTS), 3, (255,255,0))
		DISPLAYSURF.blit(pointsLabel, (75, 25))

		pygame.display.update()
		FPSCLOCK.tick(FPS)
		

#def drawObjects(swordObj_rect, swordObj, playerObj, playerObj_rect):
def spawnEnemy():
	global ENEMIES
	enemyObj = {'texture': ENEMY1_IMG,
							'x': random.randrange(0, WINDOWWIDTH - ENEMY1_IMG.get_width()),
							'y': 0,
							'moveRate': 20,
							'status': 'alive'}
	ENEMIES.append(enemyObj)


def collisionDetect(playerObj,swordObj_rect):
	global ENEMIES, POINTS, HEALTH
	for enemy in ENEMIES:
		enemyObj_rect = pygame.Rect( (enemy['x'],
												enemy['y'],
												enemy['texture'].get_width(),
												enemy['texture'].get_height()) )
		playerObj_rect = pygame.Rect( (playerObj['x'],
												 playerObj['y'],
												 playerObj['texture'].get_width(),
												 playerObj['texture'].get_height()) )
		if (swordObj_rect.colliderect(enemyObj_rect)):
			ENEMIES.remove(enemy)
			POINTS = POINTS + 100
		if (playerObj_rect.colliderect(enemyObj_rect)):
			HEALTH = HEALTH - 1;
	print(HEALTH)


def drawEnemies():
	global ENEMIES
	count = 0
	for enemy in range(len(ENEMIES)):
		enemyObj_rect = pygame.Rect( (ENEMIES[enemy]['x'],
												ENEMIES[enemy]['y'],
												ENEMIES[enemy]['texture'].get_width(),
												ENEMIES[enemy]['texture'].get_height()) )
		ENEMIES[enemy]['y'] += ENEMIES[enemy]['moveRate']
		DISPLAYSURF.blit(ENEMIES[enemy]['texture'],enemyObj_rect)	

def endOfScreen(playerObj):
	global ENEMIES
	if (playerObj['y'] > WINDOWHEIGHT):
		terminate()
	for enemy in ENEMIES:
		if (enemy['y'] > WINDOWHEIGHT):
			ENEMIES.remove(enemy)

def terminate():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()
