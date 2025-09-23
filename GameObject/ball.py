from Physics.physics import (
    Vec2,
    integrate_velocity,
    clamp_to_rect,
    resolve_circle_vs_circle,
)
import pygame as pg


class Ball:
    def __init__(self, start_pos: tuple[float, float]):
        self.start_pos = Vec2(*start_pos)
        self.pos = Vec2(*start_pos)
        self.vel = Vec2(0.0, 0.0)
        self.acc = Vec2(0.0, 0.0)

        self.radius = 10.0
        self.restitution_wall = 0.5
        self.linear_damping = 1.2

        self.sprite = pg.image.load("./assets/sprites/football.png").convert_alpha()
        diameter = int(self.radius * 2)
        self.sprite = pg.transform.smoothscale(self.sprite, (diameter, diameter))
        self.rect = self.sprite.get_rect(center=(self.pos.x, self.pos.y))

        self.angle = 0.0

        # glow
        self.glow_bool = False
        self.glow_surface = pg.Surface((self.radius * 4, self.radius * 4), pg.SRCALPHA)

    def kick(self, impulse_xy: tuple[float, float]):
        self.vel.x += float(impulse_xy[0])
        self.vel.y += float(impulse_xy[1])

    def apply_drag(self, dt: float):
        k = max(0.0, 1.0 - self.linear_damping * dt)
        self.vel.x *= k
        self.vel.y *= k

    def update(
        self, dt: float, pitch_rect: pg.Rect, goal_left: pg.Rect, goal_right: pg.Rect
    ):
        self.acc = Vec2(0.0, 0.0)
        new_pos, new_vel = integrate_velocity(self.pos, self.vel, self.acc, dt, 0.0)
        # double check
        r = self.radius
        left, top, right, bottom = (
            pitch_rect.left,
            pitch_rect.top,
            pitch_rect.right,
            pitch_rect.bottom,
        )

        # Top
        if new_pos.y - r < top:
            new_pos.y = top + r
            if new_vel.y < 0:
                new_vel.y = -new_vel.y * self.restitution_wall

        # Bottom
        if new_pos.y + r > bottom:
            new_pos.y = bottom - r
            if new_vel.y > 0:
                new_vel.y = -new_vel.y * self.restitution_wall

        # Left (skip clamp when within vertical goal mouth)
        if new_pos.x - r < left:
            if not (goal_left.top < new_pos.y < goal_left.bottom):
                new_pos.x = left + r
                if new_vel.x < 0:
                    new_vel.x = -new_vel.x * self.restitution_wall

        # Right (skip clamp when within vertical goal mouth)
        if new_pos.x + r > right:
            if not (goal_right.top < new_pos.y < goal_right.bottom):
                new_pos.x = right - r
                if new_vel.x > 0:
                    new_vel.x = -new_vel.x * self.restitution_wall

        self.pos = new_pos
        self.vel = new_vel

        self.apply_drag(dt)

        speed = self.vel.length()
        spin_rate = speed * 10.0  # tweak multiplier for faster/slower spin
        self.angle = (self.angle + spin_rate * dt) % 360

        self.rect.center = (self.pos.x, self.pos.y)

    def collide_with_player(self, player, restitution: float = 0.3):
        p1, v1, p2, v2 = resolve_circle_vs_circle(
            player.pos,
            player.radius,
            player.vel,
            self.pos,
            self.radius,
            self.vel,
            restitution,
        )
        player.pos = p1
        player.vel = v1
        self.pos = p2
        self.vel = v2

    def draw(self, surface, world_to_screen_fn, camera):
        import pygame as pg

        sx, sy = world_to_screen_fn(self.pos.x, self.pos.y, 0.0, camera)
        pg.draw.circle(surface, (240, 240, 240), (sx, sy), int(self.radius))
        pg.draw.circle(surface, (20, 20, 20), (sx, sy), int(self.radius), width=2)

        rotated_sprite = pg.transform.rotate(self.sprite, self.angle)
        draw_rect = rotated_sprite.get_rect(center=(sx, sy))
        surface.blit(rotated_sprite, draw_rect)

        if self.glow_bool:
            # Glow is centered under ball
            glow_rect = self.glow_surface.get_rect(center=(sx, sy))
            surface.blit(self.glow_surface, glow_rect)

    def reset(self):
        self.pos = self.start_pos.copy()  # quay lại vị trí spawn ban đầu
        self.vel = Vec2(0.0, 0.0)
        self.acc = Vec2(0.0, 0.0)
        self.angle = 0.0
        self.rect.center = (self.pos.x, self.pos.y)
