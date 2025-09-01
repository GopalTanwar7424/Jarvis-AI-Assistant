import speech_recognition as sr
import os
import threading
from mtranslate import translate
from colorama import Fore, init, Style
from nltk.corpus.europarl_raw import english
from speech_recognition.recognizers.whisper_api.groq import recognize

init(autoreset=True)


def print_loop():
    while True:
        print(Fore.LIGHTGREEN_EX + "Yes Boss...", end="", flush=True)
        print(Style.RESET_ALL, end="", flush=True)
        print("", end="", flush=True)


def Trans_hindi_to_english(txt):
    english_txt = translate(txt, to_language="en")
    return english_txt


def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True  # Changed to True for better adaptation
    recognizer.energy_threshold = 300  # Lowered threshold
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.energy_energy_ratio = 1.5
    recognizer.operation_timeout = None

    recognizer.non_speaking_duration = 0.5  # Increased
    recognizer.pause_threshold = 0.8  # Increased for better phrase capture

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:
            print(Fore.LIGHTGREEN_EX + "I am Listening...", end="", flush=True)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("\r" + Fore.LIGHTYELLOW_EX + "Got it, Recognizing...", end="", flush=True)

                # Try English first with better language settings
                try:
                    recognizer_txt = recognizer.recognize_google(audio, language="en-US").lower()
                except sr.UnknownValueError:
                    try:
                        recognizer_txt = recognizer.recognize_google(audio, language="hi-IN").lower()
                    except sr.UnknownValueError:
                        recognizer_txt = ""

                if recognizer_txt:
                    # Always translate to ensure English output
                    translate_txt = Trans_hindi_to_english(recognizer_txt)
                    # Show both original and translated text
                    print("\r" + Fore.BLUE + f"You said: {recognizer_txt}")
                    if recognizer_txt != translate_txt:
                        print(Fore.GREEN + f"Translated: {translate_txt}")
                    return translate_txt
                else:
                    print("\r" + Fore.RED + "No speech detected", end="", flush=True)

            except sr.UnknownValueError:
                recognizer_txt = ""
                print("\r" + Fore.RED + "Could not understand", end="", flush=True)
            except sr.WaitTimeoutError:
                print("\r" + Fore.YELLOW + "Listening timeout", end="", flush=True)
            except sr.RequestError as e:
                print("\r" + Fore.RED + f"Recognition error: {e}", end="", flush=True)
            finally:
                print("\r", end="", flush=True)

            os.system("cls" if os.name == "nt" else "clear")


def listen_once():
    """Listen for a single command and return it"""
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True  # Better adaptation
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.energy_energy_ratio = 1.5
    recognizer.operation_timeout = None

    recognizer.non_speaking_duration = 0.5
    recognizer.pause_threshold = 0.8

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(Fore.LIGHTGREEN_EX + "I am Listening...", end="", flush=True)

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("\r" + Fore.LIGHTYELLOW_EX + "Got it, Recognizing...", end="", flush=True)

            recognizer_txt = ""
            # Try English first for better accuracy
            try:
                recognizer_txt = recognizer.recognize_google(audio, language="en-US").lower()
            except sr.UnknownValueError:
                try:
                    recognizer_txt = recognizer.recognize_google(audio, language="hi-IN").lower()
                except sr.UnknownValueError:
                    pass

            if recognizer_txt:
                # Always translate to ensure English output
                translate_txt = Trans_hindi_to_english(recognizer_txt)
                # Clear the line and show both versions if different
                print("\r", end="", flush=True)
                if recognizer_txt != translate_txt:
                    print(Fore.BLUE + f"Hindi: {recognizer_txt}")
                    print(Fore.GREEN + f"English: {translate_txt}")
                return translate_txt
            else:
                print("\r", end="", flush=True)
                return ""

        except sr.WaitTimeoutError:
            print("\r", end="", flush=True)
            return ""
        except sr.RequestError as e:
            print("\r", end="", flush=True)
            return ""
        except Exception as e:
            print("\r", end="", flush=True)
            return ""
        finally:
            os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    while True:
        try:
            result = listen()
            if result:
                print(f"Recognized: {result}")
        except KeyboardInterrupt:
            print(Fore.RED + "\nExiting...")
            break
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
            continue