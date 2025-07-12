class BacklightAbstract:
    def shine(self):
        raise NotImplementedError(
            "Subclass of the BacklightAbstract must implement on_release()"
        )
