'''
A dict class with dot accessors.

Author: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
'''
class DotDict(dict):
    """
    A dict class with dot accessors.

    Example:
    m = DotDict({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(DotDict, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(DotDict, self).__delitem__(key)
        del self.__dict__[key]