"""The Meteobridge integration models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymeteobridgedata import MeteobridgeApiClient
from pymeteobridgedata.data import DataLoggerDescription


@dataclass
class MeteobridgeEntryData:
    """Data for the meteobridge integration."""

    meteobridgeapi: MeteobridgeApiClient
    coordinator: DataUpdateCoordinator
    device_data: DataLoggerDescription
    unit_descriptions: dict[str, Any]
