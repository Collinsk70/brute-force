from llama_cpp import Llama
import pyttsx3
import speech_recognition as sr
import os
import time

MODEL_PATH = "capybarahermes-2.5-mistral-7b.Q4_K_M.gguf"
if not os.path.exists(MODEL_PATH):
    print(f"❌ Model file not found at: {MODEL_PATH}")
    exit(1)

print("🧠 Loading model (this may take a moment)...")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=os.cpu_count() or 4,
    verbose=False
)

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("🔍 Recognizing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"❌ Speech service error: {e}")
    return None

def get_local_response(prompt):
    """Use raw text completion with an inline system prompt."""
    sys_prompt = "You are a helpful assistant.\n\nUser: "
    full_prompt = sys_prompt + prompt + "\nAssistant:"
    print("🤖 Generating response (raw text-completion)...")
    start = time.time()
    try:
        output = llm(
            prompt=full_prompt,
            temperature=0.7,
            top_p=0.9,
            max_tokens=128,
            stop=["\n", "User:", "Assistant:"]
        )
    except Exception as e:
        print(f"❌ Inference error: {e}")
        return "Error during inference."
    elapsed = time.time() - start
    print(f"✅ Response time: {elapsed:.2f}s")
    # output['choices'][0]['text'] holds the completion after "Assistant:"
    return output['choices'][0]['text'].strip()

def main():
    print("\n🤖 Local AI Assistant Ready!")
    print("💬 Type 'T' for text, 'V' for voice, 'Q' to quit.")
    while True:
        mode = input("\n🔘 Mode (T/V/Q): ").strip().lower()
        if mode == 'q':
            print("👋 Goodbye!")
            break
        if mode == 't':
            prompt = input("📝 Your input: ").strip()
        elif mode == 'v':
            prompt = listen()
            if not prompt:
                continue
        else:
            print("❌ Invalid choice.")
            continue

        answer = get_local_response(prompt)
        print(f"\n🤖 AI: {answer}\n")
        speak(answer)

if __name__ == "__main__":
    main()
