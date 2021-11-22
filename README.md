# // Meteobridge Datalogger for Home Assistant
![GitHub release](https://img.shields.io/github/release/briis/meteobridge.svg?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square)](https://github.com/custom-components/hacs) [![](https://img.shields.io/badge/COMMUNITY-FORUM-success?style=flat-square)](https://community.home-assistant.io/t/meteobridge-weather-logger-integration/154263)

The Meteobridge Integration adds support for retrieving data from a Meteobridge datalogger. It uses a built-in REST API from Meteobridge to retrieve current data for a local WeatherStation

[*Meteobridge*](https://www.meteobridge.com/wiki/index.php/Home) is a small device that connects your personal weather station to public weather networks like "Weather Underground". This allows you to feed your micro climate data to a weather network in the Internet and to have it there visible from wherever you are. Meteobridge also has many ways of delivering data to your local network, and this furthermore reduces the dependencies for Cloud Services when you need very local Weather Data.

Meteobridge can be delivered as complete HW and SW packages, or there is a SW solution that you then can install yourself on specific HW.

There is support for the following devices types within Home Assistant:
* Sensor
  * A whole range of individual sensors will be available. for a complete list of the sensors, see the list below.
* Binary Sensor
  * A few binary sensors will be available, that can be used to trigger automations, if f.ex. it starts raining.

If you want to have a *Weather Entity* that combines your local realtime weather data with forecast data, I recommend you look at the [Weather Template](https://www.home-assistant.io/integrations/weather.template/) that does exactly that, and here you are free to choose from all the available Weather Integrations in Home Assistant.

## Table of Contents

1. [Installation](#installation)
    * [HACS Installation](#hacs-installation)
    * [Manuel Installation](#manuel-installation)
2. [Configuration](#configuration)
    * [Configuration Options](#configuration-options)
3. [Available Sensors](#available-sensors)
4. [Available Binary Sensors](#available-binary-sensors)
5. [Enable Debug Logging](#enable-debug-logging)
6. [Contribute to Development](#contribute-to-the-project-and-developing-with-a-devcontainer)
    * [Integration](#integration)
    * [Frontend](#frontend)

## Installation

### HACS Installation
This Integration is part of the default HACS store, so search for *Meteobridge Dalogger* in HACS.

### Manual Installation

To add Meteobridge to your installation, create this folder structure in your /config directory:

`custom_components/meteobridge`.

Then, drop the following files into that folder:

```yaml
__init__.py
binary_sensor.py
config_flow.py
const.py
entity.py
manifest.json
models.py
sensor.py
translation (Directory with all files)
```

## Configuration
To add Meteobridge to your installation, do the following:
- Go to *Configuration* and *Integrations*
- Click the `+ ADD INTEGRATION` button in the lower right corner.
- Search for Meteobridge and click the integration.
- When loaded, there will be a configuration box, where you have to enter your *Logger IP Address*, *Logger Username*  and a *Logger Password* to get access to your data. When entered click *Submit* and the Integration will load all the entities.

If you want to change the update frequencies for the realtime data and number of extra sensors, then click `CONFIGURE` in the lower left corner of the Meteobridge integration, after the Integration is loaded the first time.

You can configure more than 1 instance of the Integration by using a different IP Address.

### Configuration Options
* `ip_address`: (required) IP Address of the Meteobridge device.
* `username`: (required) The username to login to your Meteobridge device. Default this *meteobridge*.
* `password`: (required) The password for your meteobridge device.
* `update_interval`: (optional) The interval in seconds between updates. (Default 60 seconds, min 15 and max 120)
* `extra_sensors`: (optional) Number of extra sensors attached to the Meteobridge Logger (Default is 0, max is 7)

## Available Sensors

Here is the list of sensors that the program generates. Calculated Sensor means, if No, then data comes directly from the Meteobridge Datalogger, if yes, it is a sensor that is derived from some of the other sensors.

As there can be many different types of Personal Weather Stations attached to a Meteobridge Datalogger, and not all of them have all types of sensors, only sensors that are providing values will be created in Home Assistant. If you later attach a new Sensor or a new Weather Station type to your Datalogger, just restart the Integration.

There is also the possibility to attach extra sensors to a Meteobridge Datalogger. If you have extra sensors attached, click on the Configure button on the Integration page and tell the Integration how many you have, and some data for these sensors will be loaded.

All entities are prefixed with `meteobridge` and names are prefixed with `Meteobridge`

| Sensor ID   | Name   | Description   | Calculated Sensor   |
| --- | --- | --- | --- |
| air_quality_pm1 | Air Quality PM1| Count of ultrafine particles with an aerodynamic diameter less than 1 micrometers | No |
| air_quality_pm10 | Air Quality PM10 | Count of particles having an aerodynamic diameter of less than 10 micrometers | No |
| air_quality_pm25 | Air Quality PM2.5 | Count of particles with an aerodynamic diameter less than 2.5 micrometers | No |
| air_temperature | Air Temperature | Outside Temperature | No |
| air_temperature_dmin | Air Temperature Day Min | Minimum Outside Temperature this day | No |
| air_temperature_dmax | Air Temperature Day Max | Maximum Outside Temperature this day | No |
| air_temperature_mmin | Air Temperature Month Min | Minimum Outside Temperature this month | No |
| air_temperature_mmax | Air Temperature Month Max | Maximum Outside Temperature this month | No |
| air_temperature_ymin | Air Temperature Year Min | Minimum Outside Temperature this year | No |
| air_temperature_ymax | Air Temperature Year Max | Maximum Outside Temperature this year | No |
| beaufort | Beaufort Scale | Beaufort scale is an empirical measure that relates wind speed to observed conditions at sea or on land | Yes ||
| beaufort_description | Beaufort Description | A descriptive text for the current Beaufort level. | Yes ||
| dewpoint | Dew Point | Dewpoint in degrees | No |
| feels_like_temperature | Feels Like Temperature | The apparent temperature, a mix of Heat Index and Wind Chill | Yes |
| heat_index | Heat Index | How warm does it feel? | No |
| lightning_strike_count | Lightning Count | Number of lightning strikes in the last minute | No |
| lightning_strike_last_distance | Lightning Distance | Distance of the last strike | No |
| lightning_strike_last_epoch | Last Lightning Strike | When the last lightning strike occurred | No |
| precipitation_rate | Rain Rate | How much is it raining right now | Yes |
| precipitation_today | Rain Today | Total rain for the current day. (Reset at midnight) | No |
| pressure_trend | Pressure Trend | Returns Steady, Falling or Rising determined by the rate of change over the past 3 hours| No |
| relative_humidity | Humidity | Relative Humidity | No |
| sealevel_pressure | Station Pressure | Preasure measurement at Sea Level | No |
| station_forecast | Station Forecast | A textual Forecast String (Davis Vantage Stations only) | No |
| station_pressure | Station Pressure | Pressure measurement where the station is located | No |
| temperature_trend | Temperature Trend | Returns Steady, Falling or Rising determined by the rate of change over the past 3 hours| No |
| solar_radiation | Solar Radiation | Electromagnetic radiation emitted by the sun | No |
| uv | UV Index | The UV index | No |
| uv_description | UV Description | A descriptive text for the current UV index | Yes |
| visibility | Visibility | Distance to the horizon | Yes |
| wind_cardinal | Wind Cardinal | Current measured Wind bearing as text | Yes |
| wind_chill | Wind Chill | How cold does it feel? | No |
| wind_direction | Wind Direction | Current measured Wind bearing in degrees | No |
| wind_gust | Wind Gust | Highest wind speed for the last minute | No |
| wind_Speed | Wind Speed | Average wind speed for the last minute | No |

## Available Binary Sensors

Here is the list of binary sensors that the program generates. These sensors are all calculated based on values from other sensors

All entities are prefixed with `meteobridge` and names are prefixed with `Meteobridge`

| Sensor ID   | Name   | Description   |
| --- | --- | --- |
| is_freezing | Is Freezing | Is the Temperature below freezing point |
| is_raining | Is Raining | Is it raining outside |
| is_battery_low | Is Battery Low | Is Meteobridge Battery Low |

## Enable Debug Logging

If logs are needed for debugging or reporting an issue, use the following configuration.yaml:

```yaml
logger:
  default: error
  logs:
    custom_components.meteobridge: debug
```

## CONTRIBUTE TO THE PROJECT AND DEVELOPING WITH A DEVCONTAINER

### Integration

1. Fork and clone the repository.
2. Open in VSCode and choose to open in devcontainer. Must have VSCode devcontainer prerequisites.
3. Run the command container start from VSCode terminal
4. A fresh Home Assistant test instance will install and will eventually be running on port 9125 with this integration running
5. When the container is running, go to http://localhost:9125 and the add Meteobridge from the Integration Page.

### Frontend

There are some sensors in this integration that provides a text as state which is not covered by the core Frontend translation. Example: `sensor.meteobridge_pressure_tend`, `sensor.meteobridge_uv_description` and `sensor.meteobridge_beaufort_description`.

As default the text in the Frontend is displayed in english if your language is not present in this integration, but if you want to help translate these texts in to a new language, please do the following:
- Go to the `translations` directory under `custom_components/meteobridge` and copy the file `sensor.en.json` to `sensor.YOUR_LANGUAGE_CODE.json` in a directory on your computer.
- Edit the file and change all the descriptions to your language.
- Make a Pull request in this Github and attach your new file.

The same procedure applies for the Configuration flow, follow the above procedure, just copy `en.json` to `YOUR_LANGUAGE_CODE.json`.
