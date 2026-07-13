import json
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

EXPERIMENTS_DIR = "experiments"

files = [
    #"Fanout 5.json",
    #"Fanout 8.json",
    "Overlord.json",
]

plt.rcParams['text.usetex'] = True
plt.style.use("paper.mplstyle")

for filename in files:

    path = os.path.join(EXPERIMENTS_DIR, filename)

    with open(path, "r") as f:
        data = json.load(f)

    # ---------------------------------
    # Collect reliabilities per fanout
    # ---------------------------------
    fanout_reliabilities = defaultdict(list)

    for run in data:
        fanout = run["fanout"]
        reliability = run["averageReliability"]

        fanout_reliabilities[fanout].append(reliability)

    # ---------------------------------
    # Compute lowest reliability per fanout
    # ---------------------------------
    fanouts = sorted(fanout_reliabilities.keys())

    lowest_reliability = [
        min(fanout_reliabilities[f])
        for f in fanouts
    ]

    # ---------------------------------
    # Plot
    # ---------------------------------
    plt.figure()

    plt.plot(
        fanouts,
        lowest_reliability,
        marker="o",
        linestyle="-"
    )

    plt.xlabel("Fanout")
    plt.ylabel("Average Reliability")
    plt.title("Lowest Average Reliability vs Fanout - " + filename.replace(".json", ""))

    plt.tight_layout()
    plt.show()