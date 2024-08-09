#!/bin/bash
set -o nounset
set -o errexit

# Install conda
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -b
rm Miniforge3-Linux-x86_64.sh
source ~/miniforge3/etc/profile.d/conda.sh

# Create conda environments
mamba env create -f https://raw.githubusercontent.com/samtygier-stfc/tomophantomtool/main/environment.yaml
mamba env create -f https://raw.githubusercontent.com/mantidproject/mantidimaging/stable/environment.yml

# Work around for old glibc on Rocky8
mamba run -n tomophantom bash setup_tomophantom.sh

# Get scripts
git clone https://github.com/samtygier-stfc/tomophantomtool.git

# Make test data
mamba run -n tomophantom tomophantomtool/tomophantomtool.py spheres_1GB.yaml data_1GB
mamba run -n tomophantom tomophantomtool/tomophantomtool.py spheres_8GB.yaml data_8GB


