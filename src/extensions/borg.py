class Borg:
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        instance = super(Borg, cls).__new__(cls, *args, **kwargs)
        instance.__dict__ = cls._shared_state

        return instance
