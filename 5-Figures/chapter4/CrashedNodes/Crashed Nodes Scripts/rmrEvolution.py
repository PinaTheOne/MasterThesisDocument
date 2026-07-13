import json
import os
import numpy as np
import matplotlib.pyplot as plt

EXPERIMENTS_DIR = "experiments"

files = [
    "Overlord.json",
    "Fanout 6.json",
    "Fanout 3.json",
]

# -----------------------------
# Toggles
# -----------------------------
SHOW_OVERLORD_FANOUT = True
OVERLORD_FILE = "Overlord.json"

SHOW_SHADED_REGION = False
RUNID_MIN = 5
RUNID_MAX = 13


# -----------------------------
# Color configuration (NEW)
# -----------------------------
COLOR_MAP = {
    "Overlord.json": "C2",
    "Fanout 6.json": "C1",
    "Fanout 3.json": "C0",
}

# -----------------------------
# Legend order (NEW)
# -----------------------------
LEGEND_ORDER = ["Overlord", "Fanout 6", "Fanout 3"]


# -----------------------------
# Helpers
# -----------------------------
def runid_to_time(data):
    data_sorted = sorted(data, key=lambda x: x["start"])
    t0 = data_sorted[0]["start"]

    return {
        run["runId"]: (run["start"] - t0) / 60000
        for run in data_sorted
    }


def mask_from_runid(data, runid_min, runid_max):
    mask = np.array([
        runid_min <= run["runId"] <= runid_max
        for run in data
    ])
    return mask


# -----------------------------
# Fanout markers (aligned)
# -----------------------------
def draw_overlord_fanout_lines(ax, data, max_time):
    fanouts = np.array([run["fanout"] for run in data])

    runid_time = runid_to_time(data)
    real_times = np.array([
        runid_time[run["runId"]] for run in data
    ])

    times = np.linspace(0, max_time, len(real_times))

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
            x - 0.7,
            ax.get_ylim()[1] + 0.05,
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
# Preprocess ALL data first
# -----------------------------
all_data = {}
max_time = 0

for filename in files:
    path = os.path.join(EXPERIMENTS_DIR, filename)

    with open(path, "r") as f:
        data = json.load(f)

    data.sort(key=lambda x: x["start"])
    all_data[filename] = data

    runid_time = runid_to_time(data)

    real_times = np.array([
        runid_time[run["runId"]] for run in data
    ])

    max_time = max(max_time, real_times.max())


# -----------------------------
# Main loop
# -----------------------------
for filename in files:

    data = all_data[filename]

    rmr = np.array([
        run["averageRMR"]
        for run in data
    ])

    runid_time = runid_to_time(data)

    real_times = np.array([
        runid_time[run["runId"]] for run in data
    ])

    times = np.linspace(0, max_time, len(real_times))

    if SHOW_SHADED_REGION and not shaded_region_drawn:

        mask = mask_from_runid(data, RUNID_MIN, RUNID_MAX)
        shaded_times = times[mask]

        if len(shaded_times) > 0:
            ax.axvspan(
                shaded_times.min(),
                shaded_times.max(),
                color="C3",
                alpha=0.3
            )
            shaded_region_drawn = True

    color = COLOR_MAP.get(filename, "black")

    ax.plot(
        times,
        rmr,
        marker="o",
        linestyle="-",
        color=color,
        label=filename.replace(".json", "")
    )


# -----------------------------
# Fanout markers (optional)
# -----------------------------
if SHOW_OVERLORD_FANOUT:
    draw_overlord_fanout_lines(
        ax,
        all_data[OVERLORD_FILE],
        max_time
    )


# -----------------------------
# Labels
# -----------------------------
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Average RMR")


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


plt.tight_layout()
plt.show()