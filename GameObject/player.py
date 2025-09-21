from Physics.physics import Vec2, integrate_velocity, clamp_to_rect
import pygame as pg


scale = 2.0
def load_and_scale(path, count):
    frames = []
    for i in range(count):
        img = pg.image.load(path.format(i)).convert_alpha()
        w, h = img.get_size()
        img = pg.transform.scale(img, (int(w * scale), int(h * scale)))
        frames.append(img)
    return frames


class Player:
    def __init__(self, start_pos: tuple[float, float], color: tuple[int, int, int] = (40, 120, 255), sprite_path: str = "./assets/sprites/player1/"):
        self.pos = Vec2(*start_pos)
        self.vel = Vec2(0.0, 0.0)
        self.acc = Vec2(0.0, 0.0)
        self.facing = Vec2(1.0, 0.0)

        self.radius = 16.0
        self.color = color

        self.max_speed = 280.0
        self.accel = 1200.0
        self.linear_damping = 4.0  

        # sprites includes, walk up, down, right(left is flipped)
        self.sprites = {
            "down": load_and_scale(f"{sprite_path}/front/tile00{{}}.png", 4),
            "up": load_and_scale(f"{sprite_path}/back/tile00{{}}.png", 4),
            "right": load_and_scale(f"{sprite_path}/walk/tile00{{}}.png", 4),
        }

        # Animation state
        self.current_anim = "right"  # which animation (up/down/right/left)
        self.anim_index = 0  # which frame in the list
        self.anim_timer = 0.0  # time accumulator
        self.anim_speed = 0.12  # seconds per frame (tweak for faster/slower walk)

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

        if self.vel.length_sq() > 1:  # moving
            # pick animation set based on facing direction
            if abs(self.facing.x) > abs(self.facing.y):
                if self.facing.x > 0:
                    self.current_anim = "right"
                else:
                    self.current_anim = "right"  # reuse right & flip when drawing
            else:
                if self.facing.y > 0:
                    self.current_anim = "down"
                else:
                    self.current_anim = "up"

            # advance animation timer
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0.0
                self.anim_index = (self.anim_index + 1) % len(
                    self.sprites[self.current_anim]
                )
        else:
            # idle: reset to first frame
            self.anim_index = 0

    def draw(self, surface, world_to_screen_fn, camera):
        sx, sy = world_to_screen_fn(self.pos.x, self.pos.y, 0.0, camera)

        # pick frame
        frame = self.sprites[self.current_anim][self.anim_index]

        # flip for left movement
        if self.current_anim == "right" and self.facing.x < 0:
            frame = pg.transform.flip(frame, True, False)

        rect = frame.get_rect(center=(sx, sy))

        # draw shadow
        # pg.draw.circle(surface, (0, 0, 0, 40), (sx, sy), int(self.radius * 1.05))

        # draw sprite
        surface.blit(frame, rect)
