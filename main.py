import pygame

# pygame setup
pygame.init()
window = pygame.display.set_mode((256, 288))
clock = pygame.time.Clock()
running = True
dt = 0

# Assigns the background image to the relevant variable
backgroundImage = pygame.image.load("Assets/Sprites/NightBackground.png")


# The tilemap outlines the layout of tiles
tilemap = [
    [1, 2, 1, 3, 1, 3, 1, 4, 2, 3, 1, 4, 2, 1, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Each number in the tilemap corresponds to a different tile
tiles = {
    0: pygame.image.load("Assets/Sprites/SnowyGround.png"),
    1: pygame.image.load("Assets/Sprites/SnowyGrass.png"),
    2: pygame.image.load("Assets/Sprites/SnowyGrassWithDivot.png"),
    3: pygame.image.load("Assets/Sprites/SnowyGrassWithMoss.png"),
    4: pygame.image.load("Assets/Sprites/SnowyGrassWithBumps.png")
}

for i in range(len(tilemap)):
    # Iterate through the tilemap to print the relevant tiles
    if i == 0:
        for j in range(16):
            window.blit(tiles[tilemap[i][j]], ((j*16), 256))
    if i == 1:
        for j in range(16):
            window.blit(tiles[tilemap[i][j]], ((j*16), 272))

# Draw a rect around the floor tile below the player
tileRect = pygame.Rect((48, 256), (16, 16))

# Defines the class for the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Assets/Sprites/Player/Player1.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)
        self.position = pygame.Vector2(48, 100)
        self.velocityY = 0
        self.gameOver = False
        self.gravity = 0.1

    def updatePosition(self):
        # Continually adds gravity to velocity so that the velocity of the player continually grows as the player falls
        self.velocityY += self.gravity
        self.position.y += self.velocityY
        self.rect.topleft = (self.position.x, self.position.y)

    def checkCollision(self, tileRect):
        if self.rect.colliderect(tileRect):
            # Player position is set to this value to prevent overlap between player sprite and floor tile sprite
            self.position.y = 242

            self.gameOver = True
            print("Collision detected!")

# Creates an instance of the player class
player = Player()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "space":
                if player.gameOver == False:
                    # Boost the player upwards everytime they press space
                    # Player velocity is reset back to 0
                    player.velocityY = 0
                    player.velocityY -= 2.5
                if player.gameOver == True:
                    # Reset the game if the player presses space again
                    player.position = pygame.Vector2(48, 100)
                    player.velocityY = 0
                    player.gameOver = False

                    # Floor tile is drawn again once the game resets to prevent some of the player sprite "remaining" drawn there since the last collision
                    window.blit(tiles[tilemap[0][2]], tileRect)

    # Background image must be redrawn each frame in order to refresh the scene and stop "onion skin" trail effect when drawing player sprite
    window.blit(backgroundImage, (0, 0))

    # Drawing player sprite
    window.blit(player.image, player.position)
    

    # Updating player position (+ velocity) and checking player collisions
    if player.gameOver == False:
        player.updatePosition()
        player.checkCollision(tileRect)

    pygame.display.flip()

    dt = clock.tick(60) / 1000


pygame.quit()