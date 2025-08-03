from groq import Groq
import sys
import os
import json

def resource_path(relative_path):
    """ Get absolute path to resource (works for PyInstaller and IDE) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Load configuration
with open(resource_path("config.json"), "r") as f:
    config = json.load(f)

client = Groq(api_key=config["groq_api_key"])

def ask_pet(prompt):
    try:
        chat_completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're a sarcastic but secretly helpful cat-shaped desktop pet. You act like you're above it all, but you *begrudgingly* give useful answers in under 30 words. Occasionally insert a '*meow*' mid-sentence. You never admit you're helping on purpose. Respond like a cat that's annoyed but too smart not to answer."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )
        reply = chat_completion.choices[0].message.content.strip()
        print("Groq (Cat Pet):", reply)
        return reply
    except Exception as e:
        print("Groq SDK error:", e)
        return "*hiss* Error. Petting privileges revoked."
