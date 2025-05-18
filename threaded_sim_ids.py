import threading
import time
import random
import can

# Shared virtual CAN bus
bus = can.Bus(interface='virtual', channel='vcan0', receive_own_messages=True)

EXPECTED_INTERVAL = 0.1
last_timestamps = {}

print(f"{'SENDER'.ljust(60)} | {'RECEIVER'}")
print("-" * 120)

# Helper to format a CAN message
def format_msg(prefix, msg_type, ecu_id, interval, data):
    return f"[{msg_type}] ID={hex(ecu_id)} Intv={interval:.3f}s Data={data}"

# Sender thread
def simulate_can_messages():
    ecu_profiles = {
        0x100: 0.1,
        0x200: 0.2,
        0x300: 0.15
    }

    while True:
        behavior = random.choices(['normal', 'attack'], weights=[0.7, 0.3])[0]

        if behavior == 'normal':
            ecu_id = random.choice(list(ecu_profiles.keys()))
            interval = ecu_profiles[ecu_id]
        else:
            ecu_id = random.choice(list(ecu_profiles.keys()))
            interval = random.uniform(0.01, 0.04)

        data = [random.randint(0x00, 0xFF) for _ in range(4)]
        msg = can.Message(arbitration_id=ecu_id, data=data, is_extended_id=False)

        try:
            bus.send(msg)
            msg_out = format_msg("SEND", behavior, ecu_id, interval, data)
            print(f"{msg_out.ljust(60)} |")  # Left-aligned in first column
            time.sleep(interval)
        except can.CanError:
            print("SEND ERROR".ljust(60) + " |")

# Receiver/IDS thread
def monitor_can_bus():
    while True:
        msg = bus.recv()
        now = time.time()
        msg_id = msg.arbitration_id

        interval = None
        if msg_id in last_timestamps:
            interval = now - last_timestamps[msg_id]
        last_timestamps[msg_id] = now

        if interval is not None:
            if abs(interval - EXPECTED_INTERVAL) < 0.05:
                alert = f"[!!!] Anomaly ID={hex(msg_id)} Intv={interval:.3f}s"
                print(f"{''.ljust(60)} | {alert}")
            else:
                msg_out = f"[RECV] ID={hex(msg_id)} Intv={interval:.3f}s"
                print(f"{''.ljust(60)} | {msg_out}")
        else:
            print(f"{''.ljust(60)} | [RECV] ID={hex(msg_id)} (first message)")

# Start both threads
threading.Thread(target=simulate_can_messages, daemon=True).start()
threading.Thread(target=monitor_can_bus, daemon=True).start()

# Keep main thread alive
while True:
    time.sleep(1)

