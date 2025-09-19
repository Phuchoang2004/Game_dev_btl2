import pygame as pg


class HUDPanel:
    def __init__(self, font: pg.font.Font, center: tuple[int, int]):
        self.font = font
        self.center = center
        self.padding_x = 20
        self.padding_y = 12
        self.spacing = 8

    def set_center(self, center: tuple[int, int]):
        self.center = center

    def draw(self, screen: pg.Surface, score: int, accuracy: float):
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        accuracy_text = self.font.render(f"Accuracy: {accuracy * 100:.2f}%", True, (255, 255, 255))

        hud_width = max(score_text.get_width(), accuracy_text.get_width()) + self.padding_x * 2
        hud_height = score_text.get_height() + self.spacing + accuracy_text.get_height() + self.padding_y * 2

        hud_rect = pg.Rect(0, 0, hud_width, hud_height)
        hud_rect.center = self.center

        hud_surface = pg.Surface((hud_rect.width, hud_rect.height), pg.SRCALPHA)
        hud_surface.fill((0, 0, 0, 120))
        screen.blit(hud_surface, hud_rect.topleft)
        pg.draw.rect(screen, (255, 255, 255), hud_rect, width=2, border_radius=8)

        score_pos = (hud_rect.centerx - score_text.get_width() // 2, hud_rect.top + self.padding_y)
        acc_pos = (
            hud_rect.centerx - accuracy_text.get_width() // 2,
            score_pos[1] + score_text.get_height() + self.spacing,
        )
        screen.blit(score_text, score_pos)
        screen.blit(accuracy_text, acc_pos)