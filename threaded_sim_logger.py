import threading
import time
import random
import logging
import queue
import os


# DEVICE REGISTRY
devices = {
    0x100: "Brake ECU",
    0x200: "Engine ECU",
    0x300: "Steering ECU",
    0x400: "Airbag ECU"
}

# LOGGING SETUP
logging.basicConfig(
    filename="security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Shared message queue between sender and logger
message_queue = queue.Queue()


# SIMULATED SYSTEM THREAD
def simulate_system():
    ecu_ids = list(devices.keys())
    unknown_ids = [0x666, 0x999]  # example suspicious or unregistered IDs

    while True:
        # 90% normal device, 10% unknown
        is_unknown = random.random() < 0.1

        if is_unknown:
            ecu_id = random.choice(unknown_ids)
            device = "Unknown Device"
        else:
            ecu_id = random.choice(ecu_ids)
            device = devices[ecu_id]

        data = [random.randint(0x00, 0xFF) for _ in range(4)]

        msg = {
            "id": ecu_id,
            "device": device,
            "data": data,
            "timestamp": time.time()
        }

        print(f"[SENDER] {device} ({hex(ecu_id)}): {data}")
        message_queue.put(msg)
        time.sleep(0.1)

# LOGGING THREAD
def log_messages():
    # Ensure log folder exists
    os.makedirs("logs", exist_ok=True)

    while True:
        msg = message_queue.get()

        # Clean device name for safe filename (e.g., replace spaces with underscores)
        device_name_clean = msg["device"].replace(" ", "_")

        # Create or append to file named after device
        log_filename = f"logs/{device_name_clean}.txt"

        # Format the log entry
        log_entry = (
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"Device: {msg['device']} | "
            f"ID: {hex(msg['id'])} | "
            f"Data: {msg['data']}\n"
        )

        # Write to the log file
        with open(log_filename, "a") as log_file:
            log_file.write(log_entry)

        message_queue.task_done()


# THREAD STARTUP
sender_thread = threading.Thread(target=simulate_system, daemon=True)
logger_thread = threading.Thread(target=log_messages, daemon=True)

sender_thread.start()
logger_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSimulation stopped.")


