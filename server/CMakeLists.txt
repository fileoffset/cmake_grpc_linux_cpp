cmake_minimum_required(VERSION 3.0)

project(gameserver)

set(SCHEMA_DIR "../data/schema")
set(PROTOBUF_IMPORT_DIRS "../data/schema/")

add_definitions("-std=c++1z")

find_package(Protobuf REQUIRED)

protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${SCHEMA_DIR}/game.proto)

file(GLOB_RECURSE SRC_FILES list_directories False ./src/*.hpp ./src/*.cpp)

include_directories( 
  .
  ${PROTOBUF_INCLUDE_DIRS}
)

add_executable(gameserver ${SRC_FILES} ${PROTO_SRCS})

target_link_libraries(gameserver 
  ${PROTOBUF_LIBRARY} 
  pthread
)
