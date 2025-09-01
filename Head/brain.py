import sys
import threading
import urllib
import webbrowser
import time
import wikipedia
import os
import re

# Suppress pygame messages
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from Head.mouth import speak
from Traning_model.model import mind


def load_qa_data(file_path):
    qa_dict = {}
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":", 1)  # Changed from 2 parts to split only on first ':'
                if len(parts) != 2:
                    continue
                q, a = parts
                qa_dict[q.strip().lower()] = a.strip()  # Store questions in lowercase for comparison
    except FileNotFoundError:
        pass
    return qa_dict


qa_file_path = r"C:\Users\gopal\OneDrive\Desktop\Jarvis\Data\brain_data\qna_dat.txt"
qa_dict = load_qa_data(qa_file_path)


def print_animated_message(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.075)
    print()


def save_qa_data(file_path, new_question, new_answer):
    """Save only new Q&A data, avoid duplicates"""
    # Check if this exact question already exists
    if new_question.strip().lower() in qa_dict:
        return  # Don't add duplicates

    # Add to memory
    qa_dict[new_question.strip().lower()] = new_answer.strip()

    # Append only the new entry to file
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{new_question.strip()}:{new_answer.strip()}\n")
    except:
        pass


def extract_search_terms(prompt):
    """Extract meaningful search terms from the prompt"""
    # Remove common words and jarvis-specific terms
    stop_words = ['jarvis', 'who', 'is', 'what', 'tell', 'me', 'about', 'search', 'find', 'wikipedia']

    # Clean the prompt
    clean_prompt = prompt.lower()
    for word in stop_words:
        clean_prompt = clean_prompt.replace(word, "")

    # Remove extra spaces and get meaningful terms
    search_terms = ' '.join(clean_prompt.split()).strip()

    return search_terms if search_terms else prompt.replace("jarvis", "").strip()


def wiki_search(prompt):
    search_prompt = extract_search_terms(prompt)

    if not search_prompt:
        speak("I need more specific information to search.")
        return

    try:
        # First try to get a summary
        wiki_summary = wikipedia.summary(search_prompt, sentences=3)
        animate_thread = threading.Thread(target=print_animated_message, args=(wiki_summary,))
        speak_thread = threading.Thread(target=speak, args=(wiki_summary,))
        animate_thread.start()
        speak_thread.start()

        animate_thread.join()
        speak_thread.join()

        # Save without duplicates
        save_qa_data(qa_file_path, prompt.strip(), wiki_summary)

    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation by trying the first suggestion
        try:
            first_option = e.options[0]
            wiki_summary = wikipedia.summary(first_option, sentences=3)
            animate_thread = threading.Thread(target=print_animated_message, args=(wiki_summary,))
            speak_thread = threading.Thread(target=speak, args=(wiki_summary,))
            animate_thread.start()
            speak_thread.start()

            animate_thread.join()
            speak_thread.join()

            save_qa_data(qa_file_path, prompt.strip(), wiki_summary)
        except:
            google_search(search_prompt)

    except wikipedia.exceptions.PageError:
        google_search(search_prompt)
    except:
        google_search(search_prompt)


def google_search(query):
    query = extract_search_terms(query)

    if query:
        url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
        webbrowser.open_new_tab(url)
        response = f"You can see search results for {query} in Google on your screen."
        speak(response)
        print(response)

        # Save the search action
        save_qa_data(qa_file_path, f"search {query}", response)
    else:
        speak("I didn't catch what you said")
        print("I didn't catch what you said")


def is_generic_response(response):
    """Check if response is too generic or unhelpful"""
    if not response:
        return True

    generic_responses = [
        "you are gopal, boss.",
        "nothing much, boss.",
        "just here to help you",
        "i don't know",
        "no answer found",
        "sorry, i don't understand",
        "i'm sorry, i don't understand that question"
    ]

    response_lower = response.lower().strip()

    # Check if response is too short (likely generic)
    if len(response_lower.split()) < 4:
        return True

    # Check against known generic responses
    for generic in generic_responses:
        if generic in response_lower:
            return True

    return False


def brain(text):
    try:
        # First check if it's a knowledge question that needs Wikipedia
        knowledge_keywords = ['what is', 'who is', 'tell me about', 'explain', 'define', 'describe']
        text_lower = text.lower()

        is_knowledge_question = any(keyword in text_lower for keyword in knowledge_keywords)

        # Try the trained model first
        response = mind(text)

        # If no response or generic response, or if it's clearly a knowledge question, use Wikipedia
        if not response or is_generic_response(response) or is_knowledge_question:
            wiki_search(text)
            return

        # Start animation and speaking concurrently
        animate_thread = threading.Thread(target=print_animated_message, args=(response,))
        speak_thread = threading.Thread(target=speak, args=(response,))

        animate_thread.start()
        speak_thread.start()

        animate_thread.join()
        speak_thread.join()

        # Only save if it's a new question-answer pair and not generic
        if text.strip().lower() not in qa_dict and not is_generic_response(response):
            save_qa_data(qa_file_path, text.strip(), response)

    except Exception:
        # Silent error handling
        wiki_search(text)