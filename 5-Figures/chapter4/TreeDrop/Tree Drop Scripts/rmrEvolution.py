import json
import os
import numpy as np
import matplotlib.pyplot as plt

EXPERIMENTS_DIR = "experiments"

files = [
    "Overlord-0p.json",
    "Overlord-25p.json",
    "Overlord-50p.json",
    "Overlord-75p.json",
]

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

plt.figure()

shaded_region_drawn = False


# -----------------------------
# Main loop
# -----------------------------
for i, filename in enumerate(files):

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
    # Label (25%, etc.)
    # -----------------------------
    label = filename.replace("Overlord-", "").replace(".json", "")
    label = label.replace("p", "%")

    # -----------------------------
    # Plot
    # -----------------------------
    plt.plot(
        times,
        rmr,
        marker="o",
        linestyle="-",
        label=label
    )


plt.xlabel("Time (minutes)")
plt.ylabel("Average RMR")
plt.legend(title="Overlord Config")

plt.tight_layout()
plt.show()