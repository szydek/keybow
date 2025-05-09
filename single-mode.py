
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


# Setup Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Setup USB MIDI
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1], out_channel=0)

# LED color when button is ON
rgb = (0, 255, 50)
rec_rgb = (255, 0, 0)
play_rgb = (0, 255, 0)
tap_rgb = (200, 200, 0)  # color for 9 keypad presses
ctl_rgb = (255,165,0) # will be color for future control button
feedback_rgb = (0, 0, 255)  # Different color for feedback (e.g., blue)

# MIDI note and velocity settings
start_note = 0  # Starting MIDI note for Keybow (C-2) - set low as possible
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
            # if note == 24:  # Check for C0 (note 24)
            #     if vel > 0:
            #         keys[11].set_led(*feedback_rgb)  # Set key 11 (index 11) to a different color
            #     else:
            #         keys[11].set_led(0, 0, 0)  # Turn off key 11 LED
            # elif note == 25:  # C#0
            #     if vel > 0:
            #         keys[10].set_led(*feedback_rgb)
            #     else:
            #         keys[10].set_led(0, 0, 0)
            # elif note == 26:  # D0
            #     if vel > 0:
            #         keys[9].set_led(*feedback_rgb)
            #     else:
            #         keys[9].set_led(0, 0, 0)
            # elif note == 27:  # D#0
            #     if vel > 0:
            #         keys[8].set_led(*feedback_rgb)
            #     else:
            #         keys[8].set_led(0, 0, 0)
            # else:
            # Handle other NoteOn messages normally for mapping
            key_index = note - start_note
            if 0 <= key_index < len(keys):  # Setup LED color per mapped key
                if vel > 0:
                    if key_index == 0:
                        # keys[key_index].set_led(*rec_rgb) # for REC mode
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 1:
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 2:
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 3:
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 4:
                        # keys[key_index].set_led(*play_rgb) # for PLAY mode
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 5:
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 6:
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 7:
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 8:
                        # keys[key_index].set_led(*ctl_rgb) # for CTRL mode
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 9:
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 10:
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 11:
                        keys[key_index].set_led(*tap_rgb)
                    elif key_index == 12:
                        keys[key_index].set_led(*tap_rgb)
                    else:
                        keys[key_index].set_led(*rgb)
                    key_led_states[key_index] = True
                else:
                    keys[key_index].set_led(0, 0, 0)
                    key_led_states[key_index] = False

        elif isinstance(msg, NoteOff):
            note = msg.note
            if note == 24:  # If it's C0 (note 24), turn off key 11's LED
                keys[11].set_led(0, 0, 0)
            elif note == 25:  # C#0
                keys[10].set_led(0, 0, 0)
            elif note == 26:  # D0
                keys[9].set_led(0, 0, 0)
            elif note == 27:  # D#0
                keys[8].set_led(0, 0, 0)
            else:
                key_index = note - start_note
                if 0 <= key_index < len(keys):
                    keys[key_index].set_led(0, 0, 0)
                    key_led_states[key_index] = False

        elif isinstance(msg, ControlChange):  # Handle CC messages separately
            cc_number = msg.control
            cc_value = msg.value
            # Use CC number to map to a key, or handle as desired
            if cc_number == 1:  # Example CC number for a specific action
                if cc_value == 0:  # Threshold example, adjust as needed
                    keys[3].set_led(*feedback_rgb) 
                    keys[2].set_led(*feedback_rgb) 
                    keys[1].set_led(*feedback_rgb) 
                elif cc_value == 4:
                    keys[3].set_led(0, 0, 0)
                    keys[2].set_led(0, 0, 0)
                    keys[1].set_led(0, 0, 0)
                elif cc_value == 1:
                    keys[7].set_led(*feedback_rgb)
                    keys[6].set_led(*feedback_rgb) 
                    keys[5].set_led(*feedback_rgb) 
                elif cc_value == 5:
                    keys[7].set_led(0, 0, 0)
                    keys[6].set_led(0, 0, 0)
                    keys[5].set_led(0, 0, 0)
                elif cc_value == 2:
                    keys[11].set_led(*feedback_rgb)
                    keys[10].set_led(*feedback_rgb) 
                    keys[9].set_led(*feedback_rgb) 
                elif cc_value == 6:
                    keys[11].set_led(0, 0, 0)
                    keys[10].set_led(0, 0, 0)
                    keys[9].set_led(0, 0, 0)
                elif cc_value == 3:
                    keys[15].set_led(*feedback_rgb)
                    keys[14].set_led(*feedback_rgb) 
                    keys[13].set_led(*feedback_rgb) 
                elif cc_value == 7:
                    keys[15].set_led(0, 0, 0)
                    keys[14].set_led(0, 0, 0)
                    keys[13].set_led(0, 0, 0)
            # Add more CC conditions as needed


# Main loop
while True:
    keybow.update()
    midi_feedback()
    time.sleep(0.01)  # Tiny sleep for smoother operation
    
    