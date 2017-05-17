cmake_minimum_required(VERSION 2.6)

set(PROGRAMS stl_info stl_png stl_path png_size png_scale png_distances
             png_offset png_path png_halftone svg_path path_join path_array
             path_ps path_dxf path_png path_rml path_sbp path_g path_camm path_epi
             path_uni path_oms path_ord png_grb png_drl
    CACHE STRING "Core program list")

find_package(PNG REQUIRED)
include_directories(${PNG_INCLUDE_DIR})

#set(CMAKE_C_FLAGS "-Wall -g")
set(CMAKE_C_FLAGS "-Wall -O3")

add_library(fabcore STATIC fab.c)

foreach(program ${PROGRAMS})
  add_executable(${program} ${program}.c)
  target_link_libraries(${program} fabcore ${PNG_LIBRARY} -lm)
endforeach(program)

if( ${CMAKE_PROJECT_NAME} MATCHES fabmod )
  install(TARGETS ${PROGRAMS} DESTINATION ${PROJECT_SOURCE_DIR}/../bin)
endif( ${CMAKE_PROJECT_NAME} MATCHES fabmod )
