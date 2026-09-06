"""
Gitea API client.

The public names are imported from the submodules lazily on first access
to keep the startup of osc and git-obs fast.
"""


# name -> submodule that defines it
_LAZY_ATTRS = {
    "Connection": "connection",
    "dt_sanitize": "common",
    "edit_message": "common",
    "BranchDoesNotExist": "exceptions",
    "BranchExists": "exceptions",
    "ForkExists": "exceptions",
    "GiteaException": "exceptions",
    "GitObsRuntimeError": "exceptions",
    "RepoExists": "exceptions",
    "UserDoesNotExist": "exceptions",
    "response_to_exception": "exceptions",
    "Branch": "branch",
    "Config": "conf",
    "Login": "conf",
    "Fork": "fork",
    "Git": "git",
    "GitDiffGenerator": "git_diff_generator",
    "Issue": "issue",
    "IssueTimelineEntry": "issue_timeline_entry",
    "json_dumps": "json",
    "Maintainership": "maintainership",
    "PullRequest": "pr",
    "PullRequestReview": "pr_review",
    "Repo": "repo",
    "SSHKey": "ssh_key",
    "StagingPullRequestWrapper": "staging",
    "TarDiff": "tardiff",
    "User": "user",
}

__all__ = tuple(_LAZY_ATTRS)


def __getattr__(name):
    try:
        module_name = _LAZY_ATTRS[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None

    import importlib  # pylint: disable=import-outside-toplevel

    value = getattr(importlib.import_module(f".{module_name}", __name__), name)
    # cache the value so the lookup doesn't go through __getattr__ again
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(_LAZY_ATTRS))
