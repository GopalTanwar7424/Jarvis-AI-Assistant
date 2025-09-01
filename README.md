# 🤖 Jarvis AI Assistant

A Python-based voice-activated AI assistant inspired by Tony Stark's Jarvis. This intelligent assistant can listen to voice commands, process them using machine learning, search the web, and respond with synthesized speech.

## 🌟 Features

- **Voice Recognition**: Multi-language support (English & Hindi) with automatic translation
- **Text-to-Speech**: Natural voice synthesis using Microsoft Edge TTS
- **Smart Search**: Intelligent query classification and routing to Wikipedia or Google
- **Local Knowledge Base**: Machine learning-powered Q&A system with TF-IDF vectorization
- **Real-time Processing**: Concurrent audio processing and response generation
- **Animated Console Output**: Typewriter-style text animation for better user experience
- **Self-Learning**: Automatically saves new Q&A pairs to improve responses

## 🎯 Capabilities

### Voice Interaction
- Wake word detection ("Jarvis")
- Multi-language speech recognition (English/Hindi)
- Natural voice responses with customizable speech rate
- Real-time audio feedback

### Intelligent Search
- **Current Events**: Latest news, weather, stock prices
- **How-to Queries**: Step-by-step tutorials and guides  
- **Factual Questions**: Wikipedia integration for encyclopedia queries
- **Local Search**: Restaurant, shopping, and location-based queries
- **Direct Commands**: Web search with browser integration

### Machine Learning
- TF-IDF vectorization for text similarity
- Cosine similarity matching for Q&A retrieval
- Intent classification for better query routing
- Dynamic similarity thresholds based on query type
- Answer quality validation

## 🛠️ Technology Stack

- **Python 3.7+**
- **Speech Recognition**: `speech_recognition`, `pyaudio`
- **Text-to-Speech**: `edge-tts`, `pygame`
- **Machine Learning**: `scikit-learn`, `nltk`
- **Web Integration**: `wikipedia`, `webbrowser`
- **Translation**: `mtranslate`
- **UI Enhancement**: `colorama` for colored terminal output

## 📁 Project Structure

```
Jarvis/
├── Head/
│   ├── brain.py          # Main AI logic and search functions
│   ├── Ear.py           # Speech recognition module
│   └── mouth.py         # Text-to-speech engine
├── Traning_model/
│   └── model.py         # Machine learning model for Q&A
├── Function/
│   ├── wish.py          # Greeting functions
│   └── welcome.py       # Welcome messages
├── Data/
│   └── brain_data/
│       └── qna_dat.txt  # Knowledge base file
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Microphone for voice input
- Internet connection for web search features

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

### Step 2: Create Virtual Environment
```bash
python -m venv jarvis_env
source jarvis_env/bin/activate  # On Windows: jarvis_env\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Step 5: Run Jarvis
```bash
python main.py
```

## 📦 Dependencies

```
speech-recognition==3.10.0
pyaudio==0.2.11
edge-tts==6.1.9
pygame==2.5.2
scikit-learn==1.3.0
nltk==3.8.1
wikipedia==1.4.0
mtranslate==1.8
colorama==0.4.6
numpy==1.24.3
```

## 🎮 Usage Examples

### Basic Interaction
```
You: "Jarvis, hello"
Jarvis: "Hello! How can I help you today?"
```

### Knowledge Queries
```
You: "Jarvis, what is machine learning?"
Jarvis: [Searches Wikipedia and provides detailed explanation]
```

### Current Information
```
You: "Jarvis, latest news today"
Jarvis: [Opens Google search with current news results]
```

### How-to Queries
```
You: "Jarvis, how to make pasta"
Jarvis: "Boil 4 cups water with salt. Add 200g pasta, cook 8-10 minutes..."
```

### Web Search
```
You: "Jarvis, search for best laptops 2024"
Jarvis: [Opens browser with Google search results]
```

## ⚙️ Configuration

### Voice Settings
Modify `VOICE` in `Head/mouth.py`:
```python
VOICE = "en-IN-PrabhatNeural"  # Indian English male voice
# Other options: "en-US-AriaNeural", "en-GB-SoniaNeural"
```

### Speech Rate
Adjust speaking speed in `Head/mouth.py`:
```python
cm_text = edge_tts.Communicate(TEXT, VOICE, rate="+35%")
```

### File Paths
Update paths in `Head/brain.py` and `Traning_model/model.py`:
```python
qa_file_path = r"your_path/Data/brain_data/qna_dat.txt"
```

## 🧠 How It Works

1. **Voice Input**: Captures audio using microphone
2. **Speech Recognition**: Converts audio to text (English/Hindi)
3. **Language Processing**: Translates non-English input to English
4. **Intent Classification**: Determines query type (factual, current, how-to, etc.)
5. **Response Generation**: 
   - Checks local knowledge base first
   - Falls back to Wikipedia for factual queries
   - Uses Google search for current information
6. **Speech Output**: Converts response to natural speech
7. **Learning**: Saves new Q&A pairs to improve future responses

## 🔧 Customization

### Adding New Knowledge
Add entries to `Data/brain_data/qna_dat.txt`:
```
question:answer
how to code in python:Start with basics like variables, loops, and functions. Practice with simple projects.
```

### Custom Voice Commands
Extend functionality in `Head/brain.py`:
```python
if "play music" in text.lower():
    # Add your music playing logic
    pass
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 Known Issues

- PyAudio installation might require additional system dependencies
- Windows users may need Microsoft C++ Build Tools
- Internet connection required for web search features
- Microphone permissions needed for voice recognition

## 🔮 Future Enhancements

- [ ] GUI interface with tkinter
- [ ] Smart home device integration
- [ ] Calendar and reminder features
- [ ] Email and messaging capabilities
- [ ] Voice command customization
- [ ] Multi-user support
- [ ] Mobile app companion

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: (https://github.com/GopalTanwar7424)
- Email: gt124176@gmail.com
- LinkedIn: [Your LinkedIn][(https://www.linkedin.com/in/gopalsinghtanwar/)]

## 🙏 Acknowledgments

- Inspired by Marvel's Jarvis AI assistant
- Built with love for the AI and open-source community
- Thanks to all contributors and users

## 📊 Project Stats

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![Issues](https://img.shields.io/github/issues/yourusername/jarvis-ai-assistant)
![Stars](https://img.shields.io/github/stars/yourusername/jarvis-ai-assistant)

---

**⭐ If you found this project helpful, please give it a star!**
