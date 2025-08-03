import platform
import random
import sys
import os
import json

if platform.system() == "Windows":
    import win32gui

import requests

def resource_path(relative_path):
    """ Get absolute path to resource (works for PyInstaller and IDE) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Load configuration
with open(resource_path("config.json"), "r") as f:
    config = json.load(f)

GROQ_API_KEY = config["groq_api_key"]


def get_active_window_name():
    if platform.system() == "Windows":
        return win32gui.GetWindowText(win32gui.GetForegroundWindow()).lower()
    return ""


def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.85
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Groq error:", e)
        return random.choice([
            "You're probably doing something useless again.",
            "Wow, still pretending to work?",
            "Look at you go — opening apps like you have a purpose."
        ])


def get_context_phrase():
    window = get_active_window_name()

    prompt = f"""You're a sarcastic, emotionally destructive desktop pet. The user is currently using a window titled: "{window}". Say one short, mocking sentence about it."""

    return ask_groq(prompt)
