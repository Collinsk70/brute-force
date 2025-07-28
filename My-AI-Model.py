from llama_cpp.llama import Llama
import pyttsx3
import speech_recognition as sr
import os

# 🧠 Load the local GGUF model
llm = Llama(
    model_path="capybarahermes-2.5-mistral-7b.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4  # Adjust based on your CPU cores
)

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

def get_local_response(prompt):
    """Query the local GGUF model and get response."""
    try:
        output = llm(
            prompt=f"[INST] {prompt} [/INST]",
            temperature=0.7,
            top_p=0.9,
            max_tokens=512,
            stop=["</s>"]
        )
        return output['choices'][0]['text'].strip()
    except Exception as e:
        print(f"❌ Error: {e}")
        return "I'm sorry, I couldn't get a response from the local AI."

def main():
    print("🤖 Welcome to your Local AI Assistant!")
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
        answer = get_local_response(prompt)
        print(f"\n🤖 AI: {answer}")
        speak(answer)

if __name__ == "__main__":
    main()
