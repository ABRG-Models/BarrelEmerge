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

set (CMAKE_CXX_STANDARD 17)

find_package(OpenMP)

# Add the host definition to CXXFLAGS along with other switches
if (APPLE)
  # OpenMP: According to
  # https://stackoverflow.com/questions/39979836/using-openmp-with-c11-on-mac-os#39983933
  # it should now be a case of:
  #
  # You should be able to get away without the libomp that's mentioned
  # in that post, as I don't use any of the runtime library OpenMP
  # features. However, the code did not compile without it, so we've moved the links to omp to the later apple if case.
  set(CMAKE_CXX_FLAGS "${MORPH_HOST_DEFINITION} -Wall -g")# -Xpreprocessor -fopenmp

else()
  # To use Intel compiler, call cmake as: cmake -DCMAKE_CXX_COMPILER=icpc ..
  if (CMAKE_CXX_COMPILER_ID MATCHES Intel)
    set(CMAKE_CXX_FLAGS "${MORPH_HOST_DEFINITION} -Wall -g -std=c++17 -xHOST -O3 -D__ICC__") #-qopenmp
  else() # GCC or Clang
    set(CMAKE_CXX_FLAGS "${MORPH_HOST_DEFINITION} -Wall -Wfatal-errors -g -Wno-unused-result -Wno-unknown-pragmas -march=native -O3") #-fopenmp
  endif()
endif()

# Tell clang to be quiet about brace initialisers
if(CMAKE_CXX_COMPILER_ID MATCHES Clang)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-missing-braces")
endif()

# Additional GL compiler flags.
#
# Following `cmake --help-policy CMP0072`
set(OpenGL_GL_PREFERENCE "GLVND")
# maybe -DGL_GLEXT_PROTOTYPES
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DGL3_PROTOTYPES -DGL_GLEXT_PROTOTYPES")

# Lib finding - we have to do this, so that the correct include paths
# are present for OpenGL, OpenCV, etc; they're all included by
# morphologica header files.
find_package(OpenCV REQUIRED)
find_package(OpenGL REQUIRED)
# X11 is required as some programs link to morphdisplay0
find_package(X11 REQUIRED)
find_package(HDF5 REQUIRED)
find_package(jsoncpp REQUIRED)
find_package(glfw3 REQUIRED)
find_package(Armadillo REQUIRED)
find_package(morphologica CONFIG REQUIRED)

if(OpenMP_Found)
  link_libraries(OpenMP::OpenMP_CXX)
endif()

add_subdirectory(sim)

# For debugging of variables:
option(DEBUG_VARIABLES OFF)
if(DEBUG_VARIABLES)
  get_cmake_property(_variableNames VARIABLES)
  foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
  endforeach()
endif(DEBUG_VARIABLES)
