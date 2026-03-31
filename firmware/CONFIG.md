# Firmware Configuration Notes

## Preventing Signal Saturation (5V Cap)

If your MyoWare signal is hitting 5V and clipping, the sensor gain is too high
for your signal amplitude. This was observed during data collection for this project.

### Fix: Reduce Gain via Onboard Potentiometer

The MyoWare 2.0 has a small potentiometer on the board that controls amplification gain.

1. Before attaching electrodes, power on the sensor.
2. Locate the potentiometer on the MyoWare board.
3. Using a small flathead screwdriver, slowly turn it **counterclockwise** to reduce gain.
4. Attach electrodes and observe the signal in your serial monitor.
5. Adjust until the signal is no longer hitting 5V during activity.

> ⚠️ Make small adjustments — the potentiometer is sensitive.

### How to Check
In your Arduino serial monitor or PuTTY output, if ADC readings are consistently
at or near **1023**, your signal is saturating. Reduce gain until peaks are
comfortably below 1023 during cramping activity.