# Command and SubCommands Specific
> [pN] N is 0~9 show the priority of this items, lower is high response to program

## Basic Command

### [p5] `config` self management

### [p9] `plugin` self-plugin management


## External Configs-related SubCommands
### [p0] `spawn`
#### Breif
copy from default or user define configs to current workspace

#### Description
usually for some "project/workspace-like" concept situations, it will yield some configs which are not easy to self-management, further more, like Jetbrains(.idea), VSCode(.vscode), even poetry or pipenv lock files are self-management, but like (.clang-format) or Pyright/Coc.nvim/Poetry/... Local configs are not, this subcommands will support easy way to define these configs rather than find examples config on Internet.

#### Example
maybe use it looks like:

```bash
$ # `td` is alias of `tweedle`
$ ls -a
. ..
$ td spawn -i # interact mode
[tweedle] Which project type [default]: python
[tweedle] List configs of `python`
[tweedle] 1. poetry.toml  2.pyrightconfig.json
[tweedle] Select [All]:<CR>
[tweedle] Done
$ ls -a
. .. pyrightconfig.json poetry.toml
```


# Configurations

## Basic Config

### Goal
- [ ] Change default behavior, give user an easy way to change them
