import pygame as pg


class CountdownTimer:
    def __init__(self, duration_ms: int):
        self.duration_ms = duration_ms
        self.reset()

    def reset(self):
        self.start_ms = pg.time.get_ticks()
        self.finished = False

    def time_left_ms(self) -> int:
        if self.finished:
            return 0
        now = pg.time.get_ticks()
        left = max(0, self.duration_ms - (now - self.start_ms))
        if left == 0:
            self.finished = True
        return left

    def format_mmss(self) -> str:
        seconds_left = self.time_left_ms() // 1000
        minutes = seconds_left // 60
        seconds = seconds_left % 60
        return f"{minutes:02d}:{seconds:02d}"


