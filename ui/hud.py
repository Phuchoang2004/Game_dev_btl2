import pygame as pg


class HUDPanel:
    def __init__(self, font_score, font_timer, center=(0,0)):
        self.font_score = font_score
        self.font_timer = font_timer
        self.center = center
        self.padding_x = 16
        self.padding_y = 8
        self.spacing = 2

    def set_center(self, center: tuple[int, int]):
        self.center = center

    def draw(self, screen: pg.Surface, score_left: int, score_right: int, time_str: str):
        score_text = self.font_score.render(f"{score_left} - {score_right}", True, (255,255,255))
        time_text = self.font_timer.render(time_str, True, (255,255,255))

        # box đủ rộng cho cả score + time
        hud_width = max(score_text.get_width(), time_text.get_width()) + self.padding_x * 2
        hud_height = score_text.get_height() + self.spacing + time_text.get_height() + self.padding_y * 2

        hud_rect = pg.Rect(0, 0, hud_width, hud_height)
        hud_rect.center = self.center

        hud_surface = pg.Surface((hud_rect.width, hud_rect.height), pg.SRCALPHA)
        hud_surface.fill((0, 0, 0, 120))
        screen.blit(hud_surface, hud_rect.topleft)
        pg.draw.rect(screen, (255, 255, 255), hud_rect, width=2, border_radius=8)

        # Vẽ time ở trên
        time_pos = (hud_rect.centerx - time_text.get_width() // 2, hud_rect.top + self.padding_y)
        screen.blit(time_text, time_pos)

        # Vẽ score bên dưới
        score_pos = (
            hud_rect.centerx - score_text.get_width() // 2,
            time_pos[1] + time_text.get_height() + self.spacing,
        )
        screen.blit(score_text, score_pos)