#!/bin/bash

./build.sh

[[ -f ./build/gameserver ]] && ./build/gameserver $* || echo "Failed to build!"
