from screen_params import Screen
import pygame
pygame.init()
pygame.display.set_caption("Pirate Era")
icon = pygame.image.load(Screen.file_path + "\\ships\\player_0.png")
pygame.display.set_icon(icon)

import random
random.seed()
import flags
import game_loop

def inRect(x, y, rect):
    if rect.left < x and x < rect.right:
        if rect.top < y and y < rect.bottom:
            return True
    return False

# screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# colors
water_blue = (51, 153, 255)
black = (0, 0, 0)
sand = (250,232,194)
dirt = (46,204,113)

# font
font = pygame.font.Font(Screen.file_path + r"\fonts\blackwood_opaque.ttf", Screen.height // 6)
heading = font.render("Pirate Era", True, black)
heading_x = (Screen.width - heading.get_width()) // 2
heading_y = Screen.height // 6

# buttons
buttons_y = int(1.75 * Screen.height // 3)

play_button = pygame.image.load(Screen.file_path + r"\ui\play.png")
play_button_rect = play_button.get_rect()
play_button_x = int(Screen.width // 2 - play_button_rect.width * 3.5)
play_button_rect.move_ip(play_button_x,buttons_y)

help_button = pygame.image.load(Screen.file_path + r"\ui\help.png")
help_button_rect = help_button.get_rect()
help_button_x = int(Screen.width // 2 - help_button_rect.width * 1.5)
help_button_rect.move_ip(help_button_x,buttons_y)

about_button = pygame.image.load(Screen.file_path + r"\ui\info.png")
about_button_rect = about_button.get_rect()
about_button_x = int(Screen.width // 2 + about_button_rect.width * 0.5)
about_button_rect.move_ip(about_button_x,buttons_y)

exit_button = pygame.image.load(Screen.file_path + r"\ui\exit.png")
exit_button_rect = exit_button.get_rect()
exit_button_x = int(Screen.width // 2 + exit_button_rect.width * 2.5)
exit_button_rect.move_ip(exit_button_x,buttons_y)

back_button = pygame.image.load(Screen.file_path + r'\ui\back.png')
back_button_rect = back_button.get_rect()
back_button_x = 2 * Screen.padding
back_button_y = (Screen.height - back_button_rect.height) // 2
back_button_rect.move_ip(back_button_x, back_button_y)

help_sprite = pygame.image.load(Screen.file_path + r'\dialogs\help.png').convert()
help_sprite_rect = help_sprite.get_rect()
help_sprite_x = (Screen.width - help_sprite_rect.width) // 2
help_sprite_y = (Screen.height - help_sprite_rect.height) // 2

about_sprite = pygame.image.load(Screen.file_path + r'\dialogs\about.png').convert()
about_sprite_rect = about_sprite.get_rect()
about_sprite_x = (Screen.width - about_sprite_rect.width) // 2
about_sprite_y = (Screen.height - about_sprite_rect.height) // 2

# crosshair
crosshair = pygame.image.load(Screen.file_path + r'\misc\crosshair.png')
crosshair = pygame.transform.scale(crosshair, (30,30))
pygame.mouse.set_visible(False)

# music
pygame.mixer.music.load(Screen.file_path + r"\sounds\bg_menu.mp3")
pygame.mixer.music.play()

class Bg_ship(pygame.sprite.Sprite):

    speed = 5

    def __init__(self):
        super(Bg_ship, self).__init__()
        self.type = random.randint(1, 4)

        self.image = pygame.image.load(Screen.file_path  + '\ships\\' + flags.SHIP_STRINGS[self.type] + '0.png')

        self.rect = self.image.get_rect()
        self.rect.left = Screen.width
        self.rect.top = random.randint(
            Screen.padding, Screen.height - self.rect.height - Screen.padding
        )

    def update(self, screen):
        self.rect.move_ip(-self.speed, 0)
        screen.blit(self.image, self.rect)
        if self.rect.right < 0:
            self.kill()


bg_ships = pygame.sprite.Group()
first_bg_ship = Bg_ship()
bg_ships.add(first_bg_ship)

bg_ship_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(bg_ship_spawn, 1000)

status = flags.STATUS_MENU
frame_rate = 24
clock = pygame.time.Clock()
running = True

while running:

    clock.tick(frame_rate)
    screen.fill(water_blue)

    x, y = pygame.mouse.get_pos()
    key_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if(status == flags.STATUS_MENU):

                    if(inRect(x,y,play_button_rect)):
                        pygame.mixer.music.stop()
                        game_loop.play(screen)
                        pygame.mixer.music.load(Screen.file_path + r'\sounds\bg_menu.mp3')
                        pygame.mixer.music.play()

                    elif(inRect(x,y,help_button_rect)):
                        status = flags.STATUS_HELP

                    elif(inRect(x,y,about_button_rect)):
                        status = flags.STATUS_ABOUT

                    elif(inRect(x,y,exit_button_rect)):
                        running = False

                else:

                    if(inRect(x,y,back_button_rect)):
                        status = flags.STATUS_MENU

        if event.type == bg_ship_spawn:
            if random.random() > 0.49:
                new_bg_ship = Bg_ship()
                bg_ships.add(new_bg_ship)

    for bg_ship in bg_ships:
        bg_ship.update(screen)

    if status == flags.STATUS_MENU:
        screen.blit(play_button, (play_button_x, buttons_y))
        screen.blit(help_button, (help_button_x, buttons_y))
        screen.blit(about_button, (about_button_x, buttons_y))
        screen.blit(exit_button, (exit_button_x, buttons_y))

        screen.blit(heading, (heading_x, heading_y))

    elif status == flags.STATUS_HELP:
        screen.blit(help_sprite, (help_sprite_x, help_sprite_y))
        screen.blit(back_button, back_button_rect)

    elif status == flags.STATUS_ABOUT:
        screen.blit(about_sprite, (about_sprite_x, about_sprite_y))
        screen.blit(back_button, back_button_rect)
    
    screen.blit(crosshair, (x-15,y-15))

    pygame.display.flip()

pygame.quit()
quit()
