import numpy as np
import matplotlib.pyplot as plt
import os

# CONFIGURATION 
folder_path = "cpa_traces_n1_2"
trace0_file = "trace_0.txt"
trace1_file = "trace_1.txt"

def load_trace(filepath):
    with open(filepath, 'r') as f:
        data = [float(line.strip()) for line in f if line.strip()]
    return np.array(data)

trace0_path = os.path.join(folder_path, trace0_file)
trace1_path = os.path.join(folder_path, trace1_file)

trace0 = load_trace(trace0_path)
trace1 = load_trace(trace1_path)

print(f"Trace 0 length: {len(trace0)} samples")
print(f"Trace 1 length: {len(trace1)} samples")

x = np.arange(len(trace0))   
if len(trace0) != len(trace1):
    print("Warning: traces have different lengths. Using the shorter length for overlay.")
    min_len = min(len(trace0), len(trace1))
    trace0 = trace0[:min_len]
    trace1 = trace1[:min_len]
    x = np.arange(min_len)

# # ---- Plot 1: Trace 0 alone ----
# plt.figure(figsize=(10, 4))
# plt.plot(x, trace0, color='blue', linewidth=0.8)
# plt.title("Trace 0 (Input: [7,0,0,0,0,0,0,0,0,0])")
# plt.xlabel("Sample index")
# plt.ylabel("Amplitude")
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.savefig("trace0_alone.png", dpi=150)
# plt.show()

# # ---- Plot 2: Trace 1 alone ----
# plt.figure(figsize=(10, 4))
# plt.plot(x, trace1, color='red', linewidth=0.8)
# plt.title("Trace 1 (Input: [-7,0,0,0,0,0,0,0,0,0])")
# plt.xlabel("Sample index")
# plt.ylabel("Amplitude")
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.savefig("trace1_alone.png", dpi=150)
# plt.show()

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(12, 5))
plt.axvline(x=5194, color='black', ls=':', lw=2, label='Window Start (5190)')
plt.axvline(x=15570, color='black', ls=':', lw=2, label='Window End (15570)')
plt.plot(x, trace0, color='blue', linewidth=0.8)
plt.plot(x, trace1, color='red', linewidth=0.8)
plt.title("Isolated multiplication operation in unprotected traces")
plt.xlabel("Sample index")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("single_power_trace.png", dpi=150)
plt.show()