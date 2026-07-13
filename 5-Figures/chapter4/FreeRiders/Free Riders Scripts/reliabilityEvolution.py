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
# Toggle
# -----------------------------
SHOW_OVERLORD_FANOUT = False
OVERLORD_FILE = "Overlord.json"

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

# -----------------------------
# Helpers
# -----------------------------
def runid_to_time(data):
    """
    Returns a dict: runId -> time (minutes since first run)
    Assumes 'start' is in milliseconds
    """
    data_sorted = sorted(data, key=lambda x: x["start"])
    t0 = data_sorted[0]["start"]

    return {
        run["runId"]: (run["start"] - t0) / 60000
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


def draw_overlord_fanout_lines(ax, experiments_dir, filename):
    path = os.path.join(experiments_dir, filename)

    with open(path, "r") as f:
        data = json.load(f)

    data.sort(key=lambda x: x["start"])

    fanouts = np.array([run["fanout"] for run in data])

    runid_time = runid_to_time(data)

    times = np.array([
        runid_time[run["runId"]] for run in data
    ])

    fanout_changes = np.zeros(len(fanouts), dtype=bool)
    fanout_changes[0] = True
    fanout_changes[1:] = fanouts[1:] != fanouts[:-1]

    for i in np.where(fanout_changes)[0]:
        x = times[i]
        current_fanout = fanouts[i]

        ax.axvline(
            x=x,
            linestyle="--",
            linewidth=1,
            color="black",
            alpha=0.7
        )

        ax.text(
            x,
            1.006,
            f"fanout={current_fanout}",
            rotation=90,
            ha="center",
            va="bottom",
            fontsize=9
        )


# -----------------------------
# Plot config
# -----------------------------
plt.rcParams['text.usetex'] = True
plt.style.use("paper.mplstyle")

fig, ax = plt.subplots()

shaded_region_drawn = False


# -----------------------------
# Main plotting loop
# -----------------------------
for filename in files:

    path = os.path.join(EXPERIMENTS_DIR, filename)

    with open(path, "r") as f:
        data = json.load(f)

    data.sort(key=lambda x: x["start"])

    # -----------------------------
    # Reliability
    # -----------------------------
    reliability = np.array([
        run["averageReliability"]
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
            ax.axvspan(
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
    ax.plot(
        times,
        reliability,
        marker="o",
        linestyle="-",
        color=color,
        label=filename.replace(".json", "")
    )


# -----------------------------
# Optional fanout markers
# -----------------------------
if SHOW_OVERLORD_FANOUT:
    draw_overlord_fanout_lines(ax, EXPERIMENTS_DIR, OVERLORD_FILE)


# -----------------------------
# Ordered legend (NEW)
# -----------------------------
handles, labels = ax.get_legend_handles_labels()
label_to_handle = dict(zip(labels, handles))

ordered = [
    (label_to_handle[name], name)
    for name in LEGEND_ORDER
    if name in label_to_handle
]

if ordered:
    handles, labels = zip(*ordered)
    ax.legend(handles, labels)


# -----------------------------
# Labels
# -----------------------------
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Reliability")

plt.tight_layout()
plt.show()