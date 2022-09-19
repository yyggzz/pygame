import pygame
import os
import sys
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255) # set the background color
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # (x, y) of top left corner, width, height of rectangle

BULLET_HIT_SOUND = pygame.mixer.Sound('/Users/yigezhang/Documents/CS/Pygame/fish_shooting/Assets/shooted_sound.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('/Users/yigezhang/Documents/CS/Pygame/fish_shooting/Assets/shooting_sound.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60 # define the frame per second to refresh display
VEL = 5 # velocity that spaceships move
BULLET_VEL = 7 # velocity of bullets
MAX_BULLETS = 3 # max num of bullets
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 70 # resize the images for spaceships (before rotation)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load('/Users/yigezhang/Documents/CS/Pygame/fish_shooting/Assets/fish1.png')
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP_IMAGE = pygame.image.load('/Users/yigezhang/Documents/CS/Pygame/fish_shooting/Assets/fish2.png')
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
SPACE = pygame.transform.scale(pygame.image.load('/Users/yigezhang/Documents/CS/Pygame/fish_shooting/Assets/fish_shooting.png'), (WIDTH, HEIGHT))

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # Left key
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # Right key. 
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # Up key
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # Down key
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # Left key
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # Right key
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # Up key
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # Down key
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < -10:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()))
    pygame.display.update()
    pygame.time.delay(5000) # pause for 5 seconds

def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_HEIGHT,SPACESHIP_WIDTH) # Note that image is rotated, so use height and width are exchanged
    red = pygame.Rect(700, 300, SPACESHIP_HEIGHT,SPACESHIP_WIDTH)
    yellow_bullets = []
    red_bullets = []
    yellow_health = 10
    red_health = 10


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # ensure the same frame rate on different computers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN: # bullets for yellow spaceship
                if event.key == pygame.K_LMETA and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5) # define size of bullet as 10 x 5
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RMETA and len(red_bullets) < MAX_BULLETS: # bullets for red spaceship
                    bullet = pygame.Rect(red.x - 10, red.y + red.height//2 - 2, 10, 5) # define size of bullet as 10 x 5
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if red_health <= 0:
            winner_text = "Left fish wins!"

        if yellow_health <= 0:
            winner_text = "Right fish wins!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed() # can get multiple keys pressed together
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)
        

    main()


if __name__ == "__main__":
    main()