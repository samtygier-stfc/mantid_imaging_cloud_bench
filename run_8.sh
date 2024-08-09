#!/bin/bash
set -o nounset
set -o errexit
source ~/miniforge3/etc/profile.d/conda.sh

# Run with 8GB dataset
mamba run -n mantidimaging python do_recon.py data_8GB/Tomo/Spheres_0000.tiff out8
