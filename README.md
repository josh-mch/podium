# Podium

Hardware state snapshots and drift detection for bare-metal fleets.

Servers rarely fail without warning. A DIMM drops out of the inventory,
a PCIe link renegotiates at half width, a firmware version changes
without a ticket. These are visible days before anything breaks — but
only if someone is recording what "normal" looked like yesterday.

Podium takes a full hardware snapshot of each machine and reports
what changed.

**Status:** early development.
