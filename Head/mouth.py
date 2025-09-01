import asyncio
import threading
import os
import edge_tts

# Hide pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

VOICE = "en-IN-PrabhatNeural"
BUFFER_SIZE = 1024


def remove_file(file_path):
    max_attempt = 3
    attempts = 0
    while attempts < max_attempt:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                break
        except Exception:
            attempts += 1


async def amain(TEXT, output_file) -> None:
    try:
        # Create communicate object with rate parameter directly
        cm_text = edge_tts.Communicate(TEXT, VOICE, rate="+35%")
        await cm_text.save(output_file)
        thread = threading.Thread(target=play_audio, args=(output_file,))
        thread.start()
        thread.join()
    except Exception:
        pass
    finally:
        remove_file(output_file)


def play_audio(file_path):
    try:
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.wait(10)

        pygame.mixer.quit()

    except Exception:
        pass


def speak(TEXT, output_file=None):
    if output_file is None:
        output_file = f"{os.getcwd()}/speak.mp3"
    asyncio.run(amain(TEXT, output_file))