import time

class Contactor:
    def __init__(self) -> None:
        self.fb_delay: int = 1000  # Feedback delay in milliseconds
        self.rising_mark: float | None = None  # Rising edge appearance time mark initialization
        self.coil: bool = False
        self.previous_coil: bool = False
        self.fb_contact: bool = False
        self.rising: bool = False

    def get_fb_status(self) -> bool:
        return self.fb_contact

    def process(self) -> dict[str, bool]:
        current_time = time.monotonic()
        if self.coil and not self.previous_coil:
            self.rising_mark = current_time
            self.rising = True

        if self.coil and self.rising:
            if (current_time - self.rising_mark) * 1000 >= self.fb_delay:
                self.fb_contact = True

        if not self.coil:
            self.rising = False
            self.fb_contact = False

        self.previous_coil = self.coil
        return {'fb_status': self.fb_contact}
    
