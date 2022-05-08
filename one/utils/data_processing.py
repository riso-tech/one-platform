import functools


def getattr_in_chain(obj, attr, *args):
    def _getattr(obj, attr):  # noqa
        try:
            return getattr(obj, attr, *args)
        except AttributeError:
            pass

    return functools.reduce(_getattr, [obj] + attr.split("."))
