#!/usr/bin/env bash

THIS_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCHEMA_SOURCE_DIR=${THIS_SCRIPT_DIR}/../data/schema
GEN_OUTPUT_DIR=${THIS_SCRIPT_DIR}/generated/
OUTPUT_DIR=${THIS_SCRIPT_DIR}/build/
GRPC_CPP_OUT=/usr/local/bin/grpc_cpp_plugin

[[ ! -d "${OUTPUT_DIR}" ]] && mkdir -p "${OUTPUT_DIR}" 2>/dev/null
[[ ! -d "${GEN_OUTPUT_DIR}" ]] && mkdir -p "${GEN_OUTPUT_DIR}" 2>/dev/null

pushd .

cd ${SCHEMA_SOURCE_DIR}

# generate the protobuf files
protoc -I=${SCHEMA_SOURCE_DIR} --cpp_out=${GEN_OUTPUT_DIR} ${SCHEMA_SOURCE_DIR}/*.proto

# generate the grpc files
protoc -I=${SCHEMA_SOURCE_DIR} --plugin=protoc-gen-grpc=${GRPC_CPP_OUT} --grpc_out=${GEN_OUTPUT_DIR} ${SCHEMA_SOURCE_DIR}/*.proto

cd ${THIS_SCRIPT_DIR}/build

cmake .. && cmake --build .

popd
