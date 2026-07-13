import json
import os
import numpy as np
import matplotlib.pyplot as plt

EXPERIMENTS_DIR = "experiments"
filename = "Overlord.json"

red_shade = False
show_nodes_markers = False  # optional (nodes already plotted)

def runid_to_time(data):
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


plt.rcParams['text.usetex'] = True
plt.style.use("paper.mplstyle")

fig, ax = plt.subplots()

# -----------------------------
# Load data
# -----------------------------
path = os.path.join(EXPERIMENTS_DIR, filename)

with open(path, "r") as f:
    data = json.load(f)

data.sort(key=lambda x: x["start"])

# -----------------------------
# Fanout
# -----------------------------
fanouts = np.array([
    run["fanout"]
    for run in data
])

# -----------------------------
# Nodes
# -----------------------------
nodes = np.array([
    run["nodes"]
    for run in data
])

# -----------------------------
# Time
# -----------------------------
runid_time = runid_to_time(data)
times = np.array([
    runid_time[run["runId"]]
    for run in data
])

# -----------------------------
# Red shaded region
# -----------------------------
if red_shade:
    times_masked, mask = mask_from_runid(data, runid_min=5, runid_max=13)

    shaded_times = times_masked[mask]
    if len(shaded_times) > 0:
        xmin = shaded_times.min()
        xmax = shaded_times.max()

        ax.axvspan(
            xmin,
            xmax,
            color="C3",
            alpha=0.3
        )

# -----------------------------
# Detect fanout changes
# -----------------------------
fanout_changes = np.zeros(len(fanouts), dtype=bool)
fanout_changes[0] = True
fanout_changes[1:] = fanouts[1:] != fanouts[:-1]

# -----------------------------
# Detect node changes
# -----------------------------
nodes_changes = np.zeros(len(nodes), dtype=bool)
nodes_changes[0] = True
nodes_changes[1:] = nodes[1:] != nodes[:-1]

# -----------------------------
# Plot nodes vs time
# -----------------------------
ax.plot(
    times,
    nodes,
    marker="o",
    linestyle="-",
    color="C0",
    label="Nodes"
)

# -----------------------------
# Vertical fanout change markers
# -----------------------------
for i in np.where(fanout_changes)[0]:
    x = times[i]
    current_fanout = fanouts[i]

    ax.axvline(
        x=x,
        linestyle="--",
        linewidth=1
    )

    ax.text(
        x-0.8,
        nodes.max() - 70,
        f"fanout={current_fanout}",
        rotation=90,
        horizontalalignment="center",
        verticalalignment="bottom",
        fontsize=9
    )

# -----------------------------
# Optional node change markers
# -----------------------------
if show_nodes_markers:
    for i in np.where(nodes_changes)[0]:
        x = times[i]
        current_nodes = nodes[i]

        ax.axvline(
            x=x,
            linestyle="--",
            linewidth=1,
            color="red"
        )

        ax.text(
            x,
            current_nodes,
            f"{current_nodes}",
            rotation=90,
            horizontalalignment="center",
            verticalalignment="bottom",
            fontsize=9
        )

ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Nodes")
ax.legend()

plt.tight_layout()
plt.show()
