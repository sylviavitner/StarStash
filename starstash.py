import pygame
import random
import time

pygame.init()

width, height = 600, 375 # window width and height
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Star Stash")

font = pygame.font.SysFont("courier", 16, bold = True)

bg = pygame.transform.scale(pygame.image.load("skybg.png"), (width, height))

# Load cat sprite
player = pygame.image.load("cat.png").convert_alpha() 
player_rect = player.get_rect(topleft=(260, 328))
player_vel = 5

# Get stars
star = pygame.image.load("star.png").convert_alpha()
star = pygame.transform.scale(star, (48, 48))
star_rect = star.get_rect(topleft= (0, 0))
object_vel = 3

# Get lives
lives = pygame.image.load("lives.png").convert_alpha()
lives = pygame.transform.scale(lives, (80, 80))

# Star starting values
star_add_increment = 2000 # ms
star_count = 0
stars = []
player_stars = 0
missed_stars = 0

black = (0, 0, 0)

# Get player image
def get_image(sprite, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sprite, (0,0), (0, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color) # get rid of black box
    
    return image

# Get player position
def update_player_position(keys, player_rect):
    global direction # fix variable
    if keys[pygame.K_LEFT] and player_rect.left - player_vel >= 0:
        player_rect.x -= player_vel # move left
        direction = 2
    if keys[pygame.K_RIGHT] and player_rect.right + player_vel <= width:
        player_rect.x += player_vel # move right
        direction = 1
    return direction


# Player direction
direction = 1 # start r
cat1 = get_image(player, 32, 32, 2, black)
cat2 = pygame.transform.flip(cat1, True, False)
cat2.set_colorkey(black) # removes black box from cat2 (since it's still there for some reason?)
cat = cat1 

start_time = time.time()
run = True
play_game = True
clock = pygame.time.Clock()
first = True
game_type = "stars"


# MAIN GAME LOOP

while run:
    hit = False
    # Event handler
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    
    if first == True:
        win.blit(bg, (0, 0))
        start_text = font.render("Stars are falling! Use the arrow keys to catch them.", 1, "white")
        win.blit(start_text, (40, 170))
        pygame.display.update()
        time.sleep(2)
        first = False
        play_game = True

    if play_game == True:
        # Time
        
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time # count seconds


        if star_count > star_add_increment:
            star_x = random.randint(0, width - star.get_width()) # Get random x coord
            star_rect = pygame.Rect(star_x, -star.get_height(), star.get_width(), star.get_height()) # so it slides onto the screen
            stars.append(star_rect)
            star_add_increment = max(400, star_add_increment - 50) # 50ms faster each time
            star_count = 0

        for star_rect in stars[:]: # Copy of coin list to keep track of stars on screen
            star_rect.y += object_vel
            if star_rect.y > height:
                missed_stars += 1
                stars.remove(star_rect)
            elif star_rect.y + star_rect.height >= player_rect.y and star_rect.colliderect(player_rect):
                hit = True
                player_stars += 1
                stars.remove(star_rect)
    
        # Keys
        keys = pygame.key.get_pressed()
        update_player_position(keys, player_rect)
        if direction == 1:
            cat = cat1
        if direction == 2:
            cat = cat2

        # Draw
        win.blit(bg, (0, 0))
        win.blit(cat, player_rect)

        time_text = font.render(f"Stars: {player_stars}", 1, "white")
        win.blit(time_text, (10, 15)) 

        for star_rect in stars:
            win.blit(star, star_rect.topleft)
    
        # Display Lives
        if missed_stars == 0:
            win.blit(lives, (530, -10))
            win.blit(lives, (500, -10))
            win.blit(lives, (470, -10))
        elif missed_stars == 1:
            win.blit(lives, (500, -10))
            win.blit(lives, (470, -10))
        elif missed_stars == 2:
            win.blit(lives, (470, -10))
        else:
            play_game = False
    
        if play_game == False:
            win.blit(bg, (0, 0))
            lost_text = font.render(f"You collected {player_stars} stars! Press SPACE to play again.", 1, "white")
            win.blit(lost_text, (50, 170))

            keys = pygame.key.get_pressed() 

            if keys[pygame.K_SPACE]:
                # Reset game variables
                missed_stars = 0
                player_stars = 0
                stars = []
                star_count = 0
                start_time = time.time()
                star_add_increment = 2000
                play_game = True

    # Check for space input to restart
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_SPACE] and not play_game:
        # Reset game variables
        missed_stars = 0
        player_stars = 0
        stars = []
        star_count = 0
        start_time = time.time()
        star_add_increment = 2000
        play_game = True

    pygame.display.update()

