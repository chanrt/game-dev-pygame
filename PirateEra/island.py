import pygame

pygame.init()
from screen_params import Screen
import random

random.seed()


class Island(pygame.sprite.Sprite):

    speed = 2
    height = 64

    def __init__(self):
        super(Island, self).__init__()
        self.image = pygame.image.load(
            Screen.file_path + r"\islands\island_" + str(random.randint(0, 7)) + ".png"
        )

        self.size = 0
        size_factor = random.randint(0, 5)
        if size_factor < 3:
            self.size = 2
        elif size_factor > 2 and size_factor < 5:
            self.size = 1
        else:
            self.size = 3

        self.image = pygame.transform.scale(
            self.image, (self.size * self.height, self.size * self.height)
        )

        self.rect = self.image.get_rect()
        self.rect.left = Screen.width
        self.rect.top = random.randint(
            Screen.padding, Screen.height - Screen.padding - self.rect.height
        )

    def update(self, screen):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        else:
            screen.blit(self.image, self.rect)

    def remove(self):
        self.kill()
