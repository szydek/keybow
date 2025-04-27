# Keybow 2040 MIDI controller with LED feedback from Ableton
# copy to code.py to run

import time
import board
from keybow2040 import Keybow2040

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

# Setup Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Setup USB MIDI
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1], out_channel=0)

# LED color when button is ON
rgb = (0, 255, 50)

# MIDI note and velocity settings
start_note = 36  # Starting MIDI note
velocity = 127   # Note on velocity

# Track LED states for each key
key_led_states = [False for _ in keys]

# Define what happens when a key is physically pressed
for key in keys:
    @keybow.on_press(key)
    def press_handler(key):
        note = start_note + key.number
        midi.send(NoteOn(note, velocity))
        key.set_led(*rgb)
        key_led_states[key.number] = True

    @keybow.on_release(key)
    def release_handler(key):
        note = start_note + key.number
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
            if 0 <= key_index < len(keys):
                if vel > 0:
                    keys[key_index].set_led(*rgb)
                    key_led_states[key_index] = True
                else:
                    keys[key_index].set_led(0, 0, 0)
                    key_led_states[key_index] = False

        elif isinstance(msg, NoteOff):
            note = msg.note
            key_index = note - start_note
            if 0 <= key_index < len(keys):
                keys[key_index].set_led(0, 0, 0)
                key_led_states[key_index] = False

# Main loop
while True:
    keybow.update()
    midi_feedback()
    time.sleep(0.01)  # Tiny sleep for smoother operation
