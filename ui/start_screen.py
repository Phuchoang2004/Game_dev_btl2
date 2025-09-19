import pygame
from pathlib import Path
from graphics.utils import scale_background_to_screen
from ui.button import Button


def run_start_screen(screen: pygame.Surface, assets_path: Path) -> None:
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(str(assets_path / "fonts" / "Terraria.TTF"), 64)
    font_button = pygame.font.Font(str(assets_path / "fonts" / "Terraria.TTF"), 36)

    bg_img = pygame.image.load(str(assets_path / "sprites" / "bg.png"))
    bg_img, bg_pos = scale_background_to_screen(bg_img, screen)

    # Start button
    title_text = font_title.render("Whack a Zombie", True, (255, 255, 255))
    start_button = Button(
        text="START",
        font=font_button,
        center=(screen.get_width() // 2, screen.get_height() // 2 + 60),
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if start_button.handle_event(event):
                running = False

        # Render
        screen.blit(bg_img, bg_pos)

        # Overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 80))
        screen.blit(overlay, (0, 0))

        # Title
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 40))
        screen.blit(title_text, title_rect)

        # Button
        start_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


