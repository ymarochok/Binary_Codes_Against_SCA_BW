import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# the binary mapping
# captured protected traces use binary codes as inputs for network
# the easiest way to store inputs value during capturing of trace is
# to save it in integer format (15bit code translated in decimal)
MAPPING = {
    -7: 0b110100010000001, # 26753
    -6: 0b010100010000010, # 10370
    -5: 0b100000000000011, # 16387
    -4: 0b100100010000100, # 18564
    -3: 0b010000000000101, # 8197
    -2: 0b110000000000110, # 24582
    -1: 0b000100010000111, # 2183
     1: 0b000100010001000, # 2184
     2: 0b110000000001001, # 24585
     3: 0b010000000001010, # 8202
     4: 0b100100010001011, # 18571
     5: 0b100000000001100, # 16396
     6: 0b010100010001101, # 10381
     7: 0b110100010001110  # 26766
}

def get_hw(value):
    return bin(int(value)).count('1')

# configuration 
N_TRACES = 2000
WINDOW_START = 0
WINDOW_END = 20000 # large window is chosed as 24573 captured protected power traces usually mean
# computation only for the first few neurons.
INPUT_COLUMN = 1 # column for specific input in inputs 
TRUE_WEIGHT = 4  # true weigth value to be recovered | stored to prettier comparative analysis of the results

print(f"[*] Loading {N_TRACES} traces...")
inputs_raw = np.loadtxt('inputs.txt')
inputs = inputs_raw[:N_TRACES, INPUT_COLUMN]

window_len = WINDOW_END - WINDOW_START + 1
traces = np.zeros((N_TRACES, window_len))

for i in range(N_TRACES):
    data = np.loadtxt(f'trace_{i}.txt')
    traces[i, :] = data[WINDOW_START:WINDOW_END+1]

# correlation analysis
weight_candidates = [w for w in range(-7, 8) if w != 0] # create weight candidates
r_traces = np.zeros((len(weight_candidates), window_len))

print("[*] Calculating Absolute Correlations using Protected Mapping...")
for w_idx, w_val in enumerate(weight_candidates):
    code_weight = MAPPING[w_val]
    # Hamming Weight of the XOR between code_input and code_weight
    # create hypothetical leakage
    hyp_hw = np.array([get_hw(int(x) ^ code_weight) for x in inputs])
    
    if np.std(hyp_hw) > 0:
        for t in range(window_len):
            # get correlation between actual traces and hypothetical leakage
            corr, _ = pearsonr(hyp_hw, traces[:, t])
            r_traces[w_idx, t] = abs(np.nan_to_num(corr))

# results 
max_corr = np.max(r_traces, axis=1)
recovered_idx = np.argmax(max_corr)
recovered = weight_candidates[recovered_idx]

print("\n" + "="*35)
print(f"{'Weight':^10} | {'Peak Correlation':^15}")
print("-" * 35)
for i, w in enumerate(weight_candidates):
    line = f"{w:^10} | {max_corr[i]:^15.6f}"
    if w == TRUE_WEIGHT:
        print(f"\033[91m{line} [TARGET]\033[0m")
    elif w == recovered:
        print(f"\033[94m{line} [GUESSED]\033[0m")
    else:
        print(line)

# visualization
plt.figure(figsize=(15, 7))
time_axis = np.arange(WINDOW_START, WINDOW_END + 1)

for i, w in enumerate(weight_candidates):
    # default styling for wrong guesses
    color, alpha, lw, z, lbl = ('gray', 0.2, 0.8, 1, None)
    
    if w == TRUE_WEIGHT:
        color, alpha, lw, z, lbl = ('red', 1.0, 2.5, 10, f'TRUE WEIGHT ({w})')
    elif w == recovered:
        color, alpha, lw, z, lbl = ('gray', 0.8, 2.0, 5, f'RECOVERED ({w})')
    
    plt.plot(time_axis, r_traces[i, :], color=color, alpha=alpha, linewidth=lw, zorder=z, label=lbl)

plt.title(f"Protected CPA: Window {WINDOW_START}-{WINDOW_END} (Weight {INPUT_COLUMN})", fontweight='bold')
plt.xlabel("Sample Index")
plt.ylabel("Absolute Correlation $|r|$")
plt.legend(loc='upper right', frameon=True, shadow=True)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"\nFinal Result: Recovered {recovered} | Target {TRUE_WEIGHT}")