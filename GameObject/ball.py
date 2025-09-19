from Physics.physics import Vec2, integrate_velocity, clamp_to_rect, resolve_circle_vs_circle


class Ball:
    def __init__(self, start_pos: tuple[float, float]):
        self.pos = Vec2(*start_pos)
        self.vel = Vec2(0.0, 0.0)
        self.acc = Vec2(0.0, 0.0)

        self.radius = 10.0
        self.restitution_wall = 0.5
        self.linear_damping = 1.2 

    def kick(self, impulse_xy: tuple[float, float]):
        self.vel.x += float(impulse_xy[0])
        self.vel.y += float(impulse_xy[1])

    def apply_drag(self, dt: float):
        k = max(0.0, 1.0 - self.linear_damping * dt)
        self.vel.x *= k
        self.vel.y *= k

    def update(self, dt: float, bounds_rect: tuple[float, float, float, float]):
        self.acc = Vec2(0.0, 0.0)
        new_pos, new_vel = integrate_velocity(self.pos, self.vel, self.acc, dt, 0.0)
        new_pos, new_vel = clamp_to_rect(new_pos, new_vel, bounds_rect, self.radius, self.restitution_wall)
        self.pos = new_pos
        self.vel = new_vel

        self.apply_drag(dt)

    def collide_with_player(self, player, restitution: float = 0.3):
        p1, v1, p2, v2 = resolve_circle_vs_circle(player.pos, player.radius, player.vel, self.pos, self.radius, self.vel, restitution)
        player.pos = p1
        player.vel = v1
        self.pos = p2
        self.vel = v2

    def draw(self, surface, world_to_screen_fn, camera):
        import pygame as pg
        sx, sy = world_to_screen_fn(self.pos.x, self.pos.y, 0.0, camera)
        pg.draw.circle(surface, (240, 240, 240), (sx, sy), int(self.radius))
        pg.draw.circle(surface, (20, 20, 20), (sx, sy), int(self.radius), width=2)
