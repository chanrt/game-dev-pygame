import pygame
from screen_params import Screen
import flags
import random

ship_sinking = pygame.mixer.Sound(Screen.file_path + r'\sounds\ship_sinking.wav')

class Ship(pygame.sprite.Sprite):

    passive_speed = 2
    active_speed = 4
    height = 66

    def __init__(self, type, ship_y):
        super(Ship, self).__init__()
        self.type = type
        self.state = 0

        if self.type == flags.NEUTRAL:
            self.full_hp = 100
        elif self.type == flags.PAPAL:
            self.full_hp = 130
        elif self.type == flags.CARGO:
            self.full_hp = 180
        elif self.type == flags.PIRATE:
            self.full_hp = 220
            self.shoot_rate = 30
            self.shoot_cycle = 0
        elif self.type == flags.WARSHIP:
            self.full_hp = 300
            self.provoked = False
            self.shoot_rate = 20
            self.shoot_cycle = 0

        self.current_hp = self.full_hp
        self.sink_cycle = 0

        self.images = []

        for num in range(0,4):
            self.images.append(pygame.image.load(Screen.file_path  + '\ships\\' + flags.SHIP_STRINGS[self.type] + str(num) + '.png'))
        
        self.rect = self.images[0].get_rect()
        self.rect.left = Screen.width
        self.rect.top = ship_y

    def update(self, screen):

        if self.current_hp >= 2 * self.full_hp // 3:
            self.state = 0
        elif self.current_hp >= self.full_hp // 3:
            self.state = 1
        elif self.current_hp < self.full_hp // 3 and self.current_hp > 0:
            self.state = 2
        elif self.current_hp <= 0:
            self.current_hp = 0
            self.state = 3

        if self.current_hp:
            self.rect.move_ip(-self.active_speed,0)
        else:
            self.rect.move_ip(-self.passive_speed,0)
            self.sink_cycle += 1

            if self.sink_cycle == 1:
                ship_sinking.play()

        if self.rect.right < 0 or self.sink_cycle > 100:
            self.kill()
            return [self.type, self.rect.left, self.rect.top]
        else:
            screen.blit(self.images[self.state], self.rect)
            return [-1]

    def take_damage(self, damage):
        self.current_hp -= damage
        
        if self.current_hp < 0:
            self.current_hp = 0

    def update_shoot(self):
        self.shoot_cycle += 1

        if self.shoot_cycle == self.shoot_rate:
            self.shoot_cycle = 0
            return True
        else:
            return False

    def provoke(self):
        self.provoked = True

    def get_mast(self):
        return self.rect.top + self.rect.height // 2

    def is_alive(self):
        return self.current_hp

    def crashed(self):
        self.current_hp = 0

    def remove(self):
        self.kill()