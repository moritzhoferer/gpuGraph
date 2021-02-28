#! /usr/bin/python3
# MIT License
# Copyright (c) 2018-2019 Jetsonhacks
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

fps = 4

gpuLoadFile="/sys/devices/gpu.0/load"
# On the Jetson Nano this is a symbolic link to:
# gpuLoadFile="/sys/devices/platform/host1x/57000000.gpu/load"

fig, gpuAx = plt.subplots(figsize=(6,2))
fig.set_facecolor('#F2F1F0')
fig.canvas.set_window_title('GPU Activity Monitor')
fig.subplots_adjust(top=.85, bottom=.25)

gpuAx.set_xlim(60, 0)
gpuAx.set_ylim(0, 102)
gpuAx.set_title('GPU History')
gpuAx.set_ylabel('GPU Usage (%)')
gpuAx.set_xlabel('Last seconds')
gpuAx.grid(color='gray', linestyle='dotted', linewidth=1)

# For the comparison
gpuLine, = gpuAx.plot([],[])

# The line points in x,y list form
gpuy_list = deque([0]*60*fps)
gpux_list = deque(np.linspace(60,0,num=60*fps))

def initGraph():
    gpuLine.set_data([],[])
    return [gpuLine] 

def updateGraph(frame):
    # Now draw the GPU usage
    gpuy_list.popleft()
    with open(gpuLoadFile, 'r') as gpuFile:
        fileData = gpuFile.read()
    # The GPU load is stored as a percentage * 10, e.g 256 = 25.6%
    gpuy_list.append(int(fileData)/10)
    gpuLine.set_data(gpux_list,gpuy_list)
    return [gpuLine]

# Keep a reference to the FuncAnimation, so it does not get garbage collected
animation = FuncAnimation(
    fig, updateGraph,
    # frames=200,
    init_func=initGraph,
    interval=int(1e3/fps),
    blit=True,
)

plt.show()
