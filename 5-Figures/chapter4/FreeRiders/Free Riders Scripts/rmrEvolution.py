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

# -----------------------------
# Color configuration (NEW)
# -----------------------------
COLOR_MAP = {
    "Fanout 5.json": "C0",
    "Fanout 8.json": "C1",
    "Overlord.json": "C2",
}

# -----------------------------
# Legend order (NEW)
# -----------------------------
LEGEND_ORDER = ["Overlord", "Fanout 8", "Fanout 5"]


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

    data.sort(key=lambda x: x["start"])

    # -----------------------------
    # RMR
    # -----------------------------
    rmr = np.array([
        run["averageRMR"]
        for run in data
    ])

    # -----------------------------
    # Time + mask
    # -----------------------------
    times, mask = mask_from_runid(data, runid_min=5, runid_max=13)

    # -----------------------------
    # Shaded region (once)
    # -----------------------------
    if not shaded_region_drawn:
        shaded_times = times[mask]

        if len(shaded_times) > 0:
            plt.axvspan(
                shaded_times.min(),
                shaded_times.max(),
                color="C3",
                alpha=0.3
            )
            shaded_region_drawn = True

    # -----------------------------
    # Colors (NEW)
    # -----------------------------
    color = COLOR_MAP.get(filename, "black")

    # -----------------------------
    # Plot
    # -----------------------------
    plt.plot(
        times,
        rmr,
        marker="o",
        linestyle="-",
        color=color,
        label=filename.replace(".json", "")
    )


# -----------------------------
# Ordered legend (NEW)
# -----------------------------
handles, labels = plt.gca().get_legend_handles_labels()
label_to_handle = dict(zip(labels, handles))

ordered = [
    (label_to_handle[name], name)
    for name in LEGEND_ORDER
    if name in label_to_handle
]

if ordered:
    handles, labels = zip(*ordered)
    plt.legend(handles, labels)


plt.xlabel("Time (minutes)")
plt.ylabel("Average RMR")
plt.tight_layout()
plt.show()