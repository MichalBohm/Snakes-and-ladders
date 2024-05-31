Hadi a žebříky
Toto je implementace klasické deskové hry "Hadi a žebříky" v jazyce Python pomocí knihovny Pygame.

K instalaci Pygame můžete použít pip:

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
Pro spuštění hry spusťte Python skript
    pygame.init()
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hadi a žebřiky")
    white, black, red, blue = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)
    Hodiny = pygame.time.Clock()
    FPS = 60
