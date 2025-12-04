import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import os

# ==========================================
# 1. SETUP & PATHS
# ==========================================
# UPDATE: The folder containing your .txt files
DATA_DIR = r"C:\ECE298A\Layout_Tests\Prelayout"

def load_spice_data_single_file(filename):
    """
    Loads VTC curves from a SINGLE space-delimited file.
    Scans columns to find valid VTC data (monotonic transitions).
    If only one VTC is found, it mirrors it to create the second curve.
    """
    full_path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(full_path):
        print(f"Warning: {filename} not found at {full_path}")
        return None, None, None, None
    
    try:
        # Read file, handling multiple spaces as delimiters
        data = pd.read_csv(full_path, delim_whitespace=True, header=None)
        
        if data.empty: 
            print(f"Warning: {filename} is empty.")
            return None, None, None, None
        
        # Helper to check if a column pair looks like a VTC
        # VTC = Voltage Transfer Characteristic (Inverter-like)
        def is_vtc(vin, vout):
            # 1. Check Output Range: Must have significant swing (e.g., > 0.5V for 1.8V logic)
            if np.ptp(vout) < 0.5: return False 
            # 2. Check Linearity: VTCs are non-linear. If Vout tracks Vin (corr > 0.99), it's just the input node.
            # We check correlation magnitude because inverters have negative correlation (-1).
            # If corr is positive and high (~1), it's likely a resistor/short, not an inverter.
            corr = np.corrcoef(vin, vout)[0,1]
            if corr > 0.95: return False # Input tracking
            return True

        # Scan pairs of columns (Sweep, Result)
        valid_curves = []
        # We assume data is [Sweep1, Val1, Sweep2, Val2, ...]
        # NGSPICE 'wrdata' often repeats the sweep variable.
        
        # Check pairs (0,1), (2,3), (4,5), etc.
        for i in range(0, data.shape[1] - 1, 2):
            vin = data.iloc[:, i].values
            vout = data.iloc[:, i+1].values
            if is_vtc(vin, vout):
                valid_curves.append((vin, vout))
        
        if not valid_curves:
            print(f"Error: No valid VTC curves found in {filename}. Check SPICE simulation.")
            return None, None, None, None

        # Logic for extracting Vin1, Vout1, Vin2, Vout2
        if len(valid_curves) >= 2:
            # We found two distinct curves (e.g. Write SNM might have two different ones)
            vin1, vout1 = valid_curves[0]
            vin2, vout2 = valid_curves[1]
        else:
            # Only one valid curve found (Common for symmetric Hold/Read tests)
            # We mirror the data to create the butterfly
            # print(f"Note: Single VTC found in {filename}. Mirroring for symmetry.")
            vin1, vout1 = valid_curves[0]
            vin2 = vin1.copy() # Use same sweep for curve 2
            vout2 = vout1.copy() # Use same output for curve 2
            
        return vin1, vout1, vin2, vout2

    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None, None, None, None

def calculate_snm(vin1, vout1, vin2, vout2):
    """Calculates SNM using the Seevinck method (45-degree rotation)."""
    # 1. Coordinate Rotation (u = x-y, v = x+y)
    u1 = vin1 - vout1
    v1 = vin1 + vout1
    u2 = vout2 - vin2
    v2 = vout2 + vin2
    
    # 2. Interpolate
    p1 = sorted(zip(u1, v1))
    p2 = sorted(zip(u2, v2))
    u1_s, v1_s = zip(*p1)
    u2_s, v2_s = zip(*p2)
    
    min_u = max(min(u1_s), min(u2_s))
    max_u = min(max(u1_s), max(u2_s))
    
    if min_u >= max_u: return 0.0, None

    u_new = np.linspace(min_u, max_u, 1000)
    v1_interp = np.interp(u_new, u1_s, v1_s)
    v2_interp = np.interp(u_new, u2_s, v2_s)
    
    # 3. Calculate SNM
    diff = np.abs(v1_interp - v2_interp)
    mid_idx = len(diff) // 2
    max_diff_1 = np.max(diff[:mid_idx])
    max_diff_2 = np.max(diff[mid_idx:])
    
    if max_diff_2 < 0.1: 
        snm_val = np.max(diff) / 2.0
        idx_max = np.argmax(diff)
    else:
        snm_val = min(max_diff_1, max_diff_2) / 2.0
        if max_diff_1 < max_diff_2:
            idx_max = np.argmax(diff[:mid_idx])
        else:
            idx_max = np.argmax(diff[mid_idx:]) + mid_idx

    center_u = u_new[idx_max]
    center_v_avg = (v1_interp[idx_max] + v2_interp[idx_max]) / 2.0
    
    cx = (center_v_avg + center_u) / 2.0
    cy = (center_v_avg - center_u) / 2.0
    
    return snm_val, (cx, cy)

def plot_butterfly(title, filename, save_name):
    print(f"Processing {title} from {filename}...")
    
    # Load ALL data from the single file
    vin1, vout1, vin2, vout2 = load_spice_data_single_file(filename)
    
    if vin1 is None:
        print(f"Skipping {title}.\n")
        return

    snm_value, center_pt = calculate_snm(vin1, vout1, vin2, vout2)
    
    plt.figure(figsize=(6, 6))
    
    # Plot Curve 1 (Standard VTC)
    plt.plot(vin1, vout1, 'b-', label='Inv 1 (Q->Qbar)', linewidth=2)
    
    # Plot Curve 2 (Mirrored VTC)
    # The data is [Input=Qbar, Output=Q]. On the plot: X=Q, Y=Qbar.
    # So we plot X=vout2 (which is Q), Y=vin2 (which is Qbar)
    plt.plot(vout2, vin2, 'r-', label='Inv 2 (Qbar->Q)', linewidth=2)
    
    plt.plot([0, 1.8], [0, 1.8], 'k--', alpha=0.3)
    
    if snm_value > 0.01 and center_pt:
        cx, cy = center_pt
        side = snm_value
        rect = patches.Rectangle((cx - side/2, cy - side/2), side, side, 
                                 linewidth=1.5, edgecolor='green', facecolor='none', linestyle='--')
        plt.gca().add_patch(rect)
        plt.text(0.95, 0.95, f'SNM = {snm_value*1000:.0f} mV', transform=plt.gca().transAxes, 
                 fontsize=12, color='green', fontweight='bold', ha='right', va='top',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", alpha=0.9))
    else:
        plt.text(0.5, 0.5, 'Unstable / Monostable', ha='center', color='gray')

    plt.title(title)
    plt.xlabel('Voltage Q (V)')
    plt.ylabel('Voltage Qbar (V)')
    plt.xlim(0, 1.8)
    plt.ylim(0, 1.8)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='lower left')
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, save_name)
    plt.savefig(save_path)
    print(f"Saved {save_name} (SNM = {snm_value:.4f} V)")
    plt.close()

# ==========================================
# RUN GENERATION
# ==========================================
# Note: Now we only pass ONE filename per test
plot_butterfly("Read SNM Curve", "readsnm.txt", "plot_read_snm.png")
plot_butterfly("Hold SNM Curve", "holdsnm.txt", "plot_hold_snm.png")
plot_butterfly("Write SNM Curve", "writesnm.txt", "plot_write_snm.png")