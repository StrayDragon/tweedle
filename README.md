# dragon-cli

---

# **TODO**:

## Python Version

- Python3.6+ (Current)

## Target Platform

- [ ] Linux : 
  - [ ] Deepin and Other Debian-based distributions.

## Functional Requirements 

`dragon-cli` can abbreviate to `dg`

- [ ] It can help the user to complete a set of operations with a more concise set of commands

  - Examples:
    - Use `$ dg blog pb ` to excute `hexo clean ; hexo g -d; hexo clean `
    - Use `$ dg blog shutdown` to excute  `git add -A;git commit -m 'update blog';git push`
    - ...

- [ ] It can help the users to create a new project from the organized templates

  - Examples:

    - Use `$ dg project init cpp --build-tools cmake --third-party googletest`

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

        

