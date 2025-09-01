import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Head.mouth import speak

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def load_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        qna_pairs = [line.strip().split(": ", 1) for line in lines if ": " in line]  # Changed from "::" to ": "
        dataset = [{'question': q, 'answer': a} for q, a in qna_pairs if
                   q.strip() and a.strip()]  # Filter empty entries
    return dataset


def preprocess_text(text):
    if not text or not text.strip():
        return text  # Return original if empty

    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    tokens = word_tokenize(text.lower())

    # Keep more tokens - only remove if it's both a stop word AND not alphanumeric
    processed_tokens = []
    for token in tokens:
        if token.isalnum():
            if token not in stop_words or len(token) > 2:  # Keep longer stop words
                processed_tokens.append(ps.stem(token))

    # If all tokens were removed, return original text (lowercased)
    if not processed_tokens:
        return text.lower()

    return ' '.join(processed_tokens)


def train_tfidf_vectorizer(dataset):
    if not dataset:
        raise ValueError("Dataset is empty!")

    corpus = []
    for qa in dataset:
        processed_question = preprocess_text(qa['question'])
        corpus.append(processed_question)

    # Check if corpus has valid content
    non_empty_corpus = [q for q in corpus if q.strip()]
    if not non_empty_corpus:
        # Use original questions if preprocessing fails
        corpus = [qa['question'].lower() for qa in dataset]

    # Use less aggressive TfidfVectorizer settings
    vectorizer = TfidfVectorizer(
        min_df=1,  # Include words that appear in at least 1 document
        max_features=None,  # Don't limit vocabulary size
        ngram_range=(1, 2),  # Include both single words and bigrams
        token_pattern=r'\b\w+\b'  # Include single characters and words
    )

    try:
        X = vectorizer.fit_transform(corpus)
        return vectorizer, X
    except ValueError as e:
        # Fallback: use original questions without preprocessing
        corpus_fallback = [qa['question'] for qa in dataset]
        vectorizer_fallback = TfidfVectorizer(min_df=1, token_pattern=r'\b\w+\b')
        X_fallback = vectorizer_fallback.fit_transform(corpus_fallback)
        return vectorizer_fallback, X_fallback


def is_knowledge_question(question):
    """Check if the question is asking for factual knowledge"""
    knowledge_indicators = [
        'what is', 'who is', 'what are', 'who are',
        'tell me about', 'explain', 'define', 'describe',
        'how does', 'how do', 'why does', 'why do',
        'when was', 'when did', 'where is', 'where are'
    ]

    question_lower = question.lower().strip()
    return any(indicator in question_lower for indicator in knowledge_indicators)


def get_answer(question, vectorizer, X, dataset):
    if not question.strip():
        return None

    try:
        processed_question = preprocess_text(question)
        if not processed_question.strip():
            processed_question = question.lower()

        question_vec = vectorizer.transform([processed_question])
        similarities = cosine_similarity(question_vec, X)

        # Get the best match
        best_match_index = similarities.argmax()
        max_similarity = similarities[0][best_match_index]

        # Increased similarity threshold for better quality responses
        if max_similarity < 0.3:  # Increased from 0.1 to 0.3
            return None

        answer = dataset[best_match_index]['answer']

        # Check if the answer is meaningful
        if is_generic_or_poor_answer(answer):
            return None

        return answer

    except Exception as e:
        return None


def is_generic_or_poor_answer(answer):
    """Check if answer is too generic or poor quality"""
    if not answer or not answer.strip():
        return True

    poor_answers = [
        "you are gopal, boss.",
        "nothing much, boss.",
        "just here to help you",
        "i don't know",
        "no answer found",
        "sorry",
        "i'm sorry",
        "i don't understand"
    ]

    answer_lower = answer.lower().strip()

    # Check if answer is too short
    if len(answer_lower.split()) < 3:
        return True

    # Check against poor answers
    for poor in poor_answers:
        if poor in answer_lower:
            return True

    # Check if answer is mostly punctuation or numbers
    if len([c for c in answer_lower if c.isalpha()]) < len(answer_lower) * 0.5:
        return True

    return False


def mind(text):
    try:
        dataset_path = r'C:\Users\gopal\OneDrive\Desktop\Jarvis\Data\brain_data\qna_dat.txt'
        dataset = load_dataset(dataset_path)

        if not dataset:
            return None  # Return None instead of speaking

        # Check if it's a knowledge question - if so, skip local dataset
        if is_knowledge_question(text):
            return None

        vectorizer, X = train_tfidf_vectorizer(dataset)
        user_question = text
        answer = get_answer(user_question, vectorizer, X, dataset)

        # Only return meaningful answers
        if answer and not is_generic_or_poor_answer(answer):
            return answer
        else:
            return None  # Return None to trigger wiki search

    except Exception as e:
        return None  # Return None on error to trigger wiki search


# Test the function
if __name__ == "__main__":
    while True:
        try:
            x = input("")
            if x.lower() in ['quit', 'exit', 'bye']:
                break
            mind(x)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")