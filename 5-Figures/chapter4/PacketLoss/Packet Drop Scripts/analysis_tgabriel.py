#from plot_utils import plot_combined_nodes
from plot_utils import plot_combined
import numpy as np
import os
import sys
from read_json_results import parse_results

SAVE = False
EXPERIMENT_DIR = "experiments"

# -------------------------------------------------
# Load experiment files
# -------------------------------------------------
if len(sys.argv) > 1:
    file_list = sys.argv[1:]
else:
    file_list = os.listdir(EXPERIMENT_DIR)

print("Using", file_list)

# -------------------------------------------------
# Process each experiment
# -------------------------------------------------
for f in file_list:
    if f == ".DS_Store" or f.startswith("."):
        continue

    path = f"{EXPERIMENT_DIR}/{f}"
    broadcast_stats = parse_results(path)

    truncation_mins = 280
    aggregation_rate_mins = 1

    max_points = int(truncation_mins / aggregation_rate_mins)
    broadcast_stats = broadcast_stats[:max_points]

    print(f"Plotting the first {len(broadcast_stats) * aggregation_rate_mins:.0f} mins")

    # -------------------------------------------------
    # Extract metrics
    # -------------------------------------------------
    fanouts = [x["fanout"] for x in broadcast_stats]
    #nodes = [x["nodes"] for x in broadcast_stats]
    data_latency = [x["averageLatency"] for x in broadcast_stats]
    data_reliability = [x["averageReliability"] * 100 for x in broadcast_stats]
    data_rmr = [x["averageRMR"] for x in broadcast_stats]

    x = np.arange(len(data_latency)) * aggregation_rate_mins

    r = { 
        "y": data_reliability,
        "metric": "Reliability"
    }

    #r = { 
    #    "y": data_latency,
    #    "metric": "Latency"
    #}

    # -------------------------------------------------
    # Build markers (WITH WORKING Y POSITIONS)
    # -------------------------------------------------
    markers = []

    y_min = min(data_reliability)
    y_range = max(data_reliability) - y_min
    y_offset = max(y_range * 0.03, 1.0)  # stable visual offset

    #y_min = min(data_latency)
    #y_range = max(data_latency) - y_min
    #y_offset = max(y_range * 0.03, 1.0)  # stable visual offset

    # Mark every 10 minutes
    #for i, t in enumerate(x):
    #    if t != 0 and t % 10 == 0:
    #        num_nodes = broadcast_stats[i]["nodes"]
    #        markers.append({
    #            "point": t,
    #            "y": data_reliability[i] + y_offset,
    #            "label": f"{num_nodes} nodes"
    #        })

    # Explicit target markers
    #for target_min in [37, 40.5]:
    #    idx = int(target_min / aggregation_rate_mins)
    #    if 0 <= idx < len(broadcast_stats):
    #        markers.append({
    #            "point": target_min,
    #            "y": data_reliability[idx] + y_offset,
    #            "label": f"{broadcast_stats[idx]['nodes']} nodes"
    #        })
    #start_idx = 6
    #step = 15

    #for idx in range(start_idx, len(x), step):
    #    markers.append({
    #        "point": x[idx],
    #        "y": r['y'][idx],    # access the list inside r['y']
    #        "label": "",         # no label needed
    #        "color": "red",      # make this point red
    #        "size": 6            # optional, makes the dot visible
    #    })

    # -------------------------------------------------
    # Plot
    # -------------------------------------------------
    title = f
    plot_combined(
        x,
        [r],
        title,
        fanouts=fanouts,
        #nodes=nodes,
        markers=markers,
        save=SAVE,
        filename=f"rel_{f.removesuffix('.json')}"
    )
    # --- MARKERS ---
