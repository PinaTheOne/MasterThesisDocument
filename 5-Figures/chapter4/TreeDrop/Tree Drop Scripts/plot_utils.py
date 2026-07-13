import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import math

import numpy as np


def plot_average_over_time(x, y, metric, file):
    avg = sum(x) / len(x)

    plt.figure(figsize=(10, 5))
    plt.scatter(y, x, label=f"{metric} (Averaged)")
    plt.axhline(avg, color="red", linestyle="--", label=f"Average: {avg:.2f}")
    plt.xlabel("Time")
    plt.ylabel(metric)
    plt.title(f"Average {metric} Over Time\n<{file}>")
    plt.legend()
    plt.show()


def plot_rewards(x, rewards, fanouts=[], title="", save=False, filename=None):
    n = len(rewards)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(
        6 * cols, 4 * rows), squeeze=False)
    fig.suptitle(title, fontsize=16, fontweight='bold')

    for i, reward in enumerate(rewards):
        ax = axes[i // cols][i % cols]

        y, metric = reward['y'], reward['metric']

        ax.plot(x, y, marker="o", label=f"{metric}")

        last_fanout = -1
        for j, f in enumerate(fanouts):
            if f != last_fanout:
                ax.axvline(x=x[j], color="orange",
                           linestyle="--", alpha=0.7)
                ax.text(
                    x[j],
                    ax.get_ylim()[1] * 0.95,
                    f"Fanout {f}",
                    rotation=90,
                    color="orange",
                    fontsize=10,
                    ha="center"
                )
                last_fanout = f

        ax.set_xlim(left=0)
        ax.set_ylabel(metric)
        ax.set_title(f"{metric}")
        ax.legend()
        ax.grid(True)

    # Remove unused subplots
    for j in range(n, rows * cols):
        fig.delaxes(axes[j // cols][j % cols])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    if save:
        if not filename:
            filename = title.replace(" ", "_")
        plt.savefig(f"plots/{filename}.png")
    else:
        plt.show()

def plot_combined_nodes(x, Y, title: str, nodes=[], markers=[], shades=[], save=False, filename=None, min_max=False, average_line=False):
    fig, axes = plt.subplots(len(Y), 1, figsize=(
        10, 5 * len(Y)), sharex=True)
    axes = axes if len(Y) > 1 else [axes]
    fig.suptitle(title, fontsize=16, fontweight='bold')

    for i, d in enumerate(Y):
        y, metric = d['y'], d['metric']

        if metric == 'Latency':
            axes[i].set_ylim(0, max(x) + (max(x) * 0.1))
        elif metric == 'Reliability':
            axes[i].set_ylim(0, 100 + 100*0.1)

        axes[i].set_xlim(0, max(x))

        axes[i].plot(x, y, marker="o", label=f"{metric}")

        last_node = -1
        for j, f in enumerate(nodes):
            if f != last_node:
                axes[i].axvline(x=x[j], color="orange",
                                linestyle="--", alpha=0.7)
                axes[i].text(
                    x[j],
                    axes[i].get_ylim()[1] * 0.95,
                    f"Nodes {f}",
                    rotation=90,
                    color="orange",
                    fontsize=10,
                    ha="center"
                )
                last_nodes = f

        if average_line:
            avg = sum(y) / len(y)
            axes[i].axhline(avg, color="red", linestyle="--",
                            label=f"Average: {avg:.2f}")


        # TODO unchecked after refactoring
        for m in markers:
            axes[i].axvline(x=m["point"], color="orange",
                            linestyle="--", alpha=0.7)
            axes[i].text(
                m["point"],
                axes[i].get_ylim()[1] * 0.95,
                m["label"],
                rotation=90,
                color="red",
                fontsize=10,
                ha="center"
            )

        for shaded_region in range(0, len(shades) - 1, 2):
            start = shades[shaded_region]["point"]
            end = shades[shaded_region + 1]["point"]
            axes[i].fill_between(
                x=[start, end],
                y1=0,
                y2=axes[i].get_ylim()[1],
                color="blue",
                alpha=0.1,
                label="Paused Region" if shaded_region == 0 else None
            )

        axes[i].set_ylabel(metric)
        #axes[i].set_title(f"{metric} Over Time")
        axes[i].legend()
        axes[i].grid(True)

    plt.tight_layout()

    if save:
        if not filename:
            filename = ""
            for d in Y:
                filename += d['metric']
            filename += "-"
            filename += "".join(c for c in title if c.isalpha()
                                or c.isdigit() or c == ' ').replace(" ", "")

        plt.savefig(f"plots/{filename}.png")
    else:
        plt.show()

def plot_combined(x, Y, title: str, fanouts=[], markers=[], shades=[], save=False, filename=None, min_max=False, average_line=False):
    fig, axes = plt.subplots(len(Y), 1, figsize=(
        10, 5 * len(Y)), sharex=True)
    axes = axes if len(Y) > 1 else [axes]
    fig.suptitle(title, fontsize=16, fontweight='bold')

    for i, d in enumerate(Y):
        y, metric = d['y'], d['metric']

        if metric == 'Latency':
            axes[i].set_ylim(0, max(x) + (max(x) * 0.1))
        elif metric == 'Reliability':
            axes[i].set_ylim(0, 100 + 100*0.1)

        axes[i].set_xlim(0, max(x))

        axes[i].plot(x, y, marker="o", color='C0', label=f"{metric}")

        last_fanout = -1
        for j, f in enumerate(fanouts):
            # TODO: Remove
            #if x[j] <= 10:
            #    continue

            if f != last_fanout:
                axes[i].axvline(
                    x=x[j],
                    color="orange",
                    linestyle="--",
                    alpha=0.7
                )
                axes[i].text(
                    x[j],
                    axes[i].get_ylim()[1] * 0.95,
                    f"Fanout {f}",
                    rotation=90,
                    color="orange",
                    fontsize=10,
                    ha="center"
                )
                last_fanout = f

        if average_line:
            avg = sum(y) / len(y)
            axes[i].axhline(avg, color="red", linestyle="--",
                            label=f"Average: {avg:.2f}")


        # TODO unchecked after refactoring
        for m in markers:
            axes[i].axvline(x=m["point"], color="orange",
                            linestyle="--", alpha=0.7)
            axes[i].text(
                m["point"],
                axes[i].get_ylim()[1] * 0.95,
                m["label"],
                rotation=90,
                color="red",
                fontsize=10,
                ha="center"
            )

        for shaded_region in range(0, len(shades) - 1, 2):
            start = shades[shaded_region]["point"]
            end = shades[shaded_region + 1]["point"]
            axes[i].fill_between(
                x=[start, end],
                y1=0,
                y2=axes[i].get_ylim()[1],
                color="blue",
                alpha=0.1,
                label="Paused Region" if shaded_region == 0 else None
            )

        axes[i].set_ylabel(metric)
        #axes[i].set_title(f"{metric} Over Time")
        axes[i].legend()
        axes[i].grid(True)

    plt.tight_layout()

    axes[-1].set_xlabel("Time (minutes)")
    axes[-1].xaxis.set_major_locator(MaxNLocator(integer=True))

    mask = ((x >= (5-1)) & (x <= (13-1))) #| ((x >= (22-5)/2) & (x <= (26-5)/2))
    #mask = (x < 0) & (x > 0)

    y_masked = np.ma.masked_where(~mask, y)

    plt.plot(x, y, marker='o', label=metric)

    plt.xlabel("Time (minutes)")
    plt.ylabel(metric)

    plt.fill_between(
        x,
        y_masked,
        color='C3',
        alpha=0.3
    )

    #plt.fill_between(
    #    x,
    #    y,
    #    where=mask,
    #    color='C3',      # or color='red'
    #    alpha=0.3,
    #    interpolate=True,
    #    label="Region [4, 8]"
    #)

    if save:
        if not filename:
            filename = ""
            for d in Y:
                filename += d['metric']
            filename += "-"
            filename += "".join(c for c in title if c.isalpha()
                                or c.isdigit() or c == ' ').replace(" ", "")

        plt.savefig(f"plots/{filename}.png")
    else:
        plt.show()


def plot_combined_with_fanout_colors(data, title: str, markers=[], shades=[], save=False, filename=None):
    fig, axes = plt.subplots(len(data), 1, figsize=(
        10, 5 * len(data)), sharex=True)
    axes = axes if len(data) > 1 else [axes]
    fig.suptitle(title, fontsize=16, fontweight='bold')

    colors = plt.cm.get_cmap(lut=len(set(data[0]['fanouts'])))

    for i, d in enumerate(data):
        x, y, metric = d['x'], d['y'], d['metric']
        fanouts = d.get('fanouts', [None] * len(x))
        avg = sum(x) / len(x)
        min_val, max_val = min(x), max(x)
        min_idx, max_idx = x.index(min_val), x.index(max_val)

        if metric == 'Latency':
            axes[i].set_ylim(0, max_val + (max_val * 0.1))
        elif metric == 'Reliability':
            axes[i].set_ylim(0, 100 + 100*0.1)

        axes[i].set_xlim(0, max(y))

        fanout_colors = {f: colors(idx % 10)
                         for idx, f in enumerate(set(fanouts))}

        for j in range(1, len(x)):
            axes[i].plot(
                y[j-1:j+1],
                x[j-1:j+1],
                color=fanout_colors[fanouts[j]],
                marker="o"
            )

        for fanout, color in fanout_colors.items():
            axes[i].plot([], [], color=color, label=f"Fanout {fanout}")

        axes[i].axhline(avg, color="red", linestyle="--",
                        label=f"Average: {avg:.2f}")

        for m in markers:
            axes[i].axvline(x=m["point"], color="orange",
                            linestyle="--", alpha=0.7)
            axes[i].text(
                m["point"],
                axes[i].get_ylim()[1] * 0.95,
                m["label"],
                rotation=90,
                color="orange",
                fontsize=10,
                ha="center"
            )

        for shaded_region in range(0, len(shades) - 1, 2):
            start = shades[shaded_region]["point"]
            end = shades[shaded_region + 1]["point"]
            axes[i].fill_between(
                x=[start, end],
                y1=0,
                y2=axes[i].get_ylim()[1],
                color="blue",
                alpha=0.1,
                label="Paused Region" if shaded_region == 0 else None
            )

        axes[i].set_ylabel(metric)
        #axes[i].set_title(f"{metric} Over Time")
        axes[i].legend()
        axes[i].grid(True)

        axes[i].annotate(f"Min: {min_val:.2f}",
                         xy=(y[min_idx], min_val),
                         xytext=(y[min_idx], min_val -
                                 (max_val - min_val) * 0.1),
                         arrowprops=dict(facecolor='green', arrowstyle="->"),
                         color="green")

        axes[i].annotate(f"Max: {max_val:.2f}",
                         xy=(y[max_idx], max_val),
                         xytext=(y[max_idx], max_val +
                                 (max_val - min_val) * 0.1),
                         arrowprops=dict(facecolor='red', arrowstyle="->"),
                         color="red")

    plt.tight_layout()

    if save:
        if not filename:
            filename = ""
            for d in data:
                filename += d['metric']
            filename += "-"
            filename += "".join(c for c in title if c.isalpha()
                                or c.isdigit() or c == ' ').replace(" ", "")

        plt.savefig(f"plots/{filename}.png")
    else:
        plt.show()
