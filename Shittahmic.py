import sounddevice as sd
import numpy as np
import scipy.signal as signal
import threading
import tkinter as tk
from tkinter import ttk

sample_rate = 16000  # sample rate
noise_level = 0.00  # annoying ahh static
amplify_factor = 500.0  # amp
clip_threshold = 2000.0  # clipping threshold

def add_bad_mic_effect(audio):
    downsampled = signal.resample(audio, len(audio) // 2)
    noisy = downsampled + np.random.normal(0, noise_level, len(downsampled))
    amplified = noisy * amplify_factor
    clipped = np.clip(amplified, -clip_threshold, clip_threshold)
    return signal.resample(clipped, len(audio))

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    bad_mic_audio = add_bad_mic_effect(indata[:, 0])
    outdata[:, 0] = bad_mic_audio

def start_stream(input_device, output_device):
    with sd.Stream(callback=callback, samplerate=sample_rate, channels=1,
                   device=(input_device, output_device)):
        print("shitty ahh mic is running Press Ctrl+C to stop.")
        threading.Event().wait()

def list_devices():
    devices = sd.query_devices()
    return devices

def on_start():
    input_index = input_device_combobox.current()
    output_index = output_device_combobox.current()
    try:
        start_stream(input_index, output_index)
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Error: {e}")

root = tk.Tk()
root.title("shitty ahh mic")

devices = list_devices()
device_names = [f"{i}: {d['name']}" for i, d in enumerate(devices)]

#Inputs
input_label = tk.Label(root, text="Select Input Device:")
input_label.pack()
input_device_combobox = ttk.Combobox(root, values=device_names, state="readonly")
input_device_combobox.pack()
input_device_combobox.current(0)

# Outputs
output_label = tk.Label(root, text="Select Output Device:")
output_label.pack()
output_device_combobox = ttk.Combobox(root, values=device_names, state="readonly")
output_device_combobox.pack()
output_device_combobox.current(0)

start_button = tk.Button(root, text="Start", command=on_start)
start_button.pack()

root.mainloop()
