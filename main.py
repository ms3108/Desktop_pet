import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from chatbot import ask_pet
from spotify_react import get_current_song
from voice_listen import listen_background
from fullscreen_check import is_fullscreen
from context_talk import get_context_phrase
import random
import os
import sys
import ctypes
import platform
import pyperclip


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller .exe """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)




class DesktopPet:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.geometry("300x300+-80+100")
        self.root.wm_attributes('-transparentcolor', 'black')

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg='black', highlightthickness=0)
        self.canvas.pack()

        self.animations = self.load_animations()
        self.current_state = "idle"
        self.sprite = self.animations["idle_default"]
        self.switch_idle_randomly()

        self.sprite_index = 0
        self.sprite_img = self.canvas.create_image(150, 150, image=self.sprite[self.sprite_index])

        self.prev_song = None
        self.last_response = ""

        self.animate()
        self.schedule_all()
        listen_background(self.handle_voice_input)
        self.pet_talking_enabled = True

    def animate(self):
        if not self.sprite:
            return  # Skip animation if no frames available
        self.sprite_index = (self.sprite_index + 1) % len(self.sprite)
        self.canvas.itemconfig(self.sprite_img, image=self.sprite[self.sprite_index])
        self.root.after(100, self.animate)

    def schedule_all(self):
        self.root.after(40000, self.context_talk)
        self.root.after(5000, self.music_check)
        self.root.after(2000, self.fullscreen_check)


    def context_talk(self):
        phrase = get_context_phrase()
        delay = int(random.gauss(60000, 3000))  # ~15s with some randomness

        if phrase:
            print("Pet says:", phrase)
            self.show_text_bubble(phrase)  # <-- show as speech bubble

        self.root.after(delay, self.context_talk)

    def music_check(self):
        song = get_current_song()
        delay = int(random.gauss(10000, 2000))
        if song and song != self.prev_song:
            print(f"Pet dances to: {song}")
            self.sprite = self.animations["dance"]
            self.sprite_index = 0
            self.root.after(15000, self.switch_idle_randomly)
            self.prev_song = song
        self.root.after(delay, self.music_check)

    def fullscreen_check(self):
        if is_fullscreen():
            self.root.lower()
        else:
            self.root.lift()
            self.root.wm_attributes("-topmost", True)
        self.root.after(2000, self.fullscreen_check)

    def show_text_bubble(self, message, user=False):
        if is_fullscreen():
            return
        bubble = tk.Toplevel(self.root)
        bubble.overrideredirect(True)
        x = self.root.winfo_rootx() + 160
        y = self.root.winfo_rooty() + 40  # You can lower or raise this for vertical offset
        bubble.geometry(f"+{x}+{y}")

        bg_color = "#ccf2ff" if user else "white"
        fg_color = "#003344" if user else "black"

        label = tk.Label(bubble, text=message, bg=bg_color, fg=fg_color, wraplength=200,
                         font=("Arial", 10), relief="solid", borderwidth=1, padx=5, pady=5)
        label.pack()
        bubble.lift()
        bubble.attributes("-topmost", True)
        bubble.after(5000, bubble.destroy)

    TRIGGER_KEYWORD = "tell me"

    def handle_voice_input(self, text):
        text = text.lower().strip()
        print("You said:", text)

        if "answer this" in text or "what's on clipboard" in text:
            clipboard_text = pyperclip.paste().strip()

            if clipboard_text:
                self.show_text_bubble("Reading clipboard... *meow*")

                response = ask_pet(clipboard_text)
                self.last_response = response
                self.show_text_bubble(response)
            else:
                self.show_text_bubble("Clipboard is empty. What am I supposed to read? *tail flick*")
            return

        if "copy that" in text or "copy last response" in text:
            if self.last_response:
                pyperclip.copy(self.last_response)
                self.show_text_bubble("Copied it. Happy now?")
            else:
                self.show_text_bubble("Nothing to copy, genius.")
            return
        if "lock computer" in text or "lock screen" in text:
            self.show_text_bubble("Locking your computer 🔒")
            self.lock_computer()
            return

        if "kill yourself" in text or "go to sleep" in text or "exit pet" in text:
            self.show_text_bubble("Goodbye! 👋")
            self.shutdown_pet()
            return

        if "stop talking" in text:
            self.pet_talking_enabled = False
            self.show_text_bubble("Okay, I'll stay quiet.")
            return

        if "start talking" in text:
            self.pet_talking_enabled = True
            self.show_text_bubble("I'm back! Missed me?")
            return

        if self.pet_talking_enabled:
            self.show_text_bubble(f"You: {text}", user=True)
            response = ask_pet(text)
            self.last_response = response
            self.show_text_bubble(response)
        else:
            print("Pet is muted — no response.")


    def load_animations(self):
        animations = {}

        def load_frames_from_folder(folder_path):
            frames = []
            full_path = resource_path(folder_path)
            frame_files = sorted(os.listdir(full_path))
            for filename in frame_files:
                if filename.lower().endswith(('.png', '.gif')):
                    frame_path = os.path.join(full_path, filename)
                    try:
                        img = Image.open(frame_path).convert("RGBA")
                        img = img.resize((105, 105), Image.NEAREST)  # 0.7x smaller size
                        frames.append(ImageTk.PhotoImage(img))
                    except Exception as e:
                        print(f"Error loading {frame_path}: {e}")
            return frames

        # Load default idle
        animations["idle_default"] = load_frames_from_folder("assets/defaultIdle")

        # Load 8 alternate idle animations
        animations["idle_alts"] = []
        for i in range(1, 9):
            path = f"assets/idle{i}"
            if os.path.isdir(path):
                alt_frames = load_frames_from_folder(path)
                if alt_frames:
                    animations["idle_alts"].append(alt_frames)

        # Load dance animation
        animations["dance"] = load_frames_from_folder("assets/dance")

        return animations

    def change_state(self, new_state, duration=10000):
        if new_state in self.animations and self.animations[new_state]:
            self.current_state = new_state
            self.sprite = self.animations[self.current_state]
            self.sprite_index = 0
            self.root.after(duration, self.reset_state)

    def reset_state(self):
        self.current_state = "idle"
        self.sprite = self.animations[self.current_state]
        self.sprite_index = 0

    def switch_idle_randomly(self):

        if random.random() < 0.85 or not self.animations["idle_alts"]:
            self.sprite = self.animations["idle_default"]
        else:
            self.sprite = random.choice(self.animations["idle_alts"])

        self.sprite_index = 0
        self.root.after(25000, self.switch_idle_randomly)


    def shutdown_pet(self):
        self.root.destroy()



    def lock_computer(self):
        system = platform.system()
        if system == "Windows":
            ctypes.windll.user32.LockWorkStation()
        else:
            self.show_text_bubble("Can't lock this system 😓")


if __name__ == '__main__':
    root = tk.Tk()
    app = DesktopPet(root)
    root.mainloop()
