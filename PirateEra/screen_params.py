import pygame
import os
pygame.init()

class Screen():

    screen_info = pygame.display.Info()
    width = screen_info.current_w
    height = screen_info.current_h
    padding = 10
    file_path = os.path.dirname(__file__)