#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt # Plotting
import skvideo.io
import sys
from tqdm import tqdm # Progress bar
from pprint import pprint
import os
import pandas as pd

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

# If we've already processed this video, read the results from txt
# This is useful for testing out modifications to the plotting code below
if os.path.isfile(filename + ".csv"):
    df = pd.read_csv(filename + ".csv")
else:
    video = skvideo.io.vreader(filename)
    results = []
    for frame in tqdm(video, total=n_frames):
        results.append(frame.sum())

    results = np.array(results)
    results = results / max_per_frame
    frame_number = np.arange(n_frames)
    df = pd.DataFrame({"frame": frame_number, "time_seconds": frame_number / frame_rate, "intensity": results})
    df.to_csv(filename + ".csv", index=False)

plt.plot(df.time_seconds, df.intensity)
plt.title("Fractional pixel intensity over time")
plt.xlabel("Time in seconds")
plt.ylabel("Intensity")
plt.savefig(filename + ".png")