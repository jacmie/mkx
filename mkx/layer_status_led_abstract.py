class LayerStatusLedAbstract:
    def update_status_led(self, layer: int):
        raise NotImplementedError(
            "Subclass of the LayerStatusLedAbstract must implement update_status_led()"
        )
