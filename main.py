import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Light Weaver with Shadowcrafting")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
WOOD_COLOR = (139, 69, 19)  # Wood-like brown color
LIGHT_GRAY = (200, 200, 200)  # Light gray for the shadow

# Player settings
player_size = 20
player_color = WHITE
player_speed = 5
player_x = screen_width // 2
player_y = screen_height - 50

# Light beam settings
beam_length = 400
beam_color = YELLOW
beam_width = 5
beam_angle = 0

# Block settings (to cast shadows)
block_x = 400
block_y = 300
block_width = 50
block_height = 50

# Game loop variables
clock = pygame.time.Clock()
running = True

def draw_player(x, y):
    pygame.draw.circle(screen, player_color, (x, y), player_size)

def draw_light_beam(start_x, start_y, end_x, end_y):
    pygame.draw.line(screen, beam_color, (start_x, start_y), (end_x, end_y), beam_width)

def draw_block(x, y, width, height):
    pygame.draw.rect(screen, WOOD_COLOR, (x, y, width, height))

def check_intersection(beam_start, beam_end, block_x, block_y, block_width, block_height):
    """ Check if the light beam passes through or touches the block. """
    beam_start_x, beam_start_y = beam_start
    beam_end_x, beam_end_y = beam_end

    # Block boundaries
    block_top = block_y
    block_bottom = block_y + block_height
    block_left = block_x
    block_right = block_x + block_width

    # Check if the beam intersects the block (horizontally and vertically)
    if (block_left <= beam_end_x <= block_right or block_left <= beam_start_x <= block_right) and \
       (block_top <= beam_end_y <= block_bottom or block_top <= beam_start_y <= block_bottom):
        return True
    return False

def cast_shadow(block_x, block_y, block_width, block_height, beam_angle):
    """ Cast shadow behind the block based on light beam angle. """
    shadow_length = 150
    shadow_width = block_height

    # Determine shadow position based on the beam angle
    if 0 <= beam_angle < 90:  # Light from top-left, shadow to bottom-right
        shadow_x = block_x + block_width
        shadow_y = block_y + block_height
    elif 90 <= beam_angle < 180:  # Light from top-right, shadow to bottom-left
        shadow_x = block_x - shadow_length
        shadow_y = block_y + block_height
    elif 180 <= beam_angle < 270:  # Light from bottom-right, shadow to top-left
        shadow_x = block_x - shadow_length
        shadow_y = block_y - shadow_width
    else:  # Light from bottom-left, shadow to top-right
        shadow_x = block_x + block_width
        shadow_y = block_y - shadow_width

    # Draw the shadow behind the block
    shadow_rect = pygame.Rect(shadow_x, shadow_y, shadow_length, shadow_width)
    pygame.draw.rect(screen, LIGHT_GRAY, shadow_rect)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement with WASD
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Move left
        player_x -= player_speed
    if keys[pygame.K_d]:  # Move right
        player_x += player_speed
    if keys[pygame.K_w]:  # Move up
        player_y -= player_speed
    if keys[pygame.K_s]:  # Move down
        player_y += player_speed

    # Light beam angle control
    if keys[pygame.K_RIGHT]:  # Rotate beam left
        beam_angle -= 2
    if keys[pygame.K_LEFT]:  # Rotate beam right
        beam_angle += 2

    # Clear screen
    screen.fill(BLACK)

    # Draw player
    draw_player(player_x, player_y)

    # Draw block
    draw_block(block_x, block_y, block_width, block_height)

    # Calculate the light beam's end point
    beam_end_x = player_x + beam_length * math.cos(math.radians(beam_angle))
    beam_end_y = player_y - beam_length * math.sin(math.radians(beam_angle))

    # Draw light beam
    draw_light_beam(player_x, player_y, beam_end_x, beam_end_y)

    # Check if the beam passes through the block
    if check_intersection((player_x, player_y), (beam_end_x, beam_end_y), block_x, block_y, block_width, block_height):
        # Cast shadow behind the block
        cast_shadow(block_x, block_y, block_width, block_height, beam_angle)

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
