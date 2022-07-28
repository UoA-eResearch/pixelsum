#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt # Plotting
import skvideo.io
import sys
from tqdm import tqdm # Progress bar
from pprint import pprint

filename = sys.argv[1]

metadata = skvideo.io.ffprobe(filename)["video"]
#pprint(metadata)
n_frames = int(metadata["@nb_frames"])
frame_rate = int(metadata["@r_frame_rate"].split("/")[0])

# Calculate the maximium value per frame
width = int(metadata["@width"])
height = int(metadata["@height"])
bits = int(metadata["@bits_per_raw_sample"])
max_pixel_value = np.power(2, bits) - 1 # 8 bits -> max value of 255
max_per_frame = width * height * max_pixel_value

video = skvideo.io.vreader(filename)
results = []
for frame in tqdm(video, total=n_frames):
    results.append(frame.sum() / max_per_frame)

results = np.array(results)
plt.plot(np.arange(n_frames) / frame_rate, results)
plt.title("Fractional pixel intensity over time")
plt.xlabel("Time in seconds")
plt.ylabel("Intensity")
plt.savefig(filename + ".png")
np.savetxt(filename + ".txt", results)