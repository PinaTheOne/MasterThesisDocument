import json
import os
import numpy as np
import matplotlib.pyplot as plt

EXPERIMENTS_DIR = "experiments"

files = [
    "Fanout 3.json",
    "Overlord.json",
]

def runid_to_time(data):
    """
    Returns a dict: runId -> time (minutes since first run)
    Assumes 'start' is in milliseconds
    """
    data_sorted = sorted(data, key=lambda x: x["start"])
    t0 = data_sorted[0]["start"]

    return {
        run["runId"]: (run["start"] - t0) / 60000  # ms -> minutes
        for run in data_sorted
    }

def mask_from_runid(data, runid_min, runid_max):
    runid_time = runid_to_time(data)

    times = np.array([
        runid_time[run["runId"]] for run in data
    ])

    mask = np.array([
        runid_min <= run["runId"] <= runid_max
        for run in data
    ])

    return times, mask

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
    # Latency
    # -----------------------------
    latency = np.array([
        run["averageLatency"]
        for run in data
    ])

    # -----------------------------
    # Time + mask (minutes)
    # -----------------------------
    times, mask = mask_from_runid(data, runid_min=5, runid_max=13)

    # -----------------------------
    # Draw shaded vertical region ONCE
    # -----------------------------
    if shaded_region_drawn:
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
        latency,
        marker="o",
        linestyle="-",
        color=color,
        label=filename.replace(".json", "")
    )


plt.xlabel("Time (minutes)")
plt.ylabel("Latency")
plt.legend()
plt.tight_layout()
plt.show()