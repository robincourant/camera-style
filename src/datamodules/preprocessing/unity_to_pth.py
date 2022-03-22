"""
This script converts RGB flow frames generated by Unity to flow field tensor
files.
"""
import argparse
from glob import glob
import os
import os.path as osp
from typing import Tuple

import matplotlib.pyplot as plt
from tqdm import tqdm
import torch

from src.utils.file_utils import create_dir, save_pth
from src.utils.flow_utils import FlowUtils


def parse_arguments() -> Tuple[str, str]:
    """Parse input arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "frame_dir",
        type=str,
        help="Path to the directory containing subdir with RGB flow frames",
    )
    parser.add_argument(
        "flow_dir",
        type=str,
        help="Path to the root flow saving directory",
    )
    args = parser.parse_args()

    return args.frame_dir, args.flow_dir


if __name__ == "__main__":
    frame_rootdir, flow_rootdir = parse_arguments()

    # Iterate over the different directories containing flow frames
    for frame_dirname in os.listdir(frame_rootdir):
        frame_path_pattern = osp.join(frame_rootdir, frame_dirname, "*.png")
        # Load RGB flow frames
        rgb_frames = [
            plt.imread(frame) for frame in sorted(glob(frame_path_pattern))
        ]
        # Convert flow frame to flow field
        flows = [FlowUtils().frame_to_flow(frame) for frame in rgb_frames]
        # Save flows as pytorch tensors
        flow_dir = osp.join(flow_rootdir, frame_dirname)
        create_dir(flow_dir)
        for k in tqdm(range(len(flows) - 1)):
            flow_filename = osp.join(flow_dir, str(k).zfill(4) + ".pth")
            flow_tensor = torch.from_numpy(flows[k])
            save_pth(flow_tensor, flow_filename)
