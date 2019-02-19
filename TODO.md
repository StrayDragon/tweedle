# **TODO**:

## Python Version

- Python 3.7+ (Current)

### Required

| Minimum version |                           Features                           |
| :-------------: | :----------------------------------------------------------: |
|       3.7       | `subprocess.run(...)` : `capture_output`  parameter support. |


## Functional Requirements 

`dragon-cli` can abbreviate to `dg`
- I want to user can use command follow order by:
  - `dg SUBCMD [ACTION] [OPTIONS]`

- [x] It can help the user to complete a set of operations with a more concise set of commands

  - Examples:
    - Use `$ dg blog publish ` to excute `hexo clean ; hexo g -d; hexo clean `
    - Use `$ dg blog finish` to excute  `git add -A;git commit -m 'update blog';git push`
    - ...

- [ ] It can help the users to create a new project from the organized templates

  - Examples:

    - Use `$ dg project new --lang cpp --build-tools cmake --third-parties googletest`

      - Then it generate a project structure like:

        ```bash
        .
        ├── CMakeLists.txt
        ├── include
        │   └── googletest
        ├── src
        │   └── main.cpp
        └── test
            └── test_main.cpp
        ```

- Like this table:

  |`CMD`|`SUBCMD`|`ACTION`|`OPTIONS`|
  |---|---|---|---|
  |`dg`| `blog` | `publish` | |
  ||  | `update` | |
  |`dg`| `project` | `new` | `--lang`<br> `--build-tools`<br> `--third-parties`|
  |`dg`| `bundle` | `new` | |
  || `export` | `shell` | |

  

## An index
```
NOT FINISH

# Install and Quickstart

# SubCommands (Submode)

```

## Refactor table
| priority | keyword | occurrence location | problem | defect (hidden danger) | reconstruction means | reconstruction may bring improvement | current status | last update date |
|---|---|--- |---|---|---|---|---|---|
| Low  | assert | test file | assertion directly detect stdout output field test file is in line with expectations | hard-coded, difficult to centrally manage output | | | Click Framework Error Output has been organizing | ` 2019-02-15 21:42:48 ` |

