# 3.1 minimum version for set(CMAKE_CXX_STANDARD 1z)
cmake_minimum_required(VERSION 3.1)
project(BarrelEmerge)

message(STATUS "Install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "  (This can be changed with `cmake -DCMAKE_INSTALL_PREFIX=/some/place`")

# From CMAKE_SYSTEM work out which of __OSX__, __GLN__, __NIX__ or
# __WIN__ are required
message(STATUS "Operating system: " ${CMAKE_SYSTEM})
if(CMAKE_SYSTEM MATCHES Linux.*)
  set(MORPH_HOST_DEFINITION "-D__GLN__")
elseif(CMAKE_SYSTEM MATCHES BSD.*)
  set(MORPH_HOST_DEFINITION "-D__NIX__")
elseif(APPLE)
  set(MORPH_HOST_DEFINITION "-D__OSX__")
elseif(CMAKE_SYSTEM MATCHES Win.*)
  set(MORPH_HOST_DEFINITION "-D__WIN__")
else()
  message(ERROR "Operating system not supported: " ${CMAKE_SYSTEM})
endif()

set(CMAKE_CXX_STANDARD 17)

# Find OpenMP first, so that we have OpenMP_CXX_FLAGS
find_package(OpenMP)

# Set up compiler flags
if (APPLE)
  set(CMAKE_CXX_FLAGS "${MORPH_HOST_DEFINITION} -Wall -g -O3")
else()
  # To use Intel compiler, call cmake as: cmake -DCMAKE_CXX_COMPILER=icpc ..
  if (CMAKE_CXX_COMPILER_ID MATCHES Intel)
    set(CMAKE_CXX_FLAGS "${MORPH_HOST_DEFINITION} -Wall -g -std=c++17 -xHOST -O3 -D__ICC__")
  else() # GCC or Clang
    set(CMAKE_CXX_FLAGS "${MORPH_HOST_DEFINITION} -Wall -g -Wfatal-errors -Wno-unused-result -Wno-unknown-pragmas -march=native -O3")
  endif()
endif()

# Tell clang to be quiet about brace initialisers
if(CMAKE_CXX_COMPILER_ID MATCHES Clang)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-missing-braces")
endif()

if(OpenMP_FOUND)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()

# Additional GL compiler flags.
#
# Following `cmake --help-policy CMP0072`
set(OpenGL_GL_PREFERENCE "GLVND")
# maybe -DGL_GLEXT_PROTOTYPES
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DGL3_PROTOTYPES -DGL_GLEXT_PROTOTYPES")

if(APPLE)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DGL_SILENCE_DEPRECATION")
endif()

# Lib finding - we have to do this, so that the correct include paths
# are present for OpenGL, OpenCV, etc; they're all included by
# morphologica header files.
find_package(OpenCV REQUIRED)
find_package(OpenGL REQUIRED)
find_package(HDF5 REQUIRED)
find_package(glfw3 REQUIRED)
find_package(Armadillo REQUIRED)
find_package(Freetype REQUIRED)

if(OpenMP_FOUND)
  link_libraries(OpenMP::OpenMP_CXX)
endif()

# Define collections of includes for the dependencies
set(MORPH_INC_CORE ${ARMADILLO_INCLUDE_DIR} ${ARMADILLO_INCLUDE_DIRS} ${HDF5_INCLUDE_DIR})
set(MORPH_INC_GL ${OpenCV_INCLUDE_DIRS} ${OPENGL_INCLUDE_DIR} ${GLFW3_INCLUDE_DIR} ${FREETYPE_INCLUDE_DIRS})
include_directories(${MORPH_INC_CORE} ${MORPH_INC_GL})

# The include path for morphologica defaults to in-tree, but user can change it if necessary
set(MORPH_INCLUDE_PATH "${PROJECT_SOURCE_DIR}/morphologica" CACHE PATH "The path to the morphologica headers (e.g. /usr/local/include or \$HOME/usr/include)")

# Show message saying where morphologica is
message(STATUS "morphologica path: ${MORPH_INCLUDE_PATH}")
message(STATUS "  (This can be changed with, e.g.: `cmake -DMORPH_INCLUDE_PATH=/usr/local/include`")

# Use our include path for the morph directories
include_directories(BEFORE ${MORPH_INCLUDE_PATH})
include_directories(BEFORE ${MORPH_INCLUDE_PATH}/include)
# Tell BarrelEmerge where the morph fonts are, to compile them into the binary
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DMORPH_FONTS_DIR=\"\\\"${PROJECT_SOURCE_DIR}/morphologica/fonts\\\"\"")

# Make a check that the morph directory exists and fail out if it can't be found
if(NOT EXISTS "${MORPH_INCLUDE_PATH}/morph")
  message(FATAL_ERROR "Make sure you have installed morphologica at the location: ${MORPH_INCLUDE_PATH}. The suggested way to do this is to git clone morphologica inside the ${PROJECT_NAME} base directory")
endif()

add_subdirectory(sim)

# For debugging of variables:
option(DEBUG_VARIABLES "Set to 1 or ON to see all of cmake's internal variables. Useful for debugging the cmake build." OFF)
if(DEBUG_VARIABLES)
  get_cmake_property(_variableNames VARIABLES)
  foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
  endforeach()
endif(DEBUG_VARIABLES)
