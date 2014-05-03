def set_defaults(d, defaults):
    if d is None:
        d = {}

    for key, value in defaults.items():
        d.setdefault(key, value)

    return d
