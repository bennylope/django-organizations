"""
nox configuration to systematize release and pre-release tasks

Several nox tasks copied from the pipx project, Copyright (c) 2018 Chad Smith
"""
import os
import subprocess

import nox


NOX_DIR = os.path.abspath(os.path.dirname(__file__))

DEFAULT_INTERPRETER = "3.8"
ALL_INTERPRETERS = (DEFAULT_INTERPRETER,)


def get_path(*names):
    return os.path.join(NOX_DIR, *names)


@nox.session
def clean(session):
    """Removes build artifacts"""
    for rmdir in ["build/", "dist/", "*.egg-info"]:
        session.run("rm", "-rf", rmdir, external=True)


@nox.session(python=DEFAULT_INTERPRETER)
def build(session):
    session.install("setuptools")
    session.install("wheel")
    session.install("docutils")
    session.install("twine")
    clean(session)
    session.run("python", "setup.py", "--quiet", "sdist", "bdist_wheel")


def has_changes():
    status = (
        subprocess.run(
            "git status --porcelain", shell=True, check=True, stdout=subprocess.PIPE
        )
        .stdout.decode()
        .strip()
    )
    return len(status) > 0


def get_branch():
    return (
        subprocess.run(
            "git rev-parse --abbrev-ref HEAD",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
        )
        .stdout.decode()
        .strip()
    )


@nox.session(python=DEFAULT_INTERPRETER)
def publish(session):
    if has_changes():
        session.error("All changes must be committed or removed before publishing")
    branch = get_branch()
    if branch != "master":
        session.error(f"Must be on 'master' branch. Currently on {branch!r} branch")
    build(session)
    session.run("twine", "check", "dist/*")
    print("REMINDER: Has the changelog been updated?")
    session.run("python", "-m", "twine", "upload", "dist/*")