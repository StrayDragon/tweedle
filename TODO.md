# Commands table

|`CMD`|`SUBCMD`|`ACTION`|`OPTIONS`|`USAGE`|
|---|---|---|---|---|
|`dragon`| `blog` | `publish` | |==`deprecated`==|
| |  | `update` | |==`deprecated`==|
|`dragon`| `project` | `new` | `--lang`<br>`--build-tools`<br>`--third-parties` |==`deprecated`==|
|`dragon`| `bundle` |  | `--new`<br>`--load`<br>`--list`<br>`--delete`<br>`--show`<br> ||
| |  |  | ||
| |  |  | ||
| |  |  | ||
| |  |  | ||


# Requirement

| Minimum version |                           Features                           |
| :-------------: | :----------------------------------------------------------: |
|       3.7       | `subprocess.run(...)` : `capture_output`  parameter support. |



# Refactor table
| priority | keyword | occurrence location | problem | defect (hidden danger) | reconstruction means | reconstruction may bring improvement | current status | last update date |
|---|---|--- |---|---|---|---|---|---|
| Low  | assert | test file | assertion directly detect stdout output field test file is in line with expectations | hard-coded, difficult to centrally manage output | | | Click Framework Error Output has been organizing | ` 2019-02-15 21:42:48 ` |

