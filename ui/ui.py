import pygame as pg
from pathlib import Path

sprites_path = Path("assets/sprites")
audio_path = Path("assets/audio")
class MuteButton: 
    def __init__(self, x, y):
        self.image = pg.image.load(sprites_path / "sound.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_muted = False

    def toggle(self, event):
        click_pos = pg.mouse.get_pos()
        if not click_pos:
            return
        if not self.rect.collidepoint(click_pos):
            return
        if event.type != pg.MOUSEBUTTONDOWN or event.button != 1:
            return
        self.is_muted = not self.is_muted

        if self.is_muted:
            self.image = pg.image.load(sprites_path / "mute.png").convert_alpha()
            pg.mixer.music.set_volume(0)
        else:
            self.image = pg.image.load(sprites_path / "sound.png").convert_alpha()
            pg.mixer.music.set_volume(0.2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class MouseCursor:
    def __init__(self, mute_button):
        self.image_idle = pg.image.load(sprites_path / "hammer.png").convert_alpha()
        self.image_hit = pg.image.load(sprites_path / "hammer_hit.png").convert_alpha()
        self.image = self.image_idle
        self.offset = (4, 19)

        # animate
        self.hit_frames_total = 10
        self.hit_frames_left = 0

        # hit sound
        self.hit_sound = pg.mixer.Sound(audio_path / "hammer_swing.mp3")

        # mute Button
        self.mute_button = mute_button

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.hit_frames_left = self.hit_frames_total
            if not self.mute_button.is_muted:
                self.hit_sound.play()

    def update(self):
        if self.hit_frames_left > 0:
            self.image = self.image_hit
            self.hit_frames_left -= 1
        else:
            self.image = self.image_idle

    def draw(self, screen):
        mouse_pos = pg.mouse.get_pos()
        screen.blit(self.image, (mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1]))
