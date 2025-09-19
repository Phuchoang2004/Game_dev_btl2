import os
import sys
import pygame as pg

from GameObject.ball import Ball
from GameObject.player import Player


SCREEN_SIZE = (960, 540)
PITCH_RECT = (60, 60, SCREEN_SIZE[0] - 60, SCREEN_SIZE[1] - 60)


def world_to_screen(x: float, y: float, z: float, camera=(0, 0)):
    cam_x, cam_y = camera
    return int(x - cam_x), int(y - cam_y)


def draw_pitch(surface: pg.Surface):
    surface.fill((18, 100, 40))
    left, top, right, bottom = PITCH_RECT
    pg.draw.rect(surface, (220, 255, 220), pg.Rect(left, top, right - left, bottom - top), width=4, border_radius=8)
    # Mid line and circle
    center_x = (left + right) // 2
    pg.draw.line(surface, (220, 255, 220), (center_x, top), (center_x, bottom), width=2)
    pg.draw.circle(surface, (220, 255, 220), (center_x, (top + bottom) // 2), 60, width=2)


def run():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pg.init()
    pg.display.set_caption("Ball Massage")
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()

    player = Player((SCREEN_SIZE[0] * 0.3, SCREEN_SIZE[1] * 0.5))
    ball = Ball((SCREEN_SIZE[0] * 0.5, SCREEN_SIZE[1] * 0.5))

    camera = (0, 0)
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            # Kick ball with space
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # aim towards mouse
                mx, my = pg.mouse.get_pos()
                dir_x = mx - player.pos.x
                dir_y = my - player.pos.y
                length = max(1.0, (dir_x * dir_x + dir_y * dir_y) ** 0.5)
                scale = 420.0 / length
                impulse = (dir_x * scale, dir_y * scale)
                ball.kick(impulse)

        pressed = pg.key.get_pressed()
        keys = {
            "left": pressed[pg.K_LEFT],
            "right": pressed[pg.K_RIGHT],
            "up": pressed[pg.K_UP],
            "down": pressed[pg.K_DOWN],
            "a": pressed[pg.K_a],
            "d": pressed[pg.K_d],
            "w": pressed[pg.K_w],
            "s": pressed[pg.K_s],
        }

        player.update(dt, keys, PITCH_RECT)
        ball.update(dt, PITCH_RECT)

        # Player-ball collision when on ground proximity
        ball.collide_with_player(player, restitution=0.2)

        # Render
        draw_pitch(screen)
        # Draw in depth order by y
        drawables = [
            (player.pos.y, lambda: player.draw(screen, world_to_screen, camera)),
            (ball.pos.y, lambda: ball.draw(screen, world_to_screen, camera)),
        ]
        for _, draw_fn in sorted(drawables, key=lambda t: t[0]):
            draw_fn()

        pg.display.flip()

    pg.quit()
    sys.exit(0)


if __name__ == "__main__":
    run()