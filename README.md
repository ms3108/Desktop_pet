# 🐾 Desktop Pet

A cute, animated desktop companion with attitude! This sarcastic cat-shaped pet sits on your desktop, reacts to your music, listens to your voice, and provides witty AI-powered responses. Built with Python and Tkinter, featuring Spotify integration, Groq AI, and advanced clipboard interactions.

![Desktop Pet Demo](assets/demo.gif) <!-- Add a demo GIF if available -->

---

## ✨ Features

### 🎵 **Music Integration**
- **Spotify Dancing**: Automatically detects when you're playing music on Spotify and switches to dance animation
- **Real-time Music Detection**: Continuously monitors your Spotify activity

### 🎙️ **Voice Interaction**
- **Continuous Speech Recognition**: Always listening for your voice commands
- **Natural Language Processing**: Understands and responds to spoken queries
- **Background Voice Processing**: Non-blocking voice recognition system

### 🤖 **AI-Powered Responses**
- **Sarcastic Personality**: Uses Groq's LLaMA 3 API for witty, cat-like responses
- **Context-Aware**: Responds differently based on your current activity
- **Smart Conversations**: Maintains personality while being secretly helpful

### 💬 **Interactive Features**
- **Speech Bubbles**: Visual text responses that appear above the pet
- **Click Interactions**: Click on the pet for random responses
- **Advanced Clipboard Integration**: 
  - Copy pet responses to clipboard with voice commands
  - Read and analyze clipboard content with AI
  - Smart clipboard text processing

### 🎭 **Smart Behavior**
- **Fullscreen Detection**: Automatically hides when you're in fullscreen mode (gaming, videos)
- **Window Context Awareness**: Different behaviors based on active applications (Chrome, VS Code, etc.)
- **Multiple Idle Animations**: Various cute idle states to keep things interesting

### 🎨 **Visual Design**
- **Pixel Art Style**: Retro-inspired animations and graphics
- **Smooth Animations**: Frame-by-frame animated GIFs
- **Compact Size**: Small 105x105 pixel footprint that doesn't obstruct your work

---

## 🛠️ Installation & Setup

### Option 1: Standalone Executable (Recommended)
1. Download the `main.exe` file from the releases
2. Run `main.exe` directly - no installation required!
3. Configure your API keys in the generated `config.json`

### Option 2: Run from Source

#### Prerequisites
- Python 3.9 or higher
- Windows OS (for full functionality)

#### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Desktop_Pet
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**
   - Copy `config.json.example` to `config.json`
   - Add your API keys (see Configuration section)

4. **Run the application**
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration

Open the `config.json` file in the project root:

```json
{
  "groq_api_key": "your_groq_api_key_here",
  "spotify": {
    "client_id": "your_spotify_client_id",
    "client_secret": "your_spotify_client_secret",
    "redirect_uri": "http://localhost:8080"
  }
}
```
Replace with your own values
### API Keys Setup

#### Groq API (Required for AI responses)
1. Visit [Groq Console](https://console.groq.com/)
2. Create an account and generate an API key
3. Add the key to your `config.json`

#### Spotify API (Optional - for music detection)
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Get your Client ID and Client Secret
4. Add them to your `config.json`

---

## 🎮 Usage & Commands

### Voice Commands

#### Basic Interaction
- **"Hey pet"** or **"Hello"** - Get the pet's attention
- **Ask questions** - The pet will respond with sarcastic but helpful answers
- **General conversation** - Chat naturally with your desktop companion

#### Clipboard Commands
- **"Copy that"** or **"Copy last response"** - Copies the pet's last response to clipboard
- **"Answer this"** or **"What's on clipboard"** - Pet reads and analyzes clipboard content with AI
- **"Read clipboard"** - Pet processes whatever text is currently in your clipboard

#### Example Clipboard Workflow:
1. Copy any text (code, question, article, etc.) to clipboard
2. Say **"Answer this"** to your pet
3. Pet reads clipboard content and provides AI-powered analysis/response
4. Say **"Copy that"** to copy the pet's response back to clipboard

### Mouse Interactions
- **Left Click** - Get a random response or context-based comment
- **Right Click** - Access pet menu (if implemented)

### Automatic Behaviors
- **Music Detection** - Starts dancing when Spotify is playing
- **Fullscreen Hide** - Disappears during fullscreen applications
- **Context Responses** - Different reactions based on your current application

---

## 📁 Project Structure

```
Desktop_Pet/
├── assets/                 # Animation and image assets
│   ├── defaultIdle/       # Default idle animation frames
│   ├── idle1/             # Alternative idle animation
│   ├── dance/             # Dancing animation frames
│   └── speech_bubble/     # Speech bubble graphics
├── main.py                # Main application entry point
├── chatbot.py             # Groq AI integration
├── voice_listen.py        # Speech recognition system
├── spotify_react.py       # Spotify API integration
├── context_talk.py        # Context-aware responses
├── fullscreen_check.py    # Fullscreen detection
├── config.json            # Configuration file (create this)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🔧 Dependencies

The following packages are required:

```
tkinter          # GUI framework (usually included with Python)
Pillow           # Image processing
pyperclip        # Clipboard operations
groq             # AI API integration
spotipy          # Spotify API wrapper
SpeechRecognition # Voice recognition
pyaudio          # Audio processing
requests         # HTTP requests
pywin32          # Windows-specific functionality
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🚀 Building Standalone Executable

To create your own standalone EXE:

```bash
python -m PyInstaller --noconfirm --onefile --windowed --add-data "assets;assets" --add-data "config.json;." main.py
```

The executable will be created in the `dist/` folder.

---

## 🎯 Use Cases & Examples

### **Code Review Assistant**
1. Copy code snippet to clipboard
2. Say "Answer this" to pet
3. Get sarcastic but helpful code analysis
4. Say "Copy that" to save the review

### **Text Analysis**
1. Copy any article, email, or document
2. Ask pet to analyze with "What's on clipboard"
3. Get AI-powered summary or insights
4. Copy response for further use

### **Quick Q&A**
1. Copy questions from forums, homework, etc.
2. Voice command "Answer this"
3. Get instant AI responses
4. Copy answers back to original source

---

## 🐛 Troubleshooting

### Common Issues

**Voice recognition not working:**
- Ensure microphone permissions are granted
- Check that `pyaudio` is properly installed
- Try running as administrator

**Clipboard commands not responding:**
- Verify clipboard contains text (not images/files)
- Try copying text again before voice command
- Check if clipboard access is blocked by security software

**Spotify integration not working:**
- Verify Spotify is running and playing music
- Check API credentials in `config.json`
- Ensure Spotify app is authorized

**Pet not appearing:**
- Check if running in fullscreen mode
- Verify all asset files are present
- Try running from command line to see error messages

**High CPU usage:**
- Voice recognition runs continuously - this is normal
- Close other audio applications if needed
- Consider adjusting recognition sensitivity

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq** for the LLaMA 3 API
- **Spotify** for the Web API
- **Python Community** for the amazing libraries
- **Pixel Art Community** for inspiration

---

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Make sure all dependencies are properly installed

**Enjoy your new sarcastic desktop companion with advanced clipboard powers! 🐱📋**
