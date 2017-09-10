#!/bin/bash

[[ ! -d build/ ]] && mkdir build

pushd .

cd build

cmake .. && cmake --build .

popd
