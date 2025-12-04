# **Design Proposal of a 6T SRAM Bit Cell**

### SkyWater 130nm Technology Process

**Author:** Robert Tang **Course:** ECE298 **Date:** December 4, 2024 

**Repository:** https://github.com/robertyt33/TinyTapeout-ECE298A

# i) Performance Target

| Category | Target | As % of VDD | Comments |
| ----- | ----- | ----- | ----- |
| **Supply** | 1.8 V | 100% | Standard definition from TinyTapeout |
| **Hold SNM** | **0.40–0.60 V** | \~22–33% | High safety margin needed to prevent background noise from flipping the bit |
| **Read SNM** | **0.20–0.30 V** | \~11–17% | Need Read SNM to prevent destructive read |
| **Write SNM** | **0.70–0.90 V** | \~39–50% |  |
| **Access Time** | **0-200ps** | / | Clock speed: assuming 50MHz (clk period: 20ns)  |
| **Read Time** | **0-200ps** | / |  |

Device Ratios

| Ratio | Definition (geometric) | Conservative target | Notes |
| ----- | ----- | ----- | ----- |
| **CR** (cell ratio) | Wpd / Wax | **1.8 – 2.2** | Larger CR \= better **read** SNM, worse write |
| **PR** (pull-up ratio) | Wpu / Wax | **0.9 – 1.2** | Smaller PR \= easier **write**, slightly worse hold |

# ii) Timeline

| Week | Tasks | Tools |
| :---- | :---- | :---- |
| **Week 5 *10/1-10/7*** | Schematic Design 6T SRAM Schematics Trying out 8bit counter project | LTSpice |
| **Week 6 *10/8-10/14*** |  | Verilog \+ CocoTB |
| **Week 7 *10/15-10/21*** |  |  |
| **Week 8 *10/22-10/28*** | SPICE Simulation for the schematic Ensure circuit design matches targeted performance Take into account of preliminary estimates of parasitic resistances and capacitances | Magic, Xschem, Ngspice |
| **Week 9 *10/29-11/4*** | SPICE Simulation (continued) Add interfacing circuitry if needed Physical Layout in Magic Draw out physical layout according to the previous LTSpice result W/L ratio  Verification of the layout | Magic, Xschem, Ngspice |
| **Week 10 *11/5-11/11*** |  |  |
| **Week 11 *11/12-11/18*** | Parasitic Extraction & Timing Verification Extract parasitics (R,C), rerun simulation w. extracted netlist Timing Verification (access/read time with python) SNM Verification | Magic, Xschem, Ngspice, Python |
| **Week 12 *11/19-11/25*** |  |  |
| **Week 13 *11/26-12/2*** | Final Verification |  |
| **Week 14 *12/3*** | Evaluation, Final Submission |  |

# iii) Schematic Diagram

![6T SRAM Schematic](/Schematics/6T_SRAM_1bit.png)
