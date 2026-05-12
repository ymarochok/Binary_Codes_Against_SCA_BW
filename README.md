# Protecting Neural Networks with Binary Codes from Side-Channel Attacks

A comprehensive research project demonstrating defense mechanisms against **Side-Channel Attacks (SCA)** on embedded neural networks. This project implements and evaluates protection strategies using binary code encoding and Look-Up Table (LUT) techniques on the **ChipWhisperer ARM** platform.

## Project Overview

This project follows a three-stage research pipeline:
1.  **Python Development**: Designing, training, and quantizing a baseline neural network.
2.  **Embedded C Implementation**: Porting the quantized model to C for ARM Cortex-M4 (CWLITEARM).
3.  **Side-Channel Analysis**: Evaluating security through **Correlation Power Analysis (CPA)** to compare unprotected vs. protected implementations.


## Project Structure

```text
BW_APPENDIX_ZIP/
├── compiled_for_CWLITEARM_unprotected_symmetrical/  # C Source for ChipWhisperer
│   ├── main.c, network.c, network.h                 # Network implementation
│   ├── network_config.h                             # Weights, biases, and scaling
│   └── makefile                                     # Build with: make PLATFORM=CWLITEARM
├── cpa_traces_unprot_n1_3_5k/                       # 5000 pre-captured power traces
│   ├── trace_0.txt ... trace_4999.txt               # Raw power data
│   ├── inputs.txt                                   # Corresponding input vectors
│   └── cpa_for_unprotected.py                       # Attack script for baseline
├── protected_traces_n1_3_5k/                        # 5000 pre-captured power traces
│   ├── trace_0.txt ... trace_4999.txt               # Raw power data
│   ├── inputs.txt                                   # Corresponding input vectors
│   └── cpa_for_protected.py                         # Attack script for protected traces
├── nn_in_python_symmetrical/                        # Python reference & quantization logic
├── nn_in_c_affine_quantization/                     # Quantization variant: Affine
├── nn_in_c_symmetrical_quantization/                # Quantization variant: Symmetrical
├── protected_nn_with_lut_MULT_ADD_.../              # LUT-protected variants
│   └── compiled_for_CWLITEARM/                      # Compiled implementations
├── cpa_for_protected.py                             # Attack script for protected versions
├── transform_dataset.py                             # Binary code encoding utility
├── capture_traces.ipynb                             # Hardware capture workflow
└── plot_*.py                                        # Visualization & analysis tools

```


## Usage Guide

### 1. Compilation & Deployment

To compile for the **ChipWhisperer ARM Lite** target:

```bash
cd compiled_for_CWLITEARM_unprotected_symmetrical
make clean
make PLATFORM=CWLITEARM

```

*This generates `simpleserial-target-CWLITEARM.hex` for flashing.*

**Local Testing (Desktop GCC):**
To test inference logic on your machine without hardware:

```bash
# For Table-scan implementation
gcc inference.c network.c data_loader.c code_multiply.c add_ops.h -o nn

# For Indexed LUT implementation
gcc inference.c network.c data_loader.c code_ops.h -o nn

```

### 2. Binary Encoding & LUT Generation

Protected versions replace standard math with encoded lookups.

1. **Generate Tables**:
```bash
gcc generate_all.c -o generate_all
./generate_all

```


2. **Transform Data**:
```bash
python transform_dataset.py


```



```
    *This maps inputs (e.g., `3`) to protected binary codes (e.g., `0b010000000001010`).*

### 3. Running CPA Attacks
Evaluate the effectiveness of the protection by trying to recover the weights.
```bash
# Attack the baseline (unprotected)
cd cpa_traces_unprot_n1_3_5k
python cpa_for_unprotected.py

# Attack the protected implementations
cd protected_traces_n1_3_5k
python ./cpa_for_protected.py

```