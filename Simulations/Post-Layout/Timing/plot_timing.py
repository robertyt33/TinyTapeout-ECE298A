import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# ==========================================
# SETTINGS
# ==========================================
# Standard styling
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.grid'] = True
plt.rcParams['font.size'] = 12

def load_spice_data(filename):
    """Loads space-delimited data from NGSPICE wrdata."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filename)

    if not os.path.exists(full_path):
        print(f"Warning: {filename} not found at {full_path}")
        return None
    
    try:
        # Read headerless space-delimited file
        data = pd.read_csv(full_path, delim_whitespace=True, header=None)
        return data
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def find_crossing_time(time, signal, threshold, edge='rising'):
    """Finds the exact time a signal crosses a threshold."""
    # Convert to numpy arrays
    t = np.array(time)
    s = np.array(signal)
    
    # Find indices where crossing occurs
    if edge == 'rising':
        # Signal was below, now above
        idx = np.where((s[:-1] < threshold) & (s[1:] >= threshold))[0]
    else: # falling
        # Signal was above, now below
        idx = np.where((s[:-1] > threshold) & (s[1:] <= threshold))[0]
        
    if len(idx) == 0:
        return None
    
    # Linear interpolation for better accuracy
    i = idx[0]
    # y = mx + c formula to find exact x (time) for y=threshold
    y1, y2 = s[i], s[i+1]
    t1, t2 = t[i], t[i+1]
    
    fraction = (threshold - y1) / (y2 - y1)
    crossing_time = t1 + fraction * (t2 - t1)
    
    return crossing_time

# ==========================================
# 1. PLOT WRITE TIMING
# ==========================================
def plot_write_timing():
    print("Plotting Write Timing...")
    data = load_spice_data("timing_write.txt")
    if data is None: return

    # NGSPICE wrdata repeats time columns: [t, val, t, val...]
    # indices: 0=time, 1=wl, 3=q, 5=qbar, 7=bl, 9=blbar
    time = data.iloc[:, 0] * 1e9 # Convert to nanoseconds
    wl   = data.iloc[:, 1]
    q    = data.iloc[:, 3]
    qbar = data.iloc[:, 5]
    bl   = data.iloc[:, 7]
    blbar= data.iloc[:, 9]

    # Calculate Delay
    t_wl_start = find_crossing_time(time, wl, 0.9, 'rising')
    t_q_flip   = find_crossing_time(time, q, 0.9, 'falling')
    
    delay_str = "N/A"
    if t_wl_start and t_q_flip:
        delay_ns = t_q_flip - t_wl_start
        delay_str = f"{delay_ns*1000:.1f} ps"

    # Create Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    
    # Top Plot: Inputs (WL, BL, BLB)
    ax1.plot(time, wl, 'k-', label='Wordline (WL)', alpha=0.8)
    ax1.plot(time, bl, 'b--', label='BL (0V)')
    ax1.plot(time, blbar, 'g--', label='BLB (1.8V)')
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title(f'Write "0" Operation (Access Time: {delay_str})')
    ax1.legend(loc='right')
    
    # Bottom Plot: Internal State (Q, Qbar)
    ax2.plot(time, q, 'r-', label='Q (Internal)', linewidth=2.5)
    ax2.plot(time, qbar, 'c-', label='Q_bar', linewidth=1.5, alpha=0.7)
    
    # Mark the delay
    if t_wl_start and t_q_flip:
        ax2.axvline(t_wl_start, color='k', linestyle=':', alpha=0.5)
        ax2.axvline(t_q_flip, color='r', linestyle=':', alpha=0.5)
        
        # Add arrow
        ax2.annotate('', xy=(t_q_flip, 0.9), xytext=(t_wl_start, 0.9),
                     arrowprops=dict(arrowstyle='<->', color='black'))
        ax2.text((t_wl_start + t_q_flip)/2, 1.0, delay_str, 
                 ha='center', color='black', fontweight='bold', backgroundcolor='white')

    ax2.set_ylabel('Voltage (V)')
    ax2.set_xlabel('Time (ns)')
    ax2.legend(loc='right')
    
    # Zoom in to relevant area (0 to 5ns usually enough)
    ax2.set_xlim(0, 5) 

    plt.tight_layout()
    plt.savefig('plot_write_timing.png')
    print(f"Saved plot_write_timing.png (Delay: {delay_str})")
    plt.close()

# ==========================================
# 2. PLOT READ TIMING
# ==========================================
def plot_read_timing():
    print("Plotting Read Timing...")
    data = load_spice_data("timing_read.txt")
    if data is None: return

    # indices: 0=time, 1=wl, 3=bl, 5=blbar, 7=diff
    time = data.iloc[:, 0] * 1e9 # ns
    wl   = data.iloc[:, 1]
    bl   = data.iloc[:, 3]
    blbar= data.iloc[:, 5]
    diff = data.iloc[:, 7] * 1000 # Convert diff to mV for easier reading

    # Calculate Delay
    t_wl_start = find_crossing_time(time, wl, 0.9, 'rising')
    t_diff_target = find_crossing_time(time, diff, 50.0, 'rising') # 50mV threshold
    
    delay_str = "N/A"
    if t_wl_start and t_diff_target:
        delay_ns = t_diff_target - t_wl_start
        delay_str = f"{delay_ns:.3f} ns"

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    # Top Plot: Bitlines (Zoomed)
    ax1.plot(time, wl, 'k-', label='WL', alpha=0.3)
    ax1.plot(time, bl, 'b-', label='BL')
    ax1.plot(time, blbar, 'g-', label='BLB')
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title(f'Read "1" Operation (Access Time: {delay_str})')
    ax1.legend(loc='lower left')
    ax1.set_ylim(1.6, 1.85) # Zoom in on the top rail to see the drop
    
    # Bottom Plot: Differential Voltage
    ax2.plot(time, diff, 'm-', label='V_diff (BL - BLB)', linewidth=2)
    ax2.axhline(50, color='k', linestyle='--', label='50mV Threshold')
    
    if t_wl_start and t_diff_target:
        ax2.axvline(t_wl_start, color='k', linestyle=':', alpha=0.5)
        ax2.axvline(t_diff_target, color='m', linestyle=':', alpha=0.5)
        
        # Add arrow
        ax2.annotate('', xy=(t_diff_target, 50), xytext=(t_wl_start, 50),
                     arrowprops=dict(arrowstyle='<->', color='black'))
        ax2.text((t_wl_start + t_diff_target)/2, 60, delay_str, 
                 ha='center', color='black', fontweight='bold', backgroundcolor='white')

    ax2.set_ylabel('Differential (mV)')
    ax2.set_xlabel('Time (ns)')
    ax2.legend()
    ax2.set_xlim(0, 5)

    plt.tight_layout()
    plt.savefig('plot_read_timing.png')
    print(f"Saved plot_read_timing.png (Delay: {delay_str})")
    plt.close()

if __name__ == "__main__":
    plot_write_timing()
    plot_read_timing()