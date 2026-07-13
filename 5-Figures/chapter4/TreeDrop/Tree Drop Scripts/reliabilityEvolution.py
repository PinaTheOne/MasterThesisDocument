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
    #"Overlord-5p.json": "25\\%",
     "Overlord-15p.json": "25\\%",
    # "Overlord-25p.json": "25\\%",
    "Overlord-50p.json": "5\\%",
}

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

    times = np.array([
        runid_time[run["runId"]] for run in data
    ])

    mask = np.array([
        runid_min <= run["runId"] <= runid_max
        for run in data
    ])

    return times, mask


def draw_overlord_fanout_lines(ax, data, color="black", alpha=0.4):
    data.sort(key=lambda x: x["start"])

    fanouts = np.array([run["fanout"] for run in data])
    runid_time = runid_to_time(data)

    times = np.array([
        runid_time[run["runId"]] for run in data
    ])

    changes = np.zeros(len(fanouts), dtype=bool)
    changes[0] = True
    changes[1:] = fanouts[1:] != fanouts[:-1]

    for i in np.where(changes)[0]:
        x = times[i]
        current_fanout = fanouts[i]

        ax.axvline(
            x=x,
            linestyle="--",
            linewidth=1,
            color=color,
            alpha=alpha
        )

        ax.text(
            x,
            ax.get_ylim()[1],
            f"{current_fanout}",
            rotation=90,
            ha="center",
            va="bottom",
            fontsize=8,
            alpha=0.7
        )


# -----------------------------
# Plot config
# -----------------------------
plt.rcParams['text.usetex'] = True
plt.style.use("paper.mplstyle")

fig, ax = plt.subplots()

shaded_region_drawn = False

# -----------------------------
# Main loop
# -----------------------------
for filename, label in files.items():

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
    # Time + mask (5–13)
    # -----------------------------
    times, mask = mask_from_runid(data, runid_min=5, runid_max=13)

    # -----------------------------
    # Shaded regions (draw once)
    # -----------------------------
    if not shaded_region_drawn:

        # Red region (runs 5–13)
        shaded_times = times[mask]
        if len(shaded_times) > 0:
            ax.axvspan(
                shaded_times.min(),
                shaded_times.max(),
                color="C3",
                alpha=0.3
            )

        # Gold region (runs 5–8)
        times_gold, mask_gold = mask_from_runid(data, runid_min=5, runid_max=8)
        shaded_times_gold = times_gold[mask_gold]

        if len(shaded_times_gold) > 0:
            ax.axvspan(
                shaded_times_gold.min(),
                shaded_times_gold.max(),
                color="gold",
                alpha=0.3
            )

        shaded_region_drawn = True

    # -----------------------------
    # Plot curve
    # -----------------------------
    ax.plot(
        times,
        reliability,
        marker="o",
        linestyle="-",
        label=label
    )

    # Optional:
    # draw_overlord_fanout_lines(ax, data)


# -----------------------------
# Labels
# -----------------------------
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Reliability")

ax.legend(title="Overlord Config")

plt.tight_layout()
plt.show()