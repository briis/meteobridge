from homeassistant.helpers.entity import Entity
import homeassistant.helpers.device_registry as dr
from homeassistant.const import ATTR_ATTRIBUTION
from .const import (
    DOMAIN,
    ATTR_BRAND,
    DEFAULT_BRAND,
    DEFAULT_ATTRIBUTION,
)


class MeteobridgeEntity(Entity):
    """Base class for Meteobridge entitties."""

    def __init__(self, coordinator, sensor, server):
        """Intialize the entity."""
        super().__init__()
        self.coordinator = coordinator
        self.sensor = sensor
        self.server = server

        self._sensor_data = self.coordinator.data[self.sensor]
        self._mac = self.server["mac_address"]
        self._unique_id = f"{self.sensor}_{self._mac}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._sensor_data["name"]

    @property
    def should_poll(self):
        """Poll Cameras to update attributes."""
        return False

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._sensor_data["device_class"]

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return {
            ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
            ATTR_BRAND: DEFAULT_BRAND,
        }

    @property
    def device_info(self):
        return {
            "connections": {(dr.CONNECTION_NETWORK_MAC, self._mac)},
            "name": self.name,
            "manufacturer": DEFAULT_BRAND,
            "model": self._sensor_data["device_class"],
            "sw_version": None,
            "via_device": (DOMAIN, self._mac),
        }

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
