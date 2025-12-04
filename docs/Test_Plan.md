# Fabrication Test Plan — 6T SRAM Bitcell

Once the fabricated 6T SRAM cell is returned from the TinyTapeout shuttle, the following tests will be used to validate correct read, write, retention, and speed behavior. The tests assume bench‑level access to the external pins:

```
bl, blbar, wl, vdd, gnd, q, qbar
```

---

## 1. Equipment Required
- Bench power supply (0–3.3 V, current‑limited)
- Oscilloscope (≥100 MHz, high‑impedance probe)
- Bitline precharge circuit or programmable source
- Function generator or digital pattern generator
- Optional: logic analyzer

---

## 2. Read Test (Power‑Up State)

### Objective
Determine the stored value without altering the cell.

### Procedure
1. Connect:
   - `vdd` → 1.8 V  
   - `gnd` → ground  
   - `wl` → 0 V  
2. Precharge both `bl` and `blbar` to **0.9 V**.  
3. Release the precharger (bitlines float).  
4. Pulse `wl` HIGH briefly.  
5. Measure `bl` and `blbar` with an oscilloscope.

### Expected Result
- One bitline discharges slightly.
- Direction of discharge reveals whether the cell holds 0 or 1.

---

## 3. Write “1” Test

### Objective
Force the cell to store a logic 1.

### Procedure
1. Precharge both bitlines to 0.9 V.
2. Drive:
   - `bl` = 1.8 V  
   - `blbar` = 0 V  
3. Assert `wl` HIGH for 50–200 ns.
4. Lower `wl`.
5. Perform the Read Test again.

### Expected Result
Readback should indicate a stored **1**.

---

## 4. Write “0” Test

### Procedure
Same as writing “1”, but swap the bitline roles:

- `bl` = 0 V  
- `blbar` = 1.8 V  

### Expected Result
Readback should indicate a stored **0**.

---

## 5. Read‑After‑Write Validation

### Objective
Verify reliable overwriting and correct readback.

### Procedure
Perform the sequence:
1. Write 1 → Read  
2. Write 0 → Read  
3. Write 1 → Read  
4. Write 0 → Read  

### Expected Result
Every read correctly reflects the most recent write.

---

## 6. Data Retention Test

### Objective
Validate hold stability with WL OFF.

### Procedure
1. Write a known value.  
2. Set `wl` = 0 V.  
3. Float the bitlines.  
4. Wait for different intervals: 1 ms → 10 ms → 100 ms → 1 s.  
5. Perform a read.

### Expected Result
The stored value remains unchanged for all intervals.

---

## 7. Speed / Access Time Test  
*(Only possible if `q` and/or `qbar` are exposed)*

### Objective
Measure propagation delay of the SRAM cell.

### Procedure
1. Attach oscilloscope probes to `q` or `qbar`.  
2. Trigger on rising edge of `wl`.  
3. Perform a read or write operation.  
4. Measure:
   - WL‑to‑Q delay  
   - Bitline differential formation time  

### Expected Result
Response time in the expected few‑nanosecond range.

---

This test plan outlines the core procedures required to validate correct SRAM bitcell operation after fabrication.
