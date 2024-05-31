import pygame
import sys
import random

# Inicializace
pygame.init()

# Rozlišení
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hadi a žebřiky")

# Barvy
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Hodiny
Hodiny = pygame.time.Clock()
FPS = 60

# Nastavení hrací plochy
TILE_SIZE = width // 10
board = []
for row in range(10):
    board_row = []
    for col in range(10):
        x = col * TILE_SIZE
        y = (9 - row) * TILE_SIZE
        board_row.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    board.append(board_row)

# Hadi a žebříky
snakes = {16: 6, 47: 26, 49: 11, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Hráči
player_colors = [red, blue]
player_positions = [1, 1]  # Start at tile 1
num_players = 2

# Fonty
font = pygame.font.SysFont(None, 36)

# Obrázky kostek
dice_images = [pygame.image.load(f'dice{i}.png') for i in range(1, 7)]

# Aktuální hod kostkou pro každého hráče
dice_rolls = [0] * num_players

# Proměnné pro animaci kostky
rolling = False
roll_count = 0
current_roll = 1
final_roll = 1

# Stav hry
game_over = False
winner = None

def draw_board():
    for row in range(10):
        for col in range(10):
            rect = board[row][col]
            pygame.draw.rect(screen, white, rect)
            pygame.draw.rect(screen, black, rect, 1)
            tile_num = row * 10 + col + 1 if row % 2 == 0 else (row + 1) * 10 - col
            text = font.render(str(tile_num), True, black)
            screen.blit(text, rect.topleft)

    for start, end in snakes.items():
        start_pos = get_tile_position(start)
        end_pos = get_tile_position(end)
        pygame.draw.line(screen, red, start_pos, end_pos, 5)

    for start, end in ladders.items():
        start_pos = get_tile_position(start)
        end_pos = get_tile_position(end)
        pygame.draw.line(screen, blue, start_pos, end_pos, 5)

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

def move_player(player, dice_roll):
    global game_over, winner
    new_pos = player_positions[player] + dice_roll

    if new_pos > 100:
        new_pos = player_positions[player]
    else:
        if new_pos in snakes:
            new_pos = snakes[new_pos]
        elif new_pos in ladders:
            new_pos = ladders[new_pos]

    player_positions[player] = new_pos

    # Zkontroluje výhru
    if new_pos == 100:
        winner = player
        game_over = True

def draw_start_screen():
    screen.fill(white)
    play_button_rect = pygame.Rect(width // 2 - 50, height // 2 - 25, 100, 50)
    pygame.draw.rect(screen, black, play_button_rect, 2)
    play_text = font.render("Začít hru", True, black)
    screen.blit(play_text, (width // 2 - play_text.get_width() // 2, height // 2 - play_text.get_height() // 2))

def draw_winner():
    winner_text = font.render(f"Hráč {winner + 1} vyhrál!", True, black)
    text_rect = winner_text.get_rect(center=(width // 2, height // 2))
    background_rect = text_rect.inflate(20, 10)  # Trochu větší obdélník pro pozadí
    pygame.draw.rect(screen, white, background_rect)
    pygame.draw.rect(screen, black, background_rect, 2)
    screen.blit(winner_text, text_rect)

def game_loop():
    global rolling, roll_count, current_roll, final_roll
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
                        play_button_rect = pygame.Rect(width // 2 - 50, height // 2 - 25, 100, 50)
                        if play_button_rect.collidepoint(mouse_pos):
                            game_started = True
            elif not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not rolling:  # Levé tlačítko myši
                        rolling = True
                        roll_count = 0
                        final_roll = roll_dice()

        if not game_started:
            draw_start_screen()
        else:
            screen.fill(black)
            draw_board()
            draw_players()

            if not game_over:
                roll_count += 1
                current_roll = random.randint(1, 6)
                dice_image = dice_images[current_roll - 1]
                screen.blit(dice_image, (width // 2 - dice_image.get_width() // 2, height // 2 - dice_image.get_height() // 2))

                if rolling and roll_count % 5 == 0:
                    rolling = False
                    dice_rolls[current_player] = final_roll
                    move_player(current_player, final_roll)
                    current_player = (current_player + 1) % num_players

                for i in range(num_players):
                    player_text = font.render(f"Hráč {i + 1} je na políčku {player_positions[i]} (hodil {dice_rolls[i]})", True, red)
                    screen.blit(player_text, (10, 40 + i * 30))
            else:
                draw_winner()

        pygame.display.flip()
        Hodiny.tick(FPS)

# Začít hru
game_loop()
