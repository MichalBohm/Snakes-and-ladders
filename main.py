import pygame
import sys
import random

#inicializace
pygame.init()

#rozlišení
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakes and Ladders")

#barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#hodiny
clock = pygame.time.Clock()
FPS = 50


#nastavení hrací plochy
TILE_SIZE = WIDTH // 10
board = []
for row in range(10):
    board_row = []
    for col in range(10):
        x = col * TILE_SIZE
        y = (9 - row) * TILE_SIZE
        board_row.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    board.append(board_row)

#hadi a žebříky
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

#hráči
player_colors = [RED, BLUE]
player_positions = [1, 1]  # Start at tile 1
num_players = 2
last_player_positions = [0] * num_players
#fonty
font = pygame.font.SysFont(None, 36)

#obrázky kostek
dice_images = [
    pygame.image.load(f'dice{i}.png') for i in range(1, 7)
]

def draw_board():
    for row in range(10):
        for col in range(10):
            rect = board[row][col]
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            tile_num = row * 10 + col + 1 if row % 2 == 0 else (row + 1) * 10 - col
            text = font.render(str(tile_num), True, BLACK)
            screen.blit(text, rect.topleft)

    for start, end in snakes.items():
        start_pos = get_tile_position(start)
        end_pos = get_tile_position(end)
        pygame.draw.line(screen, RED, start_pos, end_pos, 5)

    for start, end in ladders.items():
        start_pos = get_tile_position(start)
        end_pos = get_tile_position(end)
        pygame.draw.line(screen, BLUE, start_pos, end_pos, 5)

def get_tile_position(tile_num):
    row = (tile_num - 1) // 10
    col = (tile_num - 1) % 10 if row % 2 == 0 else 9 - (tile_num - 1) % 10
    x = col * TILE_SIZE + TILE_SIZE // 2
    y = (9 - row) * TILE_SIZE + TILE_SIZE // 2
    return (x, y)

def draw_players():
    for i, pos in enumerate(player_positions):
        x, y = get_tile_position(pos)
        player_rect = pygame.Rect(x - TILE_SIZE // 4, y - TILE_SIZE // 4, TILE_SIZE // 2, TILE_SIZE // 2)
        pygame.draw.rect(screen, player_colors[i], player_rect)


def roll_dice():
    return random.randint(1, 6)
        

def move_player(player):
    global new_pos
    dice_roll = roll_dice()
    new_pos = player_positions[player] + dice_roll

    if new_pos > 100:
        new_pos = player_positions[player]  
    else:
        if new_pos in snakes:
            new_pos = snakes[new_pos]
        elif new_pos in ladders:
            new_pos = ladders[new_pos]

    player_positions[player] = new_pos

    #zkontroluje výhru
    if new_pos == 100:
        print(f"Player {player + 1} wins!")
        return True  #konec hry

    return False
    #startovací obrazovka
def draw_start_screen():
    screen.fill(WHITE)
    play_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
    pygame.draw.rect(screen, BLACK, play_button_rect, 2)
    play_text = font.render("Play", True, BLACK)
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - play_text.get_height() // 2))

def game_loop():
    current_player = 0
    game_started = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_started:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        play_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
                        if play_button_rect.collidepoint(mouse_pos):
                            game_started = True
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if move_player(current_player):
                            return
                        current_player = (current_player + 1) % num_players
                       
        if not game_started:
            draw_start_screen()
        else:
            screen.fill(BLACK)
            draw_board()
            draw_players()
                

            # Draw the current dice roll
            dice_roll = roll_dice()
            dice_image = dice_images[dice_roll - 1]
            screen.blit(dice_image, (WIDTH // 2 - dice_image.get_width() // 2, HEIGHT // 2 - dice_image.get_height() // 2))
           

            # Display player's new position
            for i in range(num_players):
                player_text = font.render(f"Hráč {i + 1} je na políčku {player_positions[i]}", True, RED)
                screen.blit(player_text, (10, 40 + i * 30))

        pygame.display.flip()
        clock.tick(FPS)



# Start the game
game_loop()