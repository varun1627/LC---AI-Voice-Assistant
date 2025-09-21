Project Overview:
The LC---AI-Voice-Assistant is designed to let users interact with an AI agent through voice commands,
integrating functionalities like Speech-to-Text (STT), Text-to-Speech (TTS), and various automation tools.
Its primary use case is to help schedule events, manage contacts, access a knowledge base, and perform web searches using simple spoken language
Features:
Speech-to-Text (STT) and Text-to-Speech (TTS)
Natural conversational voice interface
Calendar, contact, and email integration
Web search and custom knowledge base access
Visual File Structure:
Below is a typical file structure:
/LC---AI-Voice-Assistant/
│
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── README.md                # Project overview
├── /modules/                # Feature modules
│     ├── stt.py
│     ├── tts.py
│     ├── calendar.py
│     └── contacts.py
├── /config/                 # Configuration files
│     └── config.yaml
└── /examples/               # Example scripts
      └── demo.mp3
Getting Started:
1. Clone the repo
git clone https://github.com/varun1627/LC---AI-Voice-Assistant.git
cd LC---AI-Voice-Assistant
2. Set up environment
python -m venv venv
source venv/bin/activate # For Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Configure environment variables
Add your API keys and settings inside a .env or config file as specified.
4. Run the assistant
python main.py
Visualization:
Here’s a conceptual visualization of the architecture
┌───────────────┐      ┌───────────────┐      ┌──────────────┐
│   Microphone  │ ---> │   STT Module  │ ---> │   Intent     │
└───────────────┘      └───────────────┘      │ Recognition  │
                                              └─────┬────────┘
                                                    │
                                            ┌───────▼───────┐
                                            │ AI Core/LLM   │
                                            └───────┬───────┘
                                                    │
                                   ┌────────────┐   │   ┌─────────────┐
                                   │ Calendar   │<--┘--->│  Web Search │
                                   └────────────┘        └─────────────┘
                                           │
                                   ┌────────────┐
                                   │   TTS      │
                                   └────┬───────┘
                                        │
                                  ┌──────────────┐
                                  │   Speaker    │
                                  └──────────────┘
Contribution:
Fork the repo, create feature branches, and submit PRs

Open issues for bug reports or feature requests
