# // Meteobridge Datalogger for Home Assistant
![GitHub release](https://img.shields.io/github/release/briis/meteobridge.svg?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square)](https://github.com/custom-components/hacs)

The Meteobridge Integration adds support for retrieving data from a Meteobridge datalogger. It uses a built-in REST API from Meteobridge to retrieve current data for a local WeatherStation

**NOTE:** This integration replaces [MBWeather](https://github.com/briis/mbweather), which will no longer be maintained

[*Meteobridge*](https://www.meteobridge.com/wiki/index.php/Home) is a small device that connects your personal weather station to public weather networks like "Weather Underground". This allows you to feed your micro climate data to a weather network in the Internet and to have it there visible from wherever you are. Meteobridge also has many ways of delivering data to your local network, and this furthermore reduces the dependencies for Cloud Services when you need very local Weather Data.<br>
Meteobridge can be delivered as complete HW and SW packages, or there is a SW solution that you then can install yourself on specific HW.<br>

There is support for the following devices types within Home Assistant:
* Sensor
* Binary Sensor

## BREAKING
Sensors and configuration options have changed a lot, so if you already have this Integration installed with a lower version number than 2.0, you **must** remove it first and restart Home Assistant.
I am sorry for this, but I believe that the Integration is now where I need it to be, so from now on, I should not need to change the basic structures.

## Requirements
This Custom Integration requires that you have a *Meteobridge HW Device* connected to a Weather Station on your local Network.

## Installation

### HACS Installation
This Integration is part of the default HACS store, so search for *Meteobridge Dalogger* in HACS.

### Manual Installation

To add Meteobridge to your installation, create this folder structure in your /config directory:

`custom_components/meteobridge`.
Then, drop the following files into that folder:

```yaml
__init__.py
manifest.json
sensor.py
binary_sensor.py
config_flow.py
const.py
entity.py
string.json
translation (Directory with all files)
```

## Configuration
To add Meteobridge to your installation, go to the Integrations page inside the configuration panel and add a Datalogger by providing the IP Address, Username, Password and optional name and unit system to be used.

If the Datalogger is found on the network it will be added to your installation. After that, you can add additional Dataloggers if you have more than one in your network.

**You can only add Meteobridge through the integrations page, not in configuration files.**

### CONFIGURATION VARIABLES
**IP Address**<br>
&nbsp;&nbsp;*(string)(Required)*<br>
&nbsp;&nbsp;Specify the IP Address of your Datalogger.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;None

**username**<br>
&nbsp;&nbsp;*(string)(Required)*<br>
&nbsp;&nbsp;Specify Datalogger username.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;meteobridge

**password**<br>
&nbsp;&nbsp;*(string)(Required)*<br>
&nbsp;&nbsp;Specify Datalogger password.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;None

### BINARY SENSORS
The following Binary Sensors are created in Home Assistant

* **is_raining** - A sensor indicating if it is currently raining
* **is_freezing** - A sensor indicating if it is currently freezing outside.
* **is_lowbat** - A sensor indicating if the attached Weather Station is running low on Battery

### SENSOR
The following Sensors are created in Home Assistant

* **temperature** - Current temperature
* **temphigh** - Highest temperature meassured today
* **templow** - Lowest temperature meassured today
* **dewpoint** - Dewpoint. The atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form
* **windchill** - How cold does it feel. Only valid if temperature is below 10°C (50°F)
* **heatindex** - How warm it feals. Only valid if temperature is above 26.67°C (80°F)
* **feels_like** - How the temperature is feeling.
* **windspeedavg** - Average Wind Speed in the last 10 minuttes
* **windspeed** - Current Wind Speed
* **windbearing** - Wind bearing in degrees (Example: 287°)
* **winddirection** - Wind bearing as directional text (Example: NNW)
* **windgust** - Highest Wind Speed in the last minute
* **raintoday** - Precipitation since midnight
* **rainrate** - The current precipitation rate - 0 if it is not raining
* **humidity** - Current humidity in %
* **pressure** - Current barometric pressure, taking in to account the position of the station
* **uvindex** - Current UV Index
* **solarrad** - Current Solar Radiation meassured in W/m2
* **in_temperature** - Temperature meassured by the Meteobridge Logger (indoor)
* **in_humidity** - Humidity meassured by the Meteobridge Logger (indoor)
* **temp_month_min** - Current month minimum outdoor temperature
* **temp_month_max** - Current month maximum outdoor temperature
* **temp_year_min** - Current year minimum outdoor temperature
* **temp_year_max** - Current year maximum outdoor temperature
* **wind_month_max** - Current month maximum wind speed
* **wind_year_max** - Current year maximum wind speed
* **rain_month_max** - Current month accumulated rain
* **rain_year_max** - Current year accumulated rain
* **rainrate_month_max** - Current month maximum rain rate
* **rainrate_year_max** - Current year maximum rain rate
* **forecast** - A string with the current weather forecast, delivered by the local Weather Station. **Note:** Not all Weather Station will deliver this. I only know of the Davis Weather Stations for now.
