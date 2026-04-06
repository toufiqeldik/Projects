import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 750, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Regular windowed mode
pygame.display.set_caption("Block Fighters!!")

# Load the image you want to set as the icon
icon_image = pygame.image.load('BlockFighters.png')  # Replace with your image path

# Set the icon of the window
pygame.display.set_icon(icon_image)  # Set the window icon

# Colors
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Player color
GREEN = (34, 139, 34)  # Ground
BLUE = (0, 0, 255)  # Enemy color
BLACK = (0, 0, 0)  # Death block color
NEON_GREEN = (57, 255, 20)  # Neon green block at the end
RED_SQUARE = (255, 0, 0)  # Red square for skin customization
ORANGE = (255, 165, 0)  # Player color Option
GREEN = (34, 139, 34)  # Player color Option

# Arrow Color (Updated to Black)
ARROW_COLOR = (128, 128, 128)  # Black color for arrows

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Character properties
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 50
player_speed = 5
jump_power = 15
gravity = 1
is_jumping = False
velocity_y = 0



# Life system
lives = 3
heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (30, 30))

# Weapon properties
weapon_width, weapon_height = 10, 40
weapon_side = "right"  # Initial position of the weapon
sword_angle = 0  # Angle of sword rotation (0 = upright)
is_attacking = False  # Whether the sword is currently in attack animation
attack_timer = 0  # Timer for attack animation duration

# Load sword image
sword_img = pygame.image.load("Sword.png").convert_alpha()
sword_img = pygame.transform.scale(sword_img, (weapon_width, weapon_height))

# Enemy properties
enemy_width, enemy_height = 50, 50
enemies = [
    {"x": 700 + i * 200, "y": HEIGHT - enemy_height - 50, "speed": 2, "alive": True, "last_shot_time": 0, "shoot_timer": 120}  # Shooting every 2 seconds (120 frames)
    for i in range(3)
]
arrow_speed = 5
arrows = []  # List to store active arrows
arrow_cooldown = 120  # Cooldown for arrows in frames (2 seconds at 60 FPS)

# World properties
world_scroll_x = 0
ground_height = 50
world_width = 2000

# Load assets
background_image = pygame.image.load("Sky.png").convert()
grass_image = pygame.image.load("grass.png").convert_alpha()

# Load Rocket Ship image
rocket_ship_img = pygame.image.load("RocketShip.png").convert_alpha()
rocket_ship_img = pygame.transform.scale(rocket_ship_img, (150, 150))  # Resize to match the original square size

# Camera speed factor
camera_speed_factor = 0.1

# Game loop
running = True
last_direction = "right"  # Default starting direction

def draw_lives():
    """Draw lives as hearts on the screen."""
    for i in range(lives):
        screen.blit(heart_img, (10 + i * 40, 10))

def game_over():
    """Handle game over state."""
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over!", True, RED)
    screen.blit(text, (250, 150))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    exit()


def show_start_screen():
    """Display the start screen and wait for user input to start the game."""
    # Load and display background image for start screen
    banner_image = pygame.image.load("bbl.png").convert()
    banner_image = pygame.transform.scale(banner_image, (WIDTH, HEIGHT))
    screen.blit(banner_image, (0, 0))

    # Text for instructions
    instructions_font = pygame.font.Font(None, 36)
    instructions_text = instructions_font.render("Press Play, Enter, or Space to Start", True, SKY_BLUE)
    instructions_text_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - -20))  # Adjust position
    screen.blit(instructions_text, instructions_text_rect)

    # Play button
    play_button_text = instructions_font.render("Play", True, WHITE)
    play_button_width = play_button_text.get_width() + 40
    play_button_height = 50

    play_button_rect = pygame.Rect(
        WIDTH // 2 - play_button_width // 2,
        HEIGHT // 2 + 50,  # Lower the button on the screen
        play_button_width,
        play_button_height
    )

    pygame.draw.rect(screen, (0, 255, 0), play_button_rect)
    screen.blit(
        play_button_text,
        (play_button_rect.x + (play_button_rect.width - play_button_text.get_width()) // 2,
         play_button_rect.y + (play_button_rect.height - play_button_text.get_height()) // 2)
    )

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    waiting = False


# Display the start screen
show_start_screen()

# Close button
close_button_img = pygame.image.load("close.png").convert_alpha()
close_button_img = pygame.transform.scale(close_button_img, (30, 30))
close_button_rect = close_button_img.get_rect(topright=(WIDTH - 10, 10))

# Level End Logic
level_end_x = world_width - 200  # Position of the neon green block at the end of the level

# In the reset_level function, update the enemy's appearance for the second level.
def reset_level(level=1):
    """Reset the level, loading different assets depending on the level."""
    global player_x, player_y, lives, enemies, world_scroll_x, background_image, grass_image

    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 50
    lives = 3
    world_scroll_x = 0

    if level == 1:
        background_image = pygame.image.load("Sky.png").convert()
        grass_image = pygame.image.load("grass.png").convert_alpha()
        enemies = [
            {"x": 700 + i * 200, "y": HEIGHT - enemy_height - 50, "speed": 2, "alive": True, "last_shot_time": 0, "shoot_timer": 120}
            for i in range(3)
        ]
    elif level == 2:
        background_image = pygame.image.load("space.png").convert()
        grass_image = pygame.image.load("moon.png").convert_alpha()
        enemies = [
            {"x": 700 + i * 200, "y": HEIGHT - enemy_height - 50, "speed": 2, "alive": True, "last_shot_time": 0, "shoot_timer": 120}
            for i in range(5)
        ]
        for enemy in enemies:
            enemy["color"] = (255, 255, 255)  # White enemies for the third level
    elif level == 3:
        print("Switching to level 3")  # Debugging output
        background_image = pygame.image.load("Saturn.png").convert()  # Use new background
        grass_image = pygame.image.load("Ring.png").convert_alpha()  # New ground texture
        enemies = [
            {"x": 700 + i * 200, "y": HEIGHT - enemy_height - 50, "speed": 3, "alive": True, "last_shot_time": 0, "shoot_timer": 100}
            for i in range(7)  # More enemies for level 3
        ]
        for enemy in enemies:
            enemy["color"] = (255, 255, 0)  # Yellow enemies for the third level



def show_level_complete_screen():
    """Display level complete screen and wait for next level or restart."""
    # Load and display the Blocktox image as the background for the level complete screen
    level_complete_image = pygame.image.load("Blocktox.png").convert()
    level_complete_image = pygame.transform.scale(level_complete_image, (WIDTH, HEIGHT))  # Resize to fit the screen
    screen.blit(level_complete_image, (0, 0))

    # Display text for level completion
    font = pygame.font.Font(None, 74)
    text = font.render("Level Completed!", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    # Create the "Next Level" button
    next_button_font = pygame.font.Font(None, 36)
    next_button_text = next_button_font.render("Next Level", True, WHITE)
    button_width = next_button_text.get_width() + 40  # Add padding
    next_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100, button_width, 50)
    
    # Draw the button
    pygame.draw.rect(screen, (0, 255, 0), next_button_rect)
    screen.blit(next_button_text, (next_button_rect.x + (next_button_rect.width - next_button_text.get_width()) // 2,
                                   next_button_rect.y + (next_button_rect.height - next_button_text.get_height()) // 2))

    pygame.display.flip()

    waiting_for_next_level = True
    while waiting_for_next_level:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos):
                    waiting_for_next_level = False
                    reset_level(level=level + 1)  # Reset for the next level (use the current level + 1)



def show_you_win_screen():
    """Display the 'You Win' screen with a message and wait for user input to either restart or quit."""
    # Fill the screen with a background color (e.g., green for victory)
    screen.fill((0, 255, 0))  # Green background for 'You Win' screen

    # Display text for 'You Win'
    font = pygame.font.Font(None, 74)
    text = font.render("You Win!", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    # Create the 'Quit' button
    quit_button_font = pygame.font.Font(None, 36)
    quit_button_text = quit_button_font.render("Quit", True, WHITE)
    button_width = quit_button_text.get_width() + 40  # Add padding
    quit_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100, button_width, 50)
    
    # Draw the button
    pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)  # Red button
    screen.blit(quit_button_text, (quit_button_rect.x + (quit_button_rect.width - quit_button_text.get_width()) // 2,
                                   quit_button_rect.y + (quit_button_rect.height - quit_button_text.get_height()) // 2))

    pygame.display.flip()

    waiting_for_quit = True
    while waiting_for_quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()  # Quit the game if the button is clicked





# Function to handle arrow shooting
def shoot_arrow(enemy):
    """Shoot an arrow from an enemy towards the player."""
    if enemy["alive"]:
        arrow = {
            "x": enemy["x"] + enemy_width // 2,
            "y": enemy["y"] + enemy_height // 2,
            "direction": 1 if player_x > enemy["x"] else -1,  # Shoot towards the player
        }
        arrows.append(arrow)

# Game loop
level = 1  # Start with level 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if close_button_rect.collidepoint(event.pos):
                running = False

    # Get key states
    keys = pygame.key.get_pressed()
    moving_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
    moving_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
    attack_pressed = keys[pygame.K_f]

    # Character movement
    if moving_left:
        player_x -= player_speed
        weapon_side = "left"  # Switch weapon to the left
        last_direction = "left"
    if moving_right:
        player_x += player_speed
        weapon_side = "right"  # Switch weapon to the right
        last_direction = "right"

    # Prevent character from going out of bounds in the world
    player_x = max(0, min(player_x, world_width - player_width))

    # Camera following logic
    target_scroll_x = player_x - WIDTH // 2 + player_width // 2
    world_scroll_x += (target_scroll_x - world_scroll_x) * camera_speed_factor
    world_scroll_x = max(0, min(world_scroll_x, world_width - WIDTH))

    # Jumping
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and not is_jumping:
        is_jumping = True
        velocity_y = -jump_power

    # Apply gravity
    if is_jumping:
        velocity_y += gravity
        player_y += velocity_y
        if player_y >= HEIGHT - player_height - ground_height:
            player_y = HEIGHT - player_height - ground_height
            is_jumping = False

    # Sword attack logic
    if attack_pressed and not is_attacking:
        is_attacking = True
        attack_timer = 10  # Attack lasts for 10 frames

    if is_attacking:
        sword_angle = -90 if last_direction == "right" else 90  # Rotate sword
        attack_timer -= 1

        # Sword collision with enemies
        for enemy in enemies:
            if enemy["alive"]:
                sword_rect = pygame.Rect(
                    player_x + (player_width if weapon_side == "right" else -weapon_width) - world_scroll_x,
                    player_y + player_height // 4,
                    weapon_width,
                    weapon_height,
                )
                enemy_rect = pygame.Rect(enemy["x"] - world_scroll_x, enemy["y"], enemy_width, enemy_height)

                if sword_rect.colliderect(enemy_rect):
                    enemy["alive"] = False

        if attack_timer <= 0:
            is_attacking = False
            sword_angle = 0  # Reset sword angle

    # Enemy logic (shoot arrows at the player)
    for enemy in enemies:
        if enemy["alive"]:
            if player_x < enemy["x"]:
                enemy["x"] -= enemy["speed"]
            elif player_x > enemy["x"]:
                enemy["x"] += enemy["speed"]

            # Shoot arrows periodically
            enemy["last_shot_time"] += 1
            if enemy["last_shot_time"] >= enemy["shoot_timer"]:
                shoot_arrow(enemy)
                enemy["last_shot_time"] = 0

    # Arrow movement
    for arrow in arrows:
        arrow["x"] += arrow["direction"] * arrow_speed
        arrow_rect = pygame.Rect(arrow["x"] - world_scroll_x, arrow["y"], 10, 10)
        
        # Check for collision with the player
        player_rect = pygame.Rect(player_x - world_scroll_x, player_y, player_width, player_height)
        if arrow_rect.colliderect(player_rect):
            lives -= 1
            arrows.remove(arrow)  # Remove the arrow

            # Check if the player has run out of lives
            if lives <= 0:
                game_over()  # Call the game over function if no lives remain

    # Fill screen with sky color
    screen.fill(SKY_BLUE)

    # Draw background and ground
    background_x = -world_scroll_x
    screen.blit(background_image, (background_x, 0))
    grass_x = -world_scroll_x
    screen.blit(grass_image, (grass_x, HEIGHT - ground_height))

    # Draw the enemies
    for enemy in enemies:
        if enemy["alive"]:
            enemy_rect = pygame.Rect(enemy["x"] - world_scroll_x, enemy["y"], enemy_width, enemy_height)
            pygame.draw.rect(screen, BLUE, enemy_rect)

    # Draw arrows
    for arrow in arrows:
        pygame.draw.rect(screen, ARROW_COLOR, pygame.Rect(arrow["x"] - world_scroll_x, arrow["y"], 10, 10))

    # Draw the player
    player_rect = pygame.Rect(player_x - world_scroll_x, player_y, player_width, player_height)
    pygame.draw.rect(screen, RED, player_rect)

    # Draw the sword
    if weapon_side == "right":
        sword_x = player_x + player_width - world_scroll_x
    else:
        sword_x = player_x - weapon_width - world_scroll_x

    sword_rect = pygame.Rect(sword_x, player_y + player_height // 4, weapon_width, weapon_height)
    screen.blit(pygame.transform.rotate(sword_img, sword_angle), sword_rect)

    # Draw lives
    draw_lives()

    # Draw rocket ship at level end
    rocket_rect = pygame.Rect(level_end_x - world_scroll_x, HEIGHT - ground_height - 150, rocket_ship_img.get_width(), rocket_ship_img.get_height())
    screen.blit(rocket_ship_img, rocket_rect)

    # Check for collision with rocket ship and handle level progression
    if player_rect.colliderect(rocket_rect):
        if level == 1:
            show_level_complete_screen()  # Show level complete screen and go to the next level
            level = 2  # Change to level 2

        elif level == 2:
            show_level_complete_screen()  # Show level complete screen and go to the next level
            level = 3  # Change to level 3

        elif level == 3:
            show_you_win_screen()  # Show 'You Win' screen at the end of level 3

            print(f"Current Level: {level}")
            running = False  # Exit the game after the win screen

    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

pygame.quit()
