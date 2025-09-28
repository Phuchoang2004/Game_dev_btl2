import pygame
from pathlib import Path
from ui.button import Button

def scale_background_to_screen(bg_img: pygame.Surface, screen: pygame.Surface):
    screen_width, screen_height = screen.get_size()
    bg_width, bg_height = bg_img.get_size()
    scale = max(screen_width / bg_width, screen_height / bg_height)
    new_size = (int(bg_width * scale), int(bg_height * scale))
    bg_img = pygame.transform.smoothscale(bg_img, new_size)
    bg_offset_x = (new_size[0] - screen_width) // 2
    bg_offset_y = (new_size[1] - screen_height) // 2
    return bg_img, (-bg_offset_x, -bg_offset_y)

def render_wrapped_text(text, font, color, max_width, screen, start_y, line_spacing=10):
    """
    Render text tự động xuống dòng khi vượt quá max_width.
    """
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())

    # Vẽ từng dòng ra màn hình
    y = start_y
    for line in lines:
        surface = font.render(line, True, color)
        rect = surface.get_rect(center=(screen.get_width() // 2, y))
        screen.blit(surface, rect)
        y += surface.get_height() + line_spacing

    return y
def run_start_screen(screen: pygame.Surface, assets_path: Path) -> None:
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(str(assets_path / "fonts" / "Retroville NC.TTF"), 64)
    font_button = pygame.font.Font(str(assets_path / "fonts" / "Retroville NC.TTF"), 36)
    font_tut = pygame.font.Font(str(assets_path / "fonts" / "Retroville NC.TTF"), 24)

    tutorial_lines = [
        "Player 1: WASD to move, SPACE to kick, Q to switch player",
        "Player 2: Arrows to move, Right CTRL/SHIFT to kick, P to switch player",
        "Match lasts 1 minute. Good luck!"
    ]

    bg_img = pygame.image.load(str(assets_path / "sprites" / "field.png"))
    bg_img, bg_pos = scale_background_to_screen(bg_img, screen)

    # Buttons
    title_text = font_title.render("Tiny Football", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 100))

    start_button = Button("START", font_button, (screen.get_width()//2, title_rect.bottom + 60))
    tutorial_button = Button("TUTORIAL", font_button, (screen.get_width()//2, start_button.rect.bottom + 60))
    back_button = Button("BACK", font_button, (screen.get_width()//2, screen.get_height() - 80))

    state = "menu"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if state == "menu":
                if start_button.handle_event(event):
                    running = False  # thoát start screen → vào game
                elif tutorial_button.handle_event(event):
                    state = "tutorial"

            elif state == "tutorial":
                if back_button.handle_event(event):
                    state = "menu"

        # Render
        screen.blit(bg_img, bg_pos)
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 80))
        screen.blit(overlay, (0, 0))

        if state == "menu":
            screen.blit(title_text, title_rect)
            start_button.draw(screen)
            tutorial_button.draw(screen)

        elif state == "tutorial":
            y = screen.get_height() // 2 - 80
            for text in tutorial_lines:
                y = render_wrapped_text(text, font_tut, (255, 255, 255),
                                        max_width=screen.get_width() - 100,
                                        screen=screen, start_y=y, line_spacing=10)
            back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)