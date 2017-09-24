cmake_minimum_required(VERSION 3.0)

project(gameserver)

# add local cmake find modules
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

set(SCHEMA_DIR "${CMAKE_CURRENT_LIST_DIR}/../data/schema")
set(PROTOBUF_IMPORT_DIRS "${CMAKE_CURRENT_LIST_DIR}/../data/schema")
set(GENERATED_FILES_DIR "${CMAKE_CURRENT_LIST_DIR}/generated")

add_definitions("-std=c++1z")

find_package(Protobuf REQUIRED)
message(STATUS "Using protobuf ${protobuf_VERSION}")

find_package(gRPC REQUIRED)
message(STATUS "Using gRPC ${gRPC_VERSION}")

set(PROTOS
  ${SCHEMA_DIR}/game.proto
)

file(MAKE_DIRECTORY ${GENERATED_FILES_DIR})

protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${GENERATED_FILES_DIR} ${PROTOS})
grpc_generate_cpp(GRPC_SRCS GRPC_HDRS ${GENERATED_FILES_DIR} ${PROTOS})

file(GLOB_RECURSE SRC_FILES list_directories False 
  ./src/*.hpp 
  ./src/*.cpp
)

include_directories( 
  ${GENERATED_FILES_DIR}
  ${PROTOBUF_INCLUDE_DIRS}
  ${GRPC_INCLUDE_DIR}
)

add_executable(gameserver 
  ${SRC_FILES} 
  ${PROTO_SRCS}
  ${GRPC_SRCS}
)

target_link_libraries(gameserver 
  ${GRPC_GRPC++_LIBRARY}
  ${GRPC_LIBRARY}
  ${PROTOBUF_LIBRARY} 
  pthread
)
