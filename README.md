# CCI tests for RNVS
This is a project for setting up Gitlab CI and automated tests for the tasks in the class RNVS, but can also be used for
other classes that involve network.

## What it does

- It packs everything in the `src/` folder plus the `CMakeLists.txt` in a tar.gz file you can download in GitLab
- It checks if the project builds correctly
- It checks if the tar.gz file includes all files necessary for the build to succeed
- It checks if a `server` and `client` files exists inside the `build` folder
- It performs automatic tests using a Python script and `.service` descriptions

## .service files
The Python script uses `.service` files as a script. Syntax:

| Char  | Action       | Usage/Description |
|-------|---------------|-----------|
| `<`     | Receive and expect | `<^FFFFFF%` Wait for a connection, start the program, expect `FFFFFF` (HEX)
| `>`     | Send | `^>FFFFFF%` Start the program, send `FFFFFF` (HEX) |
| `%`      | Flush         | Execute the action (`<`/`>`) with the data between the action char and flush char |
| `^`    | Start Program | Starts the program to communicate with |
| Other | Hex data      | Any number or character between `A` and `F` (not case-sensitive) |
