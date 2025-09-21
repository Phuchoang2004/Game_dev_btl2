import math


class Vec2:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = float(x)
        self.y = float(y)

    def copy(self):
        return Vec2(self.x, self.y)

    def __add__(self, other: "Vec2"):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2"):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        return Vec2(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    def __truediv__(self, scalar: float):
        if scalar == 0:
            return Vec2(self.x, self.y)
        return Vec2(self.x / scalar, self.y / scalar)

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def length_sq(self) -> float:
        return self.x * self.x + self.y * self.y

    def normalized(self):
        l = self.length()
        if l == 0:
            return Vec2(0, 0)
        return self / l

    def clamp_length(self, max_length: float):
        l = self.length()
        if l <= max_length or l == 0:
            return Vec2(self.x, self.y)
        return self * (max_length / l)

    def angle(self) -> float:
        """Return angle (in degrees) of vector relative to +x axis."""
        return math.degrees(math.atan2(self.y, self.x))


def integrate_velocity(position: Vec2, velocity: Vec2, acceleration: Vec2, dt: float,
                       linear_damping: float = 0.0) -> tuple[Vec2, Vec2]:
    new_velocity = Vec2(
        velocity.x + acceleration.x * dt,
        velocity.y + acceleration.y * dt,
    )
    if linear_damping != 0.0:
        new_velocity.x *= max(0.0, 1.0 - linear_damping * dt)
        new_velocity.y *= max(0.0, 1.0 - linear_damping * dt)
    new_position = Vec2(
        position.x + new_velocity.x * dt,
        position.y + new_velocity.y * dt,
    )
    return new_position, new_velocity


def resolve_circle_vs_circle(p1: Vec2, r1: float, v1: Vec2, p2: Vec2, r2: float, v2: Vec2,
                             restitution: float = 0.2) -> tuple[Vec2, Vec2, Vec2, Vec2]:
    delta = p2 - p1
    dist_sq = delta.length_sq()
    radii = r1 + r2
    if dist_sq == 0:
        n = Vec2(1.0, 0.0)
        penetration = radii
    else:
        dist = math.sqrt(dist_sq)
        if dist >= radii:
            return p1, v1, p2, v2
        n = delta / dist
        penetration = radii - dist

    correction = n * (penetration / 2.0)
    p1 = Vec2(p1.x - correction.x, p1.y - correction.y)
    p2 = Vec2(p2.x + correction.x, p2.y + correction.y)

    rv = v2 - v1
    vel_along_normal = rv.x * n.x + rv.y * n.y
    if vel_along_normal > 0:
        return p1, v1, p2, v2

    j = -(1 + restitution) * vel_along_normal
    j /= 2.0  
    impulse = n * j
    v1 = Vec2(v1.x - impulse.x, v1.y - impulse.y)
    v2 = Vec2(v2.x + impulse.x, v2.y + impulse.y)
    return p1, v1, p2, v2


def clamp_to_rect(position: Vec2, velocity: Vec2, rect: tuple[float, float, float, float],
                  radius: float, restitution: float = 0.4) -> tuple[Vec2, Vec2]:
    left, top, right, bottom = rect
    p = position.copy()
    v = velocity.copy()

    if p.x - radius < left:
        p.x = left + radius
        if v.x < 0:
            v.x = -v.x * restitution
    elif p.x + radius > right:
        p.x = right - radius
        if v.x > 0:
            v.x = -v.x * restitution

    if p.y - radius < top:
        p.y = top + radius
        if v.y < 0:
            v.y = -v.y * restitution
    elif p.y + radius > bottom:
        p.y = bottom - radius
        if v.y > 0:
            v.y = -v.y * restitution

    return p, v


def integrate_height(z: float, vz: float, gravity: float, dt: float,
                     restitution: float = 0.55, air_damping: float = 0.0) -> tuple[float, float]:
    if z > 0.0 or vz > 0.0:
        vz += gravity * dt
        if air_damping != 0.0:
            vz *= max(0.0, 1.0 - air_damping * dt)
        z += vz * dt
        if z <= 0.0:
            z = 0.0
            vz = -vz * restitution
            if abs(vz) < 10.0:
                vz = 0.0
    return z, vz
