# Pico micropython

## Getting started:
1.  Rename the "config copy.py" to "config.py" and populate with the specified values.

## Using
Upload all files to the Pico W pre flushed with micropython.
Run the main file manually or re plug the Pico W and it will run the main file automatically.

Note: There is no error correcting for handling no, or bad, mqtt server.

## IO
* Sensors 
    * Integrated thermostat
* Trigger
    * MQTT protocol
* Output
    * Integrated lamp
    * MQTT protocol

# Intro

This part of the project communicates with a server over MQTT to send temperature data for further processing. The onboard lamp can be toggled from the server, also over MQTT. Furthermore, the program logs a CSV formatted entry of the temperature reading together with a timestamp and saves it locally. The number of entries saved can be configured in the "Config.py".

This approach allows for bidirectional communication and rolling updates. The lamp acts as a placeholder for whatever functionality that is needed and is isolated in a callback for a mqtt-topic on which the Pico W is listening. As of now a “toggle” callback is implemented which, as implicated, toggles the lamps state from on to off and vice versa.

Every cycle of the main loop checks whether the latest entry of the temperature log is within a prespecified time interval compared to the time of the cycle. If the interval is overstepped, the log is updated, and the reading sent to the MQTT-server for processing. The functionality of reading and updating the log would benefit from being in a separate thread to the main one. If done that way, performance would drastically be boosted, and thus reduce energy consumption.

The choice of writing the program in micropython is beneficial in the case of delivering a program quickly, but with a wider time frame C/C++ could be a better choice for efficiency and freedom in formatting the program. Stability feathers like, error handling and reconnection wifi and mqtt are to must haves. Other things that could be done with a wider time frame is adding more entries to feathers like the ones that can be found in this project. 


For pin mapping please refer to following documentation,
[Pico Map](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf)

Gates like 'and', 'or' and 'inverter' can be found scattered throughout the code.
## TOD
* Error handling for, "fail to connect to MQTT server".

