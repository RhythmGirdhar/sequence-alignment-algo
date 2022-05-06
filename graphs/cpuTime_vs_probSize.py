import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

directoryPath = sys.argv[1]
paths = []
for root, dirs, files in os.walk(directoryPath, topdown=False):
    for name in files:
        if(name == "README.md" or name == ".DS_Store" or name == "README.txt" or name == "LICENSE"):
            pass
        else:
            paths.append(os.path.join(root, name))


basicTimeVsSize = {}

for filePath in paths:
    f = open(filePath, "r")
    content = f.read().split('\n')
    basicTimeVsSize[float(content[3])] = len(content[1]) + len(content[2])


sortedBasic = {k: v for k, v in sorted(basicTimeVsSize.items(), key=lambda item: item[1])}

print(sortedBasic)


basicTimes = []
basicSizes = []

for basicTime,basicSize in sortedBasic.items():
    basicTimes.append(basicTime)
    basicSizes.append(basicSize)

fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
ax.plot(basicSizes, basicTimes, label='basic')
#ax.plot(x, x**2, label='memory efficient')
ax.set_xlabel('problem size')
ax.set_ylabel('cpu time')
ax.set_title("cpu time vs problem size")
ax.legend()

plt.show()