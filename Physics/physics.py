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
        # Độ dài vector |v| = sqrt(x^2 + y^2)
        return math.hypot(self.x, self.y)

    def length_sq(self) -> float:
        # Bình phương độ dài |v|^2 = x^2 + y^2 (tránh sqrt khi chỉ cần so sánh)
        return self.x * self.x + self.y * self.y

    def normalized(self):
        # Chuẩn hoá: v_hat = v / |v|
        l = self.length()
        if l == 0:
            return Vec2(0, 0)
        return self / l

    def clamp_length(self, max_length: float):
        # Giới hạn độ dài: nếu |v| > max thì co lại theo tỉ lệ max/|v|
        l = self.length()
        if l <= max_length or l == 0:
            return Vec2(self.x, self.y)
        return self * (max_length / l)

    def angle(self) -> float:
        """Return angle (in degrees) of vector relative to +x axis."""
        # Góc của vector so với trục +x: angle = atan2(y, x) (đổi sang độ)
        return math.degrees(math.atan2(self.y, self.x))


def integrate_velocity(position: Vec2, velocity: Vec2, acceleration: Vec2, dt: float,
                       linear_damping: float = 0.0) -> tuple[Vec2, Vec2]:
    # Tích phân Euler:
    #   v(t+dt) = v(t) + a * dt
    #   x(t+dt) = x(t) + v(t+dt) * dt
    # Giảm chấn tuyến tính: v *= (1 - c*dt)
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
    # Va chạm đàn hồi đơn giản giữa 2 hình tròn (giả sử khối lượng đều = 1)
    delta = p2 - p1
    dist_sq = delta.length_sq()
    radii = r1 + r2
    if dist_sq == 0:
        # Trường hợp trùng tâm: chọn pháp tuyến bất kỳ và coi như chồng lấn tối đa
        n = Vec2(1.0, 0.0)
        penetration = radii
    else:
        dist = math.sqrt(dist_sq)
        if dist >= radii:
            # Không giao nhau => không có va chạm
            return p1, v1, p2, v2
        n = delta / dist
        penetration = radii - dist

    # Sửa xuyên: tách mỗi tâm ra 1/2 độ xuyên theo pháp tuyến n
    correction = n * (penetration / 2.0)
    p1 = Vec2(p1.x - correction.x, p1.y - correction.y)
    p2 = Vec2(p2.x + correction.x, p2.y + correction.y)

    # Vận tốc tương đối theo pháp tuyến: rv · n
    rv = v2 - v1
    vel_along_normal = rv.x * n.x + rv.y * n.y
    if vel_along_normal > 0:
        # Đang tách rời nhau, không cần phản xung
        return p1, v1, p2, v2

    # Biên độ xung (impulse scalar):
    #   j = -(1 + e) * (rv · n) / (1/m1 + 1/m2)
    # Với m1 = m2 = 1  => j /= 2
    j = -(1 + restitution) * vel_along_normal
    j /= 2.0  
    impulse = n * j
    # Áp xung theo hướng n, cập nhật vận tốc
    v1 = Vec2(v1.x - impulse.x, v1.y - impulse.y)
    v2 = Vec2(v2.x + impulse.x, v2.y + impulse.y)
    return p1, v1, p2, v2


def clamp_to_rect(position: Vec2, velocity: Vec2, rect: tuple[float, float, float, float],
                  radius: float, restitution: float = 0.4) -> tuple[Vec2, Vec2]:
    left, top, right, bottom = rect
    p = position.copy()
    v = velocity.copy()

    # Chặn biên trục X: phản xạ vận tốc theo hệ số nảy (restitution)
    if p.x - radius < left:
        p.x = left + radius
        if v.x < 0:
            v.x = -v.x * restitution
    elif p.x + radius > right:
        p.x = right - radius
        if v.x > 0:
            v.x = -v.x * restitution

    # Chặn biên trục Y: tương tự trục X
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
    # Chuyển động 1D theo trục thẳng đứng:
    #   vz(t+dt) = vz(t) + g * dt  (g âm nếu kéo xuống)
    #   z(t+dt)  = z(t)  + vz(t+dt) * dt
    # Giảm chấn không khí: vz *= (1 - c*dt)
    # Va chạm mặt đất: khi z <= 0 => bật lại: vz = -vz * e
    # Ngưỡng nhỏ: nếu |vz| < 10 coi như dừng
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
