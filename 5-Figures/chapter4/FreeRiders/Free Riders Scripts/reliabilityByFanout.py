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

plt.rcParams["text.usetex"] = True
plt.style.use("paper.mplstyle")


def compute_avg_reliability_per_fanout(data):
    """
    Returns two arrays:
    fanouts, avg_reliabilities
    """

    reliability_by_fanout = defaultdict(list)

    for run in data:
        fanout = run["fanout"]
        reliability = run["averageReliability"]

        reliability_by_fanout[fanout].append(reliability)

    fanouts = []
    avg_reliabilities = []

    for f in sorted(reliability_by_fanout.keys()):
        fanouts.append(f)
        avg_reliabilities.append(
            np.mean(reliability_by_fanout[f])
        )

    return np.array(fanouts), np.array(avg_reliabilities)


for filename in files:

    path = os.path.join(EXPERIMENTS_DIR, filename)

    with open(path, "r") as f:
        data = json.load(f)

    fanouts, avg_rel = compute_avg_reliability_per_fanout(data)

    plt.figure()

    plt.plot(
        fanouts,
        avg_rel,
        marker="o",
        linestyle="-"
    )

    plt.xlabel("Fanout")
    plt.ylabel("Average Reliability")

    plt.title("Average Reliability vs Fanout - " + filename.replace(".json", ""))

    plt.tight_layout()
    plt.show()