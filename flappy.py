import pygame, random, time
from pygame.locals import *

#VARIABLES
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

wing = 'assets/audio/wing.wav'
hit = 'assets/audio/hit.wav'

pygame.mixer.init()


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images =  [pygame.image.load('assets/sprites/gb-logo-upflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/gb-logo-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/gb-logo-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/gb-logo-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        #UPDATE HEIGHT
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]




class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self. image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))
        

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize


        self.mask = pygame.mask.from_surface(self.image)
        self.passed = False

    def update(self):
        self.rect[0] -= GAME_SPEED

        

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()
NUMBER_IMAGES = {
    '0': pygame.image.load('assets/sprites/0.png').convert_alpha(),
    '1': pygame.image.load('assets/sprites/1.png').convert_alpha(),
    '2': pygame.image.load('assets/sprites/2.png').convert_alpha(),
    '3': pygame.image.load('assets/sprites/3.png').convert_alpha(),
    '4': pygame.image.load('assets/sprites/4.png').convert_alpha(),
    '5': pygame.image.load('assets/sprites/5.png').convert_alpha(),
    '6': pygame.image.load('assets/sprites/6.png').convert_alpha(),
    '7': pygame.image.load('assets/sprites/7.png').convert_alpha(),
    '8': pygame.image.load('assets/sprites/8.png').convert_alpha(),
    '9': pygame.image.load('assets/sprites/9.png').convert_alpha()
}

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()

for i in range (2):
    ground = Ground(GROUND_WIDHT * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range (2):
    pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

def reset_game():

    global bird_group
    global bird
    global pipe_group
    global ground_group
    global begin
    global game_over
    global score
    score = 0

    # NEW BIRD
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)

    # NEW GROUND
    ground_group = pygame.sprite.Group()

    for i in range(2):
        ground = Ground(GROUND_WIDHT * i)
        ground_group.add(ground)

    # NEW PIPES
    pipe_group = pygame.sprite.Group()

    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    game_over = False
    begin = True



clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 48)
game_over = False

while True:

    reset_game()

    while begin:

        clock.tick(15)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    pygame.mixer.music.load(wing)
                    pygame.mixer.music.play()
                    begin = False

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BEGIN_IMAGE, (120, 150))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_WIDHT - 20)
            ground_group.add(new_ground)

        bird.begin()
        ground_group.update()

        bird_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()


    while not begin:

        clock.tick(15)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    if game_over:
                        begin = True
                        break
                    else:
                        bird.bump()
                        pygame.mixer.music.load(wing)
                        pygame.mixer.music.play()

        screen.blit(BACKGROUND, (0, 0))
        score_string = str(score)
        x_pos = 150
        for digit in score_string:
            screen.blit(NUMBER_IMAGES[digit], (x_pos, 50))
            x_pos += NUMBER_IMAGES[digit].get_width()
        
        if not game_over: 

            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])

                new_ground = Ground(GROUND_WIDHT - 20)
                ground_group.add(new_ground)

            if is_off_screen(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[0])
                pipe_group.remove(pipe_group.sprites()[0])

                pipes = get_random_pipes(SCREEN_WIDHT * 2)

                pipe_group.add(pipes[0])
                pipe_group.add(pipes[1])

            bird_group.update()
            ground_group.update()
            pipe_group.update()

            for pipe in pipe_group:
                if pipe.rect[1] > 0:
                    if pipe.rect.right < bird.rect.left and not pipe.passed:
                        score += 1
                        pipe.passed = True

        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)


        if not game_over:
            if (
                pygame.sprite.groupcollide(
                    bird_group,
                    ground_group,
                    False,
                    False,
                    pygame.sprite.collide_mask
                )
                or
                pygame.sprite.groupcollide(
                    bird_group,
                    pipe_group,
                    False,
                    False,
                    pygame.sprite.collide_mask
                )
            ):
                pygame.mixer.music.load(hit)
                pygame.mixer.music.play()
                game_over = True

        # DRAW GAME OVER TEXT
        if game_over:
            text = font.render("AWWWWW BEANS", True, (255, 0, 0))
            screen.blit(text, (90, 250))

        pygame.display.update()
