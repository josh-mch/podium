"""Library of pyghmi-based helper functions for talking to a BMC."""

import os
from collections import deque

from dotenv import load_dotenv
from pyghmi.ipmi import command

# Load BMC_HOST / BMC_USER / BMC_PASSWORD from a local .env file (git-ignored).
# See .env.example for the expected format.
load_dotenv()


def _require_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"{name} is not set. Copy .env.example to .env and fill in "
            f"real credentials, or export {name} in your shell."
        )
    return value


BMC_HOST = _require_env("BMC_HOST")
BMC_USER = _require_env("BMC_USER")
BMC_PASSWORD = _require_env("BMC_PASSWORD")


def check_all_sensors(cmd):
    """Read and print the current value of every sensor reported by the BMC."""
    sensor_data = cmd.get_sensor_data()
    for reading in sensor_data:
        print(
            f"{reading.name:30s} "
            f"value={reading.value!s:>10} "
            f"units={reading.units or '':5s} "
            f"health={reading.health} "
            f"states={reading.states}"
        )


def list_latest_sel_entries(cmd, count=100):
    """Print the most recent `count` System Event Log (SEL) entries.

    get_event_log() returns entries oldest-first with no built-in limit,
    so we keep only the last `count` while iterating, then print them
    newest-first.
    """
    latest = deque(cmd.get_event_log(), maxlen=count)
    for entry in reversed(latest):
        print(
            f"{entry.get('timestamp', 'unknown time'):25s} "
            f"{entry.get('event', ''):40s} "
            f"severity={entry.get('severity', '')}"
        )
    print(f"\nShowed {len(latest)} entr{'y' if len(latest) == 1 else 'ies'} "
          f"(most recent first).")


def main():
    cmd = command.Command(bmc=BMC_HOST, userid=BMC_USER, password=BMC_PASSWORD)

    try:
        power = cmd.get_power()
        print("Power state:", power)

        health = cmd.get_health()
        print("Health:", health)

        firmware = dict(cmd.get_firmware())
        print("Firmware info:", firmware)

        print("\nAll sensor values:")
        check_all_sensors(cmd)

        #print("\nLatest 100 SEL entries:")
        #list_latest_sel_entries(cmd, count=100)
    finally:
        cmd.ipmi_session.logout()


if __name__ == "__main__":
    main()
