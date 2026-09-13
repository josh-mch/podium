"""Unit tests for check_all_sensors() in bmc_library.py.

check_all_sensors() only prints, it doesn't return anything, so these
tests mock cmd.get_sensor_data() with fake readings and capture stdout
to verify what gets printed.
"""

import io
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import MagicMock

from bmc_library import check_all_sensors


def make_reading(name, value, units="", health=0, states=None):
    """Build a fake sensor reading with the attributes check_all_sensors reads."""
    return SimpleNamespace(
        name=name, value=value, units=units, health=health, states=states or []
    )


class TestCheckAllSensors(unittest.TestCase):
    def test_prints_one_line_per_sensor(self):
        cmd = MagicMock()
        cmd.get_sensor_data.return_value = [
            make_reading("CPU Temp", 33.0, units="°C"),
            make_reading("FAN1", 13300.0, units="RPM"),
        ]

        buf = io.StringIO()
        with redirect_stdout(buf):
            check_all_sensors(cmd)
        output = buf.getvalue()
        lines = [line for line in output.splitlines() if line.strip()]

        self.assertEqual(len(lines), 2)
        self.assertIn("CPU Temp", lines[0])
        self.assertIn("33.0", lines[0])
        self.assertIn("FAN1", lines[1])
        self.assertIn("13300.0", lines[1])

    def test_flags_bad_health_and_states(self):
        cmd = MagicMock()
        cmd.get_sensor_data.return_value = [
            make_reading(
                "1.05V PCH", 1.23, units="V", health=2,
                states=["upper critical threshold"],
            ),
        ]

        buf = io.StringIO()
        with redirect_stdout(buf):
            check_all_sensors(cmd)
        output = buf.getvalue()

        self.assertIn("health=2", output)
        self.assertIn("upper critical threshold", output)

    def test_handles_missing_units_and_value(self):
        # Mirrors real-world readings like "Chassis Intru" which have
        # value=None and units="".
        cmd = MagicMock()
        cmd.get_sensor_data.return_value = [
            make_reading("Chassis Intru", None, units=None, health=2,
                         states=["Chassis intrusion"]),
        ]

        buf = io.StringIO()
        with redirect_stdout(buf):
            check_all_sensors(cmd)  # should not raise
        output = buf.getvalue()

        self.assertIn("Chassis Intru", output)
        self.assertIn("None", output)

    def test_no_sensors_prints_nothing(self):
        cmd = MagicMock()
        cmd.get_sensor_data.return_value = []

        buf = io.StringIO()
        with redirect_stdout(buf):
            check_all_sensors(cmd)

        self.assertEqual(buf.getvalue(), "")

    def test_calls_get_sensor_data_once(self):
        cmd = MagicMock()
        cmd.get_sensor_data.return_value = []

        check_all_sensors(cmd)

        cmd.get_sensor_data.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
