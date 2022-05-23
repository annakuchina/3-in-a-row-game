import pygame

pygame.init()

screen = pygame.display.set_mode((400, 400)) # window
clock = pygame.time.Clock()
square = pygame.Surface((20, 20))
square.fill((255, 0, 0))

press = pygame.event.get
w = 100
h = 100
left = 0
right = 0
up = 0
down = 0

count = 0
while True:

    while count < 1200:
        print("HI")
        h += 1
        
        # screen.blit(square, (w, h))

    if left:
        w += 1
        screen.fill(0)

    elif right:
        w -= 1

    elif up:
        h -= 1

    elif down:
        h += 1
    
    screen.fill(0)
    screen.blit(square, (w, h))

    if press(pygame.QUIT):
        break

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                left = 1
                right = 0
            
            if event.key == pygame.K_LEFT:
                left = 0
                right = 1
            
            if event.key == pygame.K_UP:
                up = 1
                down = 0

            if event.key == pygame.K_DOWN:
                up = 0
                down = 1

        if event.type == pygame.KEYUP:
            up = 0
            down = 0
            left = 0
            right = 0
        
    clock.tick(60)
    pygame.display.update()
    count += 1

pygame.quit()