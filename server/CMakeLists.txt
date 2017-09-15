cmake_minimum_required(VERSION 2.8)

project(gameserver)

set(SCHEMA_DIR "../data/schema")
set(PROTOBUF_IMPORT_DIRS "../data/schema/")

find_package(Protobuf REQUIRED)

PROTOBUF_GENERATE_CPP(PROTO_SRCS PROTO_HDRS ${SCHEMA_DIR}/first.proto)

set(SRC_FILES main.cpp)

include_directories( 
  .
  ${PROTOBUF_INCLUDE_DIRS}
)

add_executable(gameserver ${SRC_FILES} ${PROTO_SRCS})

target_link_libraries(gameserver ${PROTOBUF_LIBRARY})
