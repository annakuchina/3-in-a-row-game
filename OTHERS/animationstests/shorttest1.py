import pygame, sys, os, random

pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
# screen.fill((255, 255, 255))

BLUE = pygame.image.load(os.path.join("images", "blue.png"))
GREEN = pygame.image.load(os.path.join("images", "green.png"))
ORANGE = pygame.image.load(os.path.join("images", "orange.png"))
PURPLE = pygame.image.load(os.path.join("images", "purple.png"))
RED = pygame.image.load(os.path.join("images", "red.png"))
YELLOW = pygame.image.load(os.path.join("images", "yellow.png"))

IMAGE1 = 'an_image.png'

totalItems = 64
i = 0
while i < totalItems:
    
    i = i + 1

class Item(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.width = 100
        self.height = 100
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        #the picture, and the rectangle around the picture

    # def update(self):
    #     self.rect.center = pygame.mouse.get_pos()
        # Update many different sprite classes simultaneously

# class Targets - make a new clase
# - inheritance

# newImg = pygame.image.scale("an_image.png", (10, 10))


newImg = Item(IMAGE1)
img_group = pygame.sprite.Group()
img_group.add(newImg)



# Items
itemsGroup = pygame.sprite.Group()


# screen.blit(newImage, (20, 20))



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    # screen.blit(background, (0, 0))
    img_group.draw(screen)
    clock.tick(60)





