Cmake is required to compile the C++ code.

Adding the submodule:
  1) git submodule add https://github.com/pybind/pybind11.git extern/pybind11
  2) git submodule update --init

How to build:
  1) mkdir build && cd build
  2) cmake -G "Visual Studio XX XXXX" -A x64 -DCMAKE_BUILD_TYPE=Release ..
  3) cmake --build . --config Release
