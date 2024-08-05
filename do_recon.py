#!/usr/bin/env python
import time
import sys
from pathlib import Path

import numpy as np
from mantidimaging.core.data.dataset import StrictDataset
from mantidimaging.core.io.filenames import FilenameGroup
from mantidimaging.core.io.loader import loader
from mantidimaging.core.io.saver import image_save
from mantidimaging.core.operations.divide import DivideFilter
from mantidimaging.core.reconstruct import get_reconstructor_for
from mantidimaging.core.rotation import CorTiltDataModel
from mantidimaging.core.utility.data_containers import ReconstructionParameters, ScalarCoR, Degrees

SAMPLE_PATH = Path(sys.argv[1])
SAMPLE_LOG = SAMPLE_PATH.parent.parent / "tomo.txt"
#zmin, zmax = 380, 390
OUTPUT_DIR = Path(sys.argv[2])

default_settings = {
    'algorithm': 'FBP_CUDA',
    'filter_name': 'ram-lak',
    'cor': 1,
    'tilt': 0,
    'max_projection_angle': 360
}

sample_settings = {
    'cor': None,
    'tilt': 0,
    'pixel_size': 100,
}


def load_samples(file_path: str):
    filename_group = FilenameGroup.from_file(Path(file_path))
    filename_group.find_all_files()
    filenames = [str(p) for p in filename_group.all_files()]
    image_stack = loader.load(filename_group)
    #image_stack.data = image_stack.data[:, zmin:zmax, :]
    dataset = StrictDataset(image_stack)

    print(image_stack.data.shape)

    log = loader.load_log(SAMPLE_LOG)
    log.raise_if_angle_missing(filenames)
    image_stack.log_file = log

    return dataset


def run_recon(image_stack, settings=None):
    if settings is None:
        settings = {}
    settings = default_settings | settings

    reconstructor = get_reconstructor_for(settings['algorithm'])

    settings['cor'] = ScalarCoR(settings['cor'])
    settings['tilt'] = Degrees(settings['tilt'])

    params = ReconstructionParameters(**settings)

    cor_tilt = CorTiltDataModel()
    cor_tilt.set_precalculated(params.cor, params.tilt)

    cor_list = cor_tilt.get_all_cors_from_regression(image_stack.height)

    recon = reconstructor.full(image_stack, cor_list, params, progress=None)
    #recon = DivideFilter.filter_func(recon, value=params.pixel_size, unit="micron", progress=None)

    return recon


def main():
    sample_data = load_samples(SAMPLE_PATH)
    print("Sample shape:", sample_data.sample.data.shape)

    runs = {}

    alpha, num_iter = 0.1, 10
    run_name = f"cil_num_iter_{num_iter}_alpha_{alpha}"
    runs[run_name] = {
        'algorithm': 'CIL',
        'num_iter': num_iter,
        'alpha': alpha,
        'non_negative': False,
        'regulariser': 'TV',
        'cor': sample_data.sample.data.shape[2]/2
    }

    for run_name, run_settings in runs.items():
        out_dir = Path(OUTPUT_DIR) / run_name
        #if out_dir.exists():
        #    print(out_dir, "Already exists, skipping")
        #    continue
        print(f"Starting run: {run_name}")
        t0 = time.perf_counter()
        recon = run_recon(sample_data.sample, sample_settings | run_settings)
        t1 = time.perf_counter()
        print(f"Done {run_name}. Took {t1-t0}s")
        #image_save(recon, out_dir)
        recon.data -= recon.data.min()
        recon.data *=  (2**16 / recon.data.max()) 
        print(recon.data.min(), recon.data.max())
        image_save(recon, out_dir, pixel_depth="int16", overwrite_all=True)


if __name__ == '__main__':
    main()
