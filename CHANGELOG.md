# Change Log

## [3.0.0] - 2021-11-22

This release contains **breaking changes** and you will have to re-define most of your settings in the UI and in automations after installation.

### Upgrade Instructions
Due to the many changes and entities that have been removed and replaced, we recommend the following process to upgrade from an earlier Beta or from an earlier release:

- Upgrade the Integration files, either through HACS (Recommended) or by copying the files manually to your custom_components/meteobridge directory.
- Restart Home Assistant
- Remove the Meteobridge Integration by going to the Integrations page, click the 3 dots in the lower right corner of the Meteobridge Integration and select Delete
- While still on this page, click the + ADD INTEGRATION button in the lower right corner, search for Meteobridge, and start the installation, supplying your credentials.

### Changes
- **BREAKING CHANGE** This is basically a completely new Integration, as all code as been rewritten from the beginning. This goes for the Integration itself, but also for the module `pymeteobridgedata` that this integration uses for commincating with the Meteobridge Logger. This is done to make the Integration compliant with Home Assistant coding practices and to ensure it is much easier to maintain going forward. As a consequence of that almost all sensors have a new Name and a new Unique ID, which is why a removal and re-installation is the best option when updating to this version. You will also have to change the sensor names in the UI and in Automations that are based on this Integration.
- Fixing Issue #8, by adding `meassure_time` as an attribute to min and max sensors.

### Added
- Frontend Translations are now in place for non-standard text based sensors like Pressure Trend and Beaufort Description.
