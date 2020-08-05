import paused_buttons as pb
from player import Player
from ball import Ball
from ship import Ship
from island import Island
from item import Item
from display import Hp
from screen_params import Screen

import pygame
from pygame.mixer import Sound as load_sound
import random
import flags
import math
import time
import os


def inRect(x, y, rect):
    if rect.left < x and x < rect.right:
        if rect.top < y and y < rect.bottom:
            return True
    return False


def spawn_item(ship_info, items):

    if ship_info[0] == flags.CARGO:
        new_item = Item(ship_info[1], ship_info[2], flags.CRATE)
        items.add(new_item)

    elif ship_info[0] == flags.NEUTRAL:
        if random.random() > 0.5:
            new_item = Item(ship_info[1], ship_info[2], flags.CRATE)
            items.add(new_item)

    elif ship_info[0] == flags.PAPAL:
        if random.random() < 0.34:
            new_item = Item(ship_info[1], ship_info[2], flags.INVIN_ORB)
            items.add(new_item)

        elif random.random() < 0.51:
            new_item = Item(ship_info[1], ship_info[2], flags.REGEN_ORB)
            items.add(new_item)

        else:
            new_item = Item(ship_info[1], ship_info[2], flags.FIREPOWER_ORB)
            items.add(new_item)

    elif ship_info[0] == flags.WARSHIP:
        new_item = Item(ship_info[1], ship_info[2], flags.EXP_SHOT)
        items.add(new_item)


def play(screen):

    pygame.init()
    pygame.display.set_caption("Pirate Era")
    random.seed()

    frame_rate = 30
    clock = pygame.time.Clock()

    white = (255, 255, 255)
    water_blue = (51, 153, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    gray = (190, 190, 190)

    # fonts section
    fonts_path = Screen.file_path + "\\fonts\\"
    pirate_font = pygame.font.Font(fonts_path + "blackwood_opaque.ttf", Screen.height // 20)
    comic_font = pygame.font.Font(fonts_path + "comicsans.ttf", 15)

    heading = pirate_font.render("Pirate Era", True, black)
    paused = pirate_font.render("Game Paused", True, black)
    es_info = comic_font.render(" x", True, black)
    
    heading_x = (Screen.width - heading.get_width()) // 2
    paused_x = (Screen.width - paused.get_width()) // 2
    paused_y = Screen.height // 3 - paused.get_height()

    # misc section
    misc_path = Screen.file_path + "\\misc\\"
    es_ball = pygame.transform.scale(pygame.image.load(misc_path + "cannon_ball.png"), (12,12))
    es_fire = pygame.transform.scale(pygame.image.load(misc_path + "fire.png"), (12,18))
    crosshair = pygame.image.load(misc_path + "crosshair.png")
    crosshair = pygame.transform.scale(crosshair, (30, 30))
    pygame.mouse.set_visible(False)

    # sounds section
    sounds_path = Screen.file_path + "\\sounds\\"
    player_shot = load_sound(sounds_path + "player_hit.wav")
    round_shot_fire = load_sound(sounds_path + "round_shot_fire.wav")
    explosive_shot_fire = load_sound(sounds_path + "explosive_shot_fire.wav")
    ship_aground = load_sound(sounds_path + "ship_aground.wav")
    ship_crashed = load_sound(sounds_path + "ship_crash.wav")
    ship_sinking = load_sound(sounds_path + "ship_sinking.wav")
    effect_pickup = load_sound(sounds_path + "effect_pickup.ogg")
    item_pickup = load_sound(sounds_path + "item_pickup.ogg")

    round_shot_fire.set_volume(0.5)
    explosive_shot_fire.set_volume(0.5)

    pygame.mixer.music.load(sounds_path + "bg_game_1.mp3")
    bg_music_playing = False

    # custom events
    spawn_ship = pygame.USEREVENT + 3
    spawn_island = pygame.USEREVENT + 4
    pygame.time.set_timer(spawn_ship, 1000)
    pygame.time.set_timer(spawn_island, 3000)

    player = Player()
    hp = Hp(player.full_hp, heading.get_height())
    ships = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    islands = pygame.sprite.Group()
    items = pygame.sprite.Group()

    aura_radius = player.rect.width // 2 + 20
    heart = pygame.transform.scale(pygame.image.load(Screen.file_path + r'\misc\regen.png'), (32,32))
    effect_text = ""
    effect_display = pirate_font.render(effect_text, True, black)

    status = flags.STATUS_RUNNING
    running = True
    ended = False
    player_hit = False
    left_mouse_button = False
    right_mouse_button = False

    while running:

        clock.tick(frame_rate)

        # to show the damaged state
        if status == flags.STATUS_RUNNING:
            if player_hit:
                screen.fill(red)
                player_hit = False
            else:
                screen.fill(water_blue)

        elif status == flags.STATUS_PAUSED:
            screen.fill(gray)

        # events
        x, y = pygame.mouse.get_pos()
        key_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    if status == flags.STATUS_RUNNING:
                        status = flags.STATUS_PAUSED

                    elif status == flags.STATUS_PAUSED:
                        status = flags.STATUS_RUNNING

            # stop firing
            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:
                    left_mouse_button = False
                if event.button == 3:
                    right_mouse_button = True

            # start firing
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if status == flags.STATUS_RUNNING:

                        if inRect(x, y, pb.pause_button_rect):
                            status = flags.STATUS_PAUSED

                        else:
                            left_mouse_button = True
                            right_mouse_button = False

                    if status == flags.STATUS_PAUSED:

                        if inRect(x, y, pb.resume_button_rect):
                            status = flags.STATUS_RUNNING
                        if inRect(x, y, pb.restart_button_rect):
                            pass
                        if inRect(x, y, pb.menu_button_rect):
                            running = False
                        if inRect(x, y, pb.exit_button_rect):
                            pygame.quit()
                            quit()

                elif event.button == 3:

                    right_mouse_button = True
                    left_mouse_button = False

            # custom events
            if (
                status == flags.STATUS_RUNNING
                and event.type == spawn_island
                and random.random() > 0.6
            ):
                new_island = Island()
                islands.add(new_island)

            if (
                status == flags.STATUS_RUNNING
                and event.type == spawn_ship
                and random.random() > 0.6
            ):
                ship_type = random.randint(1, 9)

                while True:
                    safe_param = True
                    y_new = random.randint(
                        Screen.padding, Screen.height - Screen.padding - Ship.height
                    )

                    for island in islands:

                        if island.rect.left > Screen.width // 3:
                            if (
                                y_new > island.rect.top - Ship.height - Screen.padding
                                and y_new < island.rect.bottom + Screen.padding
                            ):
                                safe_param = False
                                break

                    if safe_param:
                        break

                if ship_type < 6:
                    new_ship = Ship(flags.PIRATE, y_new)
                else:
                    new_ship = Ship(ship_type - 5, y_new)
                ships.add(new_ship)

        # shooting round shot
        if left_mouse_button:

            if player.can_fire() and x - player.rect.right > 0:
                if not player.effect == flags.FIREPOWER_ORB:
                    round_shot_fire.play()
                    new_ball = Ball(
                        player.rect.right,
                        player.mid_y(),
                        x,
                        y,
                        flags.ROUND_SHOT,
                    )
                else:
                    explosive_shot_fire.play()
                    new_ball = Ball(
                         player.rect.right,
                        player.mid_y(),
                        x,
                        y,
                        flags.EXPLOSIVE_SHOT,
                    )
                balls.add(new_ball)
                player.fire()

                for ship in ships:
                    if ship.type == flags.WARSHIP and not ship.provoked:
                        ship.provoke()

        # shooting explosive shot
        if right_mouse_button:

            if player.can_fire():
                if player.effect == flags.FIREPOWER_ORB or (player.num_es and x - player.rect.right > 0):
                    if not player.effect == flags.FIREPOWER_ORB:
                        player.decrease_es()
                        explosive_shot_fire.play()
                        new_ball = Ball(
                            player.rect.right,
                            player.mid_y(),
                            x,
                            y,
                            flags.EXPLOSIVE_SHOT,
                        )
                        balls.add(new_ball)
                        player.fire()

                        for ship in ships:
                            if ship.type == flags.WARSHIP and not ship.provoked:
                                ship.provoke()


        # check collissions
        for island in islands:
            if pygame.sprite.collide_rect(player, island) and not ended:
                if not player.effect == flags.INVIN_ORB:
                    ship_aground.play()
                    ended = True
                else:
                    island.remove()

        for ship in ships:
            if pygame.sprite.collide_rect(player, ship) and not ended:
                if not player.effect == flags.INVIN_ORB:
                    ended = True
                    ship_crashed.play()
                    ship.crashed()
                else:
                    ship.remove()

        for island in islands:
            for ball in balls:
                if pygame.sprite.collide_rect(ball, island) and not ended:
                    ball.remove()

        for ship in ships:
            for ball in balls:
                if pygame.sprite.collide_rect(ball, ship) and not ended:
                    if ship.current_hp > 0:
                        ship.take_damage(ball.damage)
                        ball.remove()

        for ball in balls:
            if pygame.sprite.collide_rect(ball, player) and not ended:
                if not player.effect == flags.INVIN_ORB: 
                    player_shot.play()
                    player_hit = True
                    player.take_damage(ball.damage)
                    hp.change(-ball.damage)
                ball.remove()

        for item in items:
            if pygame.sprite.collide_rect(item, player) and not ended:
                if item.type == flags.CRATE:
                    player.heal(30)
                    hp.change(30)
                    item_pickup.play()
                    item.remove()

                elif item.type == flags.EXP_SHOT:
                    player.increase_es(random.randint(5,10))
                    item_pickup.play()
                    item.remove()

                elif item.type == flags.INVIN_ORB:
                    player.set_effect(item.type)
                    effect_pickup.play()
                    item.remove()
                    effect_text = "Invincibility: "

                elif item.type == flags.REGEN_ORB:
                    player.set_effect(item.type)
                    effect_pickup.play()
                    item.remove()
                    effect_text = "Regeneration: "

                elif item.type == flags.FIREPOWER_ORB:
                    player.set_effect(item.type)
                    effect_pickup.play()
                    item.remove()
                    effect_text = "Power: "
            
        for item in items:
            for ship in ships:
                if pygame.sprite.collide_rect(item, ship):
                    item.remove()

        # updates
        if status == flags.STATUS_RUNNING:

            for island in islands:
                island.update(screen)

            for ship in ships:

                sank_ship_info = ship.update(screen)
                if sank_ship_info[0] > -1:
                    spawn_item(sank_ship_info, items)

                    if not bg_music_playing:
                        pygame.mixer.music.play()
                        bg_music_playing = True

                if ship.is_alive():
                    if ship.type == flags.PIRATE and random.random() > 0.4:
                        if ship.update_shoot() and ship.rect.left > player.rect.right:
                            new_ball = Ball(
                                ship.rect.left,
                                ship.get_mast(),
                                player.mid_x(),
                                player.mid_y(),
                                flags.ROUND_SHOT,
                            )
                            balls.add(new_ball)
                            round_shot_fire.play()

                    elif (
                        ship.type == flags.WARSHIP
                        and ship.provoked
                        and random.random() > 0.2
                    ):
                        if ship.update_shoot() and ship.rect.left > player.rect.right:
                            new_ball = Ball(
                                ship.rect.left,
                                ship.get_mast(),
                                player.mid_x(),
                                player.mid_y(),
                                flags.EXPLOSIVE_SHOT,
                            )
                            balls.add(new_ball)
                            explosive_shot_fire.play()

            for ball in balls:
                ball.update(screen)

            es_info = comic_font.render(" x" + str(player.num_es), True, black)

            if not ended:
                ended = player.update(screen, key_pressed)
            else:
                player.update_crashed(screen)

            for item in items:
                item.update(screen)

            if player.effect == flags.INVIN_ORB:
                pygame.draw.circle(screen, white, (player.mid_x(), player.mid_y()), aura_radius, 5)

            if player.effect == flags.REGEN_ORB:
                player.heal(1)
                hp.change(1)
                screen.blit(heart, (player.mid_x() - player.rect.width // 2, player.mid_y() - player.rect.width // 2))

            if player.effect == flags.FIREPOWER_ORB:
                screen.blit(es_fire, (player.mid_x() + player.rect.width // 2, player.mid_y() - player.rect.width // 2 - 18))
                screen.blit(es_ball, (player.mid_x() + player.rect.width // 2, player.mid_y() - player.rect.width // 2))

        # UI elements
        if status == flags.STATUS_RUNNING and not ended:
            screen.blit(heading, (heading_x, Screen.padding))
            screen.blit(pb.pause_button, pb.pause_button_rect)

            hp.draw_bg(screen)
            hp.draw_bar(screen)

            screen.blit(es_fire, (Screen.padding, Screen.padding) )
            screen.blit(es_ball, (Screen.padding, Screen.padding + 18))
            screen.blit(es_info, (Screen.padding + 15, 15))

            if player.effect > 0:
                effect_display = pirate_font.render(effect_text + str(player.effect_cycles // 30), True, black)
                screen.blit(effect_display, (Screen.padding, Screen.height - effect_display.get_height() - Screen.padding))

        elif status == flags.STATUS_PAUSED:
            screen.blit(paused, (paused_x, paused_y))
            screen.blit(pb.resume_button, (pb.resume_button_x, pb.paused_buttons_y))
            screen.blit(pb.restart_button, (pb.restart_button_x, pb.paused_buttons_y))
            screen.blit(pb.menu_button, (pb.menu_button_x, pb.paused_buttons_y))
            screen.blit(pb.exit_button, (pb.exit_button_x, pb.paused_buttons_y))

        if not ended:
            screen.blit(crosshair, (x - 15, y - 15))

        pygame.display.flip()

        if ended and player.update_crashed(screen):
            pygame.mixer.music.stop()
            time.sleep(2)
            running = False

    pygame.mixer.music.stop()


if __name__ == "__main__":

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    play(screen)
