# keybow
Custom MIDI controller setup for the Keybow 2040 (Raspberry Pi Pico-based)

## Pre-requisites

1. Clone this repo to your computer (macOS 15.5+ preferred).
2. Extract the library bundle:
   ```bash
   tar xvfz lib.tar.gz
   ```

## Setup Instructions for New Keybow 2040 Devices

### 1. Flash CircuitPython Firmware

After assembling the Keybow:

- Hold down the **boot/reset** button (located next to the USB-C port, top view) **while plugging the device into your computer**.
- The device will mount as a volume named `RPI-RP2`.

Flash CircuitPython firmware by copying the `.uf2` file:

```bash
cp firmware/adafruit-circuitpython-pimoroni_keybow2040-en_US-9.2.7.uf2 /Volumes/RPI-RP2
```

- The device will automatically reboot and remount as `CIRCUITPY1`.

### 2. Install the CircuitPython Library Bundle

To avoid conflicts with old libraries:

```bash
mv /Volumes/CIRCUITPY1/lib /Volumes/CIRCUITPY1/lib-orig
cp -R firmware/adafruit-circuitpython-bundle-9.x-mpy-20250425/lib /Volumes/CIRCUITPY1
```

### 3. Deploy Controller Code

Copy your selected control script (e.g., `single-mode-remapped.py`) to the board:

```bash
cp single-mode-remapped.py /Volumes/CIRCUITPY1/code.py
```

Then open `code.py` and edit the MIDI channel assignment:

```python
CHANNEL = 1  # 0 = all channels; use unique channels for each Keybow. Note: Ableton treats this as CH 2.
```

---

## Max for Live & Ableton Live Setup

### Ableton Live Configuration

After plugging in the Keybow:

- Open **Preferences > Link / Tempo / MIDI**.
- Enable **Track** and **Remote** for both **Input** and **Output** of the Keybow device.

### Track Setup

1. **Insert the latest `KritoMML.amxd`** device onto each track you want to control via Keybow.
2. Set the number of steps to **4**.
3. Enable only the **MIDI Thru** option.
   - No other configuration is needed for basic use.

4. Set **MIDI From** to the desired MIDI track with clips you'd like to be managed by the KeyBow and set **Monitor** to **IN**.
5. Use **MIDI Map Mode** in Ableton to map the **4 Keybow buttons** to the first 4 steps (mutes) in `KritoMML`.

### Optional: Global Mute Track

- Insert the latest `KeybowMutePlus.amxd` device on a separate track.
- Configure the **mute duration** (default is 40 seconds).
- This will mute all active Keybow channels globally.

---

## Final Notes

- Be sure to use distinct MIDI channels for each Keybow if using multiple devices.
- Ableton Live offsets MIDI channels (e.g., MIDI Channel 1 = CH 2 in UI).
- Changes to `code.py` require a device reboot to take effect.
