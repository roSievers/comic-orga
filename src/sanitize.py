
def sanitize(fn):
    def inner(*args, **aargs):
        # TODO: Actually sanitize the data
        return fn(*args, **aargs)
    return inner
