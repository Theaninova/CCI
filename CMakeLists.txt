cmake_minimum_required(VERSION 3.5.1)
project(Blatt3)

set(CMAKE_CXX_STANDARD 99)

add_executable(client
        src/client.c
        src/libraries/uthash.h
        src/generic/hash_helper.h
        src/generic/data_helper.h
        src/generic/network.h
        src/generic/network.c
        src/generic/hash_helper.c
        src/generic/data_helper.c src/debug.h)
add_executable(server
        src/server.c
        src/libraries/uthash.h
        src/generic/hash_helper.h
        src/generic/data_helper.h
        src/generic/network.h
        src/generic/network.c
        src/generic/hash_helper.c
        src/generic/data_helper.c src/debug.h)
