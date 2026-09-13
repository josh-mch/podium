# Podium

Hardware state snapshots and drift detection for bare-metal fleets.

Servers rarely fail without warning. A DIMM drops out of the inventory,
a PCIe link renegotiates at half width, a firmware version changes
without a ticket. These are visible days before anything breaks — but
only if someone is recording what "normal" looked like yesterday.

Podium takes a full hardware snapshot of each machine and reports
what changed.

**Status:** early development.

## Setup

Requires Python 3 with [`pyghmi`](https://pypi.org/project/pyghmi/) and
[`python-dotenv`](https://pypi.org/project/python-dotenv/) installed:

```
pip install pyghmi python-dotenv
```

Copy `.env.example` to `.env` and fill in real BMC credentials (`.env`
is git-ignored, so they never get committed):

```
cp .env.example .env
```

## Usage

`bmc_library.py` connects to the BMC named in `.env` and prints a
snapshot of power state, health, firmware, and all sensor readings:

```
python bmc_library.py
```

## Testing

There are two kinds of tests here, kept deliberately separate:

- **`test_check_all_sensors.py`** — unit tests against mocked sensor
  data. No network access, no real BMC required.

  ```
  pytest test_check_all_sensors.py
  ```

- **`test_integration_bmc.py`** — integration tests that open a real
  IPMI session against the BMC in `.env`. Skipped by default so a
  plain `pytest` never touches real hardware; opt in explicitly when
  you want to verify against a real server:

  ```
  BMC_LIVE_TEST=1 pytest test_integration_bmc.py
  ```

Running `pytest` with no arguments runs the full suite, but only the
mocked unit tests actually execute unless `BMC_LIVE_TEST=1` is set.
