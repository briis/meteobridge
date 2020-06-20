## // CHANGELOG

### V2.3

* Added two Beaufort Sensors, one with the Beaufort Scale Value `bft_value` and one with the textual representation of that value `bft_text`. Default the text is in english but if you set the Language code under *Options* or during Installation, then this text will be translated. Not all languages are supported yet, but if you are missing a language [go here](https://github.com/briis/pymeteobridgeio/tree/master/pymeteobridgeio/translations) and take one of the files, and make your translation to your language. Either make a PR or send me the file. The same goes if you find errors in any of the translations.
* As with above, the Wind Direction string `sensor.winddirection` is now also translated to local language, if a language is set. Default is English.

### V2.2

* Added Air pollution sensor - Air pollution measured in µg per m3
* Bumped pymeteobridgeio to 0.17

### V2.1

* Added Lightning Sensors - Count, Distance and Energy
* Changed Attribution to Powered by Meteobridge
* Changed the Miles per Hour unit definition from mi/h to mph
* Bumped pymeteobridgeio to 0.15
