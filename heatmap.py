#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt # Plotting
import skvideo.io
import sys
from tqdm import tqdm # Progress bar
from pprint import pprint
import os
import pandas as pd
from PIL import Image

filename = sys.argv[1]

metadata = skvideo.io.ffprobe(filename)["video"]
pprint(metadata)
n_frames = int(metadata["@nb_frames"])
duration = float(metadata["@duration"])
frame_rate = n_frames / duration
print(f"Frame rate: {frame_rate}")

# Calculate the maximium value per frame
width = int(metadata["@width"])
height = int(metadata["@height"])
bits = int(metadata.get("@bits_per_raw_sample", 8))
max_pixel_value = np.power(2, bits) - 1 # 8 bits -> max value of 255
max_per_frame = width * height * max_pixel_value

if os.path.isfile(filename + ".npy"):
    heatmap = np.load(filename + ".npy")
else:
    # Read the whole video into memory
    video = skvideo.io.vread(filename)

    # Mean intensity along the time axis & channel axis
    heatmap = video.mean(axis=0).mean(axis=-1) / max_pixel_value

    np.save(filename, heatmap)

print(heatmap.min(), heatmap.mean(), heatmap.max())
vmin, vmax = np.quantile(heatmap, [0.01, 0.99])
print(vmin, vmax)
plt.imshow(heatmap, vmin=vmin, vmax=vmax)
plt.axis('off')
plt.tight_layout()
cbar = plt.colorbar()
cbar.set_label('Mean fractional pixel intensity', rotation=270, labelpad=12)
plt.savefig(filename + "_heatmap.png")