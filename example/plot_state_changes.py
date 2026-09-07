import argparse
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def find_files(directory: str, target_suffix: str) -> list:

    """
    Walks through a directory and finds all files with the specified suffix.

    Args:
        directory (str): The directory to start the search from.
        target_suffix (str): The suffix of the files to look for.

    Returns:
        list: A list of paths to the files found.
    """
    files_found = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(target_suffix):
                rel_path = os.path.relpath(os.path.join(root, file))
                files_found.append(rel_path)
    return files_found


def process_state_changes_file(file_path: str) -> pd.DataFrame:
    """
    Reads a state change log file in the format:
        0.01s: State changed at node 5 from 0 to 1
    and converts it into a pandas DataFrame with columns:
        Time, Node, State
    """

    pattern = re.compile(
        r"(?P<time>\d+\.\d+)s:\s*State changed at node\s+(?P<node>\d+)\s+from\s+(?P<old>\d+)\s+to\s+(?P<new>\d+)"
    )

    data = []

    with open(file_path, "r") as f:
        for line in f:
            m = pattern.search(line)
            if not m:
                continue

            time = float(m.group("time"))
            node = int(m.group("node"))
            new_state = int(m.group("new"))

            data.append((time, node, new_state))

    df = pd.DataFrame(data, columns=["Time", "Node", "State"])

    # Extend last state to max time (same logic as before)
    max_time = df["Time"].max()
    last_entries = df.groupby("Node").tail(1)

    need_extension = last_entries[last_entries["Time"] < max_time].copy()
    need_extension["Time"] = max_time

    df_extended = pd.concat([df, need_extension], ignore_index=True)
    df_extended.sort_values(by=["Node", "Time"], inplace=True)

    return df_extended



def plot_state_changes(filename, show: bool = False):
    """
    Process a state change log file and plot the state transitions for each node over time.

    :param filename: path to the state change log file
    :param show: whether to show the plot instead of saving it (default: False)
    """
    df = process_state_changes_file(filename)

    # Sort values for proper plotting
    df.sort_values(by=["Node", "Time"], inplace=True)

    # Get all node IDs
    node_ids = sorted(df["Node"].unique())
    num_nodes = len(node_ids)

    # Set up subplots
    fig, axes = plt.subplots(nrows=num_nodes, ncols=1, figsize=(10, 2.5 * num_nodes), sharex=True)

    if num_nodes == 1:
        axes = [axes]  # Ensure it's iterable

    for ax, node_id in zip(axes, node_ids):
        node_df = df[df["Node"] == node_id]
        ax.step(node_df["Time"], node_df["State"], where="post")
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["INACTIVE", "ACTIVE"])
        ax.set_ylabel(f"Node {node_id}")
        ax.grid(True, linestyle="--", linewidth=0.5)

    axes[-1].set_xlabel("Time (s)")
    fig.suptitle("Markov State Transitions per Node", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    if show:
        plt.show()
    else:
        plt.savefig(filename.replace('.log', '.png'))

    plt.close()


def compute_transition_probs(group):
    """
    Computes transition probabilities from a group of state transitions.

    Parameters
    ----------
    group : pd.DataFrame
        The group of state transitions. It should have columns 'Node', 'Time', 'State', and 'PrevState'.

    Returns
    -------
    pd.Series
        A Series containing the transition probabilities 'Δ₁ (active→inactive)' and 'Δ₀ (inactive→active)'.

    Notes
    -----
    This function assumes that the sampling interval is constant and that there are enough data points to find at least one transition that represents the sampling interval.
    """
    trans_counts = group['Transition'].value_counts()
    prev_counts = group['PrevState'].value_counts()

    delta1 = trans_counts.get('1.0->0.0', 0) / prev_counts.get(1, 0) if prev_counts.get(1, 0) > 0 else 0
    delta0 = trans_counts.get('0.0->1.0', 0) / prev_counts.get(0, 0) if prev_counts.get(0, 0) > 0 else 0

    return pd.Series({'δ₀ (inactive→active)': delta0, 'δ₁ (active→inactive)': delta1, })


def compute_transition_probabilities(filename, show: bool = False):
    df = process_state_changes_file(filename)

    # We are considering the there are enough data points to find at least one transition
    # that represents the sampling interval (i.e, the minimum time difference between two consecutive state changes)
    sampling_interval = np.round(df.groupby("Node")["Time"].diff().dropna().min())

    # Generate full time index per node (10s intervals)
    full_df = []
    for node, group in df.groupby('Node'):
        time_min, time_max = group['Time'].min(), group['Time'].max()
        time_range = pd.DataFrame({'Time': np.arange(time_min, time_max + sampling_interval, sampling_interval)})
        time_range['Node'] = node
        merged = pd.merge(time_range, group, on=['Time', 'Node'], how='left')
        merged['State'] = merged['State'].ffill()  # fill missing states forward
        full_df.append(merged)

    df_full = pd.concat(full_df).sort_values(by=['Node', 'Time'])

    # Find the previous state for each transition
    df_full['PrevState'] = df_full.groupby('Node')['State'].shift(1)
    # Identify transition type 1.0 -> 0.0 or 0.0 -> 1.0
    df_full['Transition'] = df_full['PrevState'].astype(str) + '->' + df_full['State'].astype(str)

    transition_probs = df_full.groupby('Node').apply(compute_transition_probs, include_groups=False).reset_index()

    # transition_probs = df_full.groupby('Node').apply(lambda g: compute_transition_probs(g.drop(columns=['Node']))).reset_index()

    print(transition_probs)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="State Changes")
    parser.add_argument(dest="fname", type=str, default=None, help="Name of the file to process")
    parser.add_argument("--show", action="store_true", help="Show the plot")
    args = parser.parse_args()

    # Call the appropriate function based on the options
    plot_state_changes(args.fname, show=args.show)
    compute_transition_probabilities(args.fname, show=args.show)
