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
- For Developer:
```bash
 git clone https://github.com/StrayDragon/dragon-cli.git
 cd dragon-cli
  # Python3.7 required, If your pip link this version, 
  # you can run 'pip install --editable .' directly. 
 python3.7 -m pip install --editable . 
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
