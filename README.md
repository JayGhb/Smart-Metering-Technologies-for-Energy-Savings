# Smart Metering Technologies for Energy Savings
My Thesis for the School of Informatics, Aristotle University of Thessaloniki, Greece.

The document is composed in Greek, except for the abstract which is provided below.
The devices mentioned throughout the document are the RaspberryPi based [EmonPi](https://github.com/openenergymonitor/emonpi) and the Arduino based [EmonTx](https://github.com/openenergymonitor/emontx3) from the [Openenergymonitor](https://openenergymonitor.org/) open source organization.

The main points of the project could be summarized to:
* Install and use the Openenergymonitor devices, EmonPi & EmonTx.
* Set up a local database server
* Redirect data collected from the Emon devices to the local database
* Create a RESTful API in Python for the local database
* Create a minimal Air-Condition detection application generating [Tweets](https://twitter.com/TNodered) when AC is detected (extra task)

## Abstract
>Energy conservation refers to reducing energy consumption through using less of a high-consuming device in everyday life. This action is of great importance for planet Earth in general as well as for every individual human looking to save wealth. However, applying energy conservation in everyday life does not necessarily mean holding back in services provided by such machines. The subject of this thesis project is the technical part of installing and expanding an energy monitoring system of a smaller scale than an actual comercial one, for educational purpose. The “lifecycle” of an IoT device system is presented, regarding the stages of collecting, saving and accessing data. Finally, experiments where conducted using the installed monitoring system and a prototype AC-detection application was developed, using their results.

### Chapters overview
1. Introduction
1. Reference to energy metering technologies through the recent years
1. Importance of data collection, saving, retrieval on Smart Homes
1. Tools used on this project
1. Devices' , applications' and database's architecture
1. Detailed project implementation
1. Epilogue, results, (possible) future work
