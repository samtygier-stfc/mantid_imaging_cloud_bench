#!/bin/bash
set -o nounset
set -o errexit
source ~/miniforge3/etc/profile.d/conda.sh

# Run with 4GB dataset
mamba run -n mantidimaging python do_recon.py data_4GB/Tomo/Spheres_0000.tiff out4
