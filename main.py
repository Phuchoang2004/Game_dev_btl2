import os
import sys
import pygame as pg
import math

from GameObject.ball import Ball
from GameObject.player import Player
from ui.hud import HUDPanel
from ui.timer import CountdownTimer

SCREEN_SIZE = (960, 620)
PITCH_RECT = pg.Rect(100, 100, SCREEN_SIZE[0] - 100, SCREEN_SIZE[1] - 100)



def world_to_screen(x: float, y: float, z: float, camera=(0, 0)):
    cam_x, cam_y = camera
    return int(x - cam_x), int(y - cam_y)


def draw_pitch(surface: pg.Surface):
    surface.fill((85, 137, 7))
    """
    left, top, right, bottom = PITCH_RECT
    pg.draw.rect(surface, (220, 255, 220), pg.Rect(left, top, right - left, bottom - top), width=4, border_radius=8)
    # Mid line and circle
    center_x = (left + right) // 2
    pg.draw.line(surface, (220, 255, 220), (center_x, top), (center_x, bottom), width=2)
    pg.draw.circle(surface, (220, 255, 220), (center_x, (top + bottom) // 2), 60, width=2)
    # Center spot
    pg.draw.circle(surface, (220, 255, 220), (center_x, (top + bottom) // 2), 4)

    # Penalty areas
    pg.draw.rect(surface, (220, 255, 220), pg.Rect(left, (top + bottom) // 2 - 100, 120, 200), width=2)
    pg.draw.rect(surface, (220, 255, 220), pg.Rect(right - 120, (top + bottom) // 2 - 100, 120, 200), width=2)

    # goal areas
    pg.draw.rect(
        surface,
        (220, 255, 220),
        pg.Rect(left, (top + bottom) // 2 - 50, 40, 100),
        width=2,
    )
    pg.draw.rect(
        surface,
        (220, 255, 220),
        pg.Rect(right - 40, (top + bottom) // 2 - 50, 40, 100),
        width=2,
    )

    # Goals (khung thành thật, nhô ra ngoài sân)
    goal_width = 40   # độ sâu khung thành
    goal_height = 80 # chiều cao khung thành

    # Khung thành bên trái
    pg.draw.rect(
        surface,
        (220, 255, 220),
        pg.Rect(left - goal_width, (top + bottom) // 2 - goal_height // 2, goal_width, goal_height),
        width=2,
    )

    # Khung thành bên phải
    pg.draw.rect(
        surface,
        (220, 255, 220),
        pg.Rect(right, (top + bottom) // 2 - goal_height // 2, goal_width, goal_height),
        width=2,
    )

    # penalty arcs
    pg.draw.arc(surface, (220, 255, 220), pg.Rect(left +
                    120 - 60, (top + bottom) // 2 - 60, 120, 120), -0.5 * math.pi, 0.5 * math.pi, width=2)
    pg.draw.arc(surface, (220, 255, 220), pg.Rect(right - 120 - 60,
                    (top + bottom) // 2 - 60, 120, 120), 0.5 * math.pi, 1.5 * math.pi, width=2)

    # penalty spots
    pg.draw.circle(surface, (220, 255, 220), (left + 90, (top + bottom) // 2), 4)
    pg.draw.circle(surface, (220, 255, 220), (right - 90, (top + bottom) // 2), 4)"""



def run():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    left, top, right, bottom = PITCH_RECT
    pg.init()
    pg.display.set_caption("Ball Massage")
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()

    field_image = pg.image.load("assets/sprites/field.png").convert()
    field_image = pg.transform.scale(field_image, (right - left, bottom - top))

    pg.mixer.init()
    sound_ballhit = pg.mixer.Sound("assets/audio/ball_hit.mp3")
    sound_playerrun = pg.mixer.Sound("assets/audio/player_run.mp3")

    goal_width = 40   # độ sâu khung thành
    goal_height = 80 # chiều cao khung thành

    # Load font and create HUD
    font_score = pg.font.Font("assets/fonts/Retroville NC.TTF", 32)
    font_timer = pg.font.Font("assets/fonts/Retroville NC.TTF", 24)
    hud = HUDPanel(font_score, font_timer, center=(SCREEN_SIZE[0] // 2, 50))

    # Create game objects
    player1 = Player(
    (SCREEN_SIZE[0] * 0.3, SCREEN_SIZE[1] * 0.5),
    sprite_path="./assets/sprites/player1/"
    )
    player2 = Player(
    (SCREEN_SIZE[0] * 0.7, SCREEN_SIZE[1] * 0.5),
    sprite_path="./assets/sprites/player2/"
    )
    ball = Ball((SCREEN_SIZE[0] * 0.5, SCREEN_SIZE[1] * 0.5))
    goal_left = pg.Rect(left - goal_width, (top + bottom) // 2 - goal_height // 2, goal_width, goal_height)
    goal_right =  pg.Rect(right, (top + bottom) // 2 - goal_height // 2, goal_width, goal_height)

    goal_net = pg.image.load("assets/sprites/goalpost.png").convert_alpha()
    goal_net_left = pg.transform.scale(goal_net, (goal_width, goal_height))
    goal_net_right = pg.transform.scale(goal_net, (goal_width, goal_height))
    goal_net_right = pg.transform.flip(goal_net_right, True, False)

    score_left = 0
    score_right = 0

    timer = CountdownTimer(60000)

    camera = (0, 0)
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            # Kick ball with space - Giai quyet sau
            """
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # aim towards mouse
                mx, my = pg.mouse.get_pos()
                dir_x = mx - player.pos.x
                dir_y = my - player.pos.y
                length = max(1.0, (dir_x * dir_x + dir_y * dir_y) ** 0.5)
                scale = 420.0 / length
                impulse = (dir_x * scale, dir_y * scale)
                ball.kick(impulse)"""

        pressed = pg.key.get_pressed()
        play1_keys = {
            "a": pressed[pg.K_a],
            "d": pressed[pg.K_d],
            "w": pressed[pg.K_w],
            "s": pressed[pg.K_s],
        }

        play2_keys = {
            "left": pressed[pg.K_LEFT],
            "right": pressed[pg.K_RIGHT],
            "up": pressed[pg.K_UP],
            "down": pressed[pg.K_DOWN],
        }

        player1.update(dt, play1_keys, PITCH_RECT)
        player2.update(dt, play2_keys, PITCH_RECT)

        #ball.update(dt, BALL_RECT)
        ball.update(dt, PITCH_RECT, goal_left, goal_right)

        # Player-ball collision when on ground proximity
        ball.collide_with_player(player1, restitution=0.2)
        ball.collide_with_player(player2, restitution=0.2)

        # Check for goal
        if ball.rect.right < goal_left.right and goal_left.top < ball.rect.centery < goal_left.bottom:
            print("Goal for Right Team!")
            score_right += 1
            ball.reset()

        # Bóng qua vạch khung thành bên phải
        if ball.rect.left > goal_right.left and goal_right.top < ball.rect.centery < goal_right.bottom:
            print("Goal for Left Team!")
            score_left += 1
            ball.reset()
        # Render


        draw_pitch(screen) #Se xoa sau

        screen.blit(field_image, (left, top)) 

        # Goal nets
        screen.blit(goal_net_left, goal_left.topleft)
        screen.blit(goal_net_right, goal_right.topleft)
        time_str = timer.format_mmss()
        hud.draw(screen, score_left, score_right, time_str)

        
        # Draw in depth order by y
        drawables = [
            (player1.pos.y, lambda: player1.draw(screen, world_to_screen, camera)),
            (player2.pos.y, lambda: player2.draw(screen, world_to_screen, camera)),
            (ball.pos.y, lambda: ball.draw(screen, world_to_screen, camera)),
        ]
        for _, draw_fn in sorted(drawables, key=lambda t: t[0]):
            draw_fn()

        pg.display.flip()

    pg.quit()
    sys.exit(0)


if __name__ == "__main__":
    run()
