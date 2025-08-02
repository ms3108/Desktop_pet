from groq import Groq

client = Groq(api_key="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")

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



