#!/usr/bin/env bash

THIS_SCRIPT_DIR="$(dirname "$(test -L "$0" && readlink "$0" || echo "$0")")"
SCHEMA_SOURCE_DIR=${THIS_SCRIPT_DIR}/../data/schema
OUTPUT_DIR=${THIS_SCRIPT_DIR}/generated


 # generate the protobuf python stubs
python -m grpc_tools.protoc -I ${THIS_SCRIPT_DIR} -I${SCHEMA_SOURCE_DIR} --python_out=${OUTPUT_DIR} --grpc_python_out=${OUTPUT_DIR} ${SCHEMA_SOURCE_DIR}/*.proto 

if [ $? -eq 0 ]; then
  echo Generated protobuf OK
else
  echo Failed to generate protobuf!
fi

./game.py $*
