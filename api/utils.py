class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def dotify(dictionary: dict):
    dictionary = dotdict(dictionary)
    for k, v in dictionary.items():
        if type(v) == dict:
            dictionary[k] = dotify(v)
    return dictionary