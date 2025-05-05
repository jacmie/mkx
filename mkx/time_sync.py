class TimeSync:
    def __init__(self):
        self.offset = 0
        self.alpha = 0.05  # smoothing factor for drift

    def update_sync(self, remote_time, local_time):
        # New offset estimate
        new_offset = local_time - remote_time

        # Apply smoothing to avoid jitter
        self.offset = (1 - self.alpha) * self.offset + self.alpha * new_offset

    def to_local_time(self, remote_time):
        return remote_time + self.offset


# Key Event (Peripheral → Central)
# {
#   "type": "event",
#   "timestamp": 1234567,
#   "key": "KC_A",
#   "state": "down"
# }

# Sync Message (Peripheral → Central)
# {
#   "type": "sync",
#   "timestamp": 1235000
# }

# Peripheral Sync Logic
# # Send sync message every 5 seconds
# SYNC_INTERVAL = 5.0
# last_sync = time.monotonic()

# while True:
#     now = time.monotonic()
#     if now - last_sync >= SYNC_INTERVAL:
#         current_time_ms = int(time.monotonic() * 1000)
#         send_sync_packet(current_time_ms)
#         last_sync = now

#     # on key change:
#     timestamp = int(time.monotonic() * 1000)
#     send_key_event(key_code, state, timestamp)


DEBOUNCE_MS = 5

# For each key: { key_code: {'state': 'up' or 'down', 'timestamp': ms } }
debounce_state = {}

# For each frame: record final key states here
key_states = {}


def process_frame(frame_events, current_time_ms):
    global debounce_state

    # Temporarily store raw key state changes in this frame
    raw_changes = {}

    for timestamp, key, state in frame_events:
        raw_changes[key] = (timestamp, state)  # keep last event for key

    # Apply debounce filtering
    for key, (event_time, new_state) in raw_changes.items():
        last = debounce_state.get(key, None)

        if last is None:
            # First time seeing this key, start tracking
            debounce_state[key] = {"state": new_state, "timestamp": event_time}
            key_states[key] = new_state
        else:
            old_state = last["state"]
            old_time = last["timestamp"]

            if new_state != old_state:
                if event_time - old_time >= DEBOUNCE_MS:
                    # Valid state change
                    debounce_state[key] = {"state": new_state, "timestamp": event_time}
                    key_states[key] = new_state
                else:
                    # Ignore as bounce
                    pass
            else:
                # Same state repeated, update timestamp (optional)
                debounce_state[key]["timestamp"] = event_time
                key_states[key] = new_state

    # Final: extract only keys in 'down' state to send
    pressed_keys = [key for key, state in key_states.items() if state == "down"]
    send_hid_report(pressed_keys)


# Main Loop Snippet
FRAME_INTERVAL_MS = 10
last_frame_time = time.monotonic_ns() // 1_000_000
event_queue = []

while True:
    now = time.monotonic_ns() // 1_000_000
    if now - last_frame_time >= FRAME_INTERVAL_MS:
        frame_start = last_frame_time
        frame_end = frame_start + FRAME_INTERVAL_MS

        frame_events = [e for e in event_queue if frame_start <= e[0] < frame_end]
        event_queue = [e for e in event_queue if e[0] >= frame_end]

        process_frame(frame_events, frame_end)
        last_frame_time = frame_end

    # elsewhere: keep receiving and appending timestamped events
