include_directories(${GLFW3_INCLUDE_DIR})

# James model 0. RD Karbowski with variable numbers of guidance
# molecules and TC populations and runtime setting of parameters to
# examine behaviour.
add_executable(james0 james1.cpp)
target_compile_definitions(james0 PUBLIC FLT=float COMPILE_PLOTTING)
target_link_libraries(james0 ${MORPH_LDFLAGS} ${OPENGL_LIBRARIES})

# Compile compute-only with floats
add_executable(james0c james1.cpp)
target_compile_definitions(james0c PUBLIC FLT=float)
target_link_libraries(james0c ${MORPH_LDFLAGS})

# Compile with doubles:
#add_executable(james0cd james1.cpp)
#target_compile_definitions(james0cd PUBLIC FLT=double)
#target_link_libraries(james0cd ${MORPH_LDFLAGS})

# Comp 2. Supp. Sect. 7.2.
add_executable(james_comp2 james1.cpp)
target_compile_definitions(james_comp2 PUBLIC FLT=float COMPILE_PLOTTING COMP2)
target_link_libraries(james_comp2 ${MORPH_LDFLAGS} ${OPENGL_LIBRARIES})

# Compile with doubles:
#add_executable(james_comp2d james1.cpp)
#target_compile_definitions(james_comp2d PUBLIC FLT=double COMPILE_PLOTTING COMP2)
#target_link_libraries(james_comp2d ${MORPH_LDFLAGS} ${OPENGL_LIBRARIES})

# Comp 2. Supp. Sect. 7.2. No plotting.
add_executable(james_comp2c james1.cpp)
target_compile_definitions(james_comp2c PUBLIC FLT=float COMP2)
target_link_libraries(james_comp2c ${MORPH_LDFLAGS})

# Comp 2 with linear max and graphics
add_executable(james_comp2_linmax james1.cpp)
target_compile_definitions(james_comp2_linmax PUBLIC FLT=float COMPILE_PLOTTING COMP2 LINEAR_MAX)
target_link_libraries(james_comp2_linmax ${MORPH_LDFLAGS} ${OPENGL_LIBRARIES})
# Comp 2 with linear max and no graphics
add_executable(james_comp2_linmaxc james1.cpp)
target_compile_definitions(james_comp2_linmaxc PUBLIC FLT=float COMP2 LINEAR_MAX)
target_link_libraries(james_comp2_linmaxc ${MORPH_LDFLAGS})

# Divisive normalization of a_i
add_executable(james_divnorm james1.cpp)
target_compile_definitions(james_divnorm PUBLIC FLT=float COMPILE_PLOTTING DIVNORM)
target_link_libraries(james_divnorm ${MORPH_LDFLAGS} ${OPENGL_LIBRARIES})

# Divisive normalization of a_i along with competition (linear)
add_executable(james_dncomp james1.cpp)
target_compile_definitions(james_dncomp PUBLIC FLT=float COMPILE_PLOTTING DNCOMP)
target_link_libraries(james_dncomp ${MORPH_LDFLAGS} ${OPENGL_LIBRARIES})

add_executable(james_dncompc james1.cpp)
target_compile_definitions(james_dncompc PUBLIC FLT=float DNCOMP)
target_link_libraries(james_dncompc ${MORPH_LDFLAGS} ${OPENGL_LIBRARIES})

# Divisive normalization of a_i along with competition of a *logistic* nature
add_executable(james_dncomp_lg james1.cpp)
target_compile_definitions(james_dncomp_lg PUBLIC FLT=float COMPILE_PLOTTING DNCOMP BRANCHCOMP_LOGISTIC_FN)
target_link_libraries(james_dncomp_lg ${MORPH_LDFLAGS} ${OPENGL_LIBRARIES})

# Divisive normalization of a_i along with competition of power law nature
add_executable(james_dncomp_pl james1.cpp)
target_compile_definitions(james_dncomp_pl PUBLIC FLT=float COMPILE_PLOTTING DNCOMP BRANCHCOMP_A_TO_POWER_L)
target_link_libraries(james_dncomp_pl ${MORPH_LDFLAGS} ${OPENGL_LIBRARIES})

# Divisive normalization of a_i along with *per-group* competition
add_executable(james_dncomp2 james1.cpp)
target_compile_definitions(james_dncomp2 PUBLIC FLT=float COMPILE_PLOTTING DNCOMP2)
target_link_libraries(james_dncomp2 ${MORPH_LDFLAGS} ${OPENGL_LIBRARIES})

add_executable(james_dncomp2c james1.cpp)
target_compile_definitions(james_dncomp2c PUBLIC FLT=float DNCOMP2)
target_link_libraries(james_dncomp2c ${MORPH_LDFLAGS})

add_executable(dvanalyse dvanalyse.cpp)
target_compile_definitions(dvanalyse PUBLIC FLT=float COMPILE_PLOTTING)
target_link_libraries(dvanalyse ${MORPH_LDFLAGS} morphdisplay0)

add_executable(viewguidance viewguidance.cpp)
target_compile_definitions(viewguidance PUBLIC FLT=float)
target_link_libraries(viewguidance ${MORPH_LDFLAGS} morphdisplay0)

add_executable(honda honda.cpp)
target_compile_definitions(honda PUBLIC FLT=float)
target_link_libraries(honda ${MORPH_LDFLAGS})

# Dual barrel fields with shared branching normalization
add_executable(jamesdual jamesdual.cpp)
target_compile_definitions(jamesdual PUBLIC FLT=float COMPILE_PLOTTING)
target_link_libraries(jamesdual ${MORPH_LDFLAGS} morphdisplay0)
