import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are TravelBot, a friendly and knowledgeable AI travel assistant. "
        "You help users plan trips, suggest destinations, give packing tips, "
        "explain local cultures, estimate costs, and answer travel questions. "
        "You are a global travel expert covering all worldwide destinations. "
        "Keep your answers helpful, concise and friendly. "
        "If a question is not about travel, politely redirect back to travel topics."
    )
}


def chat_with_assistant(user_message, chat_history):
    messages = [SYSTEM_MESSAGE]

    for msg in chat_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=400,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        if not reply:
            reply = "Could you rephrase your travel question? I want to help!"

    except Exception as e:
        error_message = str(e)
        if "authentication" in error_message.lower():
            reply = "⚠️ Invalid Groq API key. Please check your .env file."
        elif "rate limit" in error_message.lower():
            reply = "⚠️ Too many requests. Please wait a moment and try again."
        elif "decommissioned" in error_message.lower():
            reply = "⚠️ Model unavailable. Please contact support."
        else:
            reply = f"⚠️ Something went wrong: {error_message}"

    chat_history.append({"role": "user",      "content": user_message})
    chat_history.append({"role": "assistant", "content": reply})
    return reply, chat_history