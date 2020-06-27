## // CHANGELOG

### V2.4
* Some people have extra Temperature/Humidity sensors attached to their Weather Station. This release adds support for up to 2 extra sensors. During setup of the Integration or by pressing the *Options* menu on the Integration Widget, it is now possible to select from 0 to 2 extra sensors. The extra sensors are named `sensor.temperature_2`, `sensor.humidity_2` and `sensor.heatindex_2` if one extra sensor is selected. If two are selected the *_2* will be *_3*.

  NOTE: If you go back to a lower number, the extra sensors are not being deleted, they will show up as *unavailable* so you will have to delete them manually on the *Entities* page.

### V2.3

* Added two Beaufort Sensors, one with the Beaufort Scale Value `bft_value` and one with the textual representation of that value `bft_text`. Default the text is in english but if you set the Language code under *Options* or during Installation, then this text will be translated. Not all languages are supported yet, but if you are missing a language [go here](https://github.com/briis/pymeteobridgeio/tree/master/pymeteobridgeio/translations) and take one of the files, and make your translation to your language. Either make a PR or send me the file. The same goes if you find errors in any of the translations.
* As with above, the Wind Direction string `sensor.winddirection` is now also translated to local language, if a language is set. Default is English.
* Added the possibility to change Language and Scan Interval from the Integration Widget after installation. Click on *Options* on the widget to change these settings without restarting Home Assistant.
* Bumped pymeteobridgeio to V0.19.1 which includes the new sensors and translations

### V2.2

* Added Air pollution sensor - Air pollution measured in µg per m3
* Bumped pymeteobridgeio to 0.17

### V2.1

* Added Lightning Sensors - Count, Distance and Energy
* Changed Attribution to Powered by Meteobridge
* Changed the Miles per Hour unit definition from mi/h to mph
* Bumped pymeteobridgeio to 0.15
