class SliderEvent:
    """Represents a slider key event (increase/decrease)."""

    def __init__(self, key, is_pressed):
        self.key = key
        self.is_pressed = is_pressed
