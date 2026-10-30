import time

from constants import FRAME_TIME

class FrameLimiter:
    def __init__(self):
        self.frame_times = []
        self.next_frame = time.perf_counter() + FRAME_TIME

    def limit_fps(self):
        remaining = self.next_frame - time.perf_counter() - 0.0005
        
        if remaining > 0.001:
            time.sleep(remaining)
        
        while time.perf_counter() < self.next_frame:
            pass

        self.next_frame = time.perf_counter() + FRAME_TIME

    def tick(self):
        now = time.perf_counter()
        self.frame_times.append(now)

        for frame in self.frame_times.copy():
            if now - frame >= 1:
                self.frame_times.remove(frame)

    def get_fps(self):
        return len(self.frame_times)