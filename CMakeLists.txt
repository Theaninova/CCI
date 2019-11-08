cmake_minimum_required(VERSION 3.5.1)
project(Blatt3)

set(CMAKE_CXX_STANDARD 99)

add_executable(client
        client.c)
add_executable(server
        server.c
        uthash/uthash.h)
