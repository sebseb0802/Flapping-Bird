# Required for most things in the game e.g. sprite rendering/inputs etc.
import pygame

# For deciding the y-positions of the top and bottom pipes
import random

# For dealing with the highscore.txt file
import os

# pygame setup
pygame.init()
window = pygame.display.set_mode((208, 272))
clock = pygame.time.Clock()
running = True
dt = 0

# Assigns the background image to the relevant variable
backgroundImage = pygame.image.load("Assets/Sprites/NightBackground.png")

# Defines the class for the background
class Background:
    def __init__(self):
        # Initialises the two images (pieces of ground) that are used to make the "moving" effect
        self.image1 = pygame.image.load("Assets/Sprites/NightBackground.png")
        self.image2 = pygame.image.load("Assets/Sprites/NightBackground.png")

        # Initialises position variables that are used to make the "moving" ground effect
        self.position1 = pygame.Vector2(0, 0)
        self.position2 = pygame.Vector2(208, 0)

        # Initialises the speed of the ground (must be the same as the pipeSpeed variable)
        self.speed = 1

    def moveBackground(self):
        # Draws the ground on the screen
        window.blit(self.image1, self.position1)
        '''window.blit(self.image2, self.position2)

        if player.gameOver == False:
            # If it's not game over, continue to move the ground
            self.position1.x -= self.speed
            self.position2.x -= self.speed

        # By default, the position of an image is measured from the top-left corner of the image
        if self.position1.x < -208:
            # If the first piece of ground is completely off the screen, move it to being just off the edge of the screen on the right
            self.position1.x = 208

        if self.position2.x < -208:
            # If the second piece of ground is completely off the screen, move it to being just off the edge of the screen on the right
            self.position2.x = 208'''


# Defines the class for the ground
class Ground:
    def __init__(self):
        # Initialises the rect for collisions with the player
        self.playerTileRect = pygame.Rect((96, 256), (16, 16))

        # Initialises the two images (pieces of ground) that are used to make the "moving" effect
        self.image1 = pygame.image.load("Assets/Sprites/Terrain/GrassGround.png")
        self.image2 = pygame.image.load("Assets/Sprites/Terrain/GrassGround.png")

        # Initialises position variables that are used to make the "moving" ground effect
        self.position1 = pygame.Vector2(0, 256)
        self.position2 = pygame.Vector2(208, 256)

        # Initialises the speed of the ground (must be the same as the pipeSpeed variable)
        self.speed = 1

    def moveGround(self):
        # Draws the ground on the screen
        window.blit(self.image1, self.position1)
        window.blit(self.image2, self.position2)

        if player.gameOver == False:
            # If it's not game over, continue to move the ground
            self.position1.x -= self.speed
            self.position2.x -= self.speed

        # By default, the position of an image is measured from the top-left corner of the image
        if self.position1.x < -208:
            # If the first piece of ground is completely off the screen, move it to being just off the edge of the screen on the right
            self.position1.x = 208

        if self.position2.x < -208:
            # If the second piece of ground is completely off the screen, move it to being just off the edge of the screen on the right
            self.position2.x = 208
        

# Defines the class for the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Assigns the player's moving animation frames to this array
        self.frames = [
            pygame.image.load("Assets/Sprites/Player/Player1.png"), 
            pygame.image.load("Assets/Sprites/Player/Player2.png"), 
            pygame.image.load("Assets/Sprites/Player/Player3.png"), 
            pygame.image.load("Assets/Sprites/Player/Player4.png")
        ]
        # A variable to keep track of the index of the current frame
        self.currentFrame = 0

        # Sets the starting image of the player (the first frame)
        self.image = pygame.image.load("Assets/Sprites/Player/Player1.png")

        # Creates the rectangle for the player
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

        # Sets the starting position of the player
        self.position = pygame.Vector2(96, 136)

        # Sets the starting velocity of the player
        self.velocityY = 0

        # Sets the starting gameOver state to False
        self.gameOver = False

        # Sets the starting hitPipe state to False
        self.hitPipe = False

        # Sets the force due to gravity on the player to 0.1
        self.gravity = 0.1

        # Sets the starting score of the player to 0
        self.score = 0
        print(self.score)

        self.angle = 0

    def updatePosition(self):
        # Continually adds gravity to velocity so that the velocity of the player continually grows as the player falls
        self.velocityY += self.gravity
        self.position.y += self.velocityY

        # Updates the location of the player's rect as the player falls
        self.rect.topleft = (self.position.x, self.position.y)

    def checkIllegalCollision(self, tileRect, topPipeRect1, topPipeRect2, topPipeRect3, bottomPipeRect1, bottomPipeRect2, bottomPipeRect3) -> int:
        if self.rect.colliderect(tileRect):
            hitSound.play()
            # Player position is set to this value to prevent overlap between player sprite and floor tile sprite
            self.position.y = 242

            # If the player hits the floor, gameOver is set to true
            self.gameOver = True
            print("Floor hit! Game over!")

        if self.rect.colliderect(topPipeRect1) or self.rect.colliderect(topPipeRect2) or self.rect.colliderect(topPipeRect3) or self.rect.colliderect(bottomPipeRect1) or self.rect.colliderect(bottomPipeRect2) or self.rect.colliderect(bottomPipeRect3):
            if self.hitPipe == False:
                hitSound.play()
                pygame.mixer.music.pause()
                #swooshSound.play() # Delay after hitSound before playing swooshSound
                self.hitPipe = True
                print("Pipe hit! Game over!")

    def drawPlayer(self, gameState):
        if self.gameOver == False and gameState == 2:
            if self.velocityY > 0:
                if self.angle > -90:
                    self.angle -= 2 * self.velocityY
            else:
                self.angle = 45
        elif self.rect.colliderect(ground.playerTileRect):
            # Ensures that the player always appears to land with its beak in the ground
            self.angle = -90
        else:
            self.angle = 0


        rotatedPlayer = pygame.transform.rotate(self.frames[self.currentFrame], self.angle)
        self.rect = self.frames[self.currentFrame].get_rect(topleft=self.position)
        window.blit(rotatedPlayer, self.position)
        pygame.draw.rect(window, (255, 0, 0), self.rect, 1)

    def animate(self, gameState):
        if self.gameOver == False:
            if self.currentFrame == 3:
                # If all frames of the player's animation have been cycled through, start cycling through them again by setting currentFrame to 0
                self.currentFrame = 0

            # Create a rectangle for collision around the current frame of the player sprite
            self.rect = self.frames[self.currentFrame].get_rect()
            self.rect.topleft = (100, 100)

            # Draw the player's current sprite and increment the frame counter by 1
            self.drawPlayer(gameState)
            self.currentFrame += 1

    def checkScoreCollision(self, scoreCheckerRect1, scoreCheckerRect2, scoreCheckerRect3):
        if self.hitPipe == False:
            if self.rect.colliderect(scoreCheckerRect1) or self.rect.colliderect(scoreCheckerRect2) or self.rect.colliderect(scoreCheckerRect3):
                # If the player collides with the scoreCollisionChecker of either pipe, increment the player's score by 1
                self.score += 1
                print(self.score)
                pointSound.play()


# Defines the class for the pipes
class Pipes(pygame.sprite.Sprite):
    def __init__(self, topPipe, bottomPipe, initialTopPosition, initialBottomPosition):
        pygame.sprite.Sprite.__init__(self)

        self.topPipe = pygame.image.load(topPipe)
        self.topPipeRect = self.topPipe.get_rect()
        self.topPipeRect.topleft = initialTopPosition
        self.topPipePosition = pygame.Vector2(initialTopPosition)

        self.bottomPipe = pygame.image.load(bottomPipe)
        self.bottomPipeRect = self.bottomPipe.get_rect()
        self.bottomPipeRect.topleft = initialBottomPosition
        self.bottomPipePosition = pygame.Vector2(initialBottomPosition)

        self.pipeSpeed = 1


        self.scoreCollisionChecker = pygame.rect.Rect((50, 50), (1, 48)) # legacy: (32, 48)

        self.assignPosition()

    def movePipes(self):
        window.blit(self.topPipe, self.topPipePosition)
        self.topPipeRect.topleft = self.topPipePosition
        pygame.draw.rect(window, (255, 0, 0), self.topPipeRect, 1)

        window.blit(self.bottomPipe, self.bottomPipePosition)
        self.bottomPipeRect.topleft = self.bottomPipePosition
        pygame.draw.rect(window, (255, 0, 0), self.bottomPipeRect, 1)

        if player.gameOver == False:
            self.topPipePosition.x -= self.pipeSpeed
            self.bottomPipePosition.x -= self.pipeSpeed
            self.scoreCollisionChecker.topleft = (self.topPipeRect.centerx, self.topPipeRect.bottom)
            #self.scoreCollisionChecker.left = self.topPipeRect.left

            if self.topPipePosition.x < -32:
                self.topPipePosition.x = 350
                self.bottomPipePosition.x = 350
                self.assignPosition()

    def assignPosition(self):
        if player.gameOver == False:
            topY = random.randint(-144, 0)
            bottomY = random.randint(80, 224)

            while (bottomY - topY != 224):
                # There must be a gap of 224 pixels between the top of the bottom pipe and the top of the top pipe 
                # to ensure that there is always enough of a distance for the player to pass through.
                # This check also ensures that the distance between pipes is always equal.
                topY = random.randint(-144, 0)
                bottomY = random.randint(80, 224)

            self.topPipePosition.y = topY
            self.topPipeRect.top = topY

            self.bottomPipePosition.y = bottomY
            self.bottomPipeRect.top = bottomY

            self.scoreCollisionChecker.top = self.topPipeRect.bottom


# Defines the class for the GUI in the game
class GUI:
    def __init__(self):
        # Initialises the fonts for text/numbers in the game
        self.largeTextFont = pygame.font.Font("Assets/Font/flappyBirdText.ttf", size=60)
        self.smallTextFont = pygame.font.Font("Assets/Font/flappyBirdText.ttf", size=26)
        self.smallerTextFont = pygame.font.Font("Assets/Font/flappyBirdText.ttf", size=17)

        self.inputPromptTextFont = pygame.font.Font("Assets/Font/flappyBirdText.ttf", size=26)
        self.gameOverTitleTextFont = pygame.font.Font("Assets/Font/flappyBirdText.ttf", size=52)

        self.largeNumbersFont = pygame.font.Font("Assets/Font/flappyBirdNumbers.ttf", size=48)
        self.smallNumberFont = pygame.font.Font("Assets/Font/flappyBirdNumbers.ttf", size=20)

        # Initialises the panel that is present in various places in the game
        self.textPanel = pygame.image.load("Assets/Sprites/GUI/TextPanel.png")

        # Initialises the variables for keeping track of the user's high score
        self.highScore = 0
        self.newHighScore = False

    def drawMainMenu(self):
        # Centers and draws the main title text
        mainTitleText = self.largeTextFont.render("flappingBird", False, (255, 255, 255), None)
        mainTitleRect = mainTitleText.get_rect(center=(104, 30))
        window.blit(mainTitleText, mainTitleRect)
        
        # Centers and draws the input prompt text
        inputPromptText = self.inputPromptTextFont.render("Press the Spacebar to start", False, (0, 0, 0), None)
        inputPromptRect = inputPromptText.get_rect(center=(104, 170))
        window.blit(inputPromptText, inputPromptRect)

    def drawScore(self):
        # Centers and draws the score text
        scoreText = self.largeNumbersFont.render(str(player.score), False, (255, 255, 255))
        scoreRect = scoreText.get_rect(center=(104, 30))
        window.blit(scoreText, scoreRect)

    def drawGameOver(self):
        # Centers and draws the game over text and panel
        textPanelRect = self.textPanel.get_rect(center=(104, 120))
        window.blit(self.textPanel, textPanelRect)

        gameOverText = self.gameOverTitleTextFont.render("Game over", False, (0, 0, 0), None)
        gameOverRect = gameOverText.get_rect(center=((textPanelRect.center[0]), (textPanelRect.center[1]-50)))
        window.blit(gameOverText, gameOverRect)

        # Draws and aligns the score and high score
        scoreText = self.smallTextFont.render("Score", False, (0, 0, 0), None)
        scoreTextRect = scoreText.get_rect(center=((textPanelRect.center[0]-50), (textPanelRect.center[1]-20)))
        window.blit(scoreText, scoreTextRect)

        scoreNumber = self.smallNumberFont.render(str(player.score), False, (0, 0, 0), None)
        scoreNumberRect = scoreNumber.get_rect(topleft=((scoreTextRect.center[0]+30), (scoreTextRect.center[1]-7)))
        window.blit(scoreNumber, scoreNumberRect)

        highScoreText = self.smallTextFont.render("High score", False, (0, 0, 0), None)
        highScoreTextRect = highScoreText.get_rect(center=((textPanelRect.center[0]-40), (textPanelRect.center[1]+8)))
        window.blit(highScoreText, highScoreTextRect)

        newHighScoreText = self.smallTextFont.render("0 New high score 0", False, (0, 0, 0), None)
        newHighScoreRect = newHighScoreText.get_rect(center=((textPanelRect.center[0]-1, (textPanelRect.center[1]+30))))

        self.checkHighScore()

        if self.newHighScore == True:
            # If the player attained a high score, draw a message that informs the player
            window.blit(newHighScoreText, newHighScoreRect)

        highScoreNumber = self.smallNumberFont.render(str(self.highScore), False, (0, 0, 0), None) # Fetch high score from file
        highScoreNumberRect = highScoreNumber.get_rect(topleft=((highScoreTextRect.center[0]+45), (highScoreTextRect.center[1]-7)))
        window.blit(highScoreNumber, highScoreNumberRect)

        # Draws the input prompt text
        inputPromptText = self.smallerTextFont.render("Press the Spacebar to try again", False, (0, 0, 0), None)
        inputPromptRect = inputPromptText.get_rect(center=(textPanelRect.center[0]-1, (textPanelRect.center[1]+50)))
        window.blit(inputPromptText, inputPromptRect)

    def initialiseHighScoreFile(self):
        defaultValue = 0
        if not os.path.exists("Assets/highscore.txt"):
            # If the file does not exist, create it and write the default value of 0
            with open("Assets/highscore.txt", "w") as file:
                file.write(str(defaultValue))
        else:
            with open("Assets/highscore.txt", "r+") as file:
                if file.read().strip() == "":
                    # If the file is empty, write the default value of 0
                    file.write(str(defaultValue))

    def checkHighScore(self):
        # Initialise the high score file if necessary
        self.initialiseHighScoreFile()

        with open("Assets/highscore.txt", "r") as file:
            # Strip the file of any leading and trailing whitespace and return the integer value of the high score
            self.highScore = int(file.read().strip())

        if player.score > self.highScore:
            # If the player's score was higher than the high score, set the high score to the player's score and set newHighScore to True
            self.highScore = player.score
            self.newHighScore = True
            with open("Assets/highscore.txt", "w") as file:
                file.write(str(self.highScore))



# Initialising various sound effects for the game
flapSound = pygame.mixer.Sound("Assets/Audio/Sound Effects/Flap.mp3")
pointSound = pygame.mixer.Sound("Assets/Audio/Sound Effects/Point.mp3")
hitSound = pygame.mixer.Sound("Assets/Audio/Sound Effects/Hit.mp3")
swooshSound = pygame.mixer.Sound("Assets/Audio/Sound Effects/Swoosh.mp3")


# Starts playing the background music as soon as the game begins, and sets its initial volume
pygame.mixer.music.load("Assets/Audio/Music/PixelPlains.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1) # parameter of -1 means that it will loop forever



# Creates an instance of the player class
player = Player()

# Creates an instance of the ground class
ground = Ground()

# Creates an instance of the background class
background = Background()

# Creates an instance of the GUI class
gui = GUI()

# Creates three instances of the pipes class
pipes1 = Pipes("Assets/Sprites/Pipes/TopPipe.png", "Assets/Sprites/Pipes/BottomPipe.png", (256, 0), (256, 0))
pipes2 = Pipes("Assets/Sprites/Pipes/TopPipe.png", "Assets/Sprites/Pipes/BottomPipe.png", (384, 0), (384, 0))
pipes3 = Pipes("Assets/Sprites/Pipes/TopPipe.png", "Assets/Sprites/Pipes/BottomPipe.png", (512, 0), (512, 0))

# Counts the number of frames to determine when the player should animate
playerFrameCounter = 0

# Counts the number of frames to ensure that only 1 point is added each time the player passes through two pipes
scoreFrameCounter = 0

# Specifies how often the player should animate
animationFrequency = 7

# Initialises the variable that determines the 'state' that the game is currently in (e.g. paused, waiting for player input to start, main menu etc.)
gameState = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # If the window's 'X' button is pressed, running is set to false and the main game loop ends
            running = False

        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "space":
                if player.gameOver == False and player.hitPipe == False:
                    gameState = 2
                    # Boost the player upwards everytime they press space
                    # Player velocity is reset back to 0
                    player.velocityY = 0
                    player.velocityY -= 1.75
                    flapSound.play()
                if player.gameOver == True and gameState == 3:
                    # If the user presses space when the bird has died, they are brought to game state 1, in which the bird flies straight and waits for input
                    gameState = 1

                if player.gameOver == True and gameState == 1:
                    # Reset the game if the player presses space again
                    player.position = pygame.Vector2(96, 136)
                    player.velocityY = 0
                    player.gameOver = False
                    player.hitPipe = False
                    player.score = 0
                    gui.newHighScore = False
                    # Creates 'new' pipes to reset their positions when restarting the game
                    pipes1 = Pipes("Assets/Sprites/Pipes/TopPipe.png", "Assets/Sprites/Pipes/BottomPipe.png", (256, 0), (256, 0))
                    pipes2 = Pipes("Assets/Sprites/Pipes/TopPipe.png", "Assets/Sprites/Pipes/BottomPipe.png", (384, 0), (384, 0))
                    pipes3 = Pipes("Assets/Sprites/Pipes/TopPipe.png", "Assets/Sprites/Pipes/BottomPipe.png", (512, 0), (512, 0))
    
    # 0: Main menu of the game
    if gameState == 0:
        playerFrameCounter += 1

        background.moveBackground()
        ground.moveGround()

        # Drawing the GUI for the main menu
        gui.drawMainMenu()

        if playerFrameCounter >= animationFrequency and player.gameOver == False:
            # If the required number of frames has passed, allow the player to animate (change sprite) (as long as it isn't game over)
            player.animate(gameState)
            playerFrameCounter = 0
        else:
            # Else, draw the current sprite of the player
            player.drawPlayer(gameState)


    # 1: Bird is idle, flying straight; waiting for player input
    if gameState == 1:
        playerFrameCounter += 1

        background.moveBackground()
        ground.moveGround()

        if playerFrameCounter >= animationFrequency and player.gameOver == False:
            # If the required number of frames has passed, allow the player to animate (change sprite) (as long as it isn't game over)
            player.animate(gameState)
            playerFrameCounter = 0
        else:
            # Else, draw the current sprite of the player
            player.drawPlayer(gameState)


    # 2: Scoring part of the game, where the bird falls and must be controlled etc.
    if gameState == 2:

        if player.gameOver == True: # If the player hits a pipe, gameOver does not become True until the player has hit the ground after falling
            pygame.mixer.music.unpause()
            gameState = 3

        # Increments the playerFrameCounter and scoreFrameCounter variables every frame
        playerFrameCounter += 1
        scoreFrameCounter += 1

        # Background image must be redrawn each frame in order to refresh the scene and stop "onion skin" trail effect when drawing player sprite
        background.moveBackground()

        # Allows for the sets of pipes to move and be displayed
        pipes1.movePipes()
        pipes2.movePipes()
        pipes3.movePipes()

        if playerFrameCounter >= animationFrequency and player.gameOver == False:
            # If the required number of frames has passed, allow the player to animate (change sprite) (as long as it isn't game over)
            player.animate(gameState)
            playerFrameCounter = 0
        else:
            # Else, draw the current sprite of the player
            player.drawPlayer(gameState)

        # The ground is drawn after the bottom pipe is drawn to "hide" the part of the bottom pipe that is "underground"
        ground.moveGround()

        pygame.draw.rect(window, (255, 0, 0), pipes1.scoreCollisionChecker, 1)
        pygame.draw.rect(window, (255, 0, 0), pipes2.scoreCollisionChecker, 1)
        pygame.draw.rect(window, (255, 0, 0), pipes3.scoreCollisionChecker, 1)

        # Displays the player's score on the screen
        gui.drawScore()

        # Updating player position (+ velocity) and checking player collisions
        if player.gameOver == False:
            player.updatePosition()
            if scoreFrameCounter >= 16:
                # If more than 16 frames have passed since the last time the score was incremented, allow the score to be incremented again
                # This stops points being awarded to the player multiple times as they pass through one scoreCollisionChecker
                player.checkScoreCollision(pipes1.scoreCollisionChecker, pipes2.scoreCollisionChecker, pipes3.scoreCollisionChecker)
                scoreFrameCounter = 0
            player.checkIllegalCollision(ground.playerTileRect, pipes1.topPipeRect, pipes2.topPipeRect, pipes3.topPipeRect, pipes1.bottomPipeRect, pipes2.bottomPipeRect, pipes3.bottomPipeRect)


    # 3: Game over screen
    if gameState == 3:
        # Background image must be redrawn each frame in order to refresh the scene and stop "onion skin" trail effect when drawing player sprite
        background.moveBackground()

        # Allows for the sets of pipes to move and be displayed
        pipes1.movePipes()
        pipes2.movePipes()
        pipes3.movePipes()

        player.drawPlayer(gameState)

        # Draws the game over text
        gui.drawGameOver()

        # The ground is drawn after the bottom pipe is drawn to "hide" the part of the bottom pipe that is "underground"
        ground.moveGround()

    pygame.display.flip() 

    dt = clock.tick(60) / 1000


pygame.quit()