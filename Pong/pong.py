import pygame as pg
import os
import random

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FRAME_RATE = 60

WALL_THICKNESS = SCREEN_HEIGHT // 30

BAR_LENGTH_FACTOR = 6
BAR_THICKNESS_FACTOR = 50
BAR_SPEED_FACTOR = 1

BALL_RADIUS_FACTOR = 100
BALL_SPEED_FACTOR = 2

UPPER_COEF = 1.2
LOWER_COEF = 0.9

BG_COLOR = pg.Color("black")
FG_COLOR = pg.Color("yellow")

# event flags
up_press = False
down_press = False
mouse_moved = False
failed = True

# score
score = 0

def drawWalls(screen):

    pg.draw.rect(screen, FG_COLOR, pg.Rect(0, 0, SCREEN_WIDTH, WALL_THICKNESS))
    pg.draw.rect(screen, FG_COLOR, pg.Rect(0, 0, WALL_THICKNESS, SCREEN_HEIGHT))
    pg.draw.rect(
        screen,
        FG_COLOR,
        pg.Rect(0, SCREEN_HEIGHT - WALL_THICKNESS, SCREEN_WIDTH, SCREEN_HEIGHT),
    )

def getRandom():

    return (random.random() * (UPPER_COEF - LOWER_COEF) + LOWER_COEF)

class Ball:

    RADIUS = SCREEN_HEIGHT // BALL_RADIUS_FACTOR
    SPEED = SCREEN_WIDTH // (FRAME_RATE * BALL_SPEED_FACTOR)
    global wall_hit

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.vx = self.SPEED
        self.vy = self.SPEED

    def move(self):

        global score
        global failed

        if not failed:
            new_x = self.x + self.vx

            if new_x < WALL_THICKNESS:
                wall_hit.play()
                self.vx = -self.vx * getRandom()
                new_x = self.x + self.vx

            elif new_x > SCREEN_WIDTH:
                fail_hit.play()
                failed = True
                music_playing = False
                score = 0

            elif new_x + self.RADIUS > bar.x and new_x < bar.x + Bar.WIDTH:
                if self.y > bar.y and self.y < bar.y + Bar.HEIGHT:
                    bar_hit.play()
                    self.vx = -self.vx * getRandom()
                    new_x = bar.x - self.RADIUS
                    score += 1

            new_y = self.y + self.vy

            if new_y < WALL_THICKNESS:
                wall_hit.play()
                self.vy = -self.vy * getRandom()
                new_y = WALL_THICKNESS

            elif new_y > SCREEN_HEIGHT - WALL_THICKNESS:
                wall_hit.play()
                self.vy = -self.vy * getRandom()
                new_y = SCREEN_HEIGHT - WALL_THICKNESS

            self.x = int(new_x)
            self.y = int(new_y)
            self.vx = int(self.vx)
            self.vy = int(self.vy)

    def draw(self, screen):
        pg.draw.circle(screen, FG_COLOR, (self.x, self.y), self.RADIUS)

    def spawn(self, x, y):
        self.x = x
        self.y = y
        self.vx = self.SPEED
        self.vy = self.SPEED


class Bar:

    HEIGHT = SCREEN_HEIGHT // BAR_LENGTH_FACTOR
    WIDTH = SCREEN_WIDTH // BAR_THICKNESS_FACTOR
    SPEED = SCREEN_HEIGHT // (FRAME_RATE * BAR_SPEED_FACTOR)

    def __init__(self, init_y):
        self.y = init_y
        self.x = SCREEN_WIDTH - 2 * self.WIDTH

    def draw(self, screen):
        pg.draw.rect(screen, FG_COLOR, pg.Rect(self.x, self.y, self.WIDTH, self.HEIGHT))

    def set_y(self, new_y):
        self.y = y

    def move_up(self):
        self.y -= self.SPEED

    def move_down(self):
        self.y += self.SPEED

    def get_y(self):
        return self.y

# seed random number generator
random.seed()

# load music
pg.mixer.init()
wall_hit = pg.mixer.Sound(os.path.dirname(__file__) + r"\wall_hit.wav")
bar_hit = pg.mixer.Sound(os.path.dirname(__file__) + r"\bar_hit.wav")
fail_hit = pg.mixer.Sound(os.path.dirname(__file__) + r"\fail.wav")
pg.mixer.music.load(os.path.dirname(__file__) + r'\electro_pop.wav')
music_playing = False

# load font
pg.font.init()
font = pg.font.Font(os.path.dirname(__file__)+r"\futura.ttf", SCREEN_WIDTH // 50)
display_score = font.render("Score: " + str(score), True, FG_COLOR)

# load objects
bar = Bar(SCREEN_HEIGHT // 2 - Bar.HEIGHT // 2)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Pong")

clock = pg.time.Clock()

while True:
    clock.tick(FRAME_RATE)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        if event.type == pg.MOUSEBUTTONDOWN:
            if failed:
                ball.spawn(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                failed = False

        if event.type == pg.KEYDOWN:
            if failed:
                ball.spawn(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                failed = False

            if event.key == pg.K_ESCAPE:
                pg.quit()
                quit()

            if event.key == pg.K_UP:
                up_press = True
                mouse_moved = False
            elif event.key == pg.K_DOWN:
                down_press = True
                mouse_moved = False

        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                up_press = False
            elif event.key == pg.K_DOWN:
                down_press = False

        if event.type == pg.MOUSEMOTION:
            x, y = pg.mouse.get_pos()
            mouse_moved = True
            up_press = False
            down_press = False

    screen.fill(BG_COLOR)

    if (
        mouse_moved
        and y > WALL_THICKNESS
        and y + Bar.HEIGHT + WALL_THICKNESS < SCREEN_HEIGHT
    ):
        bar.set_y(y)
    elif up_press and bar.get_y() - Bar.SPEED > WALL_THICKNESS:
        bar.move_up()
    elif (
        down_press
        and bar.get_y() + Bar.HEIGHT + WALL_THICKNESS + Bar.SPEED < SCREEN_HEIGHT
    ):
        bar.move_down()

    display_score = font.render("Score: {}".format(score),True,FG_COLOR)
    screen.blit(
        display_score, (WALL_THICKNESS, WALL_THICKNESS),
    )

    drawWalls(screen)
    bar.draw(screen)

    if not failed:
        ball.move()
        ball.draw(screen)

    if score == 3 and not music_playing:
        music_playing = True
        pg.mixer.music.play()

    pg.display.flip()
