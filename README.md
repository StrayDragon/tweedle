# dragon-cli

---

# **TODO**:
        
## Python Version

- Python3.7+ (Current)

## Target Platform

- [ ] Linux : 
  - [ ] Deepin and Other Debian-based distributions.

## Functional Requirements 

`dragon-cli` can abbreviate to `dg`
- I want to user can use command follow order by:
  - `dg SUBCMD [ACTION] [OPTIONS]`

- [ ] It can help the user to complete a set of operations with a more concise set of commands

  - Examples:
    - Use `$ dg blog pb ` to excute `hexo clean ; hexo g -d; hexo clean `
    - Use `$ dg blog update` to excute  `git add -A;git commit -m 'update blog';git push`
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
  |`dg`| `blog` | `p`,  `publish` | |
  ||  | `u`,  `update`| |
  |`dg`| `project` | `n`, `new` | `--lang`<br> `--build-tools`<br> `--third-parties`|

