import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from chatbot import ask_pet
from spotify_react import get_current_song
from voice_listen import listen_background
from fullscreen_check import is_fullscreen
from context_talk import get_context_phrase
import random
import os


# Main pet app class
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

        self.animate()
        self.schedule_all()
        listen_background(self.handle_voice_input)

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
        delay = int(random.gauss(15000, 3000))  # ~15s with some randomness

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

    def handle_voice_input(self, text):
        print("You said:", text)

        self.show_text_bubble(f"You: {text}", user=True)

        response = ask_pet(text)

        self.show_text_bubble(response)


    def load_animations(self):
        animations = {}

        def load_frames_from_folder(folder_path):
            frames = []
            frame_files = sorted(os.listdir(folder_path))
            for filename in frame_files:
                if filename.lower().endswith(('.png', '.gif')):
                    frame_path = os.path.join(folder_path, filename)
                    try:
                        img = Image.open(frame_path).convert("RGBA")

                        scale_factor = 2.8
                        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))

                        img = img.resize(new_size, Image.NEAREST)  # pixelated style

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
        # 70% chance to use default idle, 30% to use one of the random alts
        if random.random() < 0.85 or not self.animations["idle_alts"]:
            self.sprite = self.animations["idle_default"]
        else:
            self.sprite = random.choice(self.animations["idle_alts"])

        self.sprite_index = 0
        self.root.after(25000, self.switch_idle_randomly)  # every 15 seconds


if __name__ == '__main__':
    root = tk.Tk()
    app = DesktopPet(root)

    root.mainloop()
