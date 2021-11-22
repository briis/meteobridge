# Change Log

## [2.6.3]

* `NEW`: Added `sensor.meteobridge_absolute_pressure` as a new sensor, displaying the absolute or also called station pressure, as opposed to the calculated Sealevel Pressure.
* `NEW`: Added the option of having up to 7 additional sensors defined. This is the maximum supported by Meteobridge. The extra sensors are named `sensor.temperature_2`, `sensor.humidity_2` and `sensor.heatindex_2` up til `_8`.


## [2.6.2]

* `FIXED`: Added **iot_class** to `manifest.json` as required by Home Assistant 2021.5.x
* `CHANGED`: Several files to ensure future compatability with Home Assistant 2021.5.x

## [2.6.1]

* `FIXED`: Added version number to `manifest.json` as required by Home Assistant 2021.3.x


## [2.6]

* Added Domain name as Prefix to all sensors, so that if you make a new installation, the sensors will be called `sensor.meteobridge_SENSOR_NAME` and `binary_sensor.meteobridge_SENSOR_NAME`. If you allready have a running installation, `entity_id` will NOT change, only for new installations.
* Added new Sensor `sensor.meteobridge_temperature_trend` which shows the temperature trend for the last 10 minutes. State is the actual value, and units is either *falling*, *rising* or *steady*. (In local language if available)
* Added new Sensor `sensor.meteobridge_pressure_trend` which shows the pressure trend for the last 10 minutes. State is the actual value, and units is either *falling*, *rising* or *steady*. (In local language if available)

## [2.5]

**BREAKING CHANGE** This release adds the possibility to select individual units for each type of measurement. However, in order to set this up, the current Integration needs to be removed and then re-added. If you have not renamed any of the sensors, this should not be a problem. If you have them renamed, you will have to re-apply that after the installation.

With this release you will now have the option of selecting different units for the different sensor types. These units will be used regardless of the Unit System you have chosen in Home Assistant.

The following are the available options:
* **Wind**: m/s (Meters per second), mph (Miles per hour) or km/h (Kilometers per hour)
* **Rain**: mm (millimeter) and in (Inches)
* **Pressure**: hPa (Hectopascal), inHg (Inches Mercury) and mb (Millibar - Same value as hPa)
* **Distance**: km (Kilometer) and mi (Miles)

Temperature Unit cannot be set by this Integration due to the way Home Assistant works. If it spots a value with `unit_of_measurement` set to either °C or °F it will automatically convert it to the unit set by your user profile. Celcius if you have selected Metric Units or Fahrenheit if you have selected Imperial. So the only way to change this, is to change the overall Unit System. Hopefully we will have more freedom on this in the future.

**Upgrade Instructions**
1. Go to *Settings* and select the *Integration* menu.
2. Find *Meteobridge Datalogger* and press the three dots in the lower right corner and press *remove*.
  **Note** If you have more than one Datalogger set up, yu must repeat this for each of them.
3. Go to HACS, and install the V2.5 Upgrade
4. Restart Home Assistant
5. Go back to the Integration menu and install Meteobridge again.
6. During Installation you will be asked which units you want to display data in, for the different unit types and you can also change this under *Options* later should you want to do so.

## [2.4.1]
* Added better error handling in the IO module to ensure Integration does not crash when Meteobridge is unreachable.
* Added link to Github Issues in Manifest.
* Bumped pymeteobridgeio to 0.20.3

## [2.4]
* Some people have extra Temperature/Humidity sensors attached to their Weather Station. This release adds support for up to 2 extra sensors. During setup of the Integration or by pressing the *Options* menu on the Integration Widget, it is now possible to select from 0 to 2 extra sensors. The extra sensors are named `sensor.temperature_2`, `sensor.humidity_2` and `sensor.heatindex_2` if one extra sensor is selected. If two are selected the *_2* will be *_3*.

  NOTE: If you go back to a lower number, the extra sensors are not being deleted, they will show up as *unavailable* so you will have to delete them manually on the *Entities* page.

## [2.3]

* Added two Beaufort Sensors, one with the Beaufort Scale Value `bft_value` and one with the textual representation of that value `bft_text`. Default the text is in english but if you set the Language code under *Options* or during Installation, then this text will be translated. Not all languages are supported yet, but if you are missing a language [go here](https://github.com/briis/pymeteobridgeio/tree/master/pymeteobridgeio/translations) and take one of the files, and make your translation to your language. Either make a PR or send me the file. The same goes if you find errors in any of the translations.
* As with above, the Wind Direction string `sensor.winddirection` is now also translated to local language, if a language is set. Default is English.
* Added the possibility to change Language and Scan Interval from the Integration Widget after installation. Click on *Options* on the widget to change these settings without restarting Home Assistant.
* Bumped pymeteobridgeio to V0.19.1 which includes the new sensors and translations

## [2.2]

* Added Air pollution sensor - Air pollution measured in µg per m3
* Bumped pymeteobridgeio to 0.17

## [2.1]

* Added Lightning Sensors - Count, Distance and Energy
* Changed Attribution to Powered by Meteobridge
* Changed the Miles per Hour unit definition from mi/h to mph
* Bumped pymeteobridgeio to 0.15
