import os
import json

EXPERIMENTS_DIR = "./experiments"

for filename in os.listdir(EXPERIMENTS_DIR):
    if filename.endswith(".json"):
        filepath = os.path.join(EXPERIMENTS_DIR, filename)

        with open(filepath, "r") as f:
            data = json.load(f)

        new_data = []

        for run in data:
            received = run["receivedMessages"]
            duplicate = run["duplicateMessages"]
            sent = run["sentMessages"]

            delivered = received - duplicate
            denominator = delivered - sent
            new_rmr = received / denominator if denominator != 0 else None

            # rebuild dict in desired order
            new_run = {
                "runId": run["runId"],
                "runtime": run["runtime"],
                "start": run["start"],
                "end": run["end"],
                "nodes": run["nodes"],
                "receivedMessages": run["receivedMessages"],
                "duplicateMessages": run["duplicateMessages"],
                "sentMessages": run["sentMessages"],
                "deliveredMessages": delivered,   # inserted here
                "averageRMR": new_rmr,
                "averageDuplicationRate": run["averageDuplicationRate"],
                "globalDuplicationRate": run["globalDuplicationRate"],
                "averageLatency": run["averageLatency"],
                "averageReliability": run["averageReliability"],
                "averageHops": run["averageHops"],
                "fanout": run["fanout"]
            }

            new_data.append(new_run)

        with open(filepath, "w") as f:
            f.write("[\n")
            for i, run in enumerate(new_data):
                line = json.dumps(run)
                if i < len(new_data) - 1:
                    f.write(f"  {line},\n")
                else:
                    f.write(f"  {line}\n")
            f.write("]\n")

print("Processing complete.")
