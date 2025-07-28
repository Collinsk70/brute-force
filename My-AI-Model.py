from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import os

# 🔑 Setup OpenAI client using environment variable or directly (NOT RECOMMENDED to hardcode!)
client = OpenAI(api_key="YOUR_API_KEY_HERE")  # Replace with your OpenAI key or use env var

# 🗣️ Text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak the response out loud."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input from the microphone and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening... Speak your question.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("🔍 Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return None
    except sr.RequestError:
        print("❌ Speech recognition service unavailable.")
        return None

def get_gpt_response(prompt):
    """Query OpenAI's GPT model with new SDK syntax."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error: {e}")
        return "I'm sorry, I couldn't get a response from the AI."

def main():
    print("🤖 Welcome to your AI Assistant!")
    while True:
        mode = input("\n💬 Choose input mode - (T)ext, (V)oice, or (Q)uit: ").lower()

        if mode == 'q':
            print("👋 Goodbye!")
            break
        elif mode == 't':
            prompt = input("📝 Type your message: ")
        elif mode == 'v':
            prompt = listen()
            if not prompt:
                continue
        else:
            print("❌ Invalid input. Choose 'T', 'V', or 'Q'.")
            continue

        print("🔮 Thinking...")
        answer = get_gpt_response(prompt)
        print(f"\n🤖 AI: {answer}")
        speak(answer)

if __name__ == "__main__":
    main()
