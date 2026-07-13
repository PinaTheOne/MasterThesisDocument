import json
import os
import numpy as np
import matplotlib.pyplot as plt

EXPERIMENTS_DIR = "experiments"

files = [
    "Fanout 7.json",
    "Fanout 3.json",
    "Overlord.json",
]

# -----------------------------
# Toggle
# -----------------------------
SHOW_OVERLORD_FANOUT = False
OVERLORD_FILE = "Overlord.json"


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

    real_times = np.array([
        runid_time[run["runId"]] for run in data
    ])

    mask = np.array([
        runid_min <= run["runId"] <= runid_max
        for run in data
    ])

    return real_times, mask


def build_uniform_times(real_times):
    """
    Convert real timestamps into evenly spaced timeline
    while preserving total duration.
    """
    t_min = 0
    t_max = real_times.max()
    return np.linspace(t_min, t_max, len(real_times))


def draw_overlord_fanout_lines(ax, experiments_dir, filename):
    """
    Draw vertical dashed lines whenever the Overlord fanout changes.
    (uses REAL time, not uniform spacing — intentional)
    """
    path = os.path.join(experiments_dir, filename)

    with open(path, "r") as f:
        data = json.load(f)

    data.sort(key=lambda x: x["start"])

    fanouts = np.array([
        run["fanout"]
        for run in data
    ])

    runid_time = runid_to_time(data)

    times = np.array([
        runid_time[run["runId"]]
        for run in data
    ])

    # Detect fanout changes
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

    path = os.path.join(EXPERIMENTS_DIR, filename)

    with open(path, "r") as f:
        data = json.load(f)

    # Sort by start time
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
    real_times, mask = mask_from_runid(data, runid_min=5, runid_max=13)

    # NEW: uniform spacing
    times = build_uniform_times(real_times)

    # -----------------------------
    # Draw shaded vertical region ONCE
    # -----------------------------
    if shaded_region_drawn:

        shaded_times = times[mask]

        if len(shaded_times) > 0:

            xmin = shaded_times.min()
            xmax = shaded_times.max()

            ax.axvspan(
                xmin,
                xmax,
                color="C3",
                alpha=0.3
            )

            shaded_region_drawn = True

    # -----------------------------
    # Colors
    # -----------------------------
    color = (
        "C9" if filename == "Fanout 8.json"
        else "C2" if filename == "Overlord.json"
        else None
    )

    # -----------------------------
    # Plot line
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
# Labels
# -----------------------------
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Reliability")

ax.legend()

plt.tight_layout()
plt.show()