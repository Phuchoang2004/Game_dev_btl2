import pygame as pg
from ui.button import Button


class GameOverOverlay:
    def __init__(self, font_title: pg.font.Font, font_body: pg.font.Font):
        self.font_title = font_title
        self.font_body = font_body
        self._restart_button: Button | None = None

    # Render
    def draw(self, screen: pg.Surface, score: int, accuracy: float) -> pg.Rect:
        # Overlay
        overlay = pg.Surface(screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        # Title
        title_text = self.font_title.render("GAME OVER", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 40))
        screen.blit(title_text, title_rect)

        # HUD score and acc
        summary_text = self.font_body.render(f"Score: {score}  |  Accuracy: {accuracy * 100:.2f}%", True, (255, 255, 255))
        summary_rect = summary_text.get_rect(center=(screen.get_width() // 2, title_rect.bottom + 20))
        screen.blit(summary_text, summary_rect)

        # Restart button
        if self._restart_button is None:
            self._restart_button = Button(
                text="RESTART",
                font=self.font_body,
                center=(screen.get_width() // 2, summary_rect.bottom + 50),
            )
        else:
            self._restart_button.set_center((screen.get_width() // 2, summary_rect.bottom + 50))

        self._restart_button.draw(screen)
        return self._restart_button.rect

    # Event
    def handle_event(self, event) -> bool:
        if self._restart_button is None:
            return False
        return self._restart_button.handle_event(event)


