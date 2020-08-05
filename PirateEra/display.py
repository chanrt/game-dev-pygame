import pygame
pygame.init()
from screen_params import Screen

class Hp():

    def __init__(self, player_full_hp, heading_y):

        self.bg_length = Screen.width // 4
        self.bg_breadth = 14
        self.bg_x = (Screen.width - self.bg_length) // 2
        self.bg_y = heading_y + 10

        self.bg_rect = pygame.Rect(self.bg_x, self.bg_y, self.bg_length, self.bg_breadth)

        self.bar_length = self.bg_length - 4
        self.bar_breadth = self.bg_breadth - 4
        self.bar_x = self.bg_x + 2
        self.bar_y = self.bg_y + 2

        self.full_hp  = player_full_hp
        self.current_hp = self.full_hp
        self.bar_max_length = self.bar_length

    def change(self, amount):
        self.current_hp += amount
        if self.current_hp > self.full_hp:
            self.current_hp = self.full_hp
        elif self.current_hp < 0:
            self.current_hp = 0

        self.bar_length = (self.current_hp * self.bar_max_length) / self.full_hp

    def draw_bg(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.bg_rect)

    def draw_bar(self, screen):
        if self.bar_length < self.bar_max_length // 3:
            pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(self.bar_x, self.bar_y, self.bar_length, self.bar_breadth))
        elif self.bar_length < 2 * self.bar_max_length // 3:
            pygame.draw.rect(screen, pygame.Color("orange"), pygame.Rect(self.bar_x, self.bar_y, self.bar_length, self.bar_breadth))
        else:
            pygame.draw.rect(screen, pygame.Color("green"), pygame.Rect(self.bar_x, self.bar_y, self.bar_length, self.bar_breadth))