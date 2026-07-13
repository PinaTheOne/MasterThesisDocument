import json
import os
import numpy as np
import matplotlib.pyplot as plt

EXPERIMENTS_DIR = "experiments"

# -----------------------------
# File → label mapping
# -----------------------------
files = {
    "Overlord-0p.json": "100\\%",
    "Overlord-2p.json": "50\\%",
    "Overlord-5p.json": "25\\%",
    # "Overlord-15p.json": "15\\%",
    # "Overlord-25p.json": "25\\%",
    "Overlord-50p.json": "5\\%",
}

# -----------------------------
# Helpers
# -----------------------------
def mask_from_runid(data, runid_min, runid_max):
    return np.array([
        runid_min <= run["runId"] <= runid_max
        for run in data
    ])

# -----------------------------
# Plot config
# -----------------------------
plt.rcParams['text.usetex'] = True
plt.style.use("paper.mplstyle")

plt.figure()

shaded_region_drawn = False

# -----------------------------
# Main loop
# -----------------------------
for filename, label in files.items():
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
        (run["start"] - t0) / 60000  # ms -> minutes
        for run in data
    ])
    fanouts = np.array([run["fanout"] for run in data])

    # -----------------------------
    # Draw shaded regions ONCE
    # -----------------------------
    if not shaded_region_drawn:

        # Red region (runs 5–13)
        times_red = times[mask_from_runid(data, 5, 13)]
        if len(times_red) > 0:
            plt.axvspan(
                times_red.min(),
                times_red.max(),
                color="C3",
                alpha=0.3
            )

        # Gold region (runs 5–8)
        times_yellow = times[mask_from_runid(data, 5, 8)]
        if len(times_yellow) > 0:
            plt.axvspan(
                times_yellow.min(),
                times_yellow.max(),
                color="gold",
                alpha=0.3
            )

        shaded_region_drawn = True

    # -----------------------------
    # Plot
    # -----------------------------
    plt.plot(
        times,
        fanouts,
        marker='o',
        linestyle='-',
        label=label
    )

# -----------------------------
# Labels
# -----------------------------
plt.xlabel("Time (minutes)")
plt.ylabel("Fanout")
plt.legend(title="Overlord Config")

plt.tight_layout()
plt.show()