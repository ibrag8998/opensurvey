try:
    # https://github.com/gruns/icecream
    from icecream import ic
except ImportError:  # development packages are not always installed
    ic = print


def is_swagger_fake_view(view):
    return getattr(view, 'swagger_fake_view', False)
