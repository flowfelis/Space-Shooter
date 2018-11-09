# Avoider Game
# Written in Python 3.6.4
# Graphic credits to https://opengameart.org/
# Sounds credits to https://www.bfxr.net/

import pygame
import random
import os

# define game window dimensions
WIDTH = 800
HEIGHT = 600

# define frames per second
FPS = 60

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
sounds_folder = os.path.join(game_folder, 'sounds')

# Definitions
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    """ Draw a text on screen """
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_go_screen():
    """ Show Game Over Screen """
    draw_text(screen, 'AVOIDER', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, 'Arrow keys to survive!', 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, 'Press the space key to begin',
              18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                waiting = False


class Spaceship(pygame.sprite.Sprite):
    # Create a spaceship
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spaceship_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speedX = 0
        self.speedY = 0

    def update(self):
        self.speedX = 0
        self.speedY = 0

        # move spaceship with arrow keys
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedX = -5
        if keystate[pygame.K_RIGHT]:
            self.speedX = 5
        if keystate[pygame.K_UP]:
            self.speedY = -5
        if keystate[pygame.K_DOWN]:
            self.speedY = 5
        self.rect.x += self.speedX
        self.rect.y += self.speedY

        # block going out of window
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Astroid(pygame.sprite.Sprite):
    # Create an astroid
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = astroid_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.center = self.create_random_location()
        self.speed = random.randrange(1, 15)

        if self.rect.y < 0:
            self.from_where = 'top'
        elif self.rect.y > HEIGHT:
            self.from_where = 'bottom'
        elif self.rect.x < 0:
            self.from_where = 'left'
        elif self.rect.x > WIDTH:
            self.from_where = 'right'

    def create_random_location(self):
        astroid_location_list = [
            # 4 edges random locations
            # top
            (random.randrange(WIDTH - self.rect.width), -self.rect.height),
            # bottom
            (random.randrange(WIDTH - self.rect.width), HEIGHT + self.rect.height),
            # left
            (-self.rect.width, random.randrange(HEIGHT - self.rect.height)),
            # right
            (WIDTH + self.rect.width, random.randrange(HEIGHT - self.rect.height))
        ]
        # choose one location from the list
        return random.choice(astroid_location_list)

    def update(self):
        if self.from_where == 'top':
            self.rect.y += self.speed
            if self.rect.top > HEIGHT:
                self.rect.center = self.create_random_location()
        if self.from_where == 'bottom':
            self.rect.y -= self.speed
            if self.rect.bottom < 0:
                self.rect.center = self.create_random_location()
        if self.from_where == 'left':
            self.rect.x += self.speed
            if self.rect.left > WIDTH:
                self.rect.center = self.create_random_location()
        if self.from_where == 'right':
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.rect.center = self.create_random_location()


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoider")
clock = pygame.time.Clock()

# Load all game graphics
background_img = pygame.image.load(os.path.join(
    img_folder, 'starfield_alpha.png')).convert()
background_img_rect = background_img.get_rect()
spaceship_img = pygame.image.load(os.path.join(img_folder, 'ship5.png'))
astroid_img = pygame.image.load(os.path.join(img_folder, 'astroid.png'))

# Load all game sounds
explosion_sound = pygame.mixer.Sound(
    os.path.join(sounds_folder, 'Explosion.wav'))
pygame.mixer.music.load(os.path.join(sounds_folder, 'Space Heroes.ogg'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
astroids = pygame.sprite.Group()

spaceship = Spaceship()
all_sprites.add(spaceship)

for _ in range(8):
    astroid = Astroid()
    all_sprites.add(astroid)
    astroids.add(astroid)

# Start the music
pygame.mixer.music.play(loops=-1)

# Game Loop
running = True
game_over = True
while running:
    if game_over:
        show_go_screen()
        game_over = False

        # Start the game again
        all_sprites = pygame.sprite.Group()
        astroids = pygame.sprite.Group()
        spaceship = Spaceship()
        all_sprites.add(spaceship)
        for _ in range(8):
            astroid = Astroid()
            all_sprites.add(astroid)
            astroids.add(astroid)

    # keep loop at the right speed
    clock.tick(FPS)

    # Process Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update Logic
    all_sprites.update()
    hits = pygame.sprite.spritecollide(
        spaceship, astroids, False, pygame.sprite.collide_circle)
    if hits:
        explosion_sound.play()
        game_over = True

    # Render / Draw
    screen.fill(BLACK)
    screen.blit(background_img, background_img_rect)
    all_sprites.draw(screen)

    # *after* drawing everything, flip
    pygame.display.flip()

pygame.quit()
