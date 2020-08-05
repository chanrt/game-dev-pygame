import pygame
from screen_params import Screen

pygame.init()

pause_button = pygame.image.load(Screen.file_path + r'\ui\pause.png')
pause_button = pygame.transform.scale(pause_button, (60,60))
pause_button_rect = pause_button.get_rect()
pause_button_rect.move_ip(Screen.width - Screen.padding - pause_button_rect.width, Screen.padding)

paused_buttons_length = 80
resume_button = pygame.image.load(Screen.file_path + r'\ui\play.png')
resume_button = pygame.transform.scale(resume_button, (paused_buttons_length, paused_buttons_length))
resume_button_rect = resume_button.get_rect()

paused_buttons_y = (Screen.height - resume_button_rect.height) // 2
resume_button_x = int(Screen.width // 2 - resume_button_rect.width * 3.5)
resume_button_rect.move_ip(resume_button_x, paused_buttons_y)

restart_button = pygame.image.load(Screen.file_path + r'\ui\restart.png')
restart_button = pygame.transform.scale(restart_button, (paused_buttons_length, paused_buttons_length))
restart_button_rect = restart_button.get_rect()
restart_button_x = int(Screen.width // 2 - restart_button_rect.width * 1.5)
restart_button_rect.move_ip(restart_button_x, paused_buttons_y)

menu_button = pygame.image.load(Screen.file_path + r'\ui\menu.png')
menu_button = pygame.transform.scale(menu_button, (paused_buttons_length, paused_buttons_length))
menu_button_rect = menu_button.get_rect()
menu_button_x = int(Screen.width // 2 + menu_button_rect.width * 0.5)
menu_button_rect.move_ip(menu_button_x, paused_buttons_y)

exit_button = pygame.image.load(Screen.file_path + r'\ui\exit.png')
exit_button = pygame.transform.scale(exit_button, (paused_buttons_length, paused_buttons_length))
exit_button_rect = exit_button.get_rect()
exit_button_x = int(Screen.width // 2 + exit_button_rect.width * 2.5)
exit_button_rect.move_ip(exit_button_x, paused_buttons_y)