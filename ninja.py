# NINJA CLIMB

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



MAXHEALTH = 3

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
		global FPSCLOCK, DISPLAYSURF, BASICFONT, NINJA_STAND_IMG, SWORD_IMG, NINJA_ATTACK_IMG, ENEMY1_IMG, BACKGROUND_IMG, ENEMIES, HEART_IMG

		pygame.init()
		FPSCLOCK = pygame.time.Clock()
		DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
		BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
		pygame.display.set_caption('NINJA')
		
		BACKGROUND_IMG = pygame.image.load('sprites/background.png')
		NINJA_STAND_IMG = pygame.image.load('sprites/standing_ninja.png')
		SWORD_IMG = pygame.image.load('sprites/sword.png')
		NINJA_ATTACK_IMG = pygame.image.load('sprites/attacking_ninja.png')
		ENEMY1_IMG = pygame.image.load('sprites/enemy1.png')
		HEART_IMG = pygame.image.load('sprites/heart.png')

		ENEMIES = []

		while True:
			runGame()

def runGame():
	global ENEMIES
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

	SCORECOUNTER = 0

	INVUL_TIMER = 0

	enemySpawnRate = 95


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
		
			if (playerObj['y'] - F > 0):
				playerObj['y'] -= F
			else:
				playerObj['y'] = 0
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
		

		spawnCheck = random.randrange(0, 100)
		if (spawnCheck > enemySpawnRate):
			spawnEnemy()

		TEMP_ENEMIES = list(ENEMIES)
		for enemynum in range(len(ENEMIES)):
				enemyObj_rect = pygame.Rect( (ENEMIES[enemynum]['x'],
																			ENEMIES[enemynum]['y'],
																			ENEMIES[enemynum]['texture'].get_width(),
																			ENEMIES[enemynum]['texture'].get_height()) )
				if (enemyObj_rect.colliderect(swordObj_rect) != True):
					ENEMIES[enemynum]['y'] += ENEMIES[enemynum]['moveRate']
					DISPLAYSURF.blit(ENEMIES[enemynum]['texture'],enemyObj_rect)	
				else:
					del TEMP_ENEMIES[enemynum]
					SCORECOUNTER += 100

				if (enemyObj_rect.colliderect(playerObj_rect) == True and INVUL_TIMER == 0):
					playerObj['health'] -= 1
					INVUL_TIMER = 20
				if (playerObj['health'] == 0):
					endGame()

		ENEMIES = list(TEMP_ENEMIES)

		endOfScreenCheck(playerObj)

		if (INVUL_TIMER > 0):
			INVUL_TIMER -= 1

		for lives in range(playerObj['health']):
			lives += 1
			DISPLAYSURF.blit(HEART_IMG, (WINDOWWIDTH - lives * HEART_IMG.get_width(), 10))
		screenscore = BASICFONT.render(str(SCORECOUNTER), 1, (255,255,0))
		DISPLAYSURF.blit(screenscore, (10, 10))
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		

def spawnEnemy():
	global ENEMIES
	enemyObj = {'texture': ENEMY1_IMG,
							'x': random.randrange(0, WINDOWWIDTH - ENEMY1_IMG.get_width()),
							'y': 0,
							'moveRate': 5,
							'status': 'alive'}
	ENEMIES.append(enemyObj)


def endOfScreenCheck(playerObj):
	global ENEMIES
	if (playerObj['y'] > WINDOWHEIGHT):
		endGame()

	TEMP_ENEMIES = list(ENEMIES)
	for enemynum in range(len(ENEMIES)):
		if (ENEMIES[enemynum]['y'] > WINDOWHEIGHT):
			del TEMP_ENEMIES[enemynum]
	ENEMIES = list(TEMP_ENEMIES)


def endGame():
	endgametext = BASICFONT.render("GAME OVER", 1, (255,0,0))
	DISPLAYSURF.blit(endgametext, (300, 500) )
	pygame.display.update()
	while True:
		for event in pygame.event.get():
				if event.type == QUIT:
					terminate()
				elif event.type == KEYDOWN:
					if (event.key == K_q):
						terminate()


def terminate():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()
