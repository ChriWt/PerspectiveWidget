cmake_minimum_required(VERSION 3.29)
project(CShape3D)

# Assuming pybind11 is added as a submodule in extern/pybind11
add_subdirectory(extern/pybind11)

pybind11_add_module(CShape3D src/lib/cshape3d/bindings.cpp)

# If necessary, include directories can be specified explicitly
target_include_directories(CShape3D PRIVATE ${pybind11_INCLUDE_DIR})
