import shlex
import subprocess


def run(command):
    return subprocess.run(shlex.split(command))