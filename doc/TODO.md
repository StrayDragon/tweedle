# TODO
- [x] To remove the `utils.log()` and replace old one to [`click.secho()`](https://click.palletsprojects.com/en/7.x/api/?highlight=secho#click.secho)

- [x] bumpversion
- [x] pre-commit githook:precommit
- [x] tox
- [x] customize flask, mypy, yapf
- [ ] organize messy debug, build(CI), test, formatter, linter, etc configs and strip deps which not need
  - known:
    - tox
    - flask8
    - pytest
    - TravisCI
    - mypy
    - pyright
    - yapf
    - vimspector
    - coc-settings
    - precommit config -> git-hook
    - bumpversion config
    - gitignore
    - poetry config
# TODO Refactor table
| priority | keyword | occurrence location | problem | defect (hidden danger) | reconstruction means | reconstruction may bring improvement | current status | last update date |
|---|---|--- |---|---|---|---|---|---|
| Low  | assert | test file | assertion directly detect stdout output field test file is in line with expectations | hard-coded, difficult to centrally manage output | | | Click Framework Error Output has been organizing | ` 2019-02-15 21:42:48 ` |
