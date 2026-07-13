import json
import os
import numpy as np
import matplotlib.pyplot as plt

EXPERIMENTS_DIR = "experiments"

files = [
    "Fanout 5.json",
    "Fanout 8.json",
    "Overlord.json",
]

def mask_from_runid(data, runid_min, runid_max):
    return np.array([
        runid_min <= run["runId"] <= runid_max
        for run in data
    ])

plt.rcParams['text.usetex'] = True
plt.style.use("paper.mplstyle")

plt.figure()

shaded_region_drawn = False

for filename in files:
    path = os.path.join(EXPERIMENTS_DIR, filename)

    with open(path, "r") as f:
        data = json.load(f)

    # Sort by start time
    data.sort(key=lambda x: x["start"])

    # -----------------------------
    # RELATIVE TIME IN MINUTES
    # -----------------------------
    t0 = data[0]["start"]

    times = np.array([
        (run["start"] - t0) / 60000   # ms -> minutes
        for run in data
    ])

    fanouts = np.array([
        run["fanout"] for run in data
    ])

    # -----------------------------
    # Draw shaded vertical region ONCE
    # -----------------------------
    mask = mask_from_runid(data, runid_min=5, runid_max=13)

    if not shaded_region_drawn:
        shaded_times = times[mask]
        if len(shaded_times) > 0:
            xmin = shaded_times.min()
            xmax = shaded_times.max()

            plt.axvspan(
                xmin,
                xmax,
                color="C3",
                alpha=0.3
            )

            shaded_region_drawn = True

    # -----------------------------
    # Plot line + points
    # -----------------------------
    color = (
        "C9" if filename == "Fanout 8.json"
        else "C2" if filename == "Overlord.json"
        else None
    )

    plt.plot(
        times,
        fanouts,
        marker='o',
        linestyle='-',
        color=color,
        label=filename.replace(".json", "")
    )

plt.xlabel("Time (minutes)")
plt.ylabel("Fanout")
plt.legend()
plt.tight_layout()
plt.show()