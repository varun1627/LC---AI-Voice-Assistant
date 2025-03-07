from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
DefaultMessage = f'''{Username}: Hello {Assistantname}, How are You?
{Assistantname}: Welcome {Username}. I am doing well. How may I help you?'''

# Global variables
subprocesses = []
subprocess_lock = threading.Lock()  # Thread-safe lock for subprocesses
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# Helper functions
def ShowDefaultChatIfNoChats():
    """Display default chat if no chats exist."""
    chatlog_path = os.path.join('Data', 'ChatLog.json')
    try:
        with open(chatlog_path, "r", encoding='utf-8') as file:
            if len(file.read()) < 5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as db_file:
                    db_file.write("")
                with open(TempDirectoryPath('Database.dat'), 'w', encoding='utf-8') as db_file:
                    db_file.write(DefaultMessage)
    except FileNotFoundError:
        logging.warning("ChatLog.json not found. Creating a new one.")
        with open(chatlog_path, "w", encoding='utf-8') as file:
            file.write("[]")

def ReadChatLogJson():
    """Read and return the chat log from ChatLog.json."""
    chatlog_path = os.path.join('Data', 'ChatLog.json')
    try:
        with open(chatlog_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading ChatLog.json: {e}")
        return []

def ChatLogIntegration():
    """Format and integrate the chat log into the GUI."""
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Assistantname}: {entry['content']}\n"

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsGUI():
    """Display chats in the GUI."""
    try:
        with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
            data = file.read()
            if len(data) > 0:
                with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as output_file:
                    output_file.write(data)
    except FileNotFoundError as e:
        logging.error(f"Error reading Database.data: {e}")

def InitialExecution():
    """Initialize the program."""
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsGUI()

# Main execution logic
def MainExecution():
    """Process user queries and execute tasks."""
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)

    logging.debug(f"Decision: {Decision}")

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])

    Merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for query in Decision:
        if "generate" in query:
            ImageGenerationQuery = str(query)
            ImageExecution = True

        if not TaskExecution and any(query.startswith(func) for func in Functions):
            run(Automation(list(Decision)))
            TaskExecution = True

    if ImageExecution:
        image_generation_path = os.path.join('Frontend', 'Files', 'ImageGeneration.data')
        with open(image_generation_path, "w") as file:
            file.write(f"{ImageGenerationQuery},True")
        try:
            p1 = subprocess.Popen(['Python', os.path.join('Backend', 'ImageGeneration.py')],
                                  shell=False)
            with subprocess_lock:
                subprocesses.append(p1)
        except Exception as e:
            logging.error(f"Error starting ImageGeneration.py: {e}")

    if G and R or R:
        SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering>>>>")
        TextToSpeech(Answer)
    elif G:
        SetAssistantStatus("Thinking...")
        QueryFinal = Decision[0].replace("general", "")
        Answer = ChatBot(QueryModifier(QueryFinal))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering>>>>")
        TextToSpeech(Answer)
    elif "exit" in Decision:
        QueryFinal = "Okay, Bye!"
        Answer = ChatBot(QueryModifier(QueryFinal))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering>>>>")
        TextToSpeech(Answer)
        sys.exit(0)  # Graceful exit

# Thread functions
def FirstThread():
    """Handle backend logic in a separate thread."""
    while True:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus == "True":
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." in AIStatus:
                sleep(0.1)
            else:
                SetAssistantStatus("Available...")
        sleep(0.1)  # Add a small delay to reduce CPU usage

def SecondThread():
    """Start the GUI in a separate thread."""
    GraphicalUserInterface()

# Entry point
if __name__ == "__main__":
    InitialExecution()  # Initialize the program
    thread1 = threading.Thread(target=FirstThread, daemon=True)
    thread1.start()
    SecondThread() 