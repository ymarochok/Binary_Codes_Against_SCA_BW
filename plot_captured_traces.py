# import numpy as np
# import holoviews as hv
# from glob import glob

# hv.extension('bokeh')


# # =========================
# # LOAD TRACES + INPUTS
# # =========================
# def load_traces(folder_name):
#     trace_files = sorted(glob(f"{folder_name}/trace_*.txt"))
    
#     trace_waves_arr = []
#     for file in trace_files:
#         with open(file, 'r') as f:
#             samples = [float(x) for x in f.read().strip().split()]
#             trace_waves_arr.append(samples)
    
#     trace_waves_arr = np.array(trace_waves_arr, dtype=np.float32)

#     # Load inputs
#     inputs_arr = []
#     with open(f"{folder_name}/inputs.txt") as f:
#         for line in f:
#             inputs_arr.append([int(x) for x in line.strip().split()])
    
#     inputs_arr = np.array(inputs_arr, dtype=np.int16)

#     print("Loaded traces:", trace_waves_arr.shape)
#     print("Loaded inputs:", inputs_arr.shape)

#     return trace_waves_arr, inputs_arr


# # =========================
# # NORMALIZATION
# # =========================
# def normalize_traces(traces):
#     # Remove DC offset per trace
#     traces = traces - np.mean(traces, axis=1, keepdims=True)
#     return traces


# # =========================
# # PLOTTING FUNCTIONS
# # =========================
# def plot_raw_traces(traces, num_traces=5):
#     curves = []
#     for i in range(num_traces):
#         curves.append(hv.Curve(traces[i], label=f"trace {i}"))
    
#     return hv.Overlay(curves).opts(
#         height=500,
#         width=900,
#         title="Raw Traces (first few)"
#     )


# def plot_mean_trace(traces):
#     mean_trace = np.mean(traces, axis=0)
#     return hv.Curve(mean_trace, label="mean").opts(
#         height=500,
#         width=900,
#         title="Mean Trace"
#     )


# def plot_variance_trace(traces):
#     var_trace = np.var(traces, axis=0)
#     return hv.Curve(var_trace, label="variance").opts(
#         height=500,
#         width=900,
#         title="Variance Trace (IMPORTANT)"
#     )


# # =========================
# # FIND INTERESTING WINDOWS
# # =========================
# def find_high_variance_regions(traces, top_k=5, window_size=50):
#     var_trace = np.var(traces, axis=0)
    
#     regions = []
#     for _ in range(top_k):
#         idx = np.argmax(var_trace)
#         start = max(0, idx - window_size // 2)
#         end = min(len(var_trace), idx + window_size // 2)
        
#         regions.append((start, end))
        
#         # zero-out to find next peak
#         var_trace[start:end] = 0
    
#     return regions


# import matplotlib.pyplot as plt

# def plot_all(traces):
#     # Raw traces
#     plt.figure()
#     for i in range(5):
#         plt.plot(traces[i])
#     plt.title("Raw Traces")
#     plt.show()

#     # Mean trace
#     mean_trace = np.mean(traces, axis=0)
#     plt.figure()
#     plt.plot(mean_trace)
#     plt.title("Mean Trace")
#     plt.show()

#     var_trace = np.var(traces, axis=0)
#     plt.figure()
#     plt.plot(var_trace)
#     plt.title("Variance Trace")
#     plt.show()

# # =========================
# # MAIN EXECUTION
# # =========================
# if __name__ == "__main__":
#     folder = "unprotected_nops_dec"

#     # 1. Load
#     traces, inputs = load_traces(folder)

#     traces = normalize_traces(traces)

#     # 3. Plot
#     raw_plot = plot_raw_traces(traces, num_traces=5)
#     mean_plot = plot_mean_trace(traces)
#     var_plot = plot_variance_trace(traces)
#     plot_all(traces)
#     # Show plots
#     hv.output(raw_plot)
#     hv.output(mean_plot)
#     hv.output(var_plot)

#     # 4. Find candidate CPA windows
#     regions = find_high_variance_regions(traces)

#     print("\nSuggested high-variance regions (for CPA attack):")
#     for i, (start, end) in enumerate(regions):
#         print(f"Region {i}: {start} → {end}")

import numpy as np
import matplotlib.pyplot as plt
from glob import glob

# =========================
# LOAD A SINGLE TRACE
# =========================
def load_single_trace(folder_name):
    # Find all trace files
    trace_files = sorted(glob(f"{folder_name}/trace_*.txt"))
    
    if not trace_files:
        raise FileNotFoundError(f"No trace files found in '{folder_name}'")
    
    # Load only the first trace
    with open(trace_files[0], 'r') as f:
        samples = [float(x) for x in f.read().strip().split()]
    
    trace = np.array(samples, dtype=np.float32)
    print(f"Loaded 1 trace from {trace_files[0]} — {len(trace)} samples")
    return trace

# =========================
# SIMPLE PLOT
# =========================
if __name__ == "__main__":
    folder = "protected_array_dec_5_nops"   # change as needed
    
    # 1. Load one trace
    trace = load_single_trace(folder)
    
    # 2. (Optional) remove DC offset
    trace = trace - np.mean(trace)
    
    # 3. Plot the single trace
    plt.figure(figsize=(10, 4))
    plt.plot(trace, linewidth=0.8)
    plt.title("Single Trace")
    plt.xlabel("Sample index")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()