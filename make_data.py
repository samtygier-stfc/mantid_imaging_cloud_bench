#!/bin/bash
set -o nounset
set -o errexit

# Make test data
mamba run -n tomophantom tomophantomtool/tomophantomtool.py spheres_1GB.yaml data_1GB
mamba run -n tomophantom tomophantomtool/tomophantomtool.py spheres_8GB.yaml data_8GB


