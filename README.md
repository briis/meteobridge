# // Meteobridge Datalogger for Home Assistant
![GitHub release](https://img.shields.io/github/release/briis/meteobridge.svg?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square)](https://github.com/custom-components/hacs) [![](https://img.shields.io/badge/COMMUNITY-FORUM-success?style=flat-square)](https://community.home-assistant.io/t/meteobridge-weather-logger-integration/154263)

The Meteobridge Integration adds support for retrieving data from a Meteobridge datalogger. It uses a built-in REST API from Meteobridge to retrieve current data for a local WeatherStation

**NOTE:** This integration replaces [MBWeather](https://github.com/briis/mbweather), which will no longer be maintained

[*Meteobridge*](https://www.meteobridge.com/wiki/index.php/Home) is a small device that connects your personal weather station to public weather networks like "Weather Underground". This allows you to feed your micro climate data to a weather network in the Internet and to have it there visible from wherever you are. Meteobridge also has many ways of delivering data to your local network, and this furthermore reduces the dependencies for Cloud Services when you need very local Weather Data.<br>
Meteobridge can be delivered as complete HW and SW packages, or there is a SW solution that you then can install yourself on specific HW.<br>

There is support for the following devices types within Home Assistant:
* Sensor
* Binary Sensor

If you want to have a *Weather Entity* that combines your local realtime weather data with forecast data, I recommend you look at [@xannor Integration](https://github.com/xannor/hass_weather_template) that does exactly that, and here you are free to choose from all the available Weather Integrations in Home Assistant.

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

**Username**<br>
&nbsp;&nbsp;*(string)(Required)*<br>
&nbsp;&nbsp;Specify Datalogger username.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;meteobridge

**Password**<br>
&nbsp;&nbsp;*(string)(Required)*<br>
&nbsp;&nbsp;Specify Datalogger password.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;None

**Wind Unit**<br>
&nbsp;&nbsp;*(string)(Required)*<br>
&nbsp;&nbsp;Select the Wind Unit to be used. Values are: *m/s*, *mps* and *km/h*

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;*m/s* if Metric Units else *mph*

**Rain Unit**<br>
&nbsp;&nbsp;*(string)(Required)*<br>
&nbsp;&nbsp;Select the Rain Unit to be used. Values are: *mm* and *in*

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;*mm* if Metric Units else *in*

**Pressure Unit**<br>
&nbsp;&nbsp;*(string)(Required)*<br>
&nbsp;&nbsp;Select the Pressure Unit to be used. Values are: *hPa*, *inHg* and *mb*

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;*hPa* if Metric Units else *inHg*

**Distance Unit**<br>
&nbsp;&nbsp;*(string)(Required)*<br>
&nbsp;&nbsp;Select the Distance Unit to be used. Values are: *km* and *mi*

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;*km* if Metric Units else *mi*

**Scan Interval**<br>
&nbsp;&nbsp;*(integer)(Optional)*<br>
&nbsp;&nbsp;Specify how often data is pulled from Meteobridge.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;10 (seconds)

**Language**<br>
&nbsp;&nbsp;*(string)(Optional)*<br>
&nbsp;&nbsp;The language used for specific values. See below for currently supported languages.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;en (English)

**Extra Sensors**<br>
&nbsp;&nbsp;*(int)(Optional)*<br>
&nbsp;&nbsp;Select a number between 0 and 2 to add extra Temperature/Humidity/Heat Index sensors to the system. Requires that you have these sensors up and running on the Weather Station.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;0

### Supported languages
Here is the list of languages that Meteobridge can return strings in:
* da - Danish
* de - German
* fr - French
* en - English
* es - Spanish
* it - Italian
* nb - Norwegian Bokmål
* nl - Dutch
* pl - Polish
* pt - Portuguese
* sv - Swedish

### BINARY SENSORS
The following Binary Sensors are created in Home Assistant

All Binary Sensors will be prefixed with `binary_sensor.meteobridge_`

* **is_raining** - A sensor indicating if it is currently raining
* **is_freezing** - A sensor indicating if it is currently freezing outside.
* **is_lowbat** - A sensor indicating if the attached Weather Station is running low on Battery

### SENSOR
The following Sensors are created in Home Assistant

All Sensors will be prefixed with `sensor.meteobridge_`

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
* **lightning_count** - Number of Lightning strokes for the current day
* **lightning_energy** - Energy of the last stroke. There is not a unit for this, but the bigger the number the more energy in the lightning.
* **lightning_distance** - The distance of the last lihgtning stroke.
* **air_pollution** - Air pollution measured in µg per m3
* **beaufort_value** - The value on the [Beaufort Scale](https://www.rmets.org/resource/beaufort-scale) based on wind speed in m/s
* **beaufort_text** - The text representation of the Beaufort Value in local language (If language is supported)
* **temperature_trend** Shows the temperature trend for the last 10 minutes. State is the actual value, and units is either *falling*, *rising* or *steady*.
* **pressure_trend** Shows the pressure trend for the last 10 minutes. State is the actual value, and units is either *falling*, *rising* or *steady*.
* **forecast** - A string with the current weather forecast, delivered by the local Weather Station. **Note:** Not all Weather Station will deliver this. I only know of the Davis Weather Stations for now.
* **temperature_2** - Current temperature for sensor 2 (If installed)
* **humidity_2** - Current humidity in % for sensor 2 (If installed)
* **heatindex_2** - How warm it feals. Only valid if temperature is above 26.67°C (80°F) for sensor 2 (If installed)
* **temperature_3** - Current temperature for sensor 3 (If installed)
* **humidity_3** - Current humidity in % for sensor 3 (If installed)
* **heatindex_3** - How warm it feals. Only valid if temperature is above 26.67°C (80°F) for sensor 3 (If installed)
