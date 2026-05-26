# Hamulight Apex L2446

The Hamulight Apex L2446 has four buttons and a touch ring, which is not in use (cost savings I guess).

The remote is maintaining some state on it's own without feedback channel. You realize this when you press the ON/OFF key and in state ON you can use the UP/DOWN keys but not in OFF mode. I quickly realized that it's also sending different signals for this states, which is good, since for a toggle you never know the real state of a device.
The remote has a [BS84B08C](https://www.holtek.com/page/vg/BS84B08C_C12C) microcontroller and a [BC2102](https://www.holtek.com/page/vg/bc2102) capable of OOK/FSK transmitting.

I did some intesive analysis of the remotes signal with [URH](https://github.com/jopohl/urh). After some diving into the RF world I figured the Hamulight Apex L2446 remote uses a FSK encoding on 433.92MHz with a 27kHz deviation. Basically I recorded a signal, applied a bandpass filter with 62.5kHz and used "Autodetect parameters" to get the code.

Further analysis of the signals revealed that the dimming status for each step was also different. At the end of the day I figured the whole flow and that the light (or better the transformer) can handle states from 0 to 255 which gives a perfect setup for ESPhome and Homeassistant.

## Usage for ESPhome and Homeassistant

### Hardware

* CC1101 - for FSK encoding you can't use F1000A or RTX882
* Any ESP or ESP32 that is capable of handling a CC1101 

You need all eight pins to wire up the CC1101 with a ESP for best usage. Check the layout used in the YAML file or adjust the YAML accordingly. I used one of this classic cheap MCU ESP devices.

### Software

You can create a complete new device in ESPhome and copy & paste the YAML content and adjust the light name. My `generic.yaml` references other ota, time, wifi, api and webserver YAML files. Nothing with special settings.

### Key detection (if you have a L2446 remote)

The `rf_key: "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"` is a placeholder. Once your device is running, press the ON/OFF button on your remote and you will see something like the below in the log (hopefully):

```log
[13:46:38.681][W][HAMULIGHT_SNIFFER:151]: Foreign remote control detected! Key for YAML:
[13:46:38.686][W][HAMULIGHT_SNIFFER:152]: rf_key: "1,1,1,1,1,0,1,1,1,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1"
```

You should have six entries like this and there is a high chance the rf_key is always the same. If not, use the one which appears the most. Take the rf_key and update the YAML accordingly and flash the update. You are done and the device is ready because it mimics your original L2446.

### Pairing (if you have no L2446 remote)

This setup can completely replace a physical L2446 remote. Set the `rf_key` to any random key or just use the above from the log example. You need to physically switch of the LEDs for at least 10 second, then after turning it back on you can press the pairing button and the LEDs will flash three times. There can only be one remote at the same time.

### Caveat

The original remote maintains it's own state expecting the light to react accordingly. Thus if signals are send from a virtual remote it has no knowledge about this. So as soon as you use the original remote it will switch back to the state it remembered. But there is a logic in place that receives the remotes signals and maintains this values with ESPhome and Homeassitant. This is not 100% perfect but perfect enough for me.

## Technical background

### Signal
The code signal is as follows:

* Startsequence (28 Zeros): -11760 µs
* Preamble (1 One, 32 Zeros): 420 µs, -13440 µs
* Payload: Six repeats
* Inter-Block-Pause (2 Ones, 6 Zeros): 840 µs, -2520 µs
* Final Footer (2 Ones, 79 Zeros): 840 µs, -33180 µs

The payload is:

* 24-bit fixed prefix (see **NOTE** below)
* 8-bit mode
* 8-bit state_val
* 8-bit checksum
* frame terminator/trailer

**NOTE: Inside the payload is a prefix where I am assuming that it's the L2446 key. So this must probably adjusted to other remotes**

### Bit encoding and Byte order
Each bit is encoded least-significant-bit first:

* bit 1 → 1245 then -415
* bit 0 → 415 then -1245

So each bit is a pair of timings:

* 1 = long pulse then short gap (1110)
* 0 = short pulse then long gap (1000)

For the Byte Order append_byte sends each byte from bit 0 to bit 7 (LSB first).
So the transmitted frame is:

* prefix bits
* mode byte
* state_val byte
* checksum byte

### 2-FSK and ASK/OOK encoding

I first implemented sending 2-FSK, which is the modulation the remote uses. When I tried to receive the 2-FSK signals with the CC1101, there was a lot of fragmentation. But we don't need the full signal. Thus default listening is in ASK/OOK with the deviation offset which made it more robust. You may face other experiences with your CC1101.
If you are just interested in transmitting signals you can use the `hamulight_l2446_transmitonly.yaml` file.

### Additonal Files

The `rf_calc.py` and `rf_diff.py` helped me to understand the signals. I'll keep them for re-use especially since Homeassistant now provides RF support.
The `signals.txt` contains the extracts of the binary codes from the URH analysis.

## History

* 2026-05-20 First version
* 2026-05-26 Pairing & Key detection added
