import numpy as np
import pandas as pd

# parameters to create dataset
MIN_VAL = -7
MAX_VAL = 7
ALLOWED_VALUES = [v for v in range(MIN_VAL, MAX_VAL + 1) if v != 0]

def is_valid(value):
    return MIN_VAL <= value <= MAX_VAL and value != 0

def abs_diff(a, b):
    return abs(a - b)

def generate_normal_sequence(seq_len=10, max_step=4):
    seq = []
    current = np.random.choice(ALLOWED_VALUES)
    seq.append(current)
    
    for _ in range(seq_len - 1):
        candidates = [v for v in ALLOWED_VALUES 
                      if abs_diff(v, current) <= max_step]
        if not candidates:
            candidates = [current]
        current = np.random.choice(candidates)
        seq.append(current)
    return seq

def generate_anomalous_sequence(seq_len=10, max_step=4, 
                                min_anomaly_diff=7, 
                                num_anomalies=(2, 4)):
    seq = generate_normal_sequence(seq_len, max_step)
    
    k = np.random.randint(num_anomalies[0], num_anomalies[1] + 1)
    
    positions = set()
    while len(positions) < k:
        pos = np.random.randint(1, seq_len)
        positions.add(pos)
    
    for pos in positions:
        prev_val = seq[pos - 1]
        candidates = [v for v in ALLOWED_VALUES 
                      if abs_diff(v, prev_val) >= min_anomaly_diff]
        if not candidates:
            continue
        new_val = np.random.choice(candidates)
        seq[pos] = new_val
    
    return seq

def create_and_save_dataset(total_samples=10000, train_ratio=0.8, 
                            seq_len=10, max_step=4, min_anomaly_diff=7,
                            random_seed=42):
    np.random.seed(random_seed)
    
    half = total_samples // 2
    
    X_norm = [generate_normal_sequence(seq_len, max_step) for _ in range(half)]
    X_anom = [generate_anomalous_sequence(seq_len, max_step, min_anomaly_diff) 
              for _ in range(half)]
    
    X = np.vstack([X_norm, X_anom])
    y = np.array([0] * half + [1] * half)
    
    idx = np.random.permutation(len(X))
    X, y = X[idx], y[idx]
    
    split = int(total_samples * train_ratio)
    X_train, y_train = X[:split], y[:split]
    X_test, y_test = X[split:], y[split:]
    
    for name, (data_X, data_y) in [('train.csv', (X_train, y_train)),
                                   ('test.csv', (X_test, y_test))]:
        cols = [f'input_{i}' for i in range(seq_len)] + ['label']
        df = pd.DataFrame(np.column_stack([data_X, data_y]), columns=cols)
        df.to_csv(name, index=False)
        print(f"Saved {name} | Shape: {df.shape} | Labels: 0={sum(data_y==0)}, 1={sum(data_y==1)}")
    
    def avg_max_diff(seqs):
        diffs = []
        for seq in seqs:
            max_diff = max(abs(seq[i] - seq[i-1]) for i in range(1, len(seq)))
            diffs.append(max_diff)
        return np.mean(diffs)
    
    print("\nSanity check (average maximum consecutive difference):")
    print(f"  Normal sequences: {avg_max_diff(X_norm):.2f}")
    print(f"  Anomalous sequences: {avg_max_diff(X_anom):.2f}")
    print(f"  (Anomaly threshold = {min_anomaly_diff})")
    print("  (All values are from -7..7 except 0)")

if __name__ == "__main__":
    create_and_save_dataset()