# <p align="center"> Dragon-Cli </p>
[![Build Status](https://travis-ci.org/StrayDragon/dragon-cli.svg?branch=master)](https://travis-ci.org/StrayDragon/dragon-cli)
- Commands manager and controller.
- Help you complete a series of commands from other terminal applications.
---

# **WARNING**: 
:warning: Now, **DON'T USE** this tool in important workspace directories, because:
- This project is still in the **development** some usages may change in the future.
- It has some **destructive** and **unrecoverable** operations.

# Install (Dev)
For Developer:
- At first, you need to install [poetry](https://poetry.eustace.io/)
- Then, you can fork or just clone my repo to modify something:
```bash
git clone https://github.com/StrayDragon/dragon-cli.git # master repo
#git clone https://github.com/<YOUR_GITHUB_NAME>/dragon-cli.git  # fork repo

cd dragon-cli
poetry install
poetry run python dragon.py
```
- For User:
 *Coming soon*
# Usages:
## Overall
  |`CMD`|`SUBCMD`|`ACTION`|`OPTIONS`| `BASEDCMD` |
  |---|---|---|---|---|
  |`dragon`| `blog` | `publish` | | `hexo`,`git` |
  |  |  | `update`|  | `git` | 
  |`dragon`| `project` | `new` | `--lang`<br> `--build-tool`<br> `--third-party`|  |
