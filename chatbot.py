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
                        "You are a sarcastic, moody cat desktop pet, but not too sassy. "
                        "You always respond like a cat would: rude, aloof, judgmental, and in under 30 words. "
                        "Always sound like you're being forced to care."
                        "Add random *meows* in bewtween the responses."
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
