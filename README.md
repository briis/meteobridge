# Meteobridge Weather for Home Assistant
![GitHub release](https://img.shields.io/github/release/briis/mbweather.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

This a *Custom Integration* for [Home Assistant](https://www.home-assistant.io/). It combines real-time weather readings from a Meteobridge Weather Logger and Forecast data from *Dark Sky*.

[*Meteobridge*](https://www.meteobridge.com/wiki/index.php/Home) is a small device that connects your personal weather station to public weather networks like "Weather Underground". This allows you to feed your micro climate data to a weather network in the Internet and to have it there visible from wherever you are. Meteobridge also has many ways of delivering data to your local network, and this furthermore reduces the dependencies for Cloud Services when you need very local Weather Data.<br>
Meteobridge can be delivered as complete HW and SW packages, or there is a SW solution that you then can install yourself on specific HW.<br>
If you have any Davis Weatherstation I would recommend the Meteobridge Nano SD solution or else the Meteobridge PRO solution. 

This Custom Integration consist of 4 parts:
1. The main component which sets up the link to the Meteobridge Data Logger
2. A *Binary Sensor* component, that gives a couple of binary sensors, derived from the data delivered
3. A *Sensor* component delivering realtime data from the Data Logger
4. A Home Assistant *Weather* component, that retrieves Forecast data from *Dark Sky* and then replaces Dark Skys current data with the data from the local weatherstation

The `mbweather` component uses a built-in REST API from Meteobridge to retrieve current data for a local WeatherStation, which means that if you don't use the *Weather* component, everything is running inside your local network

## Requirements
This Custom Integration requires that you have a *Meteobridge HW Device* connected to a Weather Station on your local Network.

## Manual Installation
To add MBWEATHER to your installation, create this folder structure in your /config directory:

`custom_components/mbweather`.
Then, drop the following files into that folder:

```yaml
__init__.py
manifest.json
sensor.py
binary_sensor.py
weather.py
```

## HACS Installation
This Integration is part of the default HACS store, so search for *Meteobridge Weather* in HACS.

## Configuration
Start by configuring the core platform. No matter which of the entities you activate, this has to be configured. The core platform by itself does nothing else than fetch the current data from *Meteobridge*, so by activating this you will not see any entities being created in Home Assistant.

Edit your *configuration.yaml* file and add the *mbweather* component to the file:
```yaml
# Example configuration.yaml entry
mbweather:
  host: <ip address of your Meteobridge Logger>
  username: <your Meteobridge username>
  password: <Your Meteobridge Password>
  use_ssl: <false or true>
```
**host**:<br>
(string)(Required) Type the IP address of your *Meteobridge Logger*. Example: `192.168.1.10`<br>

**username**:<br>
(string)(Required) In order to access data on the *Meteobridge Data Logger* you will need the username and password you use to login with. Username will typically be **meteobridge**<br>

**password**<br>
(string)(Required) The password you are using to access your *Meteobridge Data Logger*.

**use_ssl**<br>
(string)(Optional) Type `True` if you access your Data Logger with *https*.<br>
Default value: False

### Binary Sensor
In order to use the Binary Sensors, add the following to your *configuration.yaml* file:
```yaml
# Example configuration.yaml entry
binary_sensor:
  - platform: mbweather
    monitored_conditions:
      - raining
      - freezing
      - lowbattery
```
#### Configuration Variables
**name**<br>
(string)(Optional) Additional name for the sensors.<br>
Default value: mbw

**monitored_conditions**<br>
(list)(optional) Sensors to display in the frontend.<br>
Default: If ommitted all Sensors are displayed
* **raining** - A sensor indicating if it is currently raining
* **freezing** - A sensor indicating if it is currently freezing outside.
* **lowbattery** - A sensor indicating if the attached Weather Station is running low on Battery

### Sensor
In order to use the Sensors, add the following to your *configuration.yaml* file:
```yaml
# Example configuration.yaml entry
sensor:
  - platform: mbweather
    wind_unit: kmh
    monitored_conditions:
      - temperature
      - temphigh
      - templow
      - dewpoint
      - windchill
      - heatindex
      - feels_like
      - windspeedavg
      - windspeed
      - windbearing
      - winddirection
      - windgust
      - raintoday
      - rainrate
      - humidity
      - pressure
      - uvindex
      - solarrad
      - in_temperature
      - in_humidity
      - condition
      - precip_probability
      - temp_mmin
      - temp_mmax
      - temp_ymin
      - temp_ymax
      - windspeed_mmax
      - windspeed_ymax
      - rain_mmax
      - rain_ymax
      - rainrate_mmax
      - rainrate_ymax
      - forecast
```
#### Configuration Variables
**wind_unit**<br>
(string)(optional) If Home Assistant Unit System is *metric*, specify `kmh` to get units in km/h. Else this has no effect.<br>
Default Value: m/s if Home Assistant Unit System is *metric*, and mph if Unit System is *imperial*

**name**<br>
(string)(Optional) Additional name for the sensors.<br>
Default value: mbw

**monitored_conditions**<br>
(list)(optional) Sensors to display in the frontend.<br>
Default: All Sensors are displayed
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
* **condition** - Current condition state. Only supplies data if the `weather` component is activated.
* **precip_probability** - Precipitation probability for the day. Only supplies data if the `weather` component is activated.
* **temp_mmin** - Current month minimum outdoor temperature
* **temp_mmax** - Current month maximum outdoor temperature
* **temp_ymin** - Current year minimum outdoor temperature
* **temp_ymax** - Current year maximum outdoor temperature
* **windspeed_mmax** - Current month maximum wind speed
* **windspeed_ymax** - Current year maximum wind speed
* **rain_mmax** - Current month accumulated rain
* **rain_ymax** - Current year accumulated rain
* **rainrate_mmax** - Current month maximum rain rate
* **rainrate_ymax** - Current year maximum rain rate
* **forecast** - A string with the current weather forecast, delivered by the local Weather Station. **Note:** Not all Weather Station will deliver this. I only know of the Davis Weather Stations for now.

### Weather
The Weather Entity uses Dark Sky for forecast data. So in order to use this Entity you must obtain a API Key from Dark Sky. The API key is free but requires registration. You can make up to 1000 calls per day for free which means that you could make one approximately every 86 seconds.

The difference between using this entity and the standard Dark Sky entity, is that *Current* data is coming from the local weather station, making it much more accurate than that what Dark Sky delivers.

On top of the standard attributes that a weather entity has available, the following additional attributes have been added to this Weather Entity: *Rain Today and Rain Rate*. These are all *Current* values.

In order to use the Weather component, add the following to your *configuration.yaml* file:
```yaml
# Example configuration.yaml entry
weather:
  - platform: mbweather
    api_key: <Your Dark Sky API key>
```
#### Configuration Variables
**api_key**<br>
(string)(Required) Your Dark Sky API key.<br>
**name**<br>
(string)(Optional) Additional name for the sensors.<br>
Default value: mbw<br>
**mode**<br>
(string)(Optional) *hourly* for hour based forecast, and *daily* for day based forecast<br>
Default value: hourly
