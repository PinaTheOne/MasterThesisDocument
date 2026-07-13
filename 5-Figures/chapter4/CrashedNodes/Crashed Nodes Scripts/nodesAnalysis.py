import json
import os
import numpy as np
import matplotlib.pyplot as plt

EXPERIMENTS_DIR = "experiments"

files = [
    "Fanout 6.json",
    "Fanout 3.json",
    "Overlord.json",
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
    runid_time = runid_to_time(data)

    real_times = np.array([
        runid_time[run["runId"]] for run in data
    ])

    mask = np.array([
        runid_min <= run["runId"] <= runid_max
        for run in data
    ])

    return real_times, mask


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
            x-0.7,
            ax.get_ylim()[1] * 0.75,
            f"fanout={current_fanout}",
            rotation=90,
            horizontalalignment="center",
            verticalalignment="bottom",
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

    data = all_data[filename]

    # -----------------------------
    # Nodes
    # -----------------------------
    nodes = np.array([
        run["nodes"]
        for run in data
    ])

    # -----------------------------
    # Time (COMMON timeline)
    # -----------------------------
    runid_time = runid_to_time(data)

    real_times = np.array([
        runid_time[run["runId"]] for run in data
    ])

    times = np.linspace(0, max_time, len(real_times))

    # -----------------------------
    # Shaded region
    # -----------------------------
    if SHOW_SHADED_REGION and not shaded_region_drawn:

        _, mask = mask_from_runid(
            data,
            RUNID_MIN,
            RUNID_MAX
        )

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
    # Color logic
    # -----------------------------
    color = (
        "C9" if filename == "Fanout 6.json"
        else "C2" if filename == "Overlord.json"
        else None
    )

    # -----------------------------
    # Plot
    # -----------------------------
    ax.plot(
        times,
        nodes,
        marker="o",
        linestyle="-",
        color=color,
        label=filename.replace(".json", "")
    )


# -----------------------------
# Fanout markers
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
ax.set_ylabel("Nodes")

ax.legend()

plt.tight_layout()
plt.show()