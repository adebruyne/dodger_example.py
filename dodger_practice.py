#import the modules
import pygame, random, sys
from pygame.locals import *


#####Setting up the Constant Variables
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 20           #Frames per second. If you want the game to run slower, decrease the speed.  
BADDIEMINSIZE = 20   #size of smallest baddie
BADDIEMAXSIZE = 40   #size of biggest baddie
BADDIEMINSPEED = 1   #the rate at which the baddies fall down the screen per iteration throught the game loop
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6  #a new baddie will be added to the top  if the window every addnewbaddierate iterations through the gaming loop
PLAYERMOVERATE = 8 #number of pixels the player can move in the window in each iteration of the game


#######  Defining functions


def terminate():   #Ending the game...you'll only have to cakk terminate() instead of both pygame.quit() and sys.exit()
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():      #in this function, there's an infinite loop that breaks only when a KEYDOWN or QUIT event is recieved. At the start of the loop, pygame.event.get() returns
                                     #a list of Event objects to check out. If the player has closed the window while the program is waiting for the player to press a key, pygame will
                                     #genertate a QUIT event. If the player quits, pytho calls the terminate() function. If the player pushes a key down, python checks if its an ESC key
                                     #and terminates if it is. Other wise,the code keeps looping, making the game look frozen until the player presses a key
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):    #Function will return True if the player's character collided with one of the bad guys.Baddies is a list of empty baddie dictionary. PlayerRect is a Rect object 
    for b in baddies:                           #with a method named colliderect()
                                                #the for loop iterates through each baddie dictionary in the baddies list. If any of them collide with the play, playerHasHitBaddie returns True.
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):         #this function displays text on the screen
    textobj = font.render(text, 1, TEXTCOLOR)    #render() creates a Surface object that rneders the text in a specific font
    textrect = textobj.get_rect()               #getrect() Surface method will get the size and location of the object
    textrect.topleft = (x, y)                   #This changes the location of the Rect object by setting a new tuple value for its topleft attribute
    surface.blit(textobj, textrect)             #draws the Surface object of the rendered text onto the the Surface object that was passed to the drawText() function. 







########### Set up pygame, the window, and the mouse cursor.
pygame.init()                                       # sets up pygame by calling the pygame.init() function
mainClock = pygame.time.Clock()                     # creates a pygame.time.Clock() object and stores it in the mainClock variable. This object helps keep the program from running to fast
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)    #creates a new Surface object for the window display. The arguments for this are not two integers, but one tuple of two integers.                                                                                                      Optionally, you can pass pygame.FULLSCREEN to make the window fill the entire screen.  
pygame.display.set_caption('Dodger')                # sets the caption of the window to the string 'Dodger'_ which will appear in the title bar at the top of the window                                                  
pygame.mouse.set_visible(False)                     # this makes the mouse cursor invisible. This way it doesnt get  in the way of the players image and it makes it so the mous can move the character around the screen.

########### Set up the fonts.
font = pygame.font.SysFont(None, 48)                #Since we have text, we need to give pygame module a Font object for its text. None uses default text, and 48 is the font size

########### Set up sounds.
gameOverSound = pygame.mixer.Sound('SadTrombone 2.wav') #pygame.mixer.Sound() function creates a new Sound object and stores a reference to this object in the gameOverSound variable.
pygame.mixer.music.load('background.mid')          #pygame.mixer.load() loads a sound file to play for the background music. This functions doesnt return any objects and only one background sound file can be loaded at a time
                                                   # The background music will play constantly during the game, but the Sound objects will play only when the the player losses the game by running into a baddie.

########### Set up images.
playerImage = pygame.image.load('grump.png')     #image for player
playerRect = playerImage.get_rect()               
baddieImage = pygame.image.load('badvibes.png')   #image for baddies

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)        # We pass five arguments  into the next function: 1. The string of text you want to appear. 2. The font in which you want the string to appear. 3. The Surface                                               object onto which the text will appear. 4. The x-coordinate on the Surface object at which to draw the text and 5. The Y-coordinate on the Surface object at                                                which to draw the text.
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.                                 #This while loop iterates each time the player starts a new game
    baddies = []                                                    #The baddies is set to an empty list. The variable baddies is a list of dictionary objects with the following keys: 'rect' - object that describes where and what size the baddies is. 'speed'- how fast they fall down the screen (the integer represents pixels per iteration through the game loop. 'surface' - This object has the scaled baddie image drawn on it. This is the surface that is drawn to the Surface object returned by pygame.display.set_mode().)
    score = 0                                                       #score resets to 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)     #Starting location is set to the center of the screen and 50 pixels up from the bottom.
    moveLeft = moveRight = moveUp = moveDown = False             #movement variables are set to False
    reverseCheat = slowCheat = False                            # variables set to False and only become True if player enables these cheats by holding down Z and X keys respectively.
    baddieAddCounter = 0                                       # This variable is a counter to tell the program when to add a new baddie at the top of the screen. This increments by one each time the game loop iterates.
    pygame.mixer.music.play(-1, 0.0)                           #Starts playing music by calling this function. Arguments '-1' repeats the music endlessly. '0.0' is a float that says how many seconds into the song you want it to start playing, so it starts from the beginning.

    while True: # The game loop runs while the game part is playing.       #This updates the state of the game world several times a second. By changing the position of the player and and baddies, and handling events generated  by pygame and drawing the game world on screen. 
        score += 1 # Increase score.    

        for event in pygame.event.get():                    #Quits out of game 
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:                       #Checks to see which keys are being pressed
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:                     #If the Z key or X key are used to cheat, the scores get reset to 0. This is used to discourage the player from cheating.
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:              #Escape key terminates
                        terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:         #This only happens if the cheats are not enabled. If they are, no new baddies with appear at the top of the screen
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:       #When the counter reaches the value of the rate, a new baddies will appear.
            baddieAddCounter = 0                       #first, the counter is set to 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)           #this generates a size for baddie in pixels. It will be a random interger betwwen the min and max size. 
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),        #the new baddie data structure is created. It is simply a                                                                                                                                         dictionary with keys 'rect', 'speed', 'surface.' 'rect' holds a reference to the Rect Object  that stores the location and size of the baddie. This constructor has 4 parameters: x-coord. of the top edge of the area, the y-coord of the left edge of the area, the width in pixels, and height in pixels. The baddies neeads to appear at a random point along the window, so we pass random.randint(0, WINDOWWIDTH  - baddieSize) for the x-coord. of the left edge of the baddie. The reason you pass WINDOWWIDTH - baddieSize instead of WINDOWWIDTH is that if the left edge of the baddie is too far to the right, then part of the baddie will be of the edge of the window and not visible on the screen. The bottom edge of the baddie should be just above the edge of the window. The y-coordinate ofthe top edge of the window is 0. TO put the baddie's bottom edge there, set the top edge to 0- baddieSize. The width and height of the should be the same size,since the image is a square, so we pass baddieSize for the third and fourth arguments. 
                          'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),                                #The speed is set to to a random integer between BADDIEMINSPEED and BADDIEMAX SPEED.
                          'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),             #Resizes the Surface to a new reolution (Surface(width,Height))
                         }

            baddies.append(newBaddie)                                                                          #This will then add the newly created baddie data stucture to the list of baddie data                                                                                                            structures

        # Move the player around.                                                   
        if moveLeft and playerRect.left > 0:                            #If the player is moving left and the left edge of the player's character is greater than 0(which is the left edge of the window),                                                                  then the playerRect should move left. 
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)                  #The move_ip() method will move the loaction of the Rect object horizontally or vertically by a number of pixels. The first argument is how many pixels to move the object to the right(to move left,pass a negative integer). The second argument is how many pixels to move the Rect object down(to move it up, pass a negtive integer). ip stands for 'in place' This is because the method changes the Rect object itself, rather than returning a new Rect object.
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])        #if neither cheat mode is activated, the baddie's location moves down a number of pixels equal to it speed(stored in the 'speed' key)

            elif reverseCheat:
                b['rect'].move_ip(0, -5)                #if the reverse cheat is activated, then the baddie should move up 5 pixels
            elif slowCheat:
                b['rect'].move_ip(0, 1)                 #if the slowCheat is activated, then the baddie should still move downward, but at the slow speed of 1 pixel per iteration of the game loop

        # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:                        #First we make a copy of the baddies list using the [:] operator because we dont want to add or remove list items while also iterating through the list
            if b['rect'].top > WINDOWHEIGHT:        #the b dictionary is the current baddie data structure from the baddies[:] list. Each baddie data structure in the list is a dictionary, with a 'rect'                                          key, which stores a Rect object. So b['rect'] is the Rect object for the baddie. Finally, the top attribute is the y-coordinate of the top edge of the                                          rectangle area. Remember the y-coord. increase going down. So b['rect'].top > WINDOWHEIGHT will check weather the top edge of the baddie is below the                                           bottom of the window. 
                baddies.remove(b)                   #if condition is true,  this function removes baddie data structure from the baddies list        

        # Draw the game world on the window.        
        windowSurface.fill(BACKGROUNDCOLOR)         #the Surface object in windowSurface is special because it is the one returned by pygame.display.set_mode(). Anything drwan on that Surface object will                                             appear on the screen after pygame.display.update() is called

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)                 #This expression uses string interpolation to insert the value in the score variable into the string. This string, the                                                                              Font object stored in the font variable, the Surface object to draw the text on, the x- and y-coordinates of there the                                                                              text should be placed are passed to the drawText() method, which will handle the call to render() and blit() methods
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)                                 #Informaton about the player is kept in two different variables. playerImage is a Surface object that contains all the                                                                               colored pixels that make up the player character's image. playerRect is a Rect object that stores the size and                                                                                     location of the player's charcters' The blit() method draws the player character's image(in playerImage)on                                                                                          windowSurface at the location of playerRect

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
