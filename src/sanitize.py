
def sanitize(*args, **aargs):
    def outer(fn):
        def inner(*args, **aargs):
            # TODO: Actually sanitize the data
            return fn(*args, **aargs)
        return inner
    return outer

def maybe(type):
    return type

def mapping(key_type, value_type):
    return value_type
