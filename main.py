import os
import sys
import pygame as pg
import math

from GameObject.ball import Ball
from pathlib import Path
from GameObject.player import Player
from ui.hud import HUDPanel
from ui.timer import CountdownTimer
<<<<<<< Updated upstream
=======
from controller.AI import AttackingAI, DefensiveAI
from ui.start_screen import run_start_screen
>>>>>>> Stashed changes

SCREEN_SIZE = (960, 620)
PITCH_RECT = pg.Rect(100, 100, SCREEN_SIZE[0] - 100, SCREEN_SIZE[1] - 100)



def world_to_screen(x: float, y: float, z: float, camera=(0, 0)):
    cam_x, cam_y = camera
    return int(x - cam_x), int(y - cam_y)


def draw_pitch(surface: pg.Surface):
    surface.fill((85, 137, 7))

def show_result_screen(screen, score_left, score_right, assets_path):
    font = pg.font.Font(str(assets_path / "fonts" / "Retroville NC.TTF"), 48)
    small_font = pg.font.Font(str(assets_path / "fonts" / "Retroville NC.TTF"), 28)

    if score_left > score_right:
        result_text = "Left Team Wins!"
    elif score_right > score_left:
        result_text = "Right Team Wins!"
    else:
        result_text = "It's a Draw!"

    result_surface = font.render(result_text, True, (255, 255, 255))
    score_surface = small_font.render(f"Final Score: {score_left} - {score_right}", True, (255, 255, 255))

    result_rect = result_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    score_rect = score_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 40))

    # Nút Replay
    replay_text = "REPLAY"
    replay_surface = small_font.render(replay_text, True, (0, 0, 0))
    replay_rect = replay_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))
    replay_button = pg.Rect(replay_rect.x - 30, replay_rect.y - 15, replay_rect.width + 60, replay_rect.height + 30)

    # Nút Quit (cách nút Replay thêm 80px)
    quit_text = "QUIT"
    quit_surface = small_font.render(quit_text, True, (0, 0, 0))
    quit_rect = quit_surface.get_rect(center=(screen.get_width() // 2, replay_button.centery + 80))
    quit_button = pg.Rect(quit_rect.x - 30, quit_rect.y - 15, quit_rect.width + 60, quit_rect.height + 30)

    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if replay_button.collidepoint(event.pos):
                    return "replay"
                elif quit_button.collidepoint(event.pos):
                    return "quit"

        screen.fill((0, 0, 0))
        screen.blit(result_surface, result_rect)
        screen.blit(score_surface, score_rect)

<<<<<<< Updated upstream

def run():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    left, top, right, bottom = PITCH_RECT
    pg.init()
=======
        # Vẽ nút Replay bo tròn
        pg.draw.rect(screen, (255, 255, 255), replay_button, border_radius=15)
        screen.blit(replay_surface, replay_rect)

        # Vẽ nút Quit bo tròn
        pg.draw.rect(screen, (255, 255, 255), quit_button, border_radius=15)
        screen.blit(quit_surface, quit_rect)

        pg.display.flip()
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
>>>>>>> Stashed changes
    pg.display.set_caption("Ball Massage")
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    assets_path = Path(__file__).parent / "assets"
    run_start_screen(screen,assets_path)
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
<<<<<<< Updated upstream
    player1 = Player(
    (SCREEN_SIZE[0] * 0.3, SCREEN_SIZE[1] * 0.5),
    sprite_path="./assets/sprites/player1/"
    )
    player2 = Player(
    (SCREEN_SIZE[0] * 0.7, SCREEN_SIZE[1] * 0.5),
    sprite_path="./assets/sprites/player2/"
    )
=======
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


>>>>>>> Stashed changes
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
                return "quit"
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
<<<<<<< Updated upstream
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
=======
                return "quit"
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
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
        
        # Draw in depth order by y
        drawables = [
            (player1.pos.y, lambda: player1.draw(screen, world_to_screen, camera)),
            (player2.pos.y, lambda: player2.draw(screen, world_to_screen, camera)),
            (ball.pos.y, lambda: ball.draw(screen, world_to_screen, camera)),
        ]
        for _, draw_fn in sorted(drawables, key=lambda t: t[0]):
            draw_fn()
=======
        if timer.time_left_ms() <= 0:
            return show_result_screen(screen, score_left, score_right, assets_path)
>>>>>>> Stashed changes

        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    while True:
        action = run()
        if action == "quit":
            break
        elif action == "restart":
            continue
    pg.quit()
    sys.exit(0)
