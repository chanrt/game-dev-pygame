import math
import pygame
pygame.init()
from screen_params import Screen

class Ball(pygame.sprite.Sprite):

        speed = 30

        def __init__(self, x_o, y_o, x_d, y_d, type):

            super(Ball, self).__init__()
            self.type = type
            
            if self.type == 1:
                self.image = pygame.image.load(Screen.file_path + r'\misc\cannon_ball.png')
            else: 
                self.image = pygame.image.load(Screen.file_path + r'\misc\cannon_ball.png')
                self.image = pygame.transform.scale(self.image, (12,12))
                self.fire = pygame.image.load(Screen.file_path + r'\misc\fire.png')
                self.fire = pygame.transform.scale(self.fire, (12, 18))

            self.rect = self.image.get_rect()
            self.rect.move_ip(x_o, y_o)

            self.disp = math.sqrt((x_d - x_o) ** 2 + (y_d - y_o) ** 2)
            self.speed_x = int(self.speed * (x_d - x_o) // self.disp)
            self.speed_y = int(self.speed * (y_d - y_o) // self.disp)

            if self.type == 1:
                self.damage = 25
            elif self.type == 2:
                self.damage = 40

        def update(self, screen):

            self.rect.move_ip(self.speed_x, self.speed_y)

            if self.rect.top < 0 or self.rect.bottom > Screen.height:
                self.kill()
            if self.rect.left < 0 or self.rect.right > Screen.width:
                self.kill()

            screen.blit(self.image, self.rect)
            if self.type == 2:
                screen.blit(self.fire, (self.rect.left, self.rect.top - 18))

        def remove(self):
            self.kill()