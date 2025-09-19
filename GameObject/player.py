from Physics.physics import Vec2, integrate_velocity, clamp_to_rect
import pygame as pg

class Player:
    def __init__(self, start_pos: tuple[float, float], color: tuple[int, int, int] = (40, 120, 255)):
        self.pos = Vec2(*start_pos)
        self.vel = Vec2(0.0, 0.0)
        self.acc = Vec2(0.0, 0.0)
        self.facing = Vec2(1.0, 0.0)

        self.radius = 16.0
        self.color = color

        self.max_speed = 280.0
        self.accel = 1200.0
        self.linear_damping = 4.0  

    def update(self, dt: float, keys, bounds_rect: tuple[float, float, float, float]):
        move_x = 0.0
        move_y = 0.0
        if keys is not None:
            if keys.get("left") or keys.get("a"):
                move_x -= 1.0
            if keys.get("right") or keys.get("d"):
                move_x += 1.0
            if keys.get("up") or keys.get("w"):
                move_y -= 1.0
            if keys.get("down") or keys.get("s"):
                move_y += 1.0

        move = Vec2(move_x, move_y).normalized()
        self.acc = move * self.accel

        new_pos, new_vel = integrate_velocity(self.pos, self.vel, self.acc, dt, self.linear_damping)
        
        if new_vel.length() > self.max_speed:
            new_vel = new_vel.clamp_length(self.max_speed)

        new_pos, new_vel = clamp_to_rect(new_pos, new_vel, bounds_rect, self.radius, restitution=0.0)

        self.pos = new_pos
        self.vel = new_vel

        if self.vel.length_sq() > 1e-3:
            vnorm = self.vel.normalized()
            self.facing = vnorm

    def draw(self, surface, world_to_screen_fn, camera):
        sx, sy = world_to_screen_fn(self.pos.x, self.pos.y, 0.0, camera)
        pg.draw.circle(surface, (0, 0, 0, 40), (sx, sy), int(self.radius * 1.05))
        pg.draw.circle(surface, self.color, (sx, sy), int(self.radius))
