import pygame as pg

#Global button - dung` chung cho de sau nay sang may game khac copy paste la` xong he he
class Button:
    def __init__(
        self,
        text: str,
        font: pg.font.Font,
        center: tuple[int, int],
        padding: tuple[int, int] = (24, 12),
        fill_color=(255, 255, 255),
        text_color=(0, 0, 0),
        border_color=(0, 0, 0),
        border_width: int = 2,
        radius: int = 8,
    ):
        self.text = text
        self.font = font
        self.center = center
        self.padding_x, self.padding_y = padding
        self.fill_color = fill_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.radius = radius

        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.rect = self.text_surface.get_rect()
        self.rect.center = self.center
        self.rect.inflate_ip(self.padding_x * 2, self.padding_y * 2)

    def set_center(self, center: tuple[int, int]):
        self.center = center
        inner_rect = self.text_surface.get_rect(center=center)
        self.rect = inner_rect.inflate(self.padding_x * 2, self.padding_y * 2)

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.fill_color, self.rect, border_radius=self.radius)
        pg.draw.rect(
            screen, self.border_color, self.rect, width=self.border_width, border_radius=self.radius
        )
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def handle_event(self, event) -> bool:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


