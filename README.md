# <p align="center"> :snake:Tweedle </p>

[![Build Status](https://travis-ci.org/StrayDragon/tweedle.svg?branch=master)](https://travis-ci.org/StrayDragon/tweedle)
[![GitHub last commit](https://img.shields.io/github/last-commit/straydragon/tweedle)](https://github.com/StrayDragon/tweedle/commits)
[![PyPI](https://img.shields.io/pypi/v/tweedle)](https://pypi.org/project/tweedle)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tweedle)](https://pypi.org/project/tweedle)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/tweedle)](https://pypi.org/project/tweedle)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/w/straydragon/tweedle)](https://github.com/StrayDragon/tweedle/commits)
[![PyPI - License](https://img.shields.io/pypi/l/tweedle)](https://github.com/StrayDragon/tweedle/blob/master/LICENSE)

<!--TODO:Add more icons see https://shields.io-->

Features:

- Configs manager and controller
- Project configs helper
<!-- - Commands manager and controller -->

---

# **WARNING**:

:warning: Now, **DON'T USE** this tool in important workspace directories, because:

- This project is still in the **development**, and some usages may change in the future.
- It has some **destructive** and **unrecoverable** operations.

# Install

## For Developer:

0. Checkout [issues](https://github.com/StrayDragon/tweedle/issues) and this repo [project](https://github.com/StrayDragon/tweedle/projects/1?fullscreen=true) plan, search for what you are interested in or give me suggestions
1. At first, you need to install [poetry](https://poetry.eustace.io/)
2. You can fork or just clone my repo to modify something locally:

```bash
git clone https://github.com/StrayDragon/tweedle.git # master repo

cd tweedle
poetry install
poetry shell

# unit test
pytest
```

3. if you want to contribute to this project, please make your fork and install hooks to your local git repo by using [pre-commit](https://pre-commit.com/) like these:

```bash
pre-commit run --all-files -v
pre-commit install
```

4. Now, programming with pleasure and fun :)

## For User:

_Coming soon_

# Usages:

```
Usage: tweedle [OPTIONS] COMMAND [ARGS]...

  Welcome to use tweedle, enjoy it and be efficient :P

  Please use "tweedle COMMAND --help" to get more detail of usages

Options:
  --version  show version details
  --help     show usages details

Commands:
  manage   manage to backup or recovery app configs and user data
  project  control your project workspace
```

# Dev Features Preview:

## Manage your dotfiles based by git

![](https://s1.ax1x.com/2020/04/02/GYFdQx.gif)

## Control your project by spawning specific configs

![](https://s1.ax1x.com/2020/04/02/GYFYFJ.gif)

> if your want to try it now, use [pipx](https://github.com/pipxproject/pipx) to install it and DO NOT RUN COMMANDS IN YOUR REAL WORKING SPACE
>
> `pipx install 'git+https://github.com/StrayDragon/tweedle.git@feat/subcmd_project_spawn_dev_configs'`
