cmake_minimum_required(VERSION 3.2)
project(zadanie1)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp libraries/cpp/libraries/cppjson/json.cc predicates/predicates.c)

include_directories(libraries/cpp)
include_directories(libraries/cpp/libraries/cppjson/include)

add_executable(zadanie1 ${SOURCE_FILES})

