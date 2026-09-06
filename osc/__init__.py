__all__ = [
    'babysitter',
    'build',
    'connection',
    'commandline',
    'core',
    'fetch',
    'grabber',
    'meter',
    'oscerr',
    'oscssl',
]


def __getattr__(name):
    # compute __version__ lazily on first use to avoid running 'git describe' on every import
    if name == "__version__":
        from .util import git_version
        version = git_version.get_version('1.27.3')
        globals()["__version__"] = version
        return version
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# vim: sw=4 et
