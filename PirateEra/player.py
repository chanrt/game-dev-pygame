import pygame
pygame.init()
from screen_params import Screen
import flags

class Player(pygame.sprite.Sprite):
        
        speed_front = 4
        speed_back = 2
        speed_y = 6
        angle = 0

        def __init__(self):
            super(Player, self).__init__()
            self.state = 0
            self.full_hp = 1000
            self.current_hp = self.full_hp
            self.num_es = 5
            self.ready = 0
            self.reload = 8

            self.images = []
            for num in range(0,4):
                self.images.append(pygame.image.load(Screen.file_path + r'\ships\player_' + str(num) + '.png'))
            
            self.rect = self.images[0].get_rect()
            self.rect.move_ip(Screen.padding, (Screen.height - self.rect.height) // 2)

            self.max_effect_cycles = 500
            self.effect_cycles = 0
            self.effects = flags.NONE

        def update(self, screen, key_pressed):

            if self.ready > 0:
                self.ready -= 1

            if self.effect_cycles > 0:
                self.effect_cycles -= 1
            if self.effect_cycles == 0:
                self.effect = flags.NONE

            if self.current_hp >= 2 * self.full_hp // 3:
                self.state = 0
            elif self.current_hp >= self.full_hp // 3:
                self.state = 1
            elif self.current_hp < self.full_hp // 3 and self.current_hp > 0:
                self.state = 2
            elif self.current_hp <= 0:
                self.current_hp = 0
                self.state = 3

            if self.effect == flags.FIREPOWER_ORB:
                multiplier = 2
            else:
                multiplier = 1

            if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
                self.rect.move_ip(0,-multiplier*self.speed_y)
                self.angle = 10
            elif key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
                self.rect.move_ip(0,multiplier*self.speed_y)
                self.angle = -10
            else:
                self.angle = 0

            if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
                self.rect.move_ip(-multiplier*self.speed_back,0)
            elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
                self.rect.move_ip(multiplier*self.speed_front,0)
            
            if self.rect.top < Screen.padding:
                self.rect.top = Screen.padding

            if self.rect.bottom > Screen.height - Screen.padding:
                self.rect.bottom = Screen.height - Screen.padding

            if self.rect.left < Screen.padding:
                self.rect.left = Screen.padding

            if self.rect.right > Screen.width - Screen.padding:
                self.rect.right = Screen.width - Screen.padding

            if self.angle == 0:
                screen.blit(self.images[self.state], self.rect)
            else:
                screen.blit(pygame.transform.rotate(self.images[self.state], self.angle), self.rect)

            if self.state == 3:
                return True
            else:
                 return False

        def update_crashed(self, screen):
            if self.state < 3:
                self.state += 1
            else:
                return True
            self.rect.move_ip(self.speed_front, 0)
            screen.blit(self.images[self.state], self.rect)

        def take_damage(self, damage):
            self.current_hp -= damage

            if self.current_hp < 0:
                self.current_hp = 0

        def heal(self, amount):
            self.current_hp += amount

            if self.current_hp > self.full_hp:
                self.current_hp = self.full_hp

        def decrease_es(self):
            if self.num_es > 0:
                self.num_es -= 1

        def increase_es(self, amount):
            self.num_es += amount

        def mid_x(self):
            return self.rect.left + self.rect.width // 2

        def mid_y(self):
            return self.rect.top + self.rect.height // 2
        
        def set_effect(self, effect):
            self.effect = effect
            self.effect_cycles = self.max_effect_cycles

        def fire(self):
            self.ready = self.reload

        def can_fire(self):
            return (self.ready == 0)

