import os
import sys

# Hide pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from Head.mouth import *
from Head.Ear import listen_once
from Head.brain import brain
from Function.wish import wish
from Function.welcome import welcome


def jarvis():
    # Clear screen first
    os.system("cls" if os.name == "nt" else "clear")


    wish()
    welcome()

    while True:
        try:
            text = listen_once()

            if text and text.strip():

                if "jarvis" in text.lower():
                    print(f"Jarvis: {text}")
                    print()
                    brain(text)
                    print()

        except KeyboardInterrupt:

            sys.exit(0)
        except Exception as e:

            continue


if __name__ == "__main__":
    jarvis()