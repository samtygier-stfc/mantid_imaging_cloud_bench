#!/bin/bash
set -o nounset
set -o errexit

# Tomophantomlib needs to be built on rocky 8 to support the older glibc

sudo dnf install -y --disablerepo openstack-train cmake gcc-c++ 
cd ~
git clone https://github.com/dkazanc/TomoPhantom.git
cd TomoPhantom
git checkout v3.0
mkdir build
cd build/
cmake ../ -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON
cmake --build .
cp Core/libtomophantom.so ${CONDA_PREFIX}/lib/
