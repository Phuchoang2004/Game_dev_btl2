import os
import sys
import pygame as pg
import math
from Physics.physics import resolve_circle_vs_circle, clamp_to_rect

from GameObject.ball import Ball
from GameObject.player import Player
from ui.hud import HUDPanel
from ui.timer import CountdownTimer
from controller.AI import AttackingAI, DefensiveAI

SCREEN_SIZE = (960, 620)
# Center the pitch with equal margins on all sides (100px)
PITCH_RECT = pg.Rect(100, 100, SCREEN_SIZE[0] - 200, SCREEN_SIZE[1] - 200)


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


def draw_crowds(surface: pg.Surface, crowd_img: pg.Surface):
    surface.blit(crowd_img, (0, 0)) #left
    surface.blit(crowd_img, (SCREEN_SIZE[0] // 2 - crowd_img.get_width() // 2, 0)) # middle
    surface.blit(crowd_img, (SCREEN_SIZE[0] - crowd_img.get_width(), 0)) # right
    surface.blit(crowd_img, (0, SCREEN_SIZE[1] - crowd_img.get_height()))
    surface.blit(crowd_img, (SCREEN_SIZE[0] // 2 - crowd_img.get_width() // 2, SCREEN_SIZE[1] - crowd_img.get_height()))
    surface.blit(crowd_img, (SCREEN_SIZE[0] - crowd_img.get_width(), SCREEN_SIZE[1] - crowd_img.get_height()))

def draw_indicator(surface, player, world_to_screen, camera):
    screen_x, screen_y = world_to_screen(player.pos.x, player.pos.y, 0, camera)
    # Vẽ vòng tròn highlight dưới chân
    pg.draw.circle(surface, (255, 255, 0), (screen_x, screen_y + player.radius), player.radius + 5, 2)


def run():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    left, top, right, bottom = (
        PITCH_RECT.left,
        PITCH_RECT.top,
        PITCH_RECT.right,
        PITCH_RECT.bottom,
    )
    pg.init()
    pg.display.set_caption("Ball Massage")
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()

    field_image = pg.image.load("assets/sprites/field.png").convert()
    field_image = pg.transform.scale(field_image, (right - left, bottom - top))

    crowd_image1 = pg.image.load("assets/sprites/crowd1.png").convert_alpha()
    crowd_image1 = pg.transform.scale(crowd_image1, (300, 100))
    crowd_image2 = pg.image.load("assets/sprites/crowd2.png").convert_alpha()
    crowd_image2 = pg.transform.scale(crowd_image2, (300, 100))
    crowd_images = [crowd_image1, crowd_image2]
    crowd_index = 0
    crowd_timer = 0.0
    crowd_interval = 0.3

    indicator_red = pg.image.load("assets/sprites/redteam.png").convert_alpha()
    indicator_blue = pg.image.load("assets/sprites/blueteam.png").convert_alpha()  
    indicator_blue = pg.transform.scale(indicator_blue, (40, 40))
    indicator_red = pg.transform.scale(indicator_red, (40, 40))
    indicator_blue = pg.transform.rotate(indicator_blue, 180)
    indicator_red = pg.transform.rotate(indicator_red, 180)

    pg.mixer.init()
    sound_ballhit = pg.mixer.Sound("assets/audio/ball_hit.mp3")
    sound_playerrun = pg.mixer.Sound("assets/audio/player_run.mp3")

    goal_width = 40  # độ sâu khung thành
    goal_height = 80  # chiều cao khung thành

    # Load font and create HUD
    font_score = pg.font.Font("assets/fonts/Retroville NC.TTF", 32)
    font_timer = pg.font.Font("assets/fonts/Retroville NC.TTF", 24)
    hud = HUDPanel(font_score, font_timer, center=(SCREEN_SIZE[0] // 2, 50))

    # Create game objects
    """player1 = Player(
        (SCREEN_SIZE[0] * 0.3, SCREEN_SIZE[1] * 0.5),
        sprite_path="./assets/sprites/player1/",
    )
    player2 = Player(
        (SCREEN_SIZE[0] * 0.7, SCREEN_SIZE[1] * 0.5),
        sprite_path="./assets/sprites/player2/",
    )"""
    team1_players = [
        Player((SCREEN_SIZE[0] * 0.3, SCREEN_SIZE[1] * 0.4), sprite_path="./assets/sprites/player1/"),
        Player((SCREEN_SIZE[0] * 0.3, SCREEN_SIZE[1] * 0.5), sprite_path="./assets/sprites/player1/"),
        Player((SCREEN_SIZE[0] * 0.3, SCREEN_SIZE[1] * 0.6), sprite_path="./assets/sprites/player1/"),
    ]

    team2_players = [
        Player((SCREEN_SIZE[0] * 0.7, SCREEN_SIZE[1] * 0.4), sprite_path="./assets/sprites/player2/"),
        Player((SCREEN_SIZE[0] * 0.7, SCREEN_SIZE[1] * 0.5), sprite_path="./assets/sprites/player2/"),
        Player((SCREEN_SIZE[0] * 0.7, SCREEN_SIZE[1] * 0.6), sprite_path="./assets/sprites/player2/"),
    ]
    all_players = team1_players + team2_players

    # Role-based AI instances (shared within team)
    attack_target_team1 = (right - 20, (top + bottom) // 2)
    defend_target_team1 = (left + 20, (top + bottom) // 2)
    attack_target_team2 = (left + 20, (top + bottom) // 2)
    defend_target_team2 = (right - 20, (top + bottom) // 2)

    ai_attack_team1 = AttackingAI(attack_pos=attack_target_team1)
    ai_defend_team1 = DefensiveAI(defend_pos=defend_target_team1)
    ai_attack_team2 = AttackingAI(attack_pos=attack_target_team2)
    ai_defend_team2 = DefensiveAI(defend_pos=defend_target_team2)

    active1 = 0  # cầu thủ active của team1
    active2 = 0  # cầu thủ active của team2

    # Persisted roles per player index: "attack" | "defend" | None (for active)
    roles1 = [None for _ in team1_players]
    roles2 = [None for _ in team2_players]

    # Initialize: non-active take one attack and one defend
    others1 = [i for i in range(len(team1_players)) if i != active1]
    if len(others1) >= 2:
        roles1[others1[0]] = "attack"
        roles1[others1[1]] = "defend"
    others2 = [i for i in range(len(team2_players)) if i != active2]
    if len(others2) >= 2:
        roles2[others2[0]] = "attack"
        roles2[others2[1]] = "defend"

    def on_switch(team_roles, prev_active_idx, new_active_idx):
        # Role Switch
        new_role = team_roles[new_active_idx]
        team_roles[new_active_idx] = None
        team_roles[prev_active_idx] = new_role
        all_idx = list(range(len(team_roles)))
        non_actives = [i for i in all_idx if i != new_active_idx]
        desired = {"attack", "defend"}
        present = set(r for i, r in enumerate(team_roles) if i in non_actives and r is not None)
        missing = list(desired - present)
        if missing:
            for i in non_actives:
                if team_roles[i] is None or (len(present) == 1 and team_roles[i] in present and len(missing) == 1):
                    team_roles[i] = missing[0]
                    break


    ball = Ball((SCREEN_SIZE[0] * 0.5, SCREEN_SIZE[1] * 0.5))
    goal_left = pg.Rect(
        left - goal_width,
        (top + bottom) // 2 - goal_height // 2,
        goal_width,
        goal_height,
    )
    goal_right = pg.Rect(
        right, (top + bottom) // 2 - goal_height // 2, goal_width, goal_height
    )

    goal_net = pg.image.load("assets/sprites/goalpost.png").convert_alpha()
    goal_net_left = pg.transform.scale(goal_net, (goal_width, goal_height))
    goal_net_right = pg.transform.scale(goal_net, (goal_width, goal_height))
    goal_net_right = pg.transform.flip(goal_net_right, True, False)

    score_left = 0
    score_right = 0

    timer = CountdownTimer(60000)

    camera = (0, 0)
    running = True

    pg.mixer.music.load("assets/audio/stadium_sound.mp3")
    pg.mixer.music.set_volume(0.2)
    pg.mixer.music.play(loops=-1)

    while running:

        dt = clock.tick(60) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            # Kick inputs
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    team1_players[active1].attempt_kick(ball, sound_ballhit)
                if event.key in (pg.K_RCTRL, pg.K_RSHIFT):
                    team2_players[active2].attempt_kick(ball, sound_ballhit)
                if event.key == pg.K_q:  # team1 đổi người
                    prev = active1
                    active1 = (active1 + 1) % len(team1_players)
                    on_switch(roles1, prev, active1)
                if event.key == pg.K_p:  # team2 đổi người
                    prev = active2
                    active2 = (active2 + 1) % len(team2_players)
                    on_switch(roles2, prev, active2)

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

        team1_players[active1].update(dt, play1_keys, PITCH_RECT)
        team2_players[active2].update(dt, play2_keys, PITCH_RECT)
        for i, p in enumerate(team1_players):
            if i != active1:
                role = roles1[i] or "attack"
                ai = ai_attack_team1 if role == "attack" else ai_defend_team1
                ai_keys = ai.get_keys(p, ball, teammates=team1_players)
                p.update(dt, ai_keys, PITCH_RECT)
                if ai.should_kick(p, ball):
                    p.attempt_kick(ball, sound_ballhit)
        for i, p in enumerate(team2_players):
            if i != active2:
                role = roles2[i] or "attack"
                ai = ai_attack_team2 if role == "attack" else ai_defend_team2
                ai_keys = ai.get_keys(p, ball, teammates=team2_players)
                p.update(dt, ai_keys, PITCH_RECT)
                if ai.should_kick(p, ball):
                    p.attempt_kick(ball, sound_ballhit)

        # ball.update(dt, BALL_RECT)
        ball.update(dt, PITCH_RECT, goal_left, goal_right)
        
        # Player-ball collision when on ground proximity
        for p in all_players:
            ball.collide_with_player(p, restitution=0.2)

        # Player-player hun nhau (us)
        

# Check va chạm giữa mọi cặp cầu thủ
        for i in range(len(all_players)):
            for j in range(i + 1, len(all_players)):
                p1 = all_players[i]
                p2 = all_players[j]

                p1p, p1v, p2p, p2v = resolve_circle_vs_circle(
                    p1.pos, p1.radius, p1.vel,
                    p2.pos, p2.radius, p2.vel,
                    restitution=0.0,
                )

                p1.pos, p1.vel = p1p, p1v
                p2.pos, p2.vel = p2p, p2v

        # Check for goal
        goal_sound = pg.mixer.Sound("assets/audio/goal.mp3")
        goal_sound.set_volume(0.5)
        if (
            ball.rect.right < goal_left.right
            and goal_left.top < ball.rect.centery < goal_left.bottom
        ):
            goal_sound.play()
            print("Goal for Right Team!")
            score_right += 1
            ball.reset()

        # Bóng qua vạch khung thành bên phải
        if (
            ball.rect.left > goal_right.left
            and goal_right.top < ball.rect.centery < goal_right.bottom
        ):
            goal_sound.play()
            print("Goal for Left Team!")
            score_left += 1
            ball.reset()
        # Render

        draw_pitch(screen)  # Se xoa sau

        screen.blit(field_image, (left, top))

        # draw crowds
        crowd_timer += dt
        if crowd_timer >= crowd_interval:
            crowd_timer = 0.0
            crowd_index = (crowd_index + 1) % 2
        # draw crowds
        draw_crowds(screen, crowd_images[crowd_index])

        # Draw in depth order by y
        drawables = [
            (ball.pos.y, lambda: ball.draw(screen, world_to_screen, camera)),
        ]
        for p in team1_players + team2_players:
            drawables.append((p.pos.y, lambda p=p: p.draw(screen, world_to_screen, camera)))
        for _, draw_fn in sorted(drawables, key=lambda t: t[0]):
            draw_fn()

       
        p1 = team1_players[active1]
        ind_rect = indicator_blue.get_rect(center=(p1.pos.x, p1.pos.y - p1.radius - 20))
        screen.blit(indicator_blue, ind_rect)
        p2 = team2_players[active2]
        ind_rect = indicator_red.get_rect(center=(p2.pos.x, p2.pos.y - p2.radius - 20))
        screen.blit(indicator_red, ind_rect)

        screen.blit(goal_net_left, goal_left.topleft)
        screen.blit(goal_net_right, goal_right.topleft)
        time_str = timer.format_mmss()
        hud.draw(screen, score_left, score_right, time_str)

        pg.display.flip()

    pg.quit()
    sys.exit(0)


if __name__ == "__main__":
    run()
