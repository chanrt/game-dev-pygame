import pygame
pygame.init()

from screen_params import Screen
import flags

class Item(pygame.sprite.Sprite):

    speed = 2

    def __init__(self, x, y, type):
        super(Item, self).__init__()
        self.type = type

        items_path = Screen.file_path + "\\items\\"
        if self.type == flags.CRATE:
            self.image = pygame.transform.scale(pygame.image.load(items_path + "crate.png"), (32,32))
        elif self.type == flags.REGEN_ORB:
            self.image = pygame.transform.scale(pygame.image.load(items_path + "regen_orb.png"), (55,55))
        elif self.type == flags.INVIN_ORB:
            self.image = pygame.transform.scale(pygame.image.load(items_path + "invin_orb.png"), (60,60))
        elif self.type == flags.FIREPOWER_ORB:
            self.image = pygame.transform.scale(pygame.image.load(items_path + "firepower_orb.png"), (50,50))
        elif self.type == flags.EXP_SHOT:
            self.image = pygame.transform.scale(pygame.image.load(Screen.file_path + r'\misc\cannon_ball.png'), (12,12))
            self.fire = pygame.transform.scale(pygame.image.load(Screen.file_path + r'\misc\fire.png'), (12,18))
            
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self, screen):
        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill()
        else:
            if self.type == flags.EXP_SHOT:
                screen.blit(self.image, self.rect)
                screen.blit(self.fire, (self.rect.left, self.rect.top - 18))
            else:
                screen.blit(self.image, self.rect)

    def remove(self):
        self.kill()