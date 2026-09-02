import re
import matplotlib.pyplot as plt
from collections import defaultdict

LOGFILE = "../logs/cap/1_60000000000_0_0/02_09_2026_17_37_47/0_1_TraceHarvestedPower.log"


# Regex to capture:
#   node number
#   harvested energy
#   time
pattern = re.compile(
    r"New harvested power at node#(\d+):\s*([0-9.]+)\s*J at\s*([0-9.]+)\s*s"
)

# Store per-node data
node_times = defaultdict(list)
node_energies = defaultdict(list)

with open(LOGFILE, "r") as f:
    for line in f:
        m = pattern.search(line)
        if not m:
            continue

        node = int(m.group(1))
        energy = float(m.group(2))
        time = float(m.group(3))

        # Skip zero-energy entries
        if energy == 0.0:
            continue

        node_times[node].append(time)
        node_energies[node].append(energy)

# Plot all nodes
plt.figure(figsize=(12, 6))

for node in sorted(node_times.keys()):
    plt.plot(
        node_times[node],
        node_energies[node],
        marker='o',
        linestyle='-',
        linewidth=2,
        markersize=4,
        label=f"Node {node}"
    )

plt.xlabel("Time (s)")
plt.ylabel("Harvested Energy (J)")
plt.title("Harvested Energy vs Time (per node)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
