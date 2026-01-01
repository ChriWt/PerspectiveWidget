cmake_minimum_required(VERSION 3.20)
project(CShape3D LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(CShape3D MODULE
    src/cshape3d/bindings.cpp
)

target_include_directories(CShape3D PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src/cshape3d
)

# Questa è la riga chiave: installa la .so dentro il package python "cshape3d"
install(TARGETS CShape3D
    LIBRARY DESTINATION cshape3d
    RUNTIME DESTINATION cshape3d
)
