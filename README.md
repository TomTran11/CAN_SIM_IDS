# CAN_SIM_IDS

A lightweight simulation of in-vehicle CAN communication with an integrated Intrusion Detection System (IDS) based on message timing analysis.

## What This Project Simulates

This project models a simplified **Distributed Automotive Cyber-Physical System (DACPS)** using a **virtual CAN bus**. It simulates:
- Multiple **ECUs (Electronic Control Units)** sending periodic CAN messages.
- **Normal traffic (70%)** vs. **malicious traffic (30%)**, e.g., spoofed or rapid-fire DoS-style messages.
- An **Intrusion Detection System (IDS)** that listens to the CAN bus and flags anomalies based on **unexpected timing intervals**.
- A structured log record system that:
- 	Records each message in a text file based on its source ECU name.
- 	Separates logs for known vs. unknown devices.
- 	Creates a logs/ folder containing a .txt file per ECU (e.g., Brake_ECU.txt, Unknown_Device.txt).
- 	Timestamps and formats each entry for future analysis.


###Key Features

- Multi-threaded simulation (Sender + IDS)
- Uses `python-can` virtual bus — no hardware required
- Logs anomalies based on deviation from expected message intervals
- Clean two-column console output (sender | receiver)

---

## Installation

### Python Dependencies

Ensure you have **Python 3.8+** and install required packages:

```bash
pip install python-can
```

## How to run
```bash
python3 threaded_can_sim.py
```

This will:
- Start one thread simulating CAN messages
- Start a second thread monitoring them in real time
- Print both sender and receiver activity side by side

```bash
python3 threaded_sim_logger.py
```

This will :
- Start one thread simulating CAN messages
- Start a seconod thread capture and filterign each ECU to each individual files
- A generall log coexist aside those individual one.
---

## Education purpose
This simulation was created to demonstrate CAN bus vulnerability detection using lightweight methods.
