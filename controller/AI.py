from Physics.physics import Vec2
import random


class SimpleSoccerAI:
    def __init__(
        self,
        dead_zone: float = 48.0,
        avoid_radius: float = 28.0,
        avoid_strength: float = 0.6,
        hold_off_distance: float = 80.0,
        hesitation_prob: float = 0.6,
        wrong_axis_prob: float = 0.5,
        wander_jitter: float = 220.0, #Di chuyển không ổn định
        strafe_prob: float = 0.5, #Di chuyển xoay quanh bóng
        retreat_prob: float = 0.5, #Di chuyển lùi lại
        kick_chance: float = 0.2, #Khả năng sút
    ):
        # Movement nerfs
        self.dead_zone = float(dead_zone)
        self.avoid_radius = float(avoid_radius)
        self.avoid_strength = float(avoid_strength)
        self.hold_off_distance = float(hold_off_distance)
        self.hesitation_prob = float(hesitation_prob)
        self.wrong_axis_prob = float(wrong_axis_prob)
        self.wander_jitter = float(wander_jitter)
        self.strafe_prob = float(strafe_prob)
        self.retreat_prob = float(retreat_prob)
        # Kicking nerf
        self.kick_chance = float(kick_chance)

    def compute_desired_vector(self, player, ball, teammates=None) -> Vec2:
        to_ball = Vec2(ball.pos.x - player.pos.x, ball.pos.y - player.pos.y)
        desired = Vec2(to_ball.x, to_ball.y)

        if teammates is not None:
            r2 = self.avoid_radius * self.avoid_radius
            for mate in teammates:
                if mate is player:
                    continue
                offset = Vec2(player.pos.x - mate.pos.x, player.pos.y - mate.pos.y)
                dist_sq = offset.length_sq()
                if dist_sq == 0.0 or dist_sq > r2:
                    continue
                # Tránh bu lại với cầu thủ gần nhất
                push_dir = offset.normalized()
                # Khoảng cách càng gần thì lực đẩy càng mạnh
                desired.x += push_dir.x * self.avoid_strength * (self.avoid_radius)
                desired.y += push_dir.y * self.avoid_strength * (self.avoid_radius)

        return desired

    def get_keys(self, player, ball, teammates=None) -> dict:
        # Thường xuyên ngừng động tác để làm yếu đáp ứng
        if random.random() < self.hesitation_prob:
            return {"left": False, "right": False, "up": False, "down": False}

        to_ball = Vec2(ball.pos.x - player.pos.x, ball.pos.y - player.pos.y)
        desired = self.compute_desired_vector(player, ball, teammates)

        # Giữ khoảng cách và xoay quanh bóng hoặc lùi lại gần bóng để tránh đột kích trực tiếp
        if to_ball.length() < self.hold_off_distance:
            if random.random() < self.strafe_prob:
                # xoay quanh bóng
                desired = Vec2(-to_ball.y, to_ball.x)
            elif random.random() < self.retreat_prob:
                desired = Vec2(-to_ball.x, -to_ball.y)

        # Thêm rung động ngẫu nhiên để ít chính xác hơn
        desired.x += random.uniform(-1.0, 1.0) * self.wander_jitter
        desired.y += random.uniform(-1.0, 1.0) * self.wander_jitter

        # Di chuyển dọc theo một trục duy nhất, và thường chọn trục xấu hơn
        use_x = abs(desired.x) >= abs(desired.y)
        if random.random() < self.wrong_axis_prob:
            use_x = not use_x

        keys = {"left": False, "right": False, "up": False, "down": False}
        if use_x:
            if desired.x < -self.dead_zone:
                keys["left"] = True
            elif desired.x > self.dead_zone:
                keys["right"] = True
        else:
            if desired.y < -self.dead_zone:
                keys["up"] = True
            elif desired.y > self.dead_zone:
                keys["down"] = True

        return keys

    def should_kick(self, player, ball) -> bool:
        # Giống như Player.attempt_kick nhưng thêm khả năng ngẫu nhiên thấp
        delta = Vec2(ball.pos.x - player.pos.x, ball.pos.y - player.pos.y)
        dist_sq = delta.length_sq()
        max_reach = player.radius + ball.radius + player.kick_extra_range
        in_range = dist_sq <= (max_reach * max_reach)
        return player.kick_timer <= 0.0 and in_range and (random.random() < self.kick_chance)


class AttackingAI(SimpleSoccerAI):
    def __init__(self, attack_pos: tuple[float, float], **kwargs):
        super().__init__(
            dead_zone=kwargs.get("dead_zone", 40.0),
            avoid_radius=kwargs.get("avoid_radius", 28.0),
            avoid_strength=kwargs.get("avoid_strength", 0.6),
            hold_off_distance=kwargs.get("hold_off_distance", 70.0),
            hesitation_prob=kwargs.get("hesitation_prob", 0.45),
            wrong_axis_prob=kwargs.get("wrong_axis_prob", 0.4),
            wander_jitter=kwargs.get("wander_jitter", 180.0),
            strafe_prob=kwargs.get("strafe_prob", 0.45),
            retreat_prob=kwargs.get("retreat_prob", 0.15),
            kick_chance=kwargs.get("kick_chance", 0.35),
        )
        self.attack_pos = Vec2(*attack_pos)

    def compute_desired_vector(self, player, ball, teammates=None) -> Vec2:
        # base: đi theo bóng để tấn công
        to_ball = Vec2(ball.pos.x - player.pos.x, ball.pos.y - player.pos.y)
        desired = Vec2(to_ball.x, to_ball.y)
        # Theo trái bóng để tấn công
        to_goal = Vec2(self.attack_pos.x - player.pos.x, self.attack_pos.y - player.pos.y).normalized()
        desired.x += to_goal.x * 60.0
        desired.y += to_goal.y * 60.0

        if teammates is not None:
            r2 = self.avoid_radius * self.avoid_radius
            for mate in teammates:
                if mate is player:
                    continue
                offset = Vec2(player.pos.x - mate.pos.x, player.pos.y - mate.pos.y)
                dist_sq = offset.length_sq()
                if dist_sq == 0.0 or dist_sq > r2:
                    continue
                push_dir = offset.normalized()
                desired.x += push_dir.x * self.avoid_strength * (self.avoid_radius)
                desired.y += push_dir.y * self.avoid_strength * (self.avoid_radius)

        return desired


class DefensiveAI(SimpleSoccerAI):
    def __init__(self, defend_pos: tuple[float, float], **kwargs):
        super().__init__(
            dead_zone=kwargs.get("dead_zone", 56.0),
            avoid_radius=kwargs.get("avoid_radius", 34.0),
            avoid_strength=kwargs.get("avoid_strength", 0.7),
            hold_off_distance=kwargs.get("hold_off_distance", 120.0),
            hesitation_prob=kwargs.get("hesitation_prob", 0.75),
            wrong_axis_prob=kwargs.get("wrong_axis_prob", 0.7),
            wander_jitter=kwargs.get("wander_jitter", 220.0),
            strafe_prob=kwargs.get("strafe_prob", 0.55),
            retreat_prob=kwargs.get("retreat_prob", 0.5),
            kick_chance=kwargs.get("kick_chance", 0.12),
        )
        self.defend_pos = Vec2(*defend_pos)
        self.defend_zone = kwargs.get("defend_zone", 160.0)

    def compute_desired_vector(self, player, ball, teammates=None) -> Vec2:
        # Phòng thủ chính
        to_ball = Vec2(ball.pos.x - player.pos.x, ball.pos.y - player.pos.y)
        to_def = Vec2(self.defend_pos.x - player.pos.x, self.defend_pos.y - player.pos.y)

        # Nếu bóng gần vị trí phòng thủ chính, thì ưu tiên đi theo bóng, nếu không thì ưu tiên đi theo vị trí phòng thủ chính
        ball_to_def = Vec2(ball.pos.x - self.defend_pos.x, ball.pos.y - self.defend_pos.y)
        if ball_to_def.length() < self.defend_zone:
            desired = Vec2(to_ball.x * 0.9 + to_def.x * 0.4, to_ball.y * 0.9 + to_def.y * 0.4)
        else:
            desired = Vec2(to_ball.x * 0.3 + to_def.x * 1.2, to_ball.y * 0.3 + to_def.y * 1.2)

        if teammates is not None:
            r2 = self.avoid_radius * self.avoid_radius
            for mate in teammates:
                if mate is player:
                    continue
                offset = Vec2(player.pos.x - mate.pos.x, player.pos.y - mate.pos.y)
                dist_sq = offset.length_sq()
                if dist_sq == 0.0 or dist_sq > r2:
                    continue
                push_dir = offset.normalized()
                desired.x += push_dir.x * self.avoid_strength * (self.avoid_radius)
                desired.y += push_dir.y * self.avoid_strength * (self.avoid_radius)

        return desired


