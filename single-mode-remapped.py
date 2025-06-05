# Keybow 2040 MIDI controller with LED feedback from Ableton
# copy to code.py to run
# this version also allows for different color feedback on keys second column from the right (C0, C#0, D0, D#0)
# buttons 0 + 4 are record, play respectively
# with different colors for the keypad

import time
import board
from keybow2040 import Keybow2040

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.control_change import ControlChange  # Add this import for CC messages

# CONFIG
CHANNEL = 1  # 0 = all, use distinct channels for multiple devices. Note Ableton Live maps to the channel + 1 / so 1 will map to CH2

# Setup Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Rotation remap: 90° counter-clockwise
remap = [
     3,  7, 11, 15,
     2,  6, 10, 14,
     1,  5,  9, 13,
     0,  4,  8, 12
]
reverse_remap = [0] * 16
for i, val in enumerate(remap):
    reverse_remap[val] = i

# Setup USB MIDI
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1], out_channel=CHANNEL, in_channel=CHANNEL)

# LED color when button is ON
rgb = (0, 255, 50)
rec_rgb = (255, 0, 0)
play_rgb = (0, 255, 0)
tap_rgb = (200, 200, 0)  # color for 9 keypad presses
ctl_rgb = (255, 165, 0)  # will be color for future control button
feedback_rgb = (0, 0, 255)  # Different color for feedback (e.g., blue)

# MIDI note and velocity settings
start_note = 0  # Starting MIDI note for Keybow (C-2) - set low as possible
velocity = 127  # Note on velocity

# Track LED states for each key
key_led_states = [False for _ in keys]

# Define what happens when a key is physically pressed
for key in keys:
    @keybow.on_press(key)
    def press_handler(key):
        logical_index = reverse_remap[key.number]
        note = start_note + logical_index
        midi.send(NoteOn(note, velocity))
        key.set_led(*rgb)
        key_led_states[logical_index] = True

    @keybow.on_release(key)
    def release_handler(key):
        logical_index = reverse_remap[key.number]
        note = start_note + logical_index
        midi.send(NoteOff(note, 0))
        # Don't immediately turn off LED — let Ableton feedback control it

# Handle incoming MIDI feedback
def midi_feedback():
    msg = midi.receive()
    if msg:
        if isinstance(msg, NoteOn):
            note = msg.note
            vel = msg.velocity
            key_index = note - start_note
            if 0 <= key_index < len(keys):  # Setup LED color per mapped key
                target_key = keys[remap[key_index]]
                if vel > 0:
                    if key_index in range(0, 13):
                        target_key.set_led(*tap_rgb)
                    else:
                        target_key.set_led(*rgb)
                    key_led_states[key_index] = True
                else:
                    target_key.set_led(0, 0, 0)
                    key_led_states[key_index] = False

        elif isinstance(msg, NoteOff):
            note = msg.note
            key_index = note - start_note
            if 0 <= key_index < len(keys):
                keys[remap[key_index]].set_led(0, 0, 0)
                key_led_states[key_index] = False

        elif isinstance(msg, ControlChange):
            cc_number = msg.control
            cc_value = msg.value
            def set_keys(indices, color):
                for i in indices:
                    keys[remap[i]].set_led(*color)

            def clear_keys(indices):
                for i in indices:
                    keys[remap[i]].set_led(0, 0, 0)

            if cc_number == 1:
                if cc_value == 0:
                    set_keys([3, 2, 1], feedback_rgb)
                elif cc_value == 4:
                    clear_keys([3, 2, 1])
                elif cc_value == 1:
                    set_keys([7, 6, 5], feedback_rgb)
                elif cc_value == 5:
                    clear_keys([7, 6, 5])
                elif cc_value == 2:
                    set_keys([11, 10, 9], feedback_rgb)
                elif cc_value == 6:
                    clear_keys([11, 10, 9])
                elif cc_value == 3:
                    set_keys([15, 14, 13], feedback_rgb)
                elif cc_value == 7:
                    clear_keys([15, 14, 13])

# Main loop
while True:
    keybow.update()
    midi_feedback()
    time.sleep(0.01)  # Tiny sleep for smoother operation
