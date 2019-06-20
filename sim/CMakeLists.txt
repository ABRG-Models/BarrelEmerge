# James model 0. RD Karbowski with variable numbers of guidance
# molecules and TC populations and runtime setting of parameters to
# examine behaviour.
add_executable(james0 james1.cpp)
target_compile_definitions(james0 PUBLIC FLOATTYPE=float COMPILE_PLOTTING)
target_link_libraries(james0 ${MORPH_LDFLAGS} ${HDF5LIBLINK} ${JSONLIBLINK})

# Compile compute-only with floats
add_executable(james0c james1.cpp)
target_compile_definitions(james0c PUBLIC FLOATTYPE=float)
target_link_libraries(james0c ${MORPH_LDFLAGS} ${HDF5LIBLINK} ${JSONLIBLINK})

# Compile with doubles:
#add_executable(james0cd james1.cpp)
#target_compile_definitions(james0cd PUBLIC FLOATTYPE=double)
#target_link_libraries(james0cd ${MORPH_LDFLAGS} ${HDF5LIBLINK} ${JSONLIBLINK})

# Divisive normalization of a_i
add_executable(james8 james1.cpp)
target_compile_definitions(james8 PUBLIC FLOATTYPE=float COMPILE_PLOTTING COMP8)
target_link_libraries(james8 ${MORPH_LDFLAGS} ${HDF5LIBLINK} ${JSONLIBLINK})

# Divisive normalization of a_i along with competition scheme 1, plus
# comp schemes 3 (and 7?).
add_executable(james14 james1.cpp)
target_compile_definitions(james14 PUBLIC FLOATTYPE=float COMPILE_PLOTTING COMP14)
target_link_libraries(james14 ${MORPH_LDFLAGS} ${HDF5LIBLINK} ${JSONLIBLINK})
