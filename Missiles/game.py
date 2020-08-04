# Missiles game

import pygame
import random
import os

random.seed()
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

missiles = pygame.sprite.Group()
clouds = pygame.sprite.Group()

missile_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(missile_spawn, 300)

cloud_spawn = pygame.USEREVENT + 2
pygame.time.set_timer(cloud_spawn, 1800)

file_path = os.path.dirname(__file__)

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen_padding = 10

bg_color = (62, 176, 247)
white = (255, 255, 255)
black = (0, 0, 0)

pygame.mixer.music.load(file_path + r"\sounds\background.wav")
pygame.mixer.music.set_volume(1.2)
heli_sound = pygame.mixer.Sound(file_path + r"\sounds\heli_sound.wav")
heli_sound.set_volume(0.7)
explosion_sound = pygame.mixer.Sound(file_path + r"\sounds\explosion.wav")
explosion_sound.set_volume(1.4)

font = pygame.font.Font(file_path + r"\futura.ttf", 28)
display_text = font.render("Score: 0", True, black)


class Heli(pygame.sprite.Sprite):

    speed_x = 10
    speed_y = 5

    def __init__(self):

        super(Heli, self).__init__()

        self.cycle = 0
        self.images = []
        for num in range(0, 3):
            image = pygame.image.load(file_path + r"\helis\heli_" + str(num) + ".png")
            image = pygame.transform.flip(image, True, False)
            image = pygame.transform.scale(image, (101, 40))
            image.set_colorkey((white))
            self.images.append(image)

        self.rect = self.images[0].get_rect()
        self.rect.left = 20
        self.rect.top = (screen_height - self.rect.height) // 2

    def draw(self, screen):
        screen.blit(self.images[self.cycle], self.rect)

        self.cycle += 1
        if self.cycle > 2:
            self.cycle = 0

    def update(self, keys):
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed_y)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed_y)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed_x, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed_x, 0)

        if self.rect.top < screen_padding:
            self.rect.top = screen_padding
        if self.rect.bottom > screen_height - screen_padding:
            self.rect.bottom = screen_height - screen_padding
        if self.rect.left < screen_padding:
            self.rect.left = screen_padding
        if self.rect.right > screen_width - screen_padding:
            self.rect.right = screen_width - screen_padding


class Missile(pygame.sprite.Sprite):
    def __init__(self):

        super(Missile, self).__init__()
        self.cycle = 0
        self.images = []

        for num in range(0, 8):
            image = pygame.image.load(
                file_path + r"\missiles\missile_" + str(num) + ".png"
            )
            image = pygame.transform.flip(image, True, False)
            image.set_colorkey((white))
            self.images.append(image)

        self.rect = self.images[0].get_rect()
        self.rect.left = screen_width
        self.rect.top = random.randint(
            screen_padding, screen_height - screen_padding - self.rect.height
        )
        self.speed = random.randint(5, 10)

    def draw(self, screen):
        screen.blit(self.images[self.cycle], self.rect)
        self.cycle += 1
        if self.cycle > 7:
            self.cycle = 1

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            return True
        else:
            return False


class Cloud(pygame.sprite.Sprite):
    def __init__(self):

        super(Cloud, self).__init__()
        self.image = pygame.image.load(file_path + r"\cloud.png")
        self.rect = self.image.get_rect()
        self.rect.left = screen_width
        self.rect.top = random.randint(
            screen_padding, screen_height - screen_padding - self.rect.height
        )
        self.speed = 3

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(file_path + r"\explosion.png")
        self.cycle = 0
        self.sub_cycle = 0

    def draw(self, screen):
        screen.blit(
            self.image,
            (self.x, self.y),
            (100 * self.sub_cycle, 100 * self.cycle, 100, 100),
        )
        self.sub_cycle += 1
        if self.sub_cycle > 4:
            self.sub_cycle = 0
            self.cycle += 1

        if self.cycle == 4 and self.sub_cycle == 4:
            return True
        else:
            return False


heli = Heli()

heli_sound.play(loops=-1)
pygame.mixer.music.play(loops=-1)

running = True
collided = False
score = 0

while running:
    clock.tick(30)
    screen.fill(bg_color)

    key_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == missile_spawn:
            new_missile = Missile()
            missiles.add(new_missile)

        if event.type == cloud_spawn:
            new_cloud = Cloud()
            clouds.add(new_cloud)

    for cloud in clouds:
        cloud.update()
        cloud.draw(screen)

    if not collided:
        heli.update(key_pressed)
        heli.draw(screen)

    for missile in missiles:
        if missile.update():
            score += 1
            display_text = font.render("Score: " + str(score), True, black)
        missile.draw(screen)

    if pygame.sprite.spritecollideany(heli, missiles) and not collided:
        collided = True
        explosion_sound.play()
        explosion = Explosion(heli.rect.left, heli.rect.top - 20)

    if collided:
        if explosion.draw(screen):
            running = False

    screen.blit(display_text, (screen_padding, screen_padding))

    pygame.display.flip()

pygame.quit()
quit()
