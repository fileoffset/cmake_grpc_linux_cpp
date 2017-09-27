#!/usr/bin/env bash

THIS_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pushd .

cd ${THIS_SCRIPT_DIR}/build

[[ -f gameserver ]] && rm -r gameserver

cmake .. && cmake --build .

popd
