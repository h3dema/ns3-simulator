import matplotlib.pyplot as plt
import pandas as pd
import io

fname = "../logs/cap/1_60000000000_0_0/02_09_2026_18_27_30/0_1_Energy.log"
with open(fname, "r") as f:
    raw = f.read()

# Parse CSV-like text
lines = [l for l in raw.splitlines() if l and not l.startswith("#")]
rows = [l.split(",") for l in lines]

# Build DataFrame
df = pd.DataFrame(rows, columns=["time", "node", "col3", "col4", "energy"])

# Clean columns
df["time"] = df["time"].str.replace("ns", "").str.replace("+", "").astype(float) * 1e-9
df["node"] = df["node"].astype(int)
df["energy"] = df["energy"].astype(float)

# Plot one curve per node
plt.figure(figsize=(10,5))

for node_id, group in df.groupby("node"):
    plt.plot(group["time"], group["energy"], label=f"Node {node_id}", linewidth=1.5)

plt.xlabel("Time (s)")
plt.ylabel("Energy")
plt.title("Energy vs Time per Node")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()