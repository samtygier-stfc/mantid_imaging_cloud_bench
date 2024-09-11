#!/bin/bash
set -o nounset
set -o errexit
source ~/miniforge3/etc/profile.d/conda.sh

# Make test data
mamba run -n tomophantom tomophantomtool/tomophantomtool.py spheres_1GB.yaml data_1GB
mamba run -n tomophantom tomophantomtool/tomophantomtool.py spheres_5GB.yaml data_5GB
mamba run -n tomophantom tomophantomtool/tomophantomtool.py spheres_8GB.yaml data_8GB


