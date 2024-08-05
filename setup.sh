#!/bin/bash

# Create conda environments
mamba env create -f https://raw.githubusercontent.com/samtygier-stfc/tomophantomtool/main/environment.yaml
mamba env create -f https://raw.githubusercontent.com/mantidproject/mantidimaging/stable/environment.yml

# Get scripts
git clone https://github.com/samtygier-stfc/tomophantomtool.git

# Make test data
mamba run -n tomophantom tomophantomtool/tomophantomtool.py spheres_1GB.yaml data_1GB
mamba run -n tomophantom tomophantomtool/tomophantomtool.py spheres_8GB.yaml data_8GB


