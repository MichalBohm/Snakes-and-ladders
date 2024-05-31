Hadi a žebříky
Toto je implementace klasické deskové hry "Hadi a žebříky" v jazyce Python pomocí knihovny Pygame.

Předpoklady
Před spuštěním hry se ujistěte, že máte nainstalováno:

Python 3.x
Knihovna Pygame
K instalaci Pygame můžete použít pip:

bash
Zkopírovat kód
pip install pygame
Nastavení hry
Hra je umístěna na mřížce 10x10 s očíslovanými políčky od 1 do 100. Hráči začínají na políčku 1 a jejich cílem je dosáhnout políčka 100. Hrací deska obsahuje hady a žebříky, které buď posílají hráče zpět, nebo je posouvají vpřed.

Hadi a žebříky
Hadi: Pokud hráč stoupne na políčko s hlavou hada, posune se zpět na políčko s ocasem hada.
Žebříky: Pokud hráč stoupne na políčko se spodkem žebříku, posune se vpřed na políčko s vrcholem žebříku.
Hráči
Hra podporuje dva hráče, kteří jsou reprezentováni různými barvami (červená a modrá).
Hráči se střídají ve vrhání kostkou a pohybu po desce.
První hráč, který dosáhne políčka 100, vyhrává hru.
Vrh kostkou
Hráči kliknou myší pro vrh kostkou.
Vrh kostkou je na krátkou dobu animován, než se zastaví na náhodné hodnotě mezi 1 a 6.
Začátek hry
Po spuštění hry se zobrazí úvodní obrazovka s tlačítkem "Začít hru".
Kliknutím na tlačítko "Začít hru" se spustí hra.
Spuštění hry
Pro spuštění hry spusťte Python skript:

bash
Zkopírovat kód
python snakes_and_ladders.py
Rozpis kódu
Zde je podrobný rozpis kódu:

Inicializace
Hra začíná inicializací Pygame a nastavením obrazovky, barev a hodin.

python
Zkopírovat kód
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hadi a žebřiky")
white, black, red, blue = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)
Hodiny = pygame.time.Clock()
FPS = 60
Nastavení desky
Deska je 10x10 mřížka s políčky očíslovanými od 1 do 100. Slovníky snakes a ladders mapují počáteční a koncová políčka pro hady a žebříky.

python
Zkopírovat kód
TILE_SIZE = width // 10
board = [[pygame.Rect(col * TILE_SIZE, (9 - row) * TILE_SIZE, TILE_SIZE, TILE_SIZE) for col in range(10)] for row in range(10)]
snakes = {16: 6, 47: 26, 49: 11, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
Hráči
Dva hráči jsou inicializováni s počátečními pozicemi a barvami.

python
Zkopírovat kód
player_colors = [red, blue]
player_positions = [1, 1]
num_players = 2
Fonty a obrázky kostek
Fonty jsou nastaveny pro vykreslování textu a obrázky kostek jsou načteny pro zobrazení vrhu kostky.

python
Zkopírovat kód
font = pygame.font.SysFont(None, 36)
dice_images = [pygame.image.load(f'dice{i}.png') for i in range(1, 7)]
dice_rolls = [0] * num_players
Funkce pro vykreslování
Funkce pro vykreslování desky, hráčů a dalších herních prvků.

python
Zkopírovat kód
def draw_board():
    # Vykreslení hrací desky, čísel, hadů a žebříků
    pass

def get_tile_position(tile_num):
    # Výpočet pozice políčka na obrazovce
    pass

def draw_players():
    # Vykreslení hráčů na desce
    pass

def draw_start_screen():
    # Vykreslení úvodní obrazovky
    pass

def draw_winner():
    # Zobrazení vítěze
    pass
Herní logika
Funkce pro vrh kostky a pohyb hráče.

python
Zkopírovat kód
def roll_dice():
    return random.randint(1, 6)

def move_player(player, dice_roll):
    # Pohyb hráče podle hodu kostkou a kontrola hadů nebo žebříků
    pass
Herní smyčka
Hlavní herní smyčka zpracovává události, aktualizuje stav hry a vykresluje hru.

python
Zkopírovat kód
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
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    play_button_rect = pygame.Rect(width // 2 - 50, height // 2 - 25, 100, 50)
                    if play_button_rect.collidepoint(mouse_pos):
                        game_started = True
            elif not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not rolling:
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

# Spuštění hry
game_loop()
Poznámky
Ujistěte se, že obrázky kostek (dice1.png až dice6.png) jsou ve stejném adresáři jako skript.
Hra začíná úvodní obrazovkou. Klikněte na tlačítko "Začít hru" pro spuštění.
Klikněte pro vrh kostkou a pohyb hráčů na desce.
První hráč, který dosáhne políčka 100, vyhrává hru.