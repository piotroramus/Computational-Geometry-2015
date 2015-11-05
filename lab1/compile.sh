#!/usr/bin/env bash
g++ main.cpp -L. -lpredicates -Ilibraries/cpp -Ilibraries/cpp/libraries/cppjson/include libraries/cpp/libraries/cppjson/json.cc -std=c++11 -o main
